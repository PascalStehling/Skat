import sys
sys.path.append('../')

from modules.SettingContainer import SettingContainer
import unittest

class Test_SettingContainer(unittest.TestCase):

    def test_create_SettingContainer_from_file(self):
        settingContainer = SettingContainer.create_SettingContainer_from_file()
        self.assertEqual(settingContainer.bidmessage, "{}: Do you want to bid {}? With Yes you accept the bid, with No you pass.")

    def test_load_setting_file(self):
        with self.assertRaises(Exception):
            SettingContainer._load_setting_file("hu")

        SettingContainer._load_setting_file("en")
        SettingContainer._load_setting_file("de")

    def test_create_bid_list(self):
        bid_list = SettingContainer._create_bid_list({"1":{"trumpf": "Kr", "points": 12}})
        self.assertListEqual(bid_list, [23, 24, 36, 48, 60])

        gamemode = {
        "0": {
            "name": "Farbspiel: Kreuz",
            "trumpf": "Kr",
            "order_dict": "standart_order_dict",
            "points": 12
        },
        "1": {
            "name": "Farbspiel: Pik",
            "trumpf": "P",
            "order_dict": "standart_order_dict",
            "points": 11
        },
        "2": {
            "name": "Farbspiel: Herz",
            "trumpf": "H",
            "order_dict": "standart_order_dict",
            "points": 10
        },
        "3": {
            "name": "Farbspiel: Karo",
            "trumpf": "Ka",
            "order_dict": "standart_order_dict",
            "points": 9
        },
        "4": {
            "name": "Grand",
            "trumpf": "B",
            "order_dict": "standart_order_dict",
            "points": 24
        },
        "5": {
            "name": "Null",
            "trumpf": None,
            "order_dict": "null_order_dict",
            "points": 23
        }}
        self.assertListEqual(SettingContainer._create_bid_list(gamemode), [18, 20, 22, 23, 24, 27, 30, 33, 36, 40, 44, 45, 48, 50, 55, 60, 72, 96, 120])


if __name__ == "__main__":
    unittest.main()
