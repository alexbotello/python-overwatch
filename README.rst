An Overwatch stat scraper designed for ease of use. 
Plug in a battletag, select the desired hero and filter, and call the function.
The data will be returned as a list, ready to manipulate and use as you wish.

Installation
------------

    pip install python-overwatch

Requirements
------------
Python 3.6

Usage
------------

.. code:: python

    Modes:  qp
            cp

    Filters: combat, assists, best, average, deaths, match awards
             game, miscellaneous, hero specific

    # Default filter: 'best'
    # Default mode: 'qp'

Examples
------------

Find play time for all heroes

.. code:: python

    from overwatch import Overwatch

    overwatch = Overwatch(battletag="Okush#11324")
    print(overwatch.playtime)

    [
      'Pharah', '40 hours',
      'Roadhog', '32 hours',
      'Mei', '29 hours',
      'McCree', '20 hours',
      'Soldier: 76', '17 hours',
      'Mercy', '13 hours',
    ]

Find hero specific stats

.. code:: python

    from overwatch import Overwatch

    overwatch = Overwatch(battletag="Okush#11324")
    print(overwatch(hero="mei", filter="hero specific))

    [
      'Enemies Frozen', '1,885',
      'Enemies Frozen - Most in Game', '30',
      'Blizzard Kills - Most in Game', '13',
      'Blizzard Kills', '587',
      'Damage Blocked - Most in Game', '12,569',
      'Damage Blocked', '442,710',
      'Melee Final Blows - Most in Game', '4',
      'Enemies Frozen - Average', '10.73',
      'Damage Blocked - Average', '2,521',
      'Blizzard Kills - Average', '3.34'
    ]

Find overall best stats

.. code:: python

    from overwatch import Overwatch

    overwatch = Overwatch(battletag="Okush#11324")
    print(overwatch())

    [
      'Eliminations - Most in Game', '48',
      'Final Blows - Most in Game', '31',
      'Damage Done - Most in Game', '23,924',
      'Healing Done - Most in Game', '14,379',
      'Defensive Assists - Most in Game', '26',
      'Offensive Assists - Most in Game', '8',
      'Objective Kills - Most in Game', '32',
      'Objective Time - Most in Game', '04:22',
      'Multikill - Best', '5',
      'Solo Kills - Most in Game', '31',
      'Time Spent on Fire - Most in Game', '13:29'
    ]

Find combat stats for any hero

.. code:: python

    from overwatch import Overwatch

    overwatch = Overwatch(battletag="Okush#11324")
    print(overwatch(hero="dva", filter="combat"))

    [
      'Eliminations', '541', 
      'Deaths', '149', 
      'Final Blows', '264', 
      'Solo Kills', '89', 
      'All Damage Done', '220,531', 
      'Objective Kills', '172', 
      'Objective Time', '30:47', 
      'Multikills', '9', 
      'Environmental Kills', '2', 
      'Melee Final Blows', '5', 
      'Time Spent on Fire', '36:05', 
      'Critical Hits', '4,436', 
      'Hero Damage Done', '3,111', 
      'Barrier Damage Done', '3,827', 
      'Critical Hit Accuracy', '8%', 
      'Weapon Accuracy', '31%']
    ]

Specify you want competitive mode stats

.. code:: python

    from overwatch import Overwatch

    overwatch = Overwatch(battletag="Okush#11324")
    print(overwatch(mode="cp", hero="pharah", filter="best"))

    [
      'Eliminations - Most In Life, '12',
      'All Damage Done - Most In Game', '6,943',
      'Weapon Accuracy - Best In Game', '65%',
      'Kill Streak - Best', '12',
      'All Damage Done - Most In Game', '37,699',
      'Eliminations - Most In Game', '61',
      'Final Blows - Most In Game', '45',
      'Objective Kills - Most In Game', '33',
      'Objective Time - Most In Game', '01:27',
      'Solo Kills - Most In Game', '7' 
    ]

