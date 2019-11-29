"""
Here are functions witch are needed in diffrent states of this programm
"""
from modules.card import Card

def print_multiple_cards(cards):
    if not isinstance(cards, list):
        raise TypeError("cards need to be of type list")
    elif not all(isinstance(c, Card) for c in cards):
        raise TypeError("All elements need to be of Type Card")
    
    for i in range(len(cards[0].get_ascii_card())):
        pr_str = ""
        for c in cards:
            pr_str += c.get_ascii_card()[i]+":"
        print(pr_str[:-1])

def get_player_at_position(game_dict, position):
    """
    Returns the number of the player who is Playing forehand
    """
    for player_num in game_dict["players"]:
        if  game_dict["players"][player_num]["position"] == position:
            return player_num
    raise Exception("No Player at this position")

def get_user_true_false(show_message, error_message, user_cards):
    """
    Get True or False if user wants to take the bid
    """
    print_multiple_cards(user_cards)
    print("\n", show_message)
    inp = input()

    if inp.lower() == "yes" or inp.lower() == "y":
        return True
    elif inp.lower() == "no" or inp.lower() == "n":
        return False
    else:
        print(error_message)
        return get_user_true_false(show_message, error_message, user_cards)

def get_user_card(show_message, error_message, user_cards, value_dict, suit_dict):
    """
    Get a Card from a Userinput
    """
    print_multiple_cards(user_cards)
    print("\n", show_message)
    inp = input()

    if isinstance(inp, str):
        inp = inp.split()
    
    if isinstance(inp, list) and len(inp) == 2:
        try:
            user_card = Card(inp[0], inp[1], value_dict, suit_dict)
        except (TypeError, ValueError):
            try:
                user_card = Card(inp[1], inp[0], value_dict, suit_dict)
            except (TypeError, ValueError):
                print(error_message)
                return get_user_card(show_message, error_message, user_cards, value_dict, suit_dict)
    else:
        print(error_message)
        return get_user_card(show_message, error_message, user_cards, value_dict, suit_dict)
    
    return user_card
                
def user_select_card(show_message, error_message, user_cards, value_dict, suit_dict):
    card = get_user_card(show_message, error_message, user_cards, value_dict, suit_dict)

    if card in user_cards:
        del user_cards[user_cards.index(card)]
        return user_cards, card
    else:
        print(error_message)
        return user_select_card(show_message, error_message, user_cards, value_dict, suit_dict)

def sort_cards(cards, order_dict, trumpf):
    # TODO
    if not isinstance(cards, list):
        raise TypeError("Cards need to be of Type List")
    if not all(isinstance(card, Card) for card in cards):
        raise TypeError("All Elements in Cards need to be of the same Type")
    i = 0
    while i < len(cards):
        k = 0
        while k < len(cards)-i-1:
            if not cards[k].ishigher(cards[k+1], trumpf, order_dict, True):
                tmp = cards[k]
                cards[k] = cards[k+1]
                cards[k+1] = tmp
            k += 1
        i += 1
        print_multiple_cards(cards)
    return cards