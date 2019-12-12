
from itertools import product
import json
import os

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

def create_player(player_name, player_num, player_position):
    """
    Creates a dict with all Information for one Player
    name: Name of the Player
    num: fixed number of the player
    cards: the cards of the Player
    points: the Points of the Player
    position: the position in the game (0 For-, 1 middle-, 2 Backhand)
    bid: the bid of the player. None if he hasn't bid yet, int if he bid, false if he passed
    """
    return {"name": player_name,"num": player_num,"cards": [],"points": 0,"position": player_position}

def create_players(player_names=None):
    """
    Creates a Dictionary with all 3 Players and all there Attributes
    """
    if player_names is None:
        player_names = ["Player 1", "Player 2", "Player 3"]
    elif len(player_names) != 3:
        raise ValueError("You need exactly 3 Players")

    player_dict = {}
    for i, p in enumerate(player_names):
        player_dict[i] = create_player(p, i, i) # The starting possition is the same as the number

    return player_dict

def create_game_dict(player_names=None, max_rounds=36, language='en'):
    """
    Creates the game dict, in which all the data about the game is stored.

    players: has all attributes about the players
    gamestate: the current gamestate: 1: setting up round, 2: bidding phase, TODO
    skat: the cards which are in the skat
    single_player_stack: the cards of the won round from the single player, witch need to be calculated at the end to get the points
    game_round: number of rounds which were Played
    max_rounds: maximum amount of rounds which are played
    gamemode: the gamemode which is played for the round
    turn: the player, who has its turn
    order_dict: The dictionary with the order of witch card is is higher than the other
    """
    return {"players": create_players(player_names),
            "gamestate": 1,
            "skat": [],
            "single_player_stack": [],
            "jack_multiplicator": None,
            "table_cards": [],
            "game_round": 1,
            "max_round": max_rounds,
            "settings": create_settings_from_file(language),
            "gamemode": None,
            "turn": None,
            "bidding": None,
            "order_dict": None}
