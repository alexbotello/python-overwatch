import logging
import requests
from bs4 import BeautifulSoup
from heroes import heroes


class Overwatch:
    def __init__(self, battletag=None, mode='qp', hero='all', filter='Best'):
        self.url = 'https://playoverwatch.com/en-us/career/pc/'
        self.battletag = battletag.replace('#', '-')
        self.mode = mode
        self.hero = hero
        self.filter = filter
        self.response = requests.get(self.url + 'us' + '/' + self.battletag)
        self.soup = BeautifulSoup(self.response.content, 'lxml')
        self.logger = logging.getLogger(__name__)

        if self.filter == "Hero Specific" and self.hero == 'all':
            self.logger.error(f"'{self.filter}' and '{self.hero}' are not valid filter combinations")

    def __call__(self):
        if self.mode == 'qp':
            yield from self.quickplay_results()
        elif self.mode == 'cp':
            yield from self.competitive_results()
        elif self.mode =='play_time':
            yield from self.playtime_results()

    def __repr__(self):
        return f"Overwatch stats for {self.battletag.replace('-', '#')} - {self.hero}"

    def error_handler(func):
        def decorator(self, *args):
            try:
                yield from func(self, *args)
            except AttributeError:
                self.logger.error(f"No results were found for {self.hero}")
        return decorator
            
    def playtime_results(self):
        row = self.soup.find('div', {'data-category-id': "overwatch.guid.0x0860000000000021"})
        for char in row:
            yield char.find('div', {'class': 'title'}).text
            yield char.find('div', {'class': 'description'}).text
    
    def quickplay_results(self):
        html = self.retrieve_html_block(self.soup)
        yield from self.generate_stats(html)

    def competitive_results(self):
        soup = self.soup.find('div', {'data-mode': 'competitive'})
        html = self.retrieve_html_block(soup)
        yield from self.generate_stats(html)

    def retrieve_html_block(self, soup):
        return soup.find('div', {'data-category-id': heroes[self.hero]})
    
    @error_handler
    def generate_stats(self, html):
        for stats in html.find_all('div', {'class': 'card-stat-block'}):
            title = stats.find('h5', {'class': 'stat-title'})
            if title.text == self.filter:
                for stat in stats.find_all('td'):
                    yield stat.text

    @property
    def display_filters(self):
        results = self.soup.find_all('h5', {'class': 'stat-title'})
        return list(set((filters.text for x, filters in enumerate(results))))
