from requests_html import HTMLSession

from .heroes import heroes
from .errors import (InvalidBattletag, InvalidCombination, InvalidFilter,
                     InvalidHero, NotFound)

session = HTMLSession()


class Overwatch:
    def __init__(self, battletag=None, mode='qp', hero='all', filter='best'):
        self.url = 'https://playoverwatch.com/en-us/career/pc/'

        try:
            self.battletag = battletag.replace('#', '-')
        except AttributeError:
            raise InvalidBattletag(f'battletag="{battletag}" is invalid')

        self.mode = 0 if mode == 'qp' else 1
        self.hero = hero.lower()
        self.filter = filter.title()
        self.response = session.get(self.url + 'us' + '/' + self.battletag)
        self.initial_error_check()

    def __call__(self):
        return self.generate_stats()

    def initial_error_check(self):
        if self.filter == "Hero Specific" and self.hero == 'all':
            raise InvalidCombination(f"'{self.filter}' and '{self.hero}'"
                                     " are not valid filter combinations")
        if self.filter == "Miscellaneous" and self.hero != 'all':
            raise InvalidCombination(f"'{self.filter}' and '{self.hero}'"
                                     " are not valid filter combinations")

        if self.filter not in self.filters:
            raise InvalidFilter(f'filter="{self.filter}" is invalid.')

    def error_handler(func):
        def decorator(self, *args):
            try:
                results = func(self, *args)
                return results
            except IndexError:
                raise NotFound(f"No results were found for {self._hero}"
                               " in this mode")
            except KeyError:
                raise InvalidHero(f'hero="{self.hero}" is invalid.')
        return decorator

    @error_handler
    def generate_stats(self):
        css_selector = f'div[data-category-id="{heroes[self.hero]}"]'
        hero = self.response.html.find(css_selector)
        mode = hero[self.mode]
        cards = mode.find('.card-stat-block')
        for card in cards:
            if card.text.startswith(self.filter):
                return card.text.split("\n")[1:]

    @property
    def playtime(self):
        tag = "overwatch.guid.0x0860000000000021"
        time = self.response.html.find(f'div[data-category-id="{tag}"]')
        time = time[self.mode]
        return time.text.split('\n')

    @property
    def filters(self):
        filters = self.response.html.find(".stat-title")
        return list(set((filter.text for filter in filters)))
