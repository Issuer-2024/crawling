from abc import ABC, abstractmethod
from src.base import Crawler


class CommentsCrawler(Crawler, ABC):

    @abstractmethod
    def _parse(self, html):
        pass