import logging
import requests
from lxml import html
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

        # Settings
        self.region = region or self.default_region
        self.hero = hero or self.default_hero
        self.battletag = battletag.replace('#', '-')
        self.filter = filter or self.default_filter
        self.mode = mode or self.default_mode
        self.played = False

        self.areas = ('na', 'eu', 'us', 'cn', 'kr')

        self.heroes = { 'all': ['2', '0x02E00000FFFFFFFF'],
                        'reaper': ['3', '0x02E0000000000002'],
                        'tracer': ['4', '0x02E0000000000003'],
                        'mercy': ['5', '0x02E0000000000004'],
                        'hanzo': ['6', '0x02E0000000000005'],
                        'torbjorn': ['7', '0x02E0000000000006'],
                        'reinhardt': ['8', '0x02E0000000000007'],
                        'pharah': ['9', '0x02E0000000000008'],
                        'winston': ['10', '0x02E0000000000009'],
                        'widowmaker': ['11', '0x02E000000000000A'],
                        'bastion': ['12', '0x02E0000000000015'],
                        'symmetra': ['13', '0x02E0000000000016'],
                        'zenyatta': ['14', '0x02E0000000000020'],
                        'genji': ['15', '0x02E0000000000029'],
                        'roadhog': ['16', '0x02E0000000000040'],
                        'mccree' : ['17', '0x02E0000000000042'],
                        "junkrat": ['18', '0x02E0000000000065'],
                        "zarya": ['19', '0x02E0000000000068'],
                        'solider 76': ['20', '0x02E000000000006E'],
                        'lucio': ['21', '0x02E0000000000079'],
                        'dva': ['22', '0x02E000000000007A'],
                        'mei': ['23', '0x02E00000000000DD'],
                        'sombra': ['24', '0x02E000000000012E'],
                        'ana': ['25', '0x02E000000000013B'],
                        'orisa': ['26', '0x02E000000000013E']}

        self.titles = {'hero specific': ['1'], 'combat': ['2', '1'],
                       'assists': ['3', '2'], 'best': ['4', '3'],
                       'average': ['5', '4'], 'deaths': ['6', '5'],
                       'match awards': ['7', '6'], 'game': ['8', '7'],
                       'miscellaneous': ['9', '8']}

        if self.region not in self.areas:
            self.logger.error("Not a valid region")
            exit()

        if self.filter == 'played':
            self.played = True

        if self.hero == 'all':
            # If hero filter is set to 'all' then all filter keys must have their
            # first list value removed. Due to the fact that the 'all' hero filter
            # does not have any 'hero specific' stats.
            for key in self.titles.keys():
                del(self.titles[key][0])


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
        tree = html.fromstring(response.content)

        try:

            if self.played:
                stats = self.get_time_played(tree)

            elif self.mode == "competitive":
                stats = self.get_competitive()

            else:
                stats = self.get_quickplay(tree)

            return self.dict_zip(stats)

        except IndexError:
            # IndexError will be thrown due to self.titles['hero specific']
            # purposefully having it's list value removed. As 'all' and
            # 'hero specific' are unacceptable filter combinations
            self.logger.warning("'%s' and '%s' are not valid filter "
                                "combinations", self.hero, self.filter)
            exit()

        except KeyError:
            self.logger.warning("'%s' and '%s' are not valid filter "
                                " combinations", self.hero, self.filter)
            exit()

        except TypeError:
            self.logger.warning("Found no competitive stats for '%s'", self.hero)
            exit()


    def get_quickplay(self, tree):
        """
        Gets quickplay stats
        """
        xpath = ['//*[@id="', self.mode,
                 '"]/section[3]/div/div[', self.heroes[self.hero][0],
                 ']/div[', self.titles[self.filter][0],
                 ']/div/table/tbody/tr/td/text()'
                ]
        return tree.xpath(''.join(xpath))


    def get_competitive(self):
        """
        Gets competitive stats
        """
        #TODO Make this function perform faster
        ### Using beautifulsoup makes this scraping function extremely slow.
        ### Can't use xpaths because competitive stats have unique indicies
        ### for each player depending on which heroes they have or have not
        ### played for the current season
        response = requests.get(self.base_url + self.region + '/' +
                                self.battletag)
        soup = BeautifulSoup(response.content, "lxml")
        comp = soup.find('div', {'id': 'competitive'})
        mode = {}

        stats = self.locate_stats(comp)
        mode[self.hero] = stats

        return mode[self.hero][self.filter]


    def locate_stats(self, soup):
        """
        Use for finding individual competitive hero stats
        """
        for hero in soup.find_all('div', {'data-category-id': self.heroes[self.hero][1]}):
            all_stats = {}
            for block in hero.find_all('div', {'card-stat-block'}):
                stats = []
                label = block.find('span', {'class': 'stat-title'})
                for attr in block.find_all('td'):
                    stats.append(attr.text)
                all_stats[label.text.lower()] = stats
            return all_stats


    def get_time_played(self, tree):
        """
        Gets time played for all heroes
        """
        xpath = '//*[@id="' + self.mode +'"]/section[2]/div/div[2]/div/div' \
                '/div/div/text()'

        return tree.xpath(xpath)


    def dict_zip(self, results):
        """
        Converts list of results into a dictionary
        """
        labels = [results[i] for i in range(0, len(results), 2)]
        data = [results[i] for i in range(1, len(results), 2)]

        return dict(zip(labels, data))


    def display_filters(self):
        """
        Displays available filters for users
        """
        response = requests.get(self.base_url + self.region + '/' +
                                self.battletag)
        tree = html.fromstring(response.content)

        xpath = '//*[@id="quickplay"]/section[3]/div/div[3]/div/div/table/thead/tr/th/span/text()'
        filters = tree.xpath(xpath)
        filters = [word.lower() for word in filters]
        filters.append('played')

        print(filters)
