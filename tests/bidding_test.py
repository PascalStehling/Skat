import sys
sys.path.append('../')

from modules.Bidding import Bidding
from modules.SettingContainer import SettingContainer
from modules.Players import Players
from modules.Player import Player
import unittest

class Test_bidding(unittest.TestCase):

    def setUp(self):
        Player.player_count = 0
        setting = SettingContainer.create_SettingContainer_from_file()
        self.players = Players(setting)
        self.bidding = Bidding(setting, self.players)

    def test_is_end_bidding(self):
        self.bidding.passed = []
        self.bidding.bid_player = self.players.get_player_by_num(1)
        self.assertFalse(self.bidding.is_bidding_over())
        
        self.bidding.bid_player = None
        self.assertFalse(self.bidding.is_bidding_over())

        self.bidding.passed = [self.players.get_player_by_num(0)]
        self.assertFalse(self.bidding.is_bidding_over())

        self.bidding.bid_player = self.players.get_player_by_num(1)
        self.assertFalse(self.bidding.is_bidding_over())

        self.bidding.passed = [self.players.get_player_by_num(0), self.players.get_player_by_num(1)]
        self.assertTrue(self.bidding.is_bidding_over())

        self.bidding.bid_player = None
        self.assertFalse(self.bidding.is_bidding_over())
        
        self.bidding.passed = [self.players.get_player_by_num(0), self.players.get_player_by_num(1), self.players.get_player_by_num(2)]
        self.assertTrue(self.bidding.is_bidding_over())
        
        self.bidding.bid_player = self.players.get_player_by_num(1)
        self.assertTrue(self.bidding.is_bidding_over())

    def test_end_bidding(self):
        self.bidding.bid_player = None
        self.assertTupleEqual(self.bidding.end_bidding(), (None, 1))
        self.bidding.bid_player = self.players.get_player_by_num(0)
        self.assertTupleEqual(self.bidding.end_bidding(), (self.players.get_player_by_num(0), 2))

    def test_turn_if_not_passed_backhand(self):
        self.bidding.passed = []
        self.bidding._turn_if_not_passed_backhand()
        self.assertEqual(self.bidding.turn, self.players.middlehand)
        self.bidding.passed = [self.players.middlehand]
        self.bidding._turn_if_not_passed_backhand()
        self.assertEqual(self.bidding.turn, self.players.forhand)

    def test_turn_if_not_passed_forhand(self):
        self.bidding.passed = []
        self.bidding._turn_if_not_passed_forhand()
        self.assertEqual(self.bidding.turn, self.players.middlehand)
        self.bidding.passed = [self.players.middlehand]
        self.bidding._turn_if_not_passed_forhand()
        self.assertEqual(self.bidding.turn, self.players.backhand)

    def test_turn_if_not_passed_middlehand(self):
        self.bidding.passed = []
        self.bidding._turn_if_not_passed_middlehand()
        self.assertEqual(self.bidding.turn, self.players.forhand)
        self.bidding.passed = [self.players.forhand]
        self.bidding._turn_if_not_passed_middlehand()
        self.assertEqual(self.bidding.turn, self.players.backhand)

    def test_turn_if_not_passed(self):
        num_list = [1,0,1]
        self.bidding.passed = []
        for i, num in enumerate(num_list):
            self.bidding.turn = self.players.get_player_by_num(i)
            self.bidding._turn_if_not_passed()
            self.assertEqual(self.bidding.turn, self.players.get_player_by_num(num))
    
    def test_turn_if_passed(self):
        self.bidding.turn = self.players.get_player_by_num(0)
        self.bidding._turn_if_passed()
        self.assertEqual(self.bidding.turn, self.players.get_player_by_num(2))

        self.bidding.turn = self.players.get_player_by_num(2)
        self.bidding.passed = [self.players.get_player_by_num(1)]
        self.bidding._turn_if_passed()
        self.assertEqual(self.bidding.turn, self.players.get_player_by_num(0))

        self.bidding.turn = self.players.get_player_by_num(2)
        self.bidding.passed = [self.players.get_player_by_num(0)]
        self.bidding._turn_if_passed()
        self.assertEqual(self.bidding.turn, self.players.get_player_by_num(1))

    def test_get_new_turn(self):
        self.bidding.turn = self.players.get_player_by_num(0)
        self.bidding.get_new_turn()
        self.assertEqual(self.bidding.turn, self.players.get_player_by_num(1))

        self.bidding.turn = self.players.get_player_by_num(0)
        self.bidding.passed = [self.players.get_player_by_num(0)]
        self.bidding.get_new_turn()
        self.assertEqual(self.bidding.turn, self.players.get_player_by_num(2))

    def test_bid_hear(self):
        self.bidding.turn = self.players.get_player_by_num(0)
        with self.assertRaises(ValueError):
            self.bidding.next_bid = 120
            self.bidding._bid_hear()

        self.bidding.next_bid = 23
        self.bidding._bid_hear()
        self.assertEqual(self.bidding.next_bid, 24)

    def test_bid_say(self):
        self.bidding.next_bid = 23
        self.bidding.turn = self.players.get_player_by_num(1)

        self.bidding._bid_say()
        self.assertEqual(self.bidding.bid_player, self.players.get_player_by_num(1))
        self.assertEqual(self.bidding.bid, 23)

    def test_has_forhand_passed(self):
        self.bidding.passed = [self.players.get_player_by_num(0)]
        self.assertTrue(self.bidding._has_forhand_passed())

        self.bidding.passed = [self.players.get_player_by_num(1)]
        self.assertFalse(self.bidding._has_forhand_passed())

        self.bidding.passed = [self.players.get_player_by_num(0), self.players.get_player_by_num(1)]
        self.assertTrue(self.bidding._has_forhand_passed())

        self.bidding.passed = [self.players.get_player_by_num(1), self.players.get_player_by_num(2)]
        self.assertFalse(self.bidding._has_forhand_passed())

    def test_update_bid_dict_middlehand_player(self):
        self.bidding.turn = self.players.get_player_by_num(1)
        self.bidding.passed = []
        self.bidding.next_bid = 23

        self.bidding._update_bid_dict_middlehand_player()
        self.assertEqual(self.bidding.bid_player, self.players.get_player_by_num(1))
        self.assertEqual(self.bidding.bid, 23)

        self.bidding.passed = [self.players.get_player_by_num(0)]
        self.bidding._update_bid_dict_middlehand_player()
        self.assertEqual(self.bidding.next_bid, 24)

    def test_update_bid_dict_yes_to_bid(self):
        self.bidding.passed = []
        self.bidding.turn = self.players.get_player_by_num(0)
        self.bidding.next_bid = 23
        self.bidding._update_bid_dict_yes_to_bid()
        self.assertEqual(self.bidding.next_bid, 24)

        self.bidding.turn = self.players.get_player_by_num(1)
        self.bidding.next_bid = 23
        self.bidding._update_bid_dict_yes_to_bid()
        self.assertEqual(self.bidding.bid_player, self.players.get_player_by_num(1))
        self.assertEqual(self.bidding.bid, 23)

        self.bidding.turn = self.players.get_player_by_num(2)
        self.bidding.next_bid = 23
        self.bidding._update_bid_dict_yes_to_bid()
        self.assertEqual(self.bidding.bid_player, self.players.get_player_by_num(2))
        self.assertEqual(self.bidding.bid, 23)

    def test_process_user_bid(self):
        self.bidding.turn = self.players.get_player_by_num(0)
        self.bidding.passed = []

        self.bidding._process_user_bid(False)
        self.assertListEqual(self.bidding.passed, [self.players.get_player_by_num(0)])

        self.bidding.next_bid = 23
        self.bidding.passed = []
        self.bidding._process_user_bid(True)
        self.assertEqual(self.bidding.next_bid, 24)
        self.assertEqual(self.bidding.bid_player, self.players.get_player_by_num(0))

if __name__ == "__main__":
    unittest.main()