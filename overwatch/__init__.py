import logging
import requests
from bs4 import BeautifulSoup


class Overwatch:

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
        self.wants_qp_played = False
        self.wants_cp_played = False
        self.wants_qp_feat = False
        self.wants_cp_feat = False

        # Settings
        self.region = region or self.default_region
        self.hero = hero or self.default_hero
        self.battletag = battletag.replace('#', '-')
        self.filter = filter or self.default_filter
        self.mode = mode or self.default_mode

        self.areas = ('na', 'eu', 'us', 'cn', 'kr')

        self.heroes = ('all', 'reaper', 'tracer', 'mercy',
                       'hanzo', 'torbjorn', 'reinhardt', 'pharah',
                       'winston', 'widowmaker', 'bastion', 'symmetra',
                       'zenyatta', 'genji', 'roadhog', 'mcree',
                       'junkrat', 'zarya', 'soldier 76', 'lucio',
                       'dva', 'mei', 'sombra', 'ana')

        if self.region not in self.areas:
            self.logger.error("Not a valid region")

        # Flag switches
        if self.mode == 'quickplay' and self.filter == 'featured':
            self.wants_qp_feat = True

        elif self.mode == 'quickplay' and self.filter == 'played':
            self.wants_qp_played = True

        elif self.mode == "quickplay":
            self.wants_quickplay = True

        elif self.mode == 'competitive' and self.filter == 'featured':
            self.wants_cp_feat = True

        elif self.mode == 'competitive' and self.filter == 'played':
            self.wants_cp_played = True

        elif self.mode == 'competitive':
            self.wants_competitive = True

        self.index = self.heroes.index(self.hero)


    # Setup logging
    def start_logging(self):
        """
        Initialize logging
        """

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

        if self.wants_quickplay:
            results = self.find_quickplay_heroes(soup, self.hero, self.filter)

        elif self.wants_qp_played:
            results = self.find_quickplay_top(soup)

        elif self.wants_qp_feat:
            results = self.find_quickplay_feat(soup)

        elif self.wants_cp_feat:
            results = self.find_comp_feat(soup)

        elif self.wants_cp_played:
            results = self.find_comp_top(soup)

        elif self.wants_competitive:
            results = self.find_comp_heroes(soup, self.hero, self.filter)

        return self.dict_zip(results)


    def find_quickplay_heroes(self, soup, character, filter):
        """
        Finds quickplay hero stats
        """
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
        try:
            return mode[character][filter]

        except KeyError:
            self.logger.warning("'%s' and '%s' are not valid filter "
                                "combinations", self.hero, self.filter)


    def find_quickplay_top(self, soup):
        """
        Finds top played heroes
        """
        count = 0
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
        return stats


    def find_quickplay_feat(self, soup):
        """
        Finds quickplay average stats
        """
        count = 0
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
        return stats


    def find_comp_top(self, soup):
        """
        Finds competitive top heroes played
        """
        count = 0
        stats = []

        # HTML section for competitive stats
        comp = soup.find('div', {'id': 'competitive'})

        # Find competitive stat section
        for block in comp.find_all('div', {'class': 'bar-container'}):
            title = block.find('div', {'class': 'title'})
            stats.append(title.text)
            hours = block.find('div', {'class': 'description'})
            stats.append(hours.text)

            # Grab only the top six
            if count < 5:
                count += 1
            else:
                break
        return stats

    def find_comp_feat(self, soup):
        """
        Finds competitive average stats
        """
        count = 0
        stats = []
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
        return stats

    def find_comp_heroes(self, soup, character, filter):
        """
        Finds competitive hero stats
        """
        # HTML section for competitive stats
        comp = soup.find('div', {'id': 'competitive'})
        # Find Competitive stats for all heroes
        mode = {}

        # Find All Hero competitive
        if self.index == 0:
            stats = self.locate_stats(comp, '0x02E00000FFFFFFFF')
            mode[self.heroes[0]] = stats

        # Find Reaper competitive stats
        elif self.index == 1:
            stats = self.locate_stats(comp, '0x02E0000000000002')
            mode[self.heroes[1]] = stats

        # Find Tracer competitive stats
        elif self.index == 2:
            stats = self.locate_stats(comp, '0x02E0000000000003')
            mode[self.heroes[2]] = stats

        # Find Mercy competitive stats
        elif self.index == 3:
            stats = self.locate_stats(comp, '0x02E0000000000004')
            mode[self.heroes[3]] = stats

        # Find Hanzo competitive stats
        elif self.index == 4:
            stats = self.locate_stats(comp, '0x02E0000000000005')
            mode[self.heroes[4]] = stats

        # Find Torbjorn competitive stats
        elif self.index == 5:
            stats = self.locate_stats(comp, '0x02E0000000000006')
            mode[self.heroes[5]] = stats

        # Find Reinhardt competitive stats
        elif self.index == 6:
            stats = self.locate_stats(comp, '0x02E0000000000007')
            mode[self.heroes[6]] = stats

        # Find Pharah competitive stats
        elif self.index == 7:
            stats = self.locate_stats(comp, '0x02E0000000000008')
            mode[self.heroes[7]] = stats

        # Find Winston competitive stats
        elif self.index == 8:
            stats = self.locate_stats(comp, '0x02E0000000000009')
            mode[self.heroes[8]] = stats

        # Find Widowmaker competitive stats
        elif self.index == 9:
            stats = self.locate_stats(comp, '0x02E000000000000A')
            mode[self.heroes[9]] = stats

        # Find Bastion competitive stats
        elif self.index == 10:
            stats = self.locate_stats(comp, '0x02E0000000000015')
            mode[self.heroes[10]] = stats

        # Find Symmetra competitive stats
        elif self.index == 11:
            stats = self.locate_stats(comp, '0x02E0000000000016')
            mode[self.heroes[11]] = stats

        # Find Zenyatta competitive stats
        elif self.index == 12:
            stats = self.locate_stats(comp, '0x02E0000000000020')
            mode[self.heroes[12]] = stats

        # Find Genji competitive stats
        elif self.index == 13:
            stats = self.locate_stats(comp, '0x02E0000000000029')
            mode[self.heroes[13]] = stats

        # Find RoadHog competitive stats
        elif self.index == 14:
            stats = self.locate_stats(comp, '0x02E0000000000040')
            mode[self.heroes[14]] = stats

        # Find Mcree competitive stats
        elif self.index == 15:
            stats = self.locate_stats(comp, '0x02E0000000000042')
            mode[self.heroes[15]] = stats

        # Find Junkrat competitive stats
        elif self.index == 16:
            stats = self.locate_stats(comp, '0x02E0000000000065')
            mode[self.heroes[16]] = stats

        # Find Zarya competitive stats
        elif self.index == 17:
            stats = self.locate_stats(comp, '0x02E0000000000068')
            mode[self.heroes[17]] = stats

        # Find Soldier:76 competitive stats
        elif self.index == 18:
            stats = self.locate_stats(comp, '0x02E000000000006E')
            mode[self.heroes[18]] = stats

        # Find Lucio competitive stats
        elif self.index == 19:
            stats = self.locate_stats(comp, '0x02E0000000000079')
            mode[self.heroes[19]] = stats

        # Find Dva competitive stats
        elif self.index == 20:
            stats = self.locate_stats(comp, '0x02E000000000007A')
            mode[self.heroes[20]] = stats

        # Find Mei competitive stats
        elif self.index == 21:
            stats = self.locate_stats(comp, '0x02E00000000000DD')
            mode[self.heroes[21]] = stats

        # Find Sombra competitive stats
        elif self.index == 22:
            stats = self.locate_stats(comp, '0x02E000000000012E')
            mode[self.heroes[22]] = stats

        # Find Ana competitive stats
        else:
            stats = self.locate_stats(comp, '0x02E000000000013B')
            mode[self.heroes[23]] = stats

        try:
            return mode[character][filter]
        except KeyError:
            self.logger.warning("'%s' and '%s' are not valid filter "
                                "combinations", self.hero, self.filter)
        except TypeError:
            self.logger.warning('Found no competitive stats for this hero')


    def locate_stats(self, soup, html):
        """
        Use for finding individual competitive hero stats
        """
        for hero in soup.find_all('div', {'data-category-id': html}):
            all_stats = {}
            for block in hero.find_all('div', {'card-stat-block'}):
                stats = []
                label = block.find('span', {'class': 'stat-title'})
                for attr in block.find_all('td'):
                    stats.append(attr.text)
                all_stats[label.text.lower()] = stats
            return all_stats


    def dict_zip(self, results):
        """
        Converts list of results into a dictionary
        """
        labels = [results[i] for i in range(0, len(results), 2)]
        data = [results[i] for i in range(1, len(results), 2)]

        return dict(zip(labels, data))


    def display_filters(self):
        """
        """
        response = requests.get(self.base_url + self.region + '/' +
                                self.battletag)
        soup = BeautifulSoup(response.content, 'html.parser')
        count = 0
        filters = []

        for block in soup.find_all('div', {'card-stat-block'}):
            label = block.find('span', {'class': 'stat-title'})
            if count < 9:
                filters.append(label.text.lower())
                count += 1
        filters.append('played')
        filters.append('featured')

        print(filters)
