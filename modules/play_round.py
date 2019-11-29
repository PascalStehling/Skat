
from modules.card import EmptyCard, Card
from modules.tools import print_multiple_cards, user_select_card
from copy import copy

def play_card_user(game_dict):

    table_cards = copy(game_dict["table_cards"])
    while len(table_cards) < 3:
        table_cards.append(EmptyCard())

    print(game_dict["settings"]["tablecard_message"])
    print_multiple_cards(table_cards)
    game_dict = user_play_card(game_dict)

    if game_dict["players"][game_dict["turn"]]["position"] != 2:
        game_dict["turn"] =  (game_dict["turn"] + 1)%3
        return game_dict


    
    

def user_play_card(game_dict):
    show_message = game_dict["settings"]["cardmessage"].format(game_dict["players"][game_dict["turn"]]["name"])
    error_message = game_dict["settings"]["card_errormessage"].format(game_dict["players"][game_dict["turn"]]["name"])
    cards = game_dict["players"][game_dict["turn"]]["cards"]
    value_dict = game_dict["settings"]["value_dict"]
    suit_dict = game_dict["settings"]["suit_dict"]
    trumpf = game_dict["gamemode"]["trumpf"]

    game_dict["players"][game_dict["turn"]]["cards"], table_card = user_select_card(show_message, error_message, cards, value_dict, suit_dict)

    if game_dict["table_cards"]:
        if not same_suit_or_trumpf(game_dict["table_cards"][0], table_card, trumpf, suit_dict):
            if any(same_suit_or_trumpf(game_dict["table_cards"][0], card, trumpf, suit_dict) for card in cards):
                game_dict["players"][game_dict["turn"]]["cards"].append(table_card)
                print(game_dict["settings"]["play_errormessage"].format(game_dict["players"][game_dict["turn"]]["name"]))
                return user_play_card(game_dict)
    
    game_dict["table_cards"].append(table_card)
    return game_dict

def same_suit_or_trumpf(card1, card2, trumpf, suit_dict):
    """
    Check if 2 Cards have the same Suit or both are trumpf. 
    """
    if not isinstance(card1, Card) or not isinstance(card2, Card):
        raise TypeError("Both Cards need to be of type Card")
    if not isinstance(suit_dict, dict):
        raise TypeError("Please Enter a Valid game_dict")
    if (not trumpf is None) and (not isinstance(trumpf, str)):
        raise TypeError("Trumpf needs to be string or None")

    if trumpf is None and card1.equal_suit(card2):
        return True
    elif trumpf is not None: # If not None, there is a Trumpf, else the cards are not equal, so false
        if card1.equal_suit(card2) and not (card1.card_points == 2 or card2.card_points == 2):
            return True # If they have the Same suit but none of the cards is a jack. If one is a Jack, the trumpf matters, not the color
        elif card1.card_points == 2 and card2.card_points == 2: # If there is an Trumpf, Jacks are allwys Trumpf so 2 Jacks are equal
            return True
        elif trumpf in suit_dict: # If its an Color Game, if the card is an Jack and the other card is Trumpf its equal
            if (card1.card_points == 2 and card2.suit_str == trumpf) or (card2.card_points == 2 and card1.suit_str == trumpf):
                return True
    return False
