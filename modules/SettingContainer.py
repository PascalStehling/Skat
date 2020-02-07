# pylint: disable=line-too-long, invalid-name
"""This File contains the SettingContainer Class
"""
from itertools import product
import json
import os


class SettingContainer():
    """This Class contains all Settings which are relevant for the Game.
    """
    key_list = ["value_dict", "suit_dict", "position_dict", "gamemode_dict", "standart_order_dict",
                "standart_order_dict", "null_order_dict", "bid_list", "bidmessage", "skatmessage",
                "yesno_errormessage", "cardmessage", "card_errormessage", "gamemode_message",
                "gamemode_errormessage", "tablecard_message", "play_errormessage", "winner_message",
                "point_message", "end_round_message"]

    def __init__(self, setting_dict):
        self.value_dict = setting_dict["value_dict"]
        self.suit_dict = setting_dict["suit_dict"]
        self.position_dict = setting_dict["position_dict"]
        self.gamemode_dict = setting_dict["gamemode_dict"]
        self.standart_order_dict = setting_dict["standart_order_dict"]
        self.null_order_dict = setting_dict["null_order_dict"]
        self.order_dicts = {"standart_order_dict": self.standart_order_dict,
                            "null_order_dict": self.null_order_dict}
        self.bid_list = setting_dict["bid_list"]

        self.bidmessage = setting_dict["bidmessage"]
        self.skatmessage = setting_dict["skatmessage"]
        self.yesno_errormessage = setting_dict["yesno_errormessage"]
        self.cardmessage = setting_dict["cardmessage"]
        self.card_errormessage = setting_dict["card_errormessage"]
        self.gamemode_message = setting_dict["gamemode_message"]
        self.gamemode_errormessage = setting_dict["gamemode_errormessage"]
        self.tablecard_message = setting_dict["tablecard_message"]
        self.play_errormessage = setting_dict["play_errormessage"]
        self.winner_message = setting_dict["winner_message"]
        self.point_message = setting_dict["point_message"]
        self.end_round_message = setting_dict["end_round_message"]

        self.START_ROUND = 1
        self.PLAY_ROUND = 2

        self.FORHAND_POSITION = 0
        self.MIDDLEHAND_POSITION = 1
        self.BACKHAND_POSITION = 2

        self.sorted_suit_list = self.get_sorted_suit_list()

    def get_sorted_suit_list(self):
        """returns a sorted list of all suits

        Returns:
            List: the List of string with the suits
        """
        return [x[0] for x in sorted(self.suit_dict.items(), key=lambda x: x[1], reverse=True)]

    @staticmethod
    def _check_keys(setting_dict):
        """check if alle neccessary can be found in the setting dict

        Args:
            setting_dict (dict): The Dictionary with all settings

        Raises:
            Exception: The Key which is missing
        """
        for key in SettingContainer.key_list:
            if not key in setting_dict:
                raise Exception(
                    f"No value for {key} found in language-settings")

    @staticmethod
    def create_SettingContainer_from_file(language="en"):
        """creates a SettingContainer Object from a setting.json file

        Args:
            language (str, optional): the Language of the game. Defaults to "en".

        Returns:
            SettingContainer: returns a SettingContainer Object
        """
        set_dict = SettingContainer._load_setting_file(language)
        set_dict["bid_list"] = SettingContainer._create_bid_list(
            set_dict["gamemode_dict"])
        SettingContainer._check_keys(set_dict)
        return SettingContainer(set_dict)

    @staticmethod
    def _load_setting_file(language):
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "language-settings", "Settings-"+language+".json"), "r", encoding="utf-8") as f:
                return json.loads(f.read())
        except FileNotFoundError:
            raise Exception("This language does not exists!")

    @staticmethod
    def _create_bid_list(gamemode_dict):
        point_list = [mode["points"]
                      for mode in gamemode_dict.values() if mode["trumpf"] is not None]
        bid_list = [x[0]*x[1] for x in product(point_list, range(2, 6))]
        bid_list.append(23)  # Add Null Value
        return sorted(set(bid_list))
