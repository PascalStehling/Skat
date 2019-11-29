"""
In this file all Functions are located which are needed to setup a new round
"""
from itertools import product
from modules.card import Card
from random import shuffle
from modules.tools import get_player_at_position, sort_cards
import operator

def setup_round(game_dict):
    """
    Gives every Player his cards and resets all Settings to start a new round
    """
    cards = give_cards_shuffled(game_dict["settings"])
    order_dict = game_dict["settings"]["standart_order_dict"]
    sort_trumpf = [x[0] for x in game_dict["settings"]["suit_dict"].items() if x[1]==12][0]

    for i in range(3):
        # TODO better sorting algorithm, maybe use anywhere where cards get added
        game_dict["players"][i]["cards"] = sort_cards(cards[10*i:10*(i+1)], order_dict, sort_trumpf) # save cards sorted
        game_dict["players"][i]["passed"] = False
    game_dict["skat"] = cards[-2:]
    game_dict["turn"] = get_player_at_position(game_dict, 1) # Player at middle Hand starts with bidding
    game_dict["bidding"] = {"bid": None, "bid_player": None, "passed": [], "next_bid": 18} # Bid dict for bidding
    game_dict["gamestate"] = 2
    game_dict["order_dict"] = None
    game_dict["single_player_stack"] = []
    return game_dict

def give_cards_shuffled(settings):
    """ 
    Creates 32 cards and returns them shuffled
    """
    card_nums = product(settings["value_dict"].keys(), settings["suit_dict"].keys()) # cartesian Product to get all possible card values
    cards = [Card(card[0], card[1], settings["value_dict"], settings["suit_dict"]) for card in card_nums]
    shuffle(cards)
    return cards
