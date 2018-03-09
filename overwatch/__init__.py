from requests_html import HTMLSession

from .heroes import heroes
from .errors import (InvalidBattletag, InvalidCombination, InvalidFilter,
                    InvalidHero, NotFound)

session = HTMLSession()


class Overwatch:
    def __init__(self, battletag=None, mode='qp', hero='all', filter='best'):
        self.url = 'https://playoverwatch.com/en-us/career/pc/'

        try:
            self._battletag = battletag.replace('#', '-')
        except AttributeError:
            raise InvalidBattletag(f'battletag="{battletag}" is invalid')

        self._mode = 0 if mode == 'qp' else 1
        self._hero = hero.lower()
        self._filter = filter.title()
        self._r = session.get(self.url + 'us' + '/' + self._battletag)
        self.initial_error_check()

    def __call__(self):
        return self.generate_stats()

    def initial_error_check(self):
        if self._filter == "Hero Specific" and self._hero == 'all':
            raise InvalidCombination(f"'{self._filter}' and '{self._hero}'"
                                     " are not valid filter combinations")
        if self._filter == "Miscellaneous" and self._hero != 'all':
            raise InvalidCombination(f"'{self._filter}' and '{self._hero}'"
                                     " are not valid filter combinations")

        if self._filter not in self.filters:
            raise InvalidFilter(f'filter="{self._filter}" is invalid.')

    def error_handler(func):
        def decorator(self, *args):
            try:
                results = func(self, *args)
                return results
            except IndexError:
                raise NotFound(f"No results were found for {self._hero}"
                               " in this mode")
            except KeyError:
                raise InvalidHero(f'hero="{self._hero}" is invalid.')
        return decorator

    @error_handler
    def generate_stats(self):
        html = self._r.html.find(f'div[data-category-id="{heroes[self._hero]}"]')
        hero = html[self._mode]
        cards = hero.find('.card-stat-block')
        for card in cards:
            if card.text.startswith(self._filter):
                return card.text.split("\n")[1:]

    @property
    def playtime(self):
        tag = "overwatch.guid.0x0860000000000021"
        time = self._r.html.find(f'div[data-category-id="{tag}"]')
        time = time[self._mode]
        return time.text.split('\n')

    @property
    def filters(self):
        filters = self._r.html.find(".stat-title")
        return list(set((filter.text for filter in filters)))
