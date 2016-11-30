A wrapper for playoverwatch.com stats

Installation
------------

    pip install python-overwatch

Usage
------------

    Modes:  quickplay
            competitive

    Filters: combat, assists, best, average, deaths, match awards
             game, miscellaneous, hero specific, played, featured

Examples
------------

Find your average stats for all heroes

.. code:: python

    from overwatch import Overwatch

    average = Overwatch(battletag=battletag, hero='all', mode='quickplay',
                        filter='featured')
    results = average.get_results()
    print(results)

    [
      'Eliminations - Average', '27.56',
      'Damage Done - Average', '15,005',
      'Deaths - Average', '11.3',
      'Final Blows - Average', '14.5',
      'Healing Done - Average', '1,418',
      'Objective Kills - Average', '10.86',
      'Objective Time - Average', '01:10',
      'Solo Kills - Average', '3.28'
    ]

Find hero specific stats

.. code:: python

    from overwatch import Overwatch

    mei = Overwatch(battletag=battletag, hero='mei', filter='hero specific')
    results = mei.get_results()
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

    best = Overwatch(battletag=battletag, hero='all', filter='best')
    results = best.get_results()
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

    selfies = Overwatch(battletag=battletag, hero='dva',
                        mode='quickplay', filter='miscellaneous')
    results = selfies.get_results()
    print(results)

    [
      'Self-Destruct Kills', '39',
      'Self-Destruct Kills - Most in Game', '6',
      'Multikill - Best', '3',
      'Self-Destruct Kills - Average', '2'
    ]
