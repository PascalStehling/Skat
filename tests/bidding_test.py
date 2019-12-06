import sys
sys.path.insert(0, r"C:/Users/Pascal/Desktop/Skat")

from modules import bidding
import unittest

class Test_get_player_turn(unittest.TestCase):

    def reset_game_dict(self, turn=1, passed=[]):
        self.game_dict = {"turn": turn, "bidding":{}, "players":{}}
        self.game_dict["bidding"]["passed"] = passed
        self.game_dict["players"][0] = {}
        self.game_dict["players"][0]["position"] = 0
        self.game_dict["players"][1] = {}
        self.game_dict["players"][1]["position"] = 1
        self.game_dict["players"][2] = {}
        self.game_dict["players"][2]["position"] = 2

    # No One passed, Only Forhand and middlehand can make plays/pass
    def test_no_passed_middlehand_made_play(self):
        self.reset_game_dict()
        self.assertEqual(bidding.get_new_turn(self.game_dict), 0) # After middlehand played, forhand needs to play next

    def test_no_passed_forhand_made_play(self):
        self.reset_game_dict(turn=0)
        self.assertEqual(bidding.get_new_turn(self.game_dict), 1) # After forhand played, middlehand needs to play next

    def test_no_passed_middlehand_passed(self):
        self.reset_game_dict(passed=[1])
        self.assertEqual(bidding.get_new_turn(self.game_dict), 2) # After middlehand passed, backhand needs to play next

    def test_no_passed_forhand_passed(self):
        self.reset_game_dict(turn=0, passed=[0])
        self.assertEqual(bidding.get_new_turn(self.game_dict), 2) # After forhand passed, backhand needs to play next


    # One Forhand or Middlehand passed --> backhand plays with the other one
    def test_middlehand_passed_backhand_play(self):
        self.reset_game_dict(turn=2, passed=[1])
        self.assertEqual(bidding.get_new_turn(self.game_dict), 0) # After middlehand passed and backhand played, forhand needs to play next

    def test_middlehand_passed_forhand_play(self):
        self.reset_game_dict(turn=0, passed=[1])
        self.assertEqual(bidding.get_new_turn(self.game_dict), 2) # After middlehand passed and forhand played, backhand needs to play next

    def test_forhand_passed_backhand_play(self):
        self.reset_game_dict(turn=2, passed=[0])
        self.assertEqual(bidding.get_new_turn(self.game_dict), 1) # After forhand passed and backhand played, middlehand needs to play next

    def test_forhand_passed_middlehand_play(self):
        self.reset_game_dict(turn=1, passed=[0])
        self.assertEqual(bidding.get_new_turn(self.game_dict), 2) # After forhand passed and middlehand played, backhand needs to play next


    # One Forhand or Middlehand passed --> backhand or other one passes (only possible if no one bidded yet, otherwise this function would not be called)
    def test_middlehand_passed_backhand_passes(self):
        self.reset_game_dict(turn=2, passed=[1,2])
        self.assertEqual(bidding.get_new_turn(self.game_dict), 0) # After middlehand and backhand passed, forhand needs to play next

    def test_middlehand_passed_forhand_passes(self):
        self.reset_game_dict(turn=0, passed=[1,0])
        self.assertEqual(bidding.get_new_turn(self.game_dict), 2) # After middlehand and forhand passed, backhand needs to play next

    def test_forhand_passed_backhand_passes(self):
        self.reset_game_dict(turn=2, passed=[0,2])
        self.assertEqual(bidding.get_new_turn(self.game_dict), 1) # After forhand and backhand passed, middlehand needs to play next

    def test_forhand_passed_middlehand_passes(self):
        self.reset_game_dict(turn=1, passed=[0,1])
        self.assertEqual(bidding.get_new_turn(self.game_dict), 2) # After forhand and middlehand passed, backhand needs to play next

    
class Test_check_end_bidding(unittest.TestCase):

    def reset_game_dict(self, passed=[], player=None):
        self.game_dict = {"bidding":{}}
        self.game_dict["bidding"]["passed"] = passed
        self.game_dict["bidding"]["bid_player"] = player

    def test_no_one_passes(self):
        self.reset_game_dict()
        self.assertFalse(bidding.is_end_bidding(self.game_dict))

    def test_one_passes(self):
        self.reset_game_dict(passed=[1])
        self.assertFalse(bidding.is_end_bidding(self.game_dict))

    def test_two_passes(self):
        self.reset_game_dict(passed=[1,2])
        self.assertFalse(bidding.is_end_bidding(self.game_dict))

    def test_three_passes(self):
        self.reset_game_dict(passed=[1,2,0])
        self.assertTrue(bidding.is_end_bidding(self.game_dict))

    def test_one_passes_one_plays(self):
        self.reset_game_dict(passed=[1], player=0)
        self.assertFalse(bidding.is_end_bidding(self.game_dict))
    
    def test_two_passes_one_plays(self):
        self.reset_game_dict(passed=[1,2], player=0)
        self.assertTrue(bidding.is_end_bidding(self.game_dict))

if __name__ == "__main__":
    unittest.main()