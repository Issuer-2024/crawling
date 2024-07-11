from abc import ABC, abstractmethod
from src.base import Crawler


class ContentCrawler(Crawler, ABC):

    @abstractmethod
    def _parse(self, html):
        pass

    def crawl_content(self, url):
        self._fetch_page(url)
        content_data = self._parse(self.driver.page_source)
        self._close()
        return content_data

