
from modules.card import Card

def end_round(game_dict):
    won, play_multiplicator, card_points = has_won_round(game_dict["single_player_stack"])

    if over_bidded(game_dict["gamemode"], game_dict["bidding"]["bid"], game_dict["jack_multiplicator"]) or not won:
        if won:
            play_multiplicator += 1
        points = game_dict["gamemode"]["points"]*play_multiplicator*-1
    else:
        points = game_dict["gamemode"]["points"]*play_multiplicator

    game_dict["players"][game_dict["bidding"]["bid_player"]]["points"] += points

    print(game_dict["settings"]["end_round_message"].format(game_dict["players"][game_dict["bidding"]["bid_player"]]["name"], card_points, points))
    for p in game_dict["players"]:
        print(game_dict["settings"]["point_message"].format(game_dict["players"][p]["name"], game_dict["players"][p]["points"]))

    game_dict["gamestate"] = 1
    game_dict["game_round"] += 1

    return game_dict

def calc_card_points(cards):
    if not isinstance(cards, list):
        raise TypeError("Crads need to be of Type List")
    if not all([isinstance(card, Card) for card in cards]):
        raise TypeError("All elements in Cards need to be of Type Card")
    points = 0
    for card in cards:
        points += card.card_points
    return points

def has_won_round(cards):
    points = calc_card_points(cards)
    if points == 120:
        return True, 3, points #won, Schneider, Schwarz
    elif points > 90:
        return True, 2, points # Won, schneider
    elif points > 60:
        return True, 1, points # Won
    elif points > 30:
        return False, 2, points # loose
    elif points > 0:
        return False, 3, points # loose, schneider
    else:
        return False, 4, points # loose, schneider, schwarz

def calc_user_points():
    pass

def over_bidded(game_mode, bid, jack_multipicator):
    if game_mode["trumpf"] is not None:
        points =  game_mode["points"]*jack_multipicator
    else:
        points = game_mode["points"]

    if points < bid:
        return True
    else:
        return False