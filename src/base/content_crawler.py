from abc import ABC, abstractmethod
from src.base import Crawler


class ContentCrawler(Crawler, ABC):

    @abstractmethod
    def _parse(self, html):
        pass



