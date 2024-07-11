from abc import ABC, abstractmethod
from src.base import Crawler


class IssueLoader(Crawler, ABC):

    def __init__(self):
        super().__init__()
        self.target_platforms = {}
        self.main_platform = 'unknown'

    @abstractmethod
    def _parse(self, html):
        pass