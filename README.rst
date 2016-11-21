A wrapper for playoverwatch.com stats

Installation
------------

    pip install python-overwatch

Examples
------------

Average stats for all heroes

.. code:: python

    from overwatch import Overwatch

    average = Overwatch(battletag=battletag, mode='quickplay',
                        filter='featured')
    results = average.get_results()
    print(results)

    ['Eliminations - Average', '27.56', 'Damage Done - Average', '15,005',
     'Deaths - Average', '11.3', 'Final Blows - Average', '14.5',
     'Healing Done - Average', '1,418', 'Objective Kills - Average', '10.86',
     'Objective Time - Average', '01:10', 'Solo Kills - Average', '3.28']
