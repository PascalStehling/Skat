import unittest
import sys

sys.path.insert(0, r"C:/Users/Pascal/Desktop/Skat")
from modules import card

class Test_card(unittest.TestCase):

    value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'B': 2, 'D': 3, 'K': 4, 'A': 11}
    suit_dict = {"Kr": 12, "P": 11, "H": 10, "Ka": 9}

    def test_card_wrong_input_types(self):
        with self.assertRaises(TypeError):
            c = card.Card(7, 'Kr', self.value_dict, self.suit_dict)

        with self.assertRaises(TypeError):
            c = card.Card('7', 23, self.value_dict, self.suit_dict)

        with self.assertRaises(TypeError):
            c = card.Card('7', 'Kr', [], self.suit_dict)

        with self.assertRaises(TypeError):
            c = card.Card('7', 'Kr', self.value_dict, [])

    def test_card_wrong_input_values(self):
        with self.assertRaises(ValueError):
            c = card.Card('5', 'Kr', self.value_dict, self.suit_dict)

        with self.assertRaises(ValueError):
            c = card.Card('7', '23', self.value_dict, self.suit_dict)