"""
In this file all Functions are located which are needed to setup a new round
"""
from itertools import product
from modules.card import Card
from random import shuffle
from modules.tools import get_player_at_position
import operator

def setup_round(game_dict):
    """
    Gives every Player his cards and resets all Settings to start a new round
    """
    cards = give_cards_shuffled(game_dict["settings"])
    for i in range(3):
        game_dict["players"][i]["cards"] = sorted(cards[10*i:10*(i+1)], key=lambda tmp_card: tmp_card.get_card_tuple()) # save cards sorted
        game_dict["players"][i]["passed"] = False
    game_dict["skat"] = cards[-2:]
    game_dict["turn"] = get_player_at_position(game_dict, 1) # Player at middle Hand starts with bidding
    game_dict["bidding"] = {"bid": None, "bid_player": None, "passed": [], "next_bid": 18} # Bid dict for bidding
    game_dict["gamestate"] = 2
    return game_dict

def give_cards_shuffled(settings):
    """ 
    Creates 32 cards and returns them shuffled
    """
    card_nums = product(settings["value_dict"].keys(), settings["suit_dict"].keys()) # cartesian Product to get all possible card values
    cards = [Card(card[0], card[1], settings["value_dict"], settings["suit_dict"]) for card in card_nums]
    shuffle(cards)
    return cards