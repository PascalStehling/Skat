"""
The single Player needs to decide if he wants to take the skat and which gametype he wants to play
"""
from modules.card import Card
from modules.tools import get_user_true_false, user_select_card, print_multiple_cards, get_player_at_position, sort_cards

def setup_single_play(game_dict):
    
    show_message = game_dict["settings"]["skatmessage"].format(game_dict["players"][game_dict["turn"]]["name"])
    error_message = game_dict["settings"]["yesno_errormessage"].format(game_dict["players"][game_dict["turn"]]["name"])
    cards = game_dict["players"][game_dict["turn"]]["cards"]
    value_dict = game_dict["settings"]["value_dict"]
    suit_dict = game_dict["settings"]["suit_dict"]

    if get_user_true_false(show_message, error_message, cards):
        order_dict = game_dict["settings"]["standart_order_dict"]
        sort_trumpf = [x[0] for x in game_dict["settings"]["suit_dict"].items() if x[1]==12][0]

        game_dict["players"][game_dict["turn"]]["cards"] += game_dict["skat"]
        game_dict["players"][game_dict["turn"]]["cards"] = sort_cards(game_dict["players"][game_dict["turn"]]["cards"], order_dict, sort_trumpf)
        game_dict["skat"] = []

        show_message = game_dict["settings"]["cardmessage"].format(game_dict["players"][game_dict["turn"]]["name"])
        error_message = game_dict["settings"]["card_errormessage"].format(game_dict["players"][game_dict["turn"]]["name"])
        cards = game_dict["players"][game_dict["turn"]]["cards"]

        for _ in range(2):
            game_dict["players"][game_dict["turn"]]["cards"], skat_card = user_select_card(show_message, error_message, cards, value_dict, suit_dict)
            game_dict["skat"].append(skat_card)

    show_message = game_dict["settings"]["gamemode_message"].format(game_dict["players"][game_dict["turn"]]["name"])
    error_message = game_dict["settings"]["gamemode_errormessage"].format(game_dict["players"][game_dict["turn"]]["name"])
    cards = game_dict["players"][game_dict["turn"]]["cards"]
    gamemode_dict = game_dict["settings"]["gamemode_dict"]

    game_dict["gamemode"] = get_play_type(show_message, error_message, gamemode_dict, cards)
    game_dict["order_dict"] = game_dict["settings"][game_dict["gamemode"]["order_dict"]]
    game_dict["jack_multiplicator"] = get_jack_multiplicator(cards, suit_dict, value_dict)

    for player in game_dict["players"]:
        game_dict["players"][player]["cards"] = sort_cards(game_dict["players"][player]["cards"], game_dict["order_dict"], game_dict["gamemode"]["trumpf"])
    game_dict["gamestate"] = 4
    game_dict["turn"] = get_player_at_position(game_dict, 0)

    return game_dict

    
def get_play_type(show_message, error_message, gamemode_dict, user_cards):
    print_multiple_cards(user_cards)
    print(show_message)
    for key in gamemode_dict:
        print(f"{key}: {gamemode_dict[key]['name']}")

    inp = input()
    if inp.isdigit() and int(inp) in gamemode_dict:
        return gamemode_dict[int(inp)]
    else:
        print(error_message)
        return get_play_type(show_message, error_message, gamemode_dict, user_cards)

def get_jack_multiplicator(cards, suit_dict, value_dict):
    """
    Get the jack multiplicator for the play
    """
    if not isinstance(cards, list):
        raise TypeError("table_cards need to be of Type List")
    if not all([isinstance(card, Card) for card in cards]):
        raise ValueError("Table Cards should only contain Cards")
    if not isinstance(suit_dict, dict):
        raise TypeError("Suit needs to be of Type dict")
    if not isinstance(value_dict, dict):
        raise TypeError("Suit needs to be of Type dict")

    jacks = [card for card in cards if card.card_points == 2]
    if len(jacks) == 4 or len(jacks) == 0:
        return 5
    
    suit_list = [x[0] for x in sorted(suit_dict.items(), key=lambda x: x[1], reverse=True)]
    jack_name = [x[0] for x in value_dict.items() if x[1] == 2][0]
    multi = 2
    if has_card_with_suit(jacks, suit_list[0]):
        for suit in suit_list[1:]:
            if has_card_with_suit(jacks, suit):
                multi += 1
            else:
                break
    else:
        for suit in suit_list[1:]:
            if not has_card_with_suit(jacks, suit):
                multi += 1
            else:
                break
    return multi

def has_card_with_suit(cards, suit):
    if not isinstance(cards, list):
        raise TypeError("table_cards need to be of Type List")
    if not all([isinstance(card, Card) for card in cards]):
        raise ValueError("Table Cards should only contain Cards")
    if not isinstance(suit, str):
        raise TypeError("Suit needs to be of Type String")

    for card in cards:
        if card.suit_str == suit:
            return True
    return False