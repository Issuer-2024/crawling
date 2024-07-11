import traceback
from abc import ABC

from bs4 import BeautifulSoup

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

    def _parse(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            news_items = []

            ranking_box = soup.select('div.press_ranking_home > div.press_ranking_box')

            for sub_ranking in ranking_box:
                items = self._get_news_items(sub_ranking)
                for item in items:
                    news_items.append({
                        "순위": self._get_news_rank(item),
                        "제목": self._get_news_title(item),
                        "URL": self._get_news_link(item),
                        "조회수": self._get_news_views(item),
                    })

            return news_items
        except Exception as e:
            traceback.print_exc()
            return []
