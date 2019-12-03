
from modules.card import Card

def end_round(game_dict):
    won, play_multiplicator = has_won_round(game_dict["single_player_stack"])

    if over_bidded(game_dict["game_mode"], game_dict["bidding"]["bid"], game_dict["jack_multipicato"]):
        


    pass

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
        return True, 3 #won, Schneider, Schwarz
    elif points > 90:
        return True, 2 # Won, schneider
    elif points > 60:
        return True, 1 # Won
    elif points > 30:
        return False, 2 # loose
    elif points > 0:
        return False, 3 # loose, schneider
    else:
        return False, 4 # loose, schneider, schwarz

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