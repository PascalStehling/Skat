"""
In this file all Functions are located which are needed to setup a new round
"""
from itertools import product
from card import Card, print_multiple_cards
from random import shuffle
def setup_round(game_dict):
    """
    Gives every Player his cards and resets all Settings to start a new round
    """
    cards = give_cards_shuffled(game_dict["settings"])
    for i in range(3):
        game_dict["players"][i]["cards"] = cards[10*i:10*(i+1)]
        game_dict["players"][i]["passed"] = False
    game_dict["skat"] = cards[-2:]
    game_dict["turn"] = get_start_player_bidding(game_dict["players"]) # Who starts with bidding
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

def get_start_player_bidding(players_dict):
    """
    returns the key of the Player who is first with bidding
    """
    for key in players_dict:
        if players_dict[key]["position"] == 1:
            return key


