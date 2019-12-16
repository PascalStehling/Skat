from modules.tools import get_user_true_false

def make_bid(game_round, settings, players):
    """Main Function for bidding. Ask Player if he wants to bid, checks if bidding Phase ends and select the new turn
    
    Args:
        game_dict (dict): The Dictionary with all game Informations
    
    Returns:
        dict: the updated game_dict
    """
    show_message = settings.bidmessage.format(game_round.turn.name, game_round.bidding.next_bid)
    error_message = settings.yesno_errormessage.format(game_round.turn.name)


    user_bid = get_user_true_false(show_message, error_message, game_round.turn.cards)
    game_round = update_bid_dict(user_bid, game_round, settings)
    

    game_round.turn, gamestate = check_end_bidding(game_round, players)
    return game_round, gamestate

def update_bid_dict(user_bid, game_round, settings):
    r"""Check what the user has bidden and update the bidding Dictionary (bid_dict).
    """
    if not user_bid:
        game_round.bidding.passed.append(game_round.turn)
        return game_round
    return update_bid_dict_positiv_bid(game_round, settings)

def update_bid_dict_positiv_bid(game_round, settings):
    """Updates the bid Dict if the user said Yes to the new Bid
    """
    if game_round.turn.position == 0: # Forhand can only listen
        return bid_hear(game_round, settings)
    elif game_round.turn.position  == 2: # Backhand can only say
        return bid_say(game_round)
    else: # Middlehand is playing
        return update_bid_dict_middlehand_player(game_round, settings)

def update_bid_dict_middlehand_player(game_round, settings):
    """Updates the bid Dict if the user said Yes to the new Bid and was playing middlehand
    
    Args:
        new_bid (int): The Bid the user had to decide to Play or pass
        turn (int): The number of the player who is playing now
        bid_list (list): List with all possible bids
        forhand_player (int): Number of the Player who Plays Forhand
        bid_dict (dict): The Dictionary with all relevant information for bidding
    
    Returns:
        dict: The Updated bid_dict
    """
    if [True for player in game_round.bidding.passed if player.position == 0]: # If Forhand has passed, Middlehand is hearing
        return bid_hear(game_round, settings)
    else:  # Else middle hand is saying
        return bid_say(game_round)

def bid_say(game_round):
    """Update the bid_dict when the user needed to say
    """
    game_round.bidding.bid = game_round.bidding.next_bid
    game_round.bidding.bid_player = game_round.turn
    return game_round

def bid_hear(game_round, settings):
    """Update the bid_dict when the user needed to hear
    
    Args:
        bid_dict (dict): The Dictionary with all relevant information for bidding
        new_bid (int): The Bid the user had to decide to Play or pass
        turn (int): The number of the player who is playing now
        bid_list (list): List with all possible bids
    
    Returns:
        dict: The Updated bid_dict
    """
    if settings.bid_list[-1] == game_round.bidding.next_bid:
        raise ValueError("Cant bid any higher") 
    game_round.bidding.bid_player = game_round.turn
    game_round.bidding.next_bid = settings.bid_list[settings.bid_list.index(game_round.bidding.next_bid)+1]
    return game_round

def get_new_turn(bidding, players):
    """Get the new turn for the next round of bidding
    """
    if bidding.bid_player in bidding.passed: # Player has passed
        return turn_if_passed(bidding, players)
    else: # Player has not passed
        return turn_if_not_passed(bidding, players)

def turn_if_passed(bidding, players):
    """Get the new turn for the next round of bidding if the player who played now passed.
    """
    if bidding.bid_player.position != 2:
        # If the middlehand or forhand passes backhand needs to play
        return players.backhand
    elif not players.forhand not in bidding.passed:
        # If the Backhand and forhand is still in play, forhand needs to play
        return players.forhand
    elif not players.middlehand not in bidding.passed:
        # IF Backhand passed and middlehand still in play, middlehand needs to play
        return players.backhand


def turn_if_not_passed(bidding, players):
    """Get the new turn for the next round of bidding if the player who played now said yes.
    """
    if bidding.bid_player.position == 1:
        return turn_if_not_passed_middlehand(players, bidding.passed)
    if bidding.bid_player.position == 0:
        return turn_if_not_passed_forhand(players, bidding.passed)
    if bidding.bid_player.position == 2 :
        return turn_if_not_passed_backhand(players, bidding.passed)
    else:
        raise Exception("Somthing wrong happend in turn_if_not_passed")

def turn_if_not_passed_middlehand(players, passed_players):
    """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the middlehand position (1).
    
    Args:
        forhand_player (int): Number of the Player who is plays forhand
        backhand_player (int): Number of the Player who is plays backhand
        passed_players (list): List of Numbers of the Players who passed
    
    Returns:
        int: The Number of the Player who plays next round
    """
    if players.forhand not in passed_players:
        # If middlehand was playing and forhand is still playing, it is forhand turn
        return players.forhand
    else:
        # If middlehand was playing and forhand has passed, backhand is playing
        return players.backhand

def turn_if_not_passed_forhand(players, passed_players):
    """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the forhand position (0).
    """
    if players.middlehand not in passed_players:
        # If forhand was playing and middlehand has not passed, middlehand is playing
        return players.middlehand
    else:
        # If forhand was playing and middlehand has passed, backhand is playing
        return players.backhand

def turn_if_not_passed_backhand(players, passed_players):
    """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the backhand position (2).
    """
    if players.middlehand not in passed_players:
        # If backhand was playing and middlehand has not passed, middlehand is playing
        return players.middlehand
    else:
        # If backhand was playing and forhand has not passed, forhand is playing
        return players.forhand


def check_end_bidding(game_round, players):
    """Cheks if the bidding round is finished, if not a the turn goes to another player. If its finished the end bidding function gets called
    
    
    Returns:
        tuple: Tuple with the player who has the next turn and the gamestate for the next round
    """
    if not is_end_bidding(game_round.bidding):
        return (get_new_turn(game_round.bidding, players), 2)

    return end_bidding(game_round.bidding.bid_player)

def end_bidding(bid_player):
    """Ends the bidding Phase, if there is an bid Player, he won the bidding, else it starts new with new cards

    Returns:
        tuple: Tuple with the the player who has the next turn and the new gamstate (turn, gamestate)
    """
    if bid_player is not None:
        return bid_player, 3
    else:
        # Ramsch not implemented, just new cards are given.
        # TODO Ramsch
        print("Everyone passed, cards get dealt again")
        return None, 1

def is_end_bidding(bidding):
    """Checks if the bidding finished
    
    Args:
        passed_player_list (list): List of Players who passed
        bid_player (int): Number of the Player who is highest at bidding, can be None
    
    Returns:
        bool: True if the bidding is finished, else False
    """
    return (len(bidding.passed) == 2 and bidding.bid_player is not None) or (len(bidding.passed) == 3)