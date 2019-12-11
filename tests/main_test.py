import sys

from modules import create_settings as main
import unittest


class Test_create_players(unittest.TestCase):

    def test_none(self):
        self.assertEqual(main.create_players()[0]["name"], "Player 1")

    def test_names(self):
        self.assertEqual(main.create_players(["1", "2", "3"])[1]["name"], "2")


class Test_create_settings(unittest.TestCase):
    
    def test_right_values(self):
        self.assertDictEqual(main.create_settings_from_file('de')["suit_dict"], {"Kr": 12, "P": 11, "H": 10, "Ka": 9})