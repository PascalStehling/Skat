
from itertools import product
import json
import os
from modules.player_class import Players
from modules.setting_container import SettingContainer

def create_settings_from_file(language="en"):
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "language-settings","Settings-"+language+".json"), "r", encoding="utf-8") as f:
            set_dict = json.loads(f.read())
    except FileNotFoundError as e:
        raise Exception("This language does not exists!")

    # Create Bid list
    # Get all Values except Null for bidding, Null is added afterwards, the Number of Jacks dont care for that
    point_list = [mode["points"] for mode in set_dict["gamemode_dict"].values() if mode["trumpf"] is not None]
    bid_list = [x[0]*x[1] for x in product(point_list, range(2, 6))]
    bid_list.append(23) # Add Null Value
    bid_list.sort()

    set_dict["bid_list"] = bid_list

    return set_dict

def create_game_objects(settings):
    players = Players(settings.get("player_names", ["Player 1", "Player 2", "Player 3"]))
    settings = SettingContainer(create_settings_from_file(settings.get("language", "en")))
    return players, settings
