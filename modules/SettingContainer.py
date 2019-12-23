
class SettingContainer():
    key_list = ["value_dict", "suit_dict", "position_dict", "gamemode_dict", "standart_order_dict",
                "standart_order_dict", "null_order_dict", "bid_list", "bidmessage", "skatmessage",
                "yesno_errormessage", "cardmessage", "card_errormessage", "gamemode_message",
                "gamemode_errormessage", "tablecard_message", "play_errormessage", "winner_message",
                "point_message", "end_round_message"]

    def __init__(self, setting_dict, **settings):
        self.check_keys(setting_dict)

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

    def check_keys(self, setting_dict):
        for key in self.key_list:
            if not key in setting_dict:
                raise Exception(f"No value for {key} found in language-settings")
