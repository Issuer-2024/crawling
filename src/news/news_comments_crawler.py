from datetime import datetime
import re

from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.base.comments_crawler import CommentsCrawler
import logging
logger = logging.getLogger(__name__)
def extract_article_id(url):
    # 정규 표현식을 사용하여 특정 형식의 부분을 추출
    match = re.search(r'/article/(\d+/\d+)', url)
    if match:
        return match.group(1)
    else:
        match = re.search(r'/article/comment/(\d+/\d+)', url)
        if match:
            return match.group(1)
        else:
            return None


def change_comments_date_format(date_string):
    try:
        # 초 부분이 있는 형식으로 파싱 시도
        date_obj = datetime.strptime(date_string, "%Y.%m.%d. %H:%M:%S")
    except ValueError:
        try:
            # 초 부분이 없는 형식으로 파싱
            date_obj = datetime.strptime(date_string, "%Y.%m.%d. %H:%M")
            # 초 부분을 추가하여 원하는 형식으로 변환
            formatted_date = date_obj.strftime("%Y-%m-%d_%H:%M:00")
        except ValueError as e:
            # 다른 형식의 예외 처리
            raise ValueError(f"Incorrect date format: {e}")
    else:
        # 초 부분이 있는 형식으로 변환
        formatted_date = date_obj.strftime("%Y-%m-%d_%H:%M:%S")

    return formatted_date


class NewsCommentsCrawler(CommentsCrawler):

    def _wait_more_btn(self):
        while True:
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "더보기"))
                )
                more_button = self.driver.find_element(by=By.LINK_TEXT, value='더보기')
                more_button.click()
            except Exception as e:
                break

    def _get_editor(self, elem):
        return elem.select_one(
            "div.u_cbox_comment_box div.u_cbox_info span.u_cbox_nick").text.strip()

    def _get_text(self, elem):
        return elem.select_one(
            "div.u_cbox_text_wrap span.u_cbox_contents").text.strip().replace(
            '\n', '')

    def _get_recomm(self, elem):
        return int(elem.select_one('em.u_cbox_cnt_recomm').text.strip())

    def _get_unrecomm(self, elem):
        return int(elem.select_one('em.u_cbox_cnt_unrecomm').text.strip())

    def _get_reply_num(self, elem):
        return int(elem.select_one('span.u_cbox_reply_cnt').text.strip())

    def _get_written_at(self, elem):
        return change_comments_date_format(
            elem.select_one('span.u_cbox_date').get_text(strip=True))

    def _parse(self, url):
        # '더보기' 버튼을 클릭하여 더 많은 댓글 로드
        article_id = extract_article_id(url).replace('/', '')

        # 페이지 소스 파싱
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        # 댓글 추출
        comments = []
        comment_elements = soup.select("ul.u_cbox_list li.u_cbox_comment")
        for comment_element in comment_elements:

            if comment_element.select_one("div.u_cbox_text_wrap span.u_cbox_contents"):  #삭제된 댓글 처리
                comments.append({
                    "문서 번호": article_id,
                    "작성자": self._get_editor(comment_element),
                    "내용": self._get_text(comment_element),
                    "추천 수": self._get_recomm(comment_element),
                    "비추천 수": self._get_recomm(comment_element),
                    "대댓글 수": self._get_reply_num(comment_element),
                    "작성 시간": self._get_written_at(comment_element)})
            else:
                continue
