from abc import ABC

from src.base import IssueLoader
from src.news.target_platform_list import target_news_platform_list


class NewsIssueLoader(IssueLoader, ABC):

    def __init__(self):
        super().__init__()
        self.target_platforms = target_news_platform_list
        self.main_platform = 'News'

    def _get_news_items(self, elem):
        return elem.select('ul.press_ranking_list > li.as_thumb')

    def _get_news_rank(self, elem):
        return elem.select_one('em.list_ranking_num').get_text()

    def _get_news_title(self, elem):
        return elem.select_one('strong.list_title').get_text(strip=True)

    def _get_news_link(self, elem):
        return elem.select_one('a')['href']

    def _get_news_views(self, elem):
        news_view = None
        if elem.select_one('span.list_view'):
            news_view = int(elem.select_one('span.list_view')
                            .get_text(strip=True).replace(',', '')
                            .replace('조회수', ''))
        return news_view