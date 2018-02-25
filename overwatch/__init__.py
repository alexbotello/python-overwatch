from requests_html import session

from .heroes import heroes
from .errors import InvalidFilter, InvalidCombination, NotFound, InvalidHero


class Overwatch:
    def __init__(self, battletag=None, mode='qp', hero='all', filter='best'):
        self.url = 'https://playoverwatch.com/en-us/career/pc/'
        self.battletag = battletag.replace('#', '-')
        self.mode = 0 if mode == 'qp' else 1
        self.hero = hero.lower()
        self.filter = filter.title()
        self.r = session.get(self.url + 'us' + '/' + self.battletag)

    def __call__(self):
        return self.generate_stats()

    def error_handler(func):
        def decorator(self, *args):
            if self.filter == "Hero Specific" and self.hero == 'all':
                raise InvalidCombination(f"'{self.filter}' and '{self.hero}' "
                                         "are not valid filter combinations")
            
            if self.filter == "Miscellaneous" and self.hero != 'all':
                raise InvalidCombination(f"'{self.filter}' and '{self.hero}' "
                                         "are not valid filter combinations")
            try:
                results = func(self, *args)
                if results is None:
                    raise InvalidFilter(f'filter="{self.filter}" is invalid.')
                return results
            except IndexError:
                raise NotFound(f"No results were found for {self.hero} in this mode")
            except KeyError:
                raise InvalidHero(f'hero="{self.hero}" is invalid.')
        return decorator

    @error_handler
    def generate_stats(self):
        html = self.r.html.find(f'div[data-category-id="{heroes[self.hero]}"]')
        hero = html[self.mode]
        cards = hero.find('.card-stat-block')
        for card in cards:
            if card.text.startswith(self.filter):
                return card.text.split("\n")

    @property
    def playtime(self):
        tag = "overwatch.guid.0x0860000000000021"
        time = self.r.html.find(f'div[data-category-id="{tag}"]')
        time = time[self.mode]
        return time.text.split('\n')

    @property
    def filters(self):
        filters = self.r.html.find(".stat-title")
        return list(set((filter.text for filter in filters)))
