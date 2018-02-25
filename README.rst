A wrapper for playoverwatch.com stats

Installation
------------

    pip install python-overwatch

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

    ow = Overwatch(battletag="Okush#11324")
    print(ow.playtime)

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

    mei = Overwatch(battletag="Okush#11324", hero='mei', filter='hero specific')
    results = mei()
    print(results)

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

    ow = Overwatch(battletag="Okush#11324", hero='all')
    results = ow()
    print(results)

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

Find how many D.VA self-destructs you've performed

.. code:: python

    from overwatch import Overwatch

    destructs = Overwatch(battletag="Okush#11324", hero='dva', filter='hero specific')
    results = destructs()
    print(results)

    [
      'Self-Destruct Kills', '39',
      'Self-Destruct Kills - Most in Game', '6',
      'Multikill - Best', '3',
      'Self-Destruct Kills - Average', '2'
    ]

Specify you want competitive mode stats

.. code:: python

    from overwatch import Overwatch

    get_stats = Overwatch(battletag="Okush#11324", mode='cp', hero='pharah')
    results = get_stats()
    print(results)

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

