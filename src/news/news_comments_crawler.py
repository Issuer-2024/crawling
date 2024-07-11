from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.base.comments_crawler import CommentsCrawler

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