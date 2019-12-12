import unittest
import sys

sys.path.append('../')
from modules.card import Card
from modules.end_round import *

class Test_end_round(unittest.TestCase):
    value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'B': 2, 'D': 3, 'K': 4, 'A': 11}
    suit_dict = {"Kr": 12, "P": 11, "H": 10, "Ka": 9}
    order_dict = {'7': 0, '8': 1, '9': 2, '10': 5, 'B': 7, 'D': 3, 'K': 4, 'A': 6}

    def test_has_over_bidded(self):

        self.assertTrue(has_over_bidded(None, 24, 1, 12))
        self.assertFalse(has_over_bidded(None, 24, 1, 26))


        self.assertFalse(has_over_bidded("Kr", 22, 3, 12))
        self.assertFalse(has_over_bidded("Kr", 24, 2, 12))
        self.assertFalse(has_over_bidded("H", 24, 3, 10))

    def test_has_won_round(self):

        self.assertTrue(has_won_round(65, "Kr", 22, 3, 12))
        self.assertTrue(has_won_round(90, "Kr", 24, 2, 12))
        self.assertTrue(has_won_round(95, "Kr", 24, 3, 12))

        self.assertFalse(has_won_round(65, "Kr", 24, 1, 12))
        self.assertTrue(has_won_round(65, "Kr", 24, 3, 12))

        self.assertFalse(has_won_round(60, "Kr", 24, 2, 12))
        self.assertFalse(has_won_round(30, "Kr", 24, 3, 12))

    def test_calc_card_points(self):
        a = Card("7", 'Kr', self.value_dict, self.suit_dict)
        b = Card("B", 'H', self.value_dict, self.suit_dict)
        c = Card("10", 'Kr', self.value_dict, self.suit_dict)

        self.assertEqual(calc_card_points([a,b,c]), 12)

    def test_get_win_level(self):
        self.assertEqual(get_win_level(120), 2)
        self.assertEqual(get_win_level(100), 1)
        self.assertEqual(get_win_level(80), 0)
    
    def test_calc_points_lost(self):
        self.assertEqual(calc_score_points_lost(40, 2, 12), -48)
        self.assertEqual(calc_score_points_lost(0, 2, 12), -96)

    def test_calc_points_won(self):
        self.assertEqual(calc_score_points_won(65, 3, 10), 30)
        self.assertEqual(calc_score_points_won(95, 4, 11), 55)

    def test_calculate_score(self):
        self.assertEqual(calculate_score(65, "Kr", 22, 3, 12), 36)
        self.assertEqual(calculate_score(55, "Kr", 22, 3, 10), -60)

        self.assertEqual(calculate_score(120, "Kr", 22, 4, 11), 66)
        self.assertEqual(calculate_score(22, "Kr", 22, 4, 11), -110)

if __name__ == "__main__":
    unittest.main()

