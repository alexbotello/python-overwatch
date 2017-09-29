import time
import logging
import daiquiri
import requests
from bs4 import BeautifulSoup
from heroes import heroes


class Overwatch:
    def __init__(self, battletag=None, mode='qp', hero='all', filter='Best', region='us'):
        # Init logger
        self.start_logging()
        
        self.url = 'https://playoverwatch.com/en-us/career/pc/'
        self.battletag = battletag.replace('#', '-')
        self.mode = mode
        self.hero = hero
        self.filter = filter
        self.region = region
        self.areas = ('na', 'eu', 'us', 'cn', 'kr')

        # Checks
        if self.region not in self.areas:
            self.logger.error("Not a valid region")
            exit()
        if self.filter == "Hero Specific" and self.hero == 'all':
            self.logger.error(f"'{self.filter}' and '{self.hero}' are not valid filter combinations")
            exit()
        
    def __call__(self):
        data = []
        resp = requests.get(self.url + self.region + '/' + self.battletag)
        self.soup = BeautifulSoup(resp.content, 'lxml')

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
    
    def start_logging(self):
        """ Logging all the things..."""
        daiquiri.setup(level=logging.INFO)
        self.logger = daiquiri.getLogger()

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

    def filters(self):
        """ Display available filters for stats"""
        limit = 9
        results = self.soup.find_all('h5', {'class': 'stat-title'})
        return [filters.text for x, filters in enumerate(results) if x < limit]
