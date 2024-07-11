import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class Crawler:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 브라우저를 열지 않고 실행
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Remote(command_executor=os.getenv('WEB_DRIVER_HUB_URL'), options=chrome_options)
