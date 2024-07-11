from src.base import IssueLoader


class NewsIssueLoader(IssueLoader):

    def __init__(self):
        super().__init__()
        self.target_platforms = target_news_platform_list
        self.main_platform = 'News'