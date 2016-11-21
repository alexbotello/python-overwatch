import requests
from bs4 import BeautifulSoup


class Overwatch:
    # TODO add in data validation for filters
    # TODO add a parse data function for stats
    # TODO add competetive stats for every hero
    # TODO add logging

    base_url = 'https://playoverwatch.com/en-us/career/pc/'

    default_region = 'us'
    default_hero = 'all'
    default_filter = 'best'
    default_mode = 'quickplay'

    def __init__(self, battletag=None, hero=None, filter=None,
                 mode=None, region=None):

        self.region = region or self.default_region
        self.hero = hero or self.default_hero
        self.battletag = battletag.replace('#', '-')
        self.filter = filter or self.default_filter
        self.mode = mode or self.default_mode

        self.results = {}

        self.heroes = ['all', 'reaper', 'tracer', 'mercy',
                       'hanzo', 'torbjorn', 'reinhardt', 'pharah',
                       'winston', 'widowmaker', 'bastion', 'symmetra',
                       'zenyatta', 'genji', 'roadhog', 'mcree',
                       'junkrat', 'zarya', 'soldier 76', 'lucio',
                       'dva', 'mei', 'sombra', 'ana']

        if self.mode == 'competitive':
            self.hero = self.default_hero

    def get_results(self):
        """
        Gets results from playoverwatch.com based on filters provided
        """

        response = requests.get(self.base_url + self.region + '/' +
                                self.battletag)
        soup = BeautifulSoup(response.content, 'html.parser')

        # FIND QUICKPLAY STATS
        # Find top played heroes in quickplay
        count = 0
        played_stats = {}
        stats = []

        for block in soup.find_all('div', {'class': 'bar-container'}):
            title = block.find('div', {'class': 'title'})
            stats.append(title.text)
            hours = block.find('div', {'class': 'description'})
            stats.append(hours.text)

            # Grab only the top six
            if count < 5:
                count += 1
            else:
                break
        played_stats['played'] = stats

        # Find featured stats in quickplay
        count = 0
        featured_stats = {}
        stats = []

        for card in soup.find_all('div', {'class': 'card-content'}):
            stat_title = card.find('p', {'class': 'card-copy'})
            stats.append(stat_title.text)
            data = card.find('h3', {'class': 'card-heading'})
            stats.append(data.text)

            # Grab only the first eight results
            if count < 7:
                count += 1
            else:
                break
        featured_stats['featured'] = stats

        # Find quickplay stats for every hero
        mode = {}
        hero = 0

        # Find each hero's stat page
        for char in soup.find_all('div', {'data-group-id': 'stats'}):
            all_stats = {}
            # Loop though each subsection
            for block in char.find_all('div', {'class': 'card-stat-block'}):
                stats = []
                label = block.find('span', {'class': 'stat-title'})
                for attr in block.find_all('td'):
                    stats.append(attr.text)
                all_stats[label.text.lower()] = stats

            # Stop loop to avoid scraping competitive stats
            if hero == 24:
                break
            else:
                mode[self.heroes[hero]] = all_stats
                hero += 1

        # Add 'played' and 'featured' into 'all' dict
        mode[self.heroes[0]].update(played_stats)
        mode[self.heroes[0]].update(featured_stats)

        # Enter all stats into mode 'quickplay'
        self.results['quickplay'] = mode

        # FIND COMPETITIVE STATS
        # As of right now there are no hero specific competetive stats
        # The only filters available are through hero='all'
        # Ex: (hero='all', filter='played'), (hero='all', filter='best')

        # Find top played heroes in competitive
        count = 0
        played_stats = {}
        stats = []

        # Find competitive stat section
        for play in soup.find_all('div', {'id': 'competitive'}):
            for block in play.find_all('div', {'class': 'bar-container'}):
                title = block.find('div', {'class': 'title'})
                stats.append(title.text)
                hours = block.find('div', {'class': 'description'})
                stats.append(hours.text)

                # Grab only the top six
                if count < 5:
                    count += 1
                else:
                    break
        played_stats['played'] = stats

        # Find featured stats in competitive
        count = 0
        featured_stats = {}
        stats = []

        for play in soup.find_all('div', {'id': 'competitive'}):
            for card in soup.find_all('div', {'class': 'card-content'}):
                # Skip the first 8 results
                if count >= 8:
                    stat_title = card.find('p', {'class': 'card-copy'})
                    stats.append(stat_title.text)
                    data = card.find('h3', {'class': 'card-heading'})
                    stats.append(data.text)
                    count += 1
                else:
                    count += 1

        featured_stats['featured'] = stats

        # Find Competitive stats for all heroes
        mode = {}
        for comp in soup.find_all('div', {'data-category-id':
                                          '0x02E00000FFFFFFFF'}):
            all_stats = {}
            for block in comp.find_all('div', {'card-stat-block'}):
                stats = []
                label = block.find('span', {'class': 'stat-title'})
                for attr in block.find_all('td'):
                    stats.append(attr.text)
                all_stats[label.text.lower()] = stats
            mode[self.heroes[0]] = all_stats

        # Add 'played' and 'featured' into 'all' dict
        mode[self.heroes[0]].update(played_stats)
        mode[self.heroes[0]].update(featured_stats)

        # Enter all stats into mode 'competitive'
        self.results['competitive'] = mode

        # Return results
        return self.results[self.mode][self.hero][self.filter]


    def show_filters(self):
        """
        Shows filters that can be specified
        """
        print('Modes: ')
        for k in self.results.keys():
            print('\t* ' + k)
        print('Heroes:')
        for k in self.results['quickplay'].keys():
            print('\t* ' + k)
        print('Filters:')
        for k in self.results['quickplay']['all'].keys():
            print('\t* ' + k)
        print('\t* hero specific')
