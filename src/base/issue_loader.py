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

    def crawl_issues(self):
        all_issues = []
        for platform, url in self.target_platforms.items():
            self._fetch_page(url)
            issue_items = self._parse(self.driver.page_source)
            for i in range(len(issue_items)):
                issue_items[i]['플랫폼'] = platform
                issue_items[i]['상위 플랫폼'] = self.main_platform
                issue_items[i]['하위 플랫폼'] = platform
            all_issues += issue_items
        self._close()
        return all_issues
