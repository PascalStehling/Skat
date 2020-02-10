Domain Specific Language
========================
There were 2 cases of DSL in the code. 
The first is in line 43 of Round.py. 
This initializes a Stich object, plays the Stich, assigns the cards to the winner and finally returns the winner.

.. code-block:: python

    self.turn = Stich(self.players, self.turn, self.settings).play_stich().assign_stich_to_winner().get_winner()

The second case can be found in line 29 of main.py. 
Here a round is initialized first, then played and finally finished.

.. code-block:: python

    self.round.setup().play_round().end_round()