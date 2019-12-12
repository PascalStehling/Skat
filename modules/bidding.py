from modules.tools import get_user_true_false, get_player_at_position

def make_bid(game_dict):
    """Main Function for bidding. Ask Player if he wants to bid, checks if bidding Phase ends and select the new turn
    
    Args:
        game_dict (dict): The Dictionary with all game Informations
    
    Returns:
        dict: the updated game_dict
    """
    new_bid = game_dict["bidding"]["next_bid"]
    turn = game_dict["players"][game_dict["turn"]]["position"]

    show_message = game_dict["settings"]["bidmessage"].format(game_dict["players"][turn]["name"], new_bid)
    error_message = game_dict["settings"]["yesno_errormessage"].format(game_dict["players"][turn]["name"])
    cards = game_dict["players"][turn]["cards"]

    user_bid = get_user_true_false(show_message, error_message, cards)
    bid_list = game_dict["settings"]["bid_list"]
    game_dict["bidding"] = update_bid_dict(user_bid, new_bid, game_dict["bidding"], bid_list, turn, game_dict["players"][turn]["position"], get_player_at_position(game_dict["players"], 0))
    
    passed_players = game_dict["bidding"]["passed"]

    game_dict["turn"], game_dict["gamestate"] = check_end_bidding(game_dict["bidding"]["bid_player"],
                                                                    passed_players,
                                                                    game_dict["gamestate"],
                                                                    turn,
                                                                    game_dict["players"][turn]["position"],
                                                                    get_player_at_position(game_dict["players"], 0),
                                                                    get_player_at_position(game_dict["players"], 1),
                                                                    get_player_at_position(game_dict["players"], 2))
    return game_dict

def update_bid_dict(user_bid, new_bid, bid_dict, bid_list, turn, old_turn_position, forhand_player):
    r"""Check what the user has bidden and update the bidding Dictionary (bid_dict).
    
    Args:
        user_bid (bool): If the user said Yes(True) or No\Passed(False) to the bid.
        new_bid (int): The Bid the user had to decide to Play or pass
        bid_dict (dict): The Dictionary with all relevant information for bidding
        bid_list (list): List with all possible bids
        turn (int): The number of the player who is playing now
        old_turn_position (int): The position of the Player who is playing now
        forhand_player (int): Number of the Player who Plays Forhand
    
    Returns:
        dict: The Updated bid_dict
    """
    if not user_bid:
        bid_dict["passed"].append(turn)
        return bid_dict
    return update_bid_dict_positiv_bid(old_turn_position, new_bid, bid_list, turn, forhand_player ,bid_dict)

def update_bid_dict_positiv_bid(old_turn_position, new_bid, bid_list, turn, forhand_player, bid_dict):
    """Updates the bid Dict if the user said Yes to the new Bid
    
    Args:
        old_turn_position (int): The position of the Player who is playing now
        new_bid (int): The Bid the user had to decide to Play or pass
        bid_list (list): List with all possible bids
        turn (int): The number of the player who is playing now
        forhand_player (int): Number of the Player who Plays Forhand
        bid_dict (dict): The Dictionary with all relevant information for bidding
    
    Returns:
        dict: The Updated bid_dict
    """
    if old_turn_position == 0: # Forhand can only listen
        return bid_hear(bid_dict, new_bid, turn, bid_list)
    elif old_turn_position == 2: # Backhand can only say
        return bid_say(bid_dict, new_bid, turn)
    else: # Middlehand is playing
        return update_bid_dict_middlehand_player(new_bid, turn, bid_list, forhand_player, bid_dict)

def update_bid_dict_middlehand_player(new_bid, turn, bid_list, forhand_player, bid_dict):
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
    if forhand_player in bid_dict["passed"]: # If Forhand has passed, Middlehand is hearing
        return bid_hear(bid_dict, new_bid, turn, bid_list)
    else:  # Else middle hand is saying
        return bid_say(bid_dict, new_bid, turn)

