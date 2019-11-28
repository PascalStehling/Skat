from modules.card import print_multiple_cards
from modules.tools import get_player_at_position

def make_bid(game_dict):
    """
    Main Function for bidding. Ask Player if he wants to bid, checks if bidding Phase ends and select the new turn
    """
    new_bid = game_dict["bidding"]["next_bid"]

    if get_user_bid(new_bid, game_dict):
        if game_dict["players"][game_dict["turn"]]["position"] == 0: # Forhand can only listen
            game_dict = bid_hear(game_dict, new_bid)
        elif game_dict["players"][game_dict["turn"]]["position"] == 2: # Backhand can only say
            game_dict = bid_say(game_dict, new_bid)
        else: # Middlehand is playing
            if get_player_at_position(game_dict, 0) in game_dict["bidding"]["passed"]: # If Forhand has passed, Middlehand is hearing
                game_dict = bid_hear(game_dict, new_bid)
            else:                                                                      # Else middle hand is saying
                game_dict = bid_say(game_dict, new_bid)
    else:
        game_dict["bidding"]["passed"].append(game_dict["turn"])
        
        if check_end_bidding(game_dict):
            if game_dict["bidding"]["bid_player"] is not None:
                game_dict["turn"] = game_dict["bidding"]["bid_player"]
                game_dict["gamestate"] = 3
            else:
                # Ramsch not implemented, just new cards are given.
                # TODO Ramsch
                game_dict["gamestate"] = 1
            return game_dict

    game_dict["turn"] = get_player_turn(game_dict)

    return game_dict

def bid_say(game_dict, new_bid):
    game_dict["bidding"]["bid"] = new_bid
    game_dict["bidding"]["bid_player"] = game_dict["turn"]
    return game_dict

def bid_hear(game_dict, new_bid):
    bid_list = game_dict["settings"]["bid_list"]
    game_dict["bidding"]["bid_player"] = game_dict["turn"]
    game_dict["bidding"]["next_bid"] = bid_list[bid_list.index(new_bid)+1]
    return game_dict

def get_user_bid(bid, game_dict):
    """
    Get True or False if user wants to take the bid
    """
    print_multiple_cards(game_dict["players"][game_dict["turn"]]["cards"])
    print("\n", game_dict["settings"]["bidmessage"].format(game_dict["players"][game_dict["turn"]]["name"], bid))
    inp = input()

    if inp.lower() == "yes" or inp.lower() == "y":
        return True
    elif inp.lower() == "no" or inp.lower() == "n":
        return False
    else:
        print(game_dict["players"][game_dict["turn"]]["name"]+": Please enter Yes or No!")
        return get_user_bid(bid, game_dict)

def get_player_turn(game_dict):
    if game_dict["turn"] in game_dict["bidding"]["passed"]: # Player has passed
        if game_dict["players"][game_dict["turn"]]["position"] == 1 and get_player_at_position(game_dict, 0) not in game_dict["bidding"]["passed"]:
            # If the middlehand passes and the forhand and backhand are still in the game, the backhand needs to play
            turn = get_player_at_position(game_dict, 2)
        elif game_dict["players"][game_dict["turn"]]["position"] == 1 and get_player_at_position(game_dict, 0) in game_dict["bidding"]["passed"]:
            # If the Forhand and middlehand passed, backhand needs to play
            turn = get_player_at_position(game_dict, 2)
        elif game_dict["players"][game_dict["turn"]]["position"] == 0:
            # If the Forhand passes the backhand needs to play
            turn = get_player_at_position(game_dict, 2)
        elif game_dict["players"][game_dict["turn"]]["position"] == 2 and get_player_at_position(game_dict, 0) not in game_dict["bidding"]["passed"]:
            # If the Backhand and forhand is still in play, it needs to play
            turn = get_player_at_position(game_dict, 0)
        elif game_dict["players"][game_dict["turn"]]["position"] == 2 and get_player_at_position(game_dict, 1) not in game_dict["bidding"]["passed"]:
            # IF Backhand passed and middlehand still in play, it needs to play
            turn = get_player_at_position(game_dict, 1)
        else:
            raise Exception("Somthing wrong happend in get_player_turn")
    else: # Player has not passed
        if game_dict["players"][game_dict["turn"]]["position"] == 1 and get_player_at_position(game_dict, 0) not in game_dict["bidding"]["passed"]:
            # If middlehand was playing and forhand is still playing, it is its turn
            turn = get_player_at_position(game_dict, 0)
        elif game_dict["players"][game_dict["turn"]]["position"] == 1 and get_player_at_position(game_dict, 0) in game_dict["bidding"]["passed"]:
            # If middlehand was playing and forhand has passed, backhand is playing
            turn = get_player_at_position(game_dict, 2)
        elif game_dict["players"][game_dict["turn"]]["position"] == 0 and get_player_at_position(game_dict, 1) not in game_dict["bidding"]["passed"]:
            # If forhand was playing and middlehand has not passed, middlehand is playing
            turn = get_player_at_position(game_dict, 1)
        elif game_dict["players"][game_dict["turn"]]["position"] == 0 and get_player_at_position(game_dict, 1) in game_dict["bidding"]["passed"]:
            # If forhand was playing and middlehand has passed, backhand is playing
            turn = get_player_at_position(game_dict, 2)
        elif game_dict["players"][game_dict["turn"]]["position"] == 2 and get_player_at_position(game_dict, 1) not in game_dict["bidding"]["passed"]:
            # If backhand was playing and middlehand has not passed, middlehand is playing
            turn = get_player_at_position(game_dict, 1)
        elif game_dict["players"][game_dict["turn"]]["position"] == 2 and get_player_at_position(game_dict, 0) not in game_dict["bidding"]["passed"]:
            # If backhand was playing and forhand has not passed, forhand is playing
            turn = get_player_at_position(game_dict, 0)
        else:
            raise Exception("Somthing wrong happend in get_player_turn")
    return turn


def check_end_bidding(game_dict):
    if (len(game_dict["bidding"]["passed"]) == 2 and game_dict["bidding"]["bid_player"] is not None) or (len(game_dict["bidding"]["passed"]) == 3):
        return True
    else:
        return False