
from modules.card import Card

def end_round(game_dict):
    """The main function to end the round
    
    Args:
        game_dict (dict): Dictionary with all game Infos
    
    Returns:
        game_dict (dict): updated Dictionary with all game Infos
    """
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
    """Calculate the score points of the single_player
    
    Args:
        single_player_card_points (int): number of Card-Points the single_player got
        trumpf (str): None or String of the trumpf thatz is played
        bid (int): the bid of the single player
        jack_multiplicator (int): the multiplicator of the jacks (play with/without jacks plus 1 (take game))
        gamemode_points (int): points of the gamemode
    
    Returns:
        int: the score points the player achieved
    """
    if has_won_round(single_player_card_points, trumpf, bid, jack_multiplicator, gamemode_points):
        return calc_score_points_won(single_player_card_points, jack_multiplicator, gamemode_points)
    else:
        return calc_score_points_lost(single_player_card_points, jack_multiplicator, gamemode_points)

def calc_score_points_won(single_player_card_points, jack_multiplicator, gamemode_points):
    """Get the Score points if the player won
    
    Args:
        single_player_card_points (int): number of Card-Points the single_player got
        jack_multiplicator (int): the multiplicator of the jacks (play with/without jacks plus 1 (take game))
        gamemode_points (int): points of the gamemode
    
    Returns:
        int: the score points the player achieved
    """
    return (get_win_level(single_player_card_points)+jack_multiplicator)*gamemode_points

def calc_score_points_lost(single_player_card_points, jack_multiplicator, gamemode_points):
    """Get the Score points if the player Lost
    
    Args:
        single_player_card_points (int): number of Card-Points the single_player got
        jack_multiplicator (int): the multiplicator of the jacks (play with/without jacks plus 1 (take game))
        gamemode_points (int): points of the gamemode
    
    Returns:
        int: the score points the player achieved
    """
    return (get_win_level(120-single_player_card_points)+jack_multiplicator)*gamemode_points*-2


def get_win_level(card_points):
    """Get the win states the Player has.
    
    Args:
        card_points (int): number of Points the single_player got
    
    Returns:
        int: 0 for playing, 1 for Schneider and 2 for Schwarz
    """
    if card_points == 120:
        return 2
    if card_points > 90:
        return 1
    
    return 0

def calc_card_points(cards):
    """Calculate the points from a list of Cards
    
    Args:
        cards (list): A List of Card Objects
    
    Returns:
        int: number of points the Player got
    """
    points = 0
    for card in cards:
        points += card.card_points
    return points

def has_won_round(card_points, trumpf, bid, jack_multipicator, gamemode_points):
    """Checks if the Player has won this round. If he has over 90 he always wins, under 60 allways loose and between 60 and 90 it depends if he overbidded
    
    Args:
        card_points (int): number of Points the single_player got
        trumpf (str): None or String of the trumpf thatz is played
        bid (int): the bid of the single player
        jack_multiplicator (int): the multiplicator of the jacks (play with/without jacks plus 1 (take game))
        gamemode_points (int): points of the gamemode
    
    Returns:
        bool: True if the Player won, else False
    """
    if card_points >= 90:
        return True

    if card_points <= 60:
        return False

    return not has_over_bidded(trumpf, bid, jack_multipicator, gamemode_points)
    

def has_over_bidded(trumpf, bid, jack_multiplicator, gamemode_points):
    """Checks is the Player has overbidden
    
    Args:
        trumpf (str): None or String of the trumpf thatz is played
        bid (int): the bid of the single player
        jack_multiplicator (int): the multiplicator of the jacks (play with/without jacks plus 1 (take game))
        gamemode_points (int): points of the gamemode
    
    Returns:
        bool: True if the player has overbidded, else False
    """
    if trumpf is not None:
        return (gamemode_points*jack_multiplicator) < bid
    else:
        return gamemode_points < bid