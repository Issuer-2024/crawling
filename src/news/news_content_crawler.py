from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.base import ContentCrawler
import logging
import traceback

logger = logging.getLogger(__name__)


def change_news_date_format(date_string):
    # "오전"/"오후"를 "AM"/"PM"으로 변환
    date_string = date_string.replace("오전", "AM").replace("오후", "PM")
    date_string.replace("오전", "AM").replace("오후", "PM")
    # 문자열을 datetime 객체로 변환
    date_obj = datetime.strptime(date_string, "%Y.%m.%d. %p %I:%M")
    # 원하는 형식으로 변환
    formatted_date = date_obj.strftime("%Y-%m-%d_%H:00:00")

    return formatted_date


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


class NewsContentCrawler(ContentCrawler):

    def _get_news_title(self, soup):
        return soup.select_one('h2#title_area').get_text(strip=True)

    def _get_news_created_at(self, soup):
        return change_news_date_format(soup.select_one('span._ARTICLE_DATE_TIME').get_text(strip=True))

    def _get_news_editor(self, soup):
        editor = ''
        if soup.select_one('em.media_end_head_journalist_name'):
            editor = soup.select_one('em.media_end_head_journalist_name').get_text(strip=True)
        return editor

    def _get_news_article_body(self, soup):
        return soup.select_one('article#dic_area').get_text(strip=True)

    def _get_news_recommendations_num(self, soup):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "u_likeit_text"))
            )
            return int(soup.select_one('span.u_likeit_text').get_text(strip=True).replace('추천', '').replace(',', ''))
        except Exception as e:
            logger.error(f"[Content Warning] Could not find recommendations")
            traceback.print_exc()

            return None

    def _get_news_comments_num(self, soup):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "u_cbox_count"))
            )
            return int(soup.select_one('span.u_cbox_count').get_text(strip=True).replace(',', ''))
        except Exception as e:
            logger.error(f"[Content Warning] Could not find Comments Num")
            traceback.print_exc()
            return None

    def convert_comments_url(self, url):
        article_id = extract_article_id(url)
        return "https://n.news.naver.com/article/comment/" + article_id