def bid_say(bid_dict, new_bid, turn):
    """Update the bid_dict when the user needed to say
    
    Args:
        bid_dict (dict): The Dictionary with all relevant information for bidding
        new_bid (int): The Bid the user had to decide to Play or pass
        turn (int): The number of the player who is playing now
    
    Returns:
        dict: The Updated bid_dict
    """
    bid_dict["bid"] = new_bid
    bid_dict["bid_player"] = turn
    return bid_dict

def bid_hear(bid_dict, new_bid, turn, bid_list):
    """Update the bid_dict when the user needed to hear
    
    Args:
        bid_dict (dict): The Dictionary with all relevant information for bidding
        new_bid (int): The Bid the user had to decide to Play or pass
        turn (int): The number of the player who is playing now
        bid_list (list): List with all possible bids
    
    Returns:
        dict: The Updated bid_dict
    """
    if bid_list[-1] == new_bid:
        raise ValueError("Cant bid any higher") 
    bid_dict["bid_player"] = turn
    bid_dict["next_bid"] = bid_list[bid_list.index(new_bid)+1]
    return bid_dict

def get_new_turn(old_turn, old_turn_position, forhand_player, middlehand_player, backhand_player, passed_players):
    """Get the new turn for the next round of bidding
    
    Args:
        old_turn (int): Number of the player who has the turn this round
        old_turn_position (int): Position of the Player who has the turn this round
        forhand_player (int): Number of the Player who is plays forhand
        middlehand_player (int): Number of the Player who is plays middlehand
        backhand_player (int): Number of the Player who is plays backhand
        passed_players (list): List of Numbers of the Players who passed
    
    Returns:
        int: The Number of the Player who plays next round
    """
    if old_turn in passed_players: # Player has passed
        return turn_if_passed(old_turn_position, forhand_player, middlehand_player, backhand_player, passed_players)
    else: # Player has not passed
        return turn_if_not_passed(old_turn_position, forhand_player, middlehand_player, backhand_player, passed_players)

def turn_if_passed(old_turn_position, forhand_player, middlehand_player, backhand_player, passed_players):
    """Get the new turn for the next round of bidding if the player who played now passed.
    
    Args:
        old_turn_position (int): Position of the Player who has the turn this round
        forhand_player (int): Number of the Player who is plays forhand
        middlehand_player (int): Number of the Player who is plays middlehand
        backhand_player (int): Number of the Player who is plays backhand
        passed_players (list): List of Numbers of the Players who passed
    
    Raises:
        Exception: If somthing happens what is not possible. 
    
    Returns:
        int: The Number of the Player who plays next round
    """
    if old_turn_position != 2:
        # If the middlehand or forhand passes backhand needs to play
        return backhand_player
    elif forhand_player not in passed_players:
        # If the Backhand and forhand is still in play, forhand needs to play
        return forhand_player
    elif middlehand_player not in passed_players:
        # IF Backhand passed and middlehand still in play, middlehand needs to play
        return middlehand_player
    else:
        raise Exception("Somthing wrong happend in turn_if_passed")

def turn_if_not_passed(old_turn_position, forhand_player, middlehand_player, backhand_player, passed_players):
    """Get the new turn for the next round of bidding if the player who played now said yes.
    
    Args:
        old_turn_position (int): Position of the Player who has the turn this round
        forhand_player (int): Number of the Player who is plays forhand
        middlehand_player (int): Number of the Player who is plays middlehand
        backhand_player (int): Number of the Player who is plays backhand
        passed_players (list): List of Numbers of the Players who passed
    
    Raises:
        Exception: [description]
    
    Returns:
        int: The Number of the Player who plays next round
    """
    if old_turn_position == 1:
        return turn_if_not_passed_middlehand(forhand_player, backhand_player, passed_players)
    if old_turn_position == 0:
        return turn_if_not_passed_forhand(middlehand_player, backhand_player, passed_players)
    if old_turn_position == 2 :
        return turn_if_not_passed_backhand(middlehand_player, forhand_player, passed_players)
    else:
        raise Exception("Somthing wrong happend in turn_if_not_passed")

