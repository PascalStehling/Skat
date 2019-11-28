    
import unittest
import sys

sys.path.insert(0, r"C:/Users/Pascal/Desktop/Skat")
from modules import card
from modules.tools import print_multiple_cards



class Test_tools(unittest.TestCase):

    value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'B': 2, 'D': 3, 'K': 4, 'A': 11}
    suit_dict = {"Kr": 12, "P": 11, "H": 10, "Ka": 9}

    def test_print_multiple_cards_type(self):
        c1 = card.Card('7', 'Kr', self.value_dict, self.suit_dict)
        c2 = card.Card('K', 'H', self.value_dict, self.suit_dict)
        c3 = card.Card('A', 'P', self.value_dict, self.suit_dict)
        c4 = card.Card('10', 'Ka', self.value_dict, self.suit_dict)
        cards = [c1,c2,c3,c4]
        with self.assertRaises(TypeError):
            print_multiple_cards("cards")
        with self.assertRaises(TypeError):
            print_multiple_cards(cards+["asd"])

        print()
        print_multiple_cards(cards) # Test if its looks right