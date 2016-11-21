A wrapper for playoverwatch.com stats

Installation
------------

    pip install python-overwatch

Examples
------------

Find your average stats for all heroes

.. code:: python

    from overwatch import Overwatch

    average = Overwatch(battletag=battletag, hero='all', filter='featured')
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
