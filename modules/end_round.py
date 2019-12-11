
from modules.card import Card

def end_round(game_dict):
    won_cards = game_dict["single_player_stack"]
    jack_multiplicator = game_dict["jack_multiplicator"]
    gamemode_points = game_dict["gamemode"]["points"]
    trumpf = game_dict["gamemode"]["trumpf"]
    bid = game_dict["bidding"]["bid"]

    single_player_card_points = calc_card_points(won_cards)
    score = calculate_score(single_player_card_points, trumpf, bid, jack_multiplicator, gamemode_points)
    game_dict["players"][game_dict["bidding"]["bid_player"]]["points"] += score

    print(game_dict["settings"]["end_round_message"].format(game_dict["players"][game_dict["bidding"]["bid_player"]]["name"], single_player_card_points, score))
    for p in game_dict["players"]:
        print(game_dict["settings"]["point_message"].format(game_dict["players"][p]["name"], game_dict["players"][p]["points"]))

    game_dict["gamestate"] = 1
    game_dict["game_round"] += 1

    return game_dict

def calculate_score(single_player_card_points, trumpf, bid, jack_multiplicator, gamemode_points):
    if has_won_round(single_player_card_points, trumpf, bid, jack_multiplicator, gamemode_points):
        return calc_points_won(single_player_card_points, jack_multiplicator, gamemode_points)
    else:
        return calc_points_lost(single_player_card_points, jack_multiplicator, gamemode_points)

def calc_points_won(single_player_card_points, jack_multiplicator, gamemode_points):
    return (get_win_level(single_player_card_points)+jack_multiplicator)*gamemode_points

def calc_points_lost(single_player_card_points, jack_multiplicator, gamemode_points):
    return (get_win_level(120-single_player_card_points)+jack_multiplicator)*gamemode_points*-2


def get_win_level(card_points):
    if card_points == 120:
        return 2
    if card_points > 90:
        return 1
    
    return 0

def calc_card_points(cards):
    points = 0
    for card in cards:
        points += card.card_points
    return points

def has_won_round(card_points, trumpf, bid, jack_multipicator, gamemode_points):
    if card_points >= 90:
        return True

    if card_points <= 60:
        return False

    return not has_over_bidded(trumpf, bid, jack_multipicator, gamemode_points)
    

def has_over_bidded(trumpf, bid, jack_multiplicator, gamemode_points):
    if trumpf is not None:
        return (gamemode_points*jack_multiplicator) < bid
    else:
        return gamemode_points < bid