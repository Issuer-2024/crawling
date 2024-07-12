import logging

import requests
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
import time

logger = logging.getLogger(__name__)
load_dotenv()


class Crawler:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 브라우저를 열지 않고 실행
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = None
        while self.driver is None:
            try:
                self.driver = webdriver.Remote(
                    command_executor=os.getenv('WEB_DRIVER_HUB_URL'),
                    options=chrome_options
                )
                logger.info("Connected to the remote WebDriver.")
            except WebDriverException as e:
                logger.info(f"Connection failed: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    def _fetch_page(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)
        except Exception as e:
            logger.error(f"[FETCH ERROR] Page Load Failed: {e}")

    def _close(self):
        self.driver.quit()
        node_url = os.getenv('WEB_DRIVER_HUB_URL') + '/session/' + self.driver.session_id  # 노드 URL 및 세션 ID 설정
        response = requests.delete(node_url)
        if response.status_code == 200:  # DELETE 요청 보내기
            return True
        return False
