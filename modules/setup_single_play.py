"""
The single Player needs to decide if he wants to take the skat and which gametype he wants to play
"""

from modules.tools import get_user_true_false, user_select_card, print_multiple_cards, get_player_at_position

def setup_single_play(game_dict):
    
    show_message = game_dict["settings"]["skatmessage"].format(game_dict["players"][game_dict["turn"]]["name"])
    error_message = game_dict["settings"]["yesno_errormessage"].format(game_dict["players"][game_dict["turn"]]["name"])
    cards = game_dict["players"][game_dict["turn"]]["cards"]

    if get_user_true_false(show_message, error_message, cards):
        game_dict["players"][game_dict["turn"]]["cards"] += game_dict["skat"]
        game_dict["skat"] = []

        show_message = game_dict["settings"]["cardmessage"].format(game_dict["players"][game_dict["turn"]]["name"])
        error_message = game_dict["settings"]["card_errormessage"].format(game_dict["players"][game_dict["turn"]]["name"])
        cards = game_dict["players"][game_dict["turn"]]["cards"]
        value_dict = game_dict["settings"]["value_dict"]
        suit_dict = game_dict["settings"]["suit_dict"]

        for _ in range(2):
            game_dict["players"][game_dict["turn"]]["cards"], skat_card = user_select_card(show_message, error_message, cards, value_dict, suit_dict)
            game_dict["skat"].append(skat_card)

    show_message = game_dict["settings"]["gamemode_message"].format(game_dict["players"][game_dict["turn"]]["name"])
    error_message = game_dict["settings"]["gamemode_errormessage"].format(game_dict["players"][game_dict["turn"]]["name"])
    cards = game_dict["players"][game_dict["turn"]]["cards"]
    gamemode_dict = game_dict["settings"]["gamemode_dict"]

    game_dict["gamemode"] = get_play_type(show_message, error_message, gamemode_dict, cards)
    game_dict["order_dict"] = game_dict["settings"][game_dict["gamemode"]["order_dict"]]
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

    