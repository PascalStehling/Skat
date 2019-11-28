
def get_player_at_position(game_dict, position):
    """
    Returns the number of the player who is Playing forehand
    """
    for player_num in game_dict["players"]:
        if  game_dict["players"][player_num]["position"] == position:
            return player_num
    raise Exception("No Player at this position")