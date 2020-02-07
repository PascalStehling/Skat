import sys
sys.path.append('../')

from modules.Player import Player
import unittest

class Test_Player(unittest.TestCase):

    def test_player_init(self):
        with self.assertRaises(TypeError):
            Player(["Name"])
        
        Player("Name")
        player = Player("Name", auto_play_cards=True)
        self.assertTrue(player.auto_play)

    def test_equal(self):
        player1 = Player("1")
        player2 = Player("2")
        with self.assertRaises(TypeError):
            player1 == "Player 2"

        self.assertFalse(player1 == player2)
        self.assertTrue(player1 == player1)

    def test_repr(self):
        Player.player_count = 0
        self.assertEqual(repr(Player("Player 1")), "0: Player 1")

    def test_has_cards(self):
        player = Player("1")
        self.assertFalse(player.has_cards())
        player.cards = ["Karte"]
        self.assertTrue(player.has_cards())

if __name__ == "__main__":
    unittest.main()