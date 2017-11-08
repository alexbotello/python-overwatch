import time
import logging
import requests
from bs4 import BeautifulSoup
from .heroes import heroes


class Overwatch:
    def __init__(self, battletag=None, mode='qp', hero='all', filter='Best',
                 log_level=logging.ERROR, use_daquiri=False):
        # Init logger
        self.start_logging(log_level, daquiri=use_daquiri)

        self.url = 'https://playoverwatch.com/en-us/career/pc/'
        self.battletag = battletag.replace('#', '-')
        self.mode = mode
        self.hero = hero
        self.filter = filter
        self.resp = requests.get(self.url + 'us' + '/' + self.battletag)

        # Checks
        if self.filter == "Hero Specific" and self.hero == 'all':
            self.logger.error(f"'{self.filter}' and '{self.hero}' are not valid filter combinations")
            exit()

    def __call__(self):
        data = []
        self.soup = BeautifulSoup(self.resp.content, 'lxml')

        if self.mode == 'qp':
            for stat in self.find_qp():
                data.append(stat)
        elif self.mode == 'cp':
            for stat in self.find_cp():
                data.append(stat)
        elif self.mode =='play_time':
            for time in self.find_playtime():
                data.append(time)
        return data

    def __repr__(self):
        return f"{self.battletag.replace('-', '#')}'|'{self.hero}'"

    def start_logging(self, level, daquiri=False):
        """ Logging all the things..."""
        if daquiri:
            import daiquiri
            daiquiri.setup(level=level)
            self.logger = daiquiri.getLogger()
        else:
            self.logger = logging.getLogger(__name__)

    def find_qp(self):
        """ Retrieve quickplay stats"""
        row = self.soup.find('div', {'data-category-id': heroes[self.hero]})
        try:
            for stats in row.find_all('div', {'class': 'card-stat-block'}):
                title = stats.find('h5', {'class': 'stat-title'})

                if title.text == self.filter:
                    for stat in stats.find_all('td'):
                        yield stat.text
        except AttributeError:
            self.logger.error(f'No quickplay stats found for {self.hero}')
            exit()

    def find_cp(self):
        """ Retrieve competitive stats """
        row = self.soup.find('div', {'data-mode': 'competitive'})
        char = row.find('div', {'data-category-id': heroes[self.hero]})
        try:
            for stats in char.find_all('div', {'class': 'card-stat-block'}):
                title = stats.find('h5', {'class': 'stat-title'})

                if title.text == self.filter:
                    for stat in stats.find_all('td'):
                        yield stat.text
        except AttributeError:
            self.logger.error(f"No competitive stats found for {self.hero}")
            exit()

    def find_playtime(self):
        """ Retrieve time played for heroes """
        row = self.soup.find('div', {'data-category-id': "overwatch.guid.0x0860000000000021"})
        for char in row:
            yield char.find('div', {'class': 'title'}).text
            yield char.find('div', {'class': 'description'}).text

    @property
    def filters(self):
        """ Display available filters for stats"""
        soup = BeautifulSoup(self.resp.content, 'lxml')        
        results = soup.find_all('h5', {'class': 'stat-title'})
        return set((filters.text for x, filters in enumerate(results)))

