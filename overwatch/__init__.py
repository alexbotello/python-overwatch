from requests_html import HTMLSession

from .selections import heroes, compare
from .errors import (InvalidBattletag, InvalidCombination, InvalidFilter,
                     InvalidHero, NotFound)


session = HTMLSession()


class Overwatch:
    def __init__(self, battletag=None):
        if battletag is None:
            raise InvalidBattletag(f'battletag="{battletag}" is invalid')
        
        self.battletag = battletag.replace('#', '-')
        self.url = 'https://playoverwatch.com/en-us/career/pc/'
        self.response = session.get(self.url + 'us' + '/' + self.battletag)

    def __call__(self, mode='qp', hero='all', filter='best'):
        """
        Parameters
        -----------
        mode : `str`
            Select quickplay or competitive game modes with `qp` or `cp`.
            This defaults to `qp`
        hero : `str`
            The specific hero to select stats for. Defaults to `all`. 
        filter : `str`
            The specific stat category to retrieve. List of filters can be seen
            using `Overwatch.filters`. This defaults to `best`.
        """
        self.mode = 0 if mode == 'qp' else 1
        self.hero = hero.lower()
        self.filter = filter.title()
        self.initial_error_check()
        return self._generate_hero_stats()

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
    def _generate_hero_stats(self):
        css_selector = f'div[data-category-id="{heroes[self.hero]}"]'
        hero = self.response.html.find(css_selector)
        mode = hero[self.mode]
        cards = mode.find('.card-stat-block')
        for card in cards:
            if card.text.startswith(self.filter):
                return card.text.split("\n")[1:]
    
    def _generate_comparisons(self, selector):
        data = self.response.html.find(f'div[data-category-id="{selector}"]')
        comparison = data[self.mode]
        return comparison.text.split("\n")

    @property
    def playtime(self):
        return self._generate_comparisons(compare['playtime']);
    
    @property
    def games_won(self):
        return self._generate_comparisons(compare['games']);     

    @property
    def weapon_accuracy(self):
        return self._generate_comparisons(compare['weapons']);
    
    @property
    def multikills(self):
        return self._generate_comparisons(compare['multikills']);
    
    @property
    def eliminations_per_life(self):
        return self._generate_comparisons(compare['eliminations']);
    
    @property
    def objective_kills(self):
        return self._generate_comparisons(compare['objective']);
    
    @property
    def filters(self):
        filters = self.response.html.find(".stat-title")
        return list(set((filter.text for filter in filters)))
