
from modules.card import Card

def end_round(game_round, settings, players):
    """The main function to end the round   
    """
    
    single_player_card_points = calc_card_points(game_round.single_player_stack)
    score = calculate_score(single_player_card_points, game_round)
    game_round.bidding.bid_player.score += score

    print(settings.end_round_message.format(game_round.bidding.bid_player, single_player_card_points, score))
    for p in players:
        print(settings.point_message.format(p.name, p.score))

    players.players_on_next_position()

    return game_round

def calculate_score(single_player_card_points, game_round):
    """Calculate the score points of the single_player
    
    Returns:
        int: the score points the player achieved
    """
    if has_won_round(single_player_card_points, game_round):
        return calc_score_points_won(single_player_card_points, game_round)
    else:
        return calc_score_points_lost(single_player_card_points, game_round)

def calc_score_points_won(single_player_card_points, game_round):
    """Get the Score points if the player won
    Returns:
        int: the score points the player achieved
    """
    return (get_win_level(single_player_card_points)+game_round.jack_multiplicator)*game_round.gamemode["points"]

def calc_score_points_lost(single_player_card_points, game_round):
    """Get the Score points if the player Lost

    Returns:
        int: the score points the player achieved
    """
    return (get_win_level(120-single_player_card_points)+game_round.jack_multiplicator)*game_round.gamemode["points"]*-2


def get_win_level(card_points):
    """Get the win states the Player has.

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

    Returns:
        int: number of points the Player got
    """
    points = 0
    for card in cards:
        points += card.card_points
    return points

def has_won_round(card_points, game_round):
    """Checks if the Player has won this round. If he has over 90 he always wins, under 60 allways loose and between 60 and 90 it depends if he overbidded

    Returns:
        bool: True if the Player won, else False
    """
    if card_points >= 90:
        return True

    if card_points <= 60:
        return False

    return not has_over_bidded(game_round)
    

def has_over_bidded(game_round):
    """Checks is the Player has overbidden

    Returns:
        bool: True if the player has overbidded, else False
    """
    if Card.trumpf is not None:
        return (game_round.gamemode["points"]*game_round.jack_multiplicator) < game_round.bidding.bid
    else:
        return game_round.gamemode["points"] < game_round.bidding.bid