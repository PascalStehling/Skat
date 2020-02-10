Functional Programming
======================

Only Final Datastructures: 

    * SettingContainer is only created once in main.py and then only passed on, but not overwritten/changed.
    * Card objects are only created once when the cards are dealt and then passed on. A change of the cards does not take place here either. Each new round the old cards are deleted and new ones are created. This is done in the function create_shuffled_cards in Cards.py.

(mostly) side effect free functions:

    * In this project we tried that all functions are as good as SiedeEffect free. This can be seen particularly well in the Bidding.py. Often the only exceptions are the functions which have to display information for the user on the terminal.

the use of higher order functions:

    * The use of higher order functions can be found in several classes. Most often it occurs in the SettingContainer.py in the form of the @staticmethod Decorator. A decorator in Python is a wrapper function which takes the function written below as input and executes it. So every decorator is always a higher order function.

use clojures / anonymous functions and function as parameter:

    * The function get_sorted_suit_list in the SettingContainer.py uses a lambda function, which is a parameter of the sorted function, to specify the value to be sorted by.