def turn_if_not_passed_middlehand(forhand_player, backhand_player, passed_players):
    """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the middlehand position (1).
    
    Args:
        forhand_player (int): Number of the Player who is plays forhand
        backhand_player (int): Number of the Player who is plays backhand
        passed_players (list): List of Numbers of the Players who passed
    
    Returns:
        int: The Number of the Player who plays next round
    """
    if forhand_player not in passed_players:
        # If middlehand was playing and forhand is still playing, it is forhand turn
        return forhand_player
    else:
        # If middlehand was playing and forhand has passed, backhand is playing
        return backhand_player

def turn_if_not_passed_forhand(middlehand_player, backhand_player, passed_players):
    """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the forhand position (0).
    
    Args:
        middlehand_player (int): Number of the Player who is plays middlehand
        backhand_player (int): Number of the Player who is plays backhand
        passed_players (list): List of Numbers of the Players who passed
    
    Returns:
        int: The Number of the Player who plays next round
    """
    if middlehand_player not in passed_players:
        # If forhand was playing and middlehand has not passed, middlehand is playing
        return middlehand_player
    else:
        # If forhand was playing and middlehand has passed, backhand is playing
        return backhand_player

def turn_if_not_passed_backhand(middlehand_player, forhand_player, passed_players):
    """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the backhand position (2).
    
    Args:
        middlehand_player (int): Number of the Player who is plays middlehand
        forhand_player (int): Number of the Player who is plays forhand
        passed_players (list): List of Numbers of the Players who passed
    
    Returns:
        int: The Number of the Player who plays next round
    """
    if middlehand_player not in passed_players:
        # If backhand was playing and middlehand has not passed, middlehand is playing
        return middlehand_player
    else:
        # If backhand was playing and forhand has not passed, forhand is playing
        return forhand_player


def check_end_bidding(bid_player, passed_players, gamestate, old_turn, old_turn_position, forhand_player, middlehand_player, backhand_player):
    """Cheks if the bidding round is finished, if not a the turn goes to another player. If its finished the end bidding function gets called
    
    Args:
        bid_player (int): Number of the Player who is highest at bidding
        passed_players (list): List of Numbers of the Players who passed
        gamestate (int): the gamestate at the moment
        old_turn (int): Number of the player who has the turn this round
        old_turn_position (int): Position of the Player who has the turn this round
        forhand_player (int): Number of the Player who is plays forhand
        middlehand_player (int): Number of the Player who is plays middlehand
        backhand_player (int): Number of the Player who is plays backhand
    
    Returns:
        tuple: Tuple with the player who has the next turn and the gamestate for the next round
    """
    if not is_end_bidding(passed_players, bid_player):
        return (get_new_turn(old_turn, old_turn_position, forhand_player, middlehand_player, backhand_player, passed_players), gamestate)

    return end_bidding(bid_player, forhand_player)

def end_bidding(bid_player, forhand_player_num):
    """Ends the bidding Phase, if there is an bid Player, he won the bidding, else it starts new with new cards
    
    Args:
        bid_player (int): the Number of the Player who set the highest bid. It can also be None
        forhand_player_num (int): the number of the player who plays forhand
    
    Returns:
        tuple: Tuple with the the player who has the next turn and the new gamstate (turn, gamestate)
    """
    if bid_player is not None:
        return bid_player, 3
    else:
        # Ramsch not implemented, just new cards are given.
        # TODO Ramsch
        print("Everyone passed, cards get dealt again")
        return forhand_player_num, 1

def is_end_bidding(passed_player_list, bid_player):
    """Checks if the bidding finished
    
    Args:
        passed_player_list (list): List of Players who passed
        bid_player (int): Number of the Player who is highest at bidding, can be None
    
    Returns:
        bool: True if the bidding is finished, else False
    """
    return (len(passed_player_list) == 2 and bid_player is not None) or (len(passed_player_list) == 3)