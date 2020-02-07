import sys
sys.path.append('../')

from modules.Players import Players
from modules.Player import Player
from modules.SettingContainer import SettingContainer
import unittest
from copy import deepcopy

class Test_Players(unittest.TestCase):
    settingContainer = SettingContainer.create_SettingContainer_from_file()
    def test_players_init(self):
        
        players = Players(self.settingContainer)
        self.assertEqual(players.players[1].name, "Player 2")

        with self.assertRaises(ValueError):
            Players(self.settingContainer, player_names=["1", "2", "3", "4"])
        
        players = Players(self.settingContainer, player_names=["1", "2", "3"], auto_play_cards=True)
        self.assertTrue(players.players[2].auto_play)

    def test_iter(self):
        Player.player_count=0
        players = Players(self.settingContainer)

        num_sum = 0
        for player in players:
            num_sum += player.num
        self.assertEqual(num_sum, 3)

    def test_get_next_player(self):
        Player.player_count=0
        players = Players(self.settingContainer)
        self.assertEqual(players.get_next_player(players.players[0]).num, 1)
        self.assertEqual(players.get_next_player(players.players[2]).num, 0)

    def test_set_players_on_next_position(self):
        Player.player_count=0
        players = Players(self.settingContainer)

        p_forhand = deepcopy(players.forhand)
        players.set_players_on_next_position()
        self.assertEqual(p_forhand, players.middlehand)

    def test_get_player_by_num(self):
        Player.player_count=0
        players = Players(self.settingContainer)

        self.assertEqual(players.get_player_by_num(1), players.players[1])
        with self.assertRaises(Exception):
            players.get_player_by_num(4)
