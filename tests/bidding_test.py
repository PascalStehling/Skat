import sys
sys.path.append('../')

from modules.bidding import *
import unittest

class Test_bidding(unittest.TestCase):

    def test_is_end_bidding(self):
        self.assertFalse(is_end_bidding([], None))
        self.assertFalse(is_end_bidding([], 1))

        self.assertFalse(is_end_bidding([0], None))
        self.assertFalse(is_end_bidding([0], 1))

        self.assertFalse(is_end_bidding([0,1], None))
        self.assertTrue(is_end_bidding([0,1], 1))

        self.assertTrue(is_end_bidding([0,1,2], None))
        self.assertTrue(is_end_bidding([0,1,2], 1))

    def test_end_bidding(self):
        self.assertTupleEqual(end_bidding(None, 2), (2,1))
        self.assertTupleEqual(end_bidding(0, 1), (0,3))

    def test_check_end_bidding(self):
        self.assertTupleEqual(check_end_bidding(1, [0], 2, 1, 2, 0, 1, 2), (1, 2))
        self.assertTupleEqual(check_end_bidding(1, [0,2], 2, 1, 2, 1, 2, 0), (1, 3))

    def test_turn_if_not_passed_backhand(self):
        self.assertEqual(turn_if_not_passed_backhand(2, 1, [0]), 2)
        self.assertEqual(turn_if_not_passed_backhand(2, 1, [2]), 1)

    def test_turn_if_not_passed_forhand(self):
        self.assertEqual(turn_if_not_passed_forhand(2,0, [1]), 2)
        self.assertEqual(turn_if_not_passed_forhand(2,0, [2]), 0)

    def test_turn_if_not_passed_middlehand(self):
        self.assertEqual(turn_if_not_passed_middlehand(1,0, [2]), 1)
        self.assertEqual(turn_if_not_passed_middlehand(1,0, [1]), 0)

    def test_turn_if_not_passed(self):
        self.assertEqual(turn_if_not_passed(0, 1, 2, 0, [2]), 0)
        self.assertEqual(turn_if_not_passed(1, 1, 2, 0, [1]), 0)
        self.assertEqual(turn_if_not_passed(2, 1, 2, 0, [1]), 2)
        with self.assertRaises(Exception):
            turn_if_not_passed(4, 1, 2, 0, [0])
    
    def test_turn_if_passed(self):
        self.assertEqual(turn_if_passed(1, 2, 0, 1, [0]), 1)
        self.assertEqual(turn_if_passed(2, 2, 0, 1, [1,0]), 2)
        self.assertEqual(turn_if_passed(2, 2, 0, 1, [1,2]), 0)

    def test_get_new_turn(self):
        self.assertEqual(get_new_turn(2,1,1,2,0,[]), 1)
        self.assertEqual(get_new_turn(2,1,1,2,0,[2]), 0)

    def test_bid_hear(self):
        self.assertDictEqual(bid_hear({}, 24, 2, [22,23,24,26,28]), {"bid_player":2, "next_bid": 26})
        with self.assertRaises(ValueError):
            bid_hear({}, 28, 2, [22,23,24,26,28])

    def test_bid_say(self):
        self.assertDictEqual(bid_say({"bid_player":None, "bid": None}, 24,2), {"bid_player":2, "bid": 24})

    def test_update_bid_dict_middlehand_player(self):
        self.assertDictEqual(update_bid_dict_middlehand_player(24,2,[22,23,24,26,28], 1, {"passed": [1], "bid_player": None, "bid": None, "next_bid": None}),
                                {"passed": [1], "bid_player": 2, "bid": None, "next_bid": 26})

        self.assertDictEqual(update_bid_dict_middlehand_player(24,2,[22,23,24,26,28], 1, {"passed": [], "bid_player": None, "bid": None, "next_bid": None}),
                                {"passed": [], "bid_player": 2, "bid": 24, "next_bid": None})

    def test_update_bid_dict_positiv_bid(self):
        self.assertDictEqual(update_bid_dict_positiv_bid(0, 24, [23,24,26], 0, 0, {"passed": [], "bid_player": None, "bid": None, "next_bid": None}),
                                {"passed": [], "bid_player": 0, "bid": None, "next_bid": 26})
        
        self.assertDictEqual(update_bid_dict_positiv_bid(1, 24, [23,24,26], 0, 0, {"passed": [], "bid_player": None, "bid": None, "next_bid": None}),
                                {"passed": [], "bid_player": 0, "bid": 24, "next_bid": None})

        self.assertDictEqual(update_bid_dict_positiv_bid(2, 24, [23,24,26], 0, 0, {"passed": [], "bid_player": None, "bid": None, "next_bid": None}),
                                {"passed": [], "bid_player": 0, "bid": 24, "next_bid": None})

    def test_update_bid_dict(self):
        self.assertDictEqual(update_bid_dict(False, 24, {"passed": [], "bid_player": None, "bid": None, "next_bid": None}, [23,24,26], 0, 0, 0),
                                {"passed": [0], "bid_player": None, "bid": None, "next_bid": None})
        self.assertDictEqual(update_bid_dict(True, 24, {"passed": [], "bid_player": None, "bid": None, "next_bid": None}, [23,24,26], 0, 0, 0),
                                {"passed": [], "bid_player": 0, "bid": None, "next_bid": 26})

                
    

if __name__ == "__main__":
    unittest.main()