import logging
import requests
from bs4 import BeautifulSoup


class Overwatch:
    # TODO add in data validation for filters
    # TODO add a parse data function for stats

    base_url = 'https://playoverwatch.com/en-us/career/pc/'

    default_region = 'us'
    default_hero = 'all'
    default_filter = 'best'
    default_mode = 'quickplay'

    def __init__(self, battletag=None, hero=None, filter=None,
                 mode=None, region=None):
        # Logging
        self.start_logging()
        # Flags
        self.wants_quickplay = False
        self.wants_competitive = False

        self.results = {}

        self.region = region or self.default_region
        self.hero = hero or self.default_hero
        self.battletag = battletag.replace('#', '-')
        self.filter = filter or self.default_filter
        self.mode = mode or self.default_mode

        self.areas = ['na', 'eu', 'us', 'cn', 'kr']

        self.heroes = ['all', 'reaper', 'tracer', 'mercy',
                       'hanzo', 'torbjorn', 'reinhardt', 'pharah',
                       'winston', 'widowmaker', 'bastion', 'symmetra',
                       'zenyatta', 'genji', 'roadhog', 'mcree',
                       'junkrat', 'zarya', 'soldier 76', 'lucio',
                       'dva', 'mei', 'sombra', 'ana']

        if self.region not in self.areas:
            self.logger.error("Not a valid region")

        if self.mode == 'quickplay':
            self.wants_quickplay = True

        if self.mode == 'competitive':
            self.wants_competitive = True

        self.index = self.heroes.index(self.hero)

    # Setup logging
    def start_logging(self):
        self.logger = logging.getLogger('python-overwatch')
        self.handler = logging.StreamHandler()
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.WARNING)
        self.handler.setLevel(logging.WARNING)


    def get_results(self):
        """
        Gets results from playoverwatch.com based on filters provided
        """

        response = requests.get(self.base_url + self.region + '/' +
                                self.battletag)
        soup = BeautifulSoup(response.content, 'html.parser')

        # FIND QUICKPLAY STATS
        # Find top played heroes in quickplay
        if self.wants_quickplay:
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
        if self.wants_competitive:
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

            # HTML section for competitive stats
            comp = soup.find('div', {'id': 'competitive'})

            # Find Reaper competitive stats
            if self.index == 1:
                for reaper in comp.find_all('div', {'data-category-id':
                                                    '0x02E0000000000002'}):
                    all_stats = {}
                    for block in reaper.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[1]] = all_stats

            # Find Tracer competitive stats
            if self.index == 2:
                for tracer in comp.find_all('div', {'data-category-id':
                                                    '0x02E0000000000003'}):
                    all_stats = {}
                    for block in tracer.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[2]] = all_stats

            # Find Mercy competitive stats
            if self.index == 3:
                for mercy in comp.find_all('div', {'data-category-id':
                                                   '0x02E0000000000004'}):
                    all_stats = {}
                    for block in mercy.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[3]] = all_stats

            # Find Hanzo competitive stats
            if self.index == 4:
                for hanzo in comp.find_all('div', {'data-category-id':
                                                   '0x02E0000000000005'}):
                    all_stats = {}
                    for block in hanzo.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[4]] = all_stats

            # Find Torbjorn competitive stats
            if self.index == 5:
                for torb in comp.find_all('div', {'data-category-id':
                                                  '0x02E0000000000006'}):
                    all_stats = {}
                    for block in torb.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[5]] = all_stats

            # Find Reinhardt competitive stats
            if self.index == 6:
                for rein in comp.find_all('div', {'data-category-id':
                                                  '0x02E0000000000007'}):
                    all_stats = {}
                    for block in rein.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[6]] = all_stats

            # Find Pharah competitive stats
            if self.index == 7:
                for pharah in comp.find_all('div', {'data-category-id':
                                                    '0x02E0000000000008'}):
                    all_stats = {}
                    for block in pharah.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[7]] = all_stats

            # Find Winston competitive stats
            if self.index == 8:
                for winston in comp.find_all('div', {'data-category-id':
                                                     '0x02E0000000000009'}):
                    all_stats = {}
                    for block in winston.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[8]] = all_stats

            # Find Widowmaker competitive stats
            if self.index == 9:
                for widow in comp.find_all('div', {'data-category-id':
                                                   '0x02E000000000000A'}):
                    all_stats = {}
                    for block in widow.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[9]] = all_stats

            # Find Bastion competitive stats
            if self.index == 10:
                for bast in comp.find_all('div', {'data-category-id':
                                                  '0x02E0000000000015'}):
                    all_stats = {}
                    for block in bast.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[10]] = all_stats

            # Find Symmetra competitive stats
            if self.index == 11:
                for sym in comp.find_all('div', {'data-category-id':
                                                 '0x02E0000000000016'}):
                    all_stats = {}
                    for block in sym.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[11]] = all_stats

            # Find Zenyatta competitive stats
            if self.index == 12:
                for zen in comp.find_all('div', {'data-category-id':
                                                 '0x02E0000000000020'}):
                    all_stats = {}
                    for block in zen.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[12]] = all_stats

            # Find Genji competitive stats
            if self.index == 13:
                for genji in comp.find_all('div', {'data-category-id':
                                                   '0x02E0000000000029'}):
                    all_stats = {}
                    for block in genji.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[13]] = all_stats

            # Find RoadHog competitive stats
            if self.index == 14:
                for hog in comp.find_all('div', {'data-category-id':
                                                 '0x02E0000000000040'}):
                    all_stats = {}
                    for block in hog.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[14]] = all_stats

            # Find Mcree competitive stats
            if self.index == 15:
                for mcree in comp.find_all('div', {'data-category-id':
                                                   '0x02E0000000000042'}):
                    all_stats = {}
                    for block in mcree.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[15]] = all_stats

            # Find Junkrat competitive stats
            if self.index == 16:
                for junk in comp.find_all('div', {'data-category-id':
                                                  '0x02E0000000000065'}):
                    all_stats = {}
                    for block in junk.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[16]] = all_stats

            # Find Zarya competitive stats
            if self.index == 17:
                for zarya in comp.find_all('div', {'data-category-id':
                                                   '0x02E0000000000068'}):
                    all_stats = {}
                    for block in zarya.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[17]] = all_stats

            # Find Soldier:76 competitive stats
            if self.index == 18:
                for soldier in comp.find_all('div', {'data-category-id':
                                                     '0x02E000000000006E'}):
                    all_stats = {}
                    for block in soldier.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[18]] = all_stats

            # Find Lucio competitive stats
            if self.index == 19:
                for lucio in comp.find_all('div', {'data-category-id':
                                                   '0x02E0000000000079'}):
                    all_stats = {}
                    for block in lucio.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[19]] = all_stats

            # Find Dva competitive stats
            if self.index == 20:
                for dva in comp.find_all('div', {'data-category-id':
                                                 '0x02E000000000007A'}):
                    all_stats = {}
                    for block in dva.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[20]] = all_stats

            # Find Mei competitive stats
            if self.index == 21:
                for mei in comp.find_all('div', {'data-category-id':
                                                 '0x02E00000000000DD'}):
                    all_stats = {}
                    for block in mei.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[21]] = all_stats

            # Find Sombra competitive stats
            if self.index == 22:
                for sombra in comp.find_all('div', {'data-category-id':
                                                    '0x02E000000000012E'}):
                    all_stats = {}
                    for block in sombra.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[22]] = all_stats

            # Find Ana competitive stats
            if self.index == 23:
                for ana in comp.find_all('div', {'data-category-id':
                                                 '0x02E000000000013B'}):
                    all_stats = {}
                    for block in ana.find_all('div', {'card-stat-block'}):
                        stats = []
                        label = block.find('span', {'class': 'stat-title'})
                        for attr in block.find_all('td'):
                            stats.append(attr.text)
                        all_stats[label.text.lower()] = stats
                    mode[self.heroes[23]] = all_stats

            # Add 'played' and 'featured' into 'all' dict
            mode[self.heroes[0]].update(played_stats)
            mode[self.heroes[0]].update(featured_stats)

            # Enter all stats into mode 'competitive'
            self.results['competitive'] = mode

        # Return results
        try:
            return self.results[self.mode][self.hero][self.filter]
        except KeyError:
            self.logger.warning("'%s' and '%s' are not valid filter "
                                "combinations", self.hero, self.filter)


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
