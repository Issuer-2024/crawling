from abc import ABC, abstractmethod
from src.base import Crawler


class CommentsCrawler(Crawler, ABC):

    @abstractmethod
    def _parse(self, html):
        pass

    def crawl_comments(self, url):
        self._fetch_page(url)
        comments_data = self._parse(url)
        self._close()
        return comments_data