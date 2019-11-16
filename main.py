"""
This is the main File with starts the skat App
"""
from setup_round import setup_round

def create_settings(language='en'):
    """
    Choose the settings for the game
    language: Change the Language in which you play the game
    """
    if not isinstance(language, str):
        raise TypeError("language needs to be of type str")
    if language == 'en':
        value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'J': 2, 'Q': 3, 'K': 4, 'A': 11}
        suit_dict = {"C": 12, "S": 11, "H": 10, "D": 9}
        position_dict = {0: "Forhand", 1: "Middlehand", 2: "Backhand"}
    elif language == 'de':
        value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'B': 2, 'D': 3, 'K': 4, 'A': 11}
        suit_dict = {"Kr": 12, "P": 11, "H": 10, "Ka": 9}
        position_dict = {0: "Vorhand", 1: "Mittelhand", 2: "Rückhand"}
    else:
        raise ValueError("Please choose Between english (en) and german (de)")

    return {"value_dict": value_dict, "suit_dict": suit_dict, "position_dict": position_dict}

def create_player(player_name, player_num, player_position):
    """
    Creates a dict with all Information for one Player
    name: Name of the Player
    num: fixed number of the player
    cards: the cards of the Player
    points: the Points of the Player
    position: the position in the game (0 For-, 1 middle-, 2 Backhand)
    passed: if the player has passed by bidding
    """
    return {"name": player_name,"num": player_num,"cards": [],"points": 0,"position": player_position, "passed": False}

def create_players(player_names=None):
    """
    Creates a Dictionary with all 3 Players and all there Attributes
    """
    if player_names is None:
        player_names = ["Player 1", "Player 2", "Player 3"]
    elif not isinstance(player_names, list):
        raise TypeError("Player names need to be of type list")
    elif len(player_names) != 3:
        raise ValueError("You need exactly 3 Players")
    elif any([not isinstance(p, str) for p in player_names]): # Checks if all Player names are Strings
        raise TypeError("All player Names need to be Strings")

    player_dict = {}
    for i, p in enumerate(player_names):
        player_dict[i] = create_player(p, i, i) # The starting possition is the same as the number

    return player_dict

def create_game_dict(player_names=None, max_rounds=36, language='en'):
    """
    Creates the game dict, in which all the data about the game is stored.

    players: has all attributes about the players
    gamestate: the current gamestate: 1: setting up round, 2: bidding phase, TODO
    skat: the cards which are in the skat
    single_player_stack: the cards of the won round from the single player, witch need to be calculated at the end to get the points
    game_round: number of rounds which were Played
    max_rounds: maximum amount of rounds which are played
    gamemode: the gamemode which is played for the round
    turn: the player, who has its turn
    """
    return {"players": create_players(player_names), 
            "gamestate": 1, 
            "skat": [], 
            "single_player_stack": [], 
            "game_round": 1, 
            "max_round": max_rounds,
            "settings": create_settings(language),
            "gamemode": None,
            "turn": None}

def create_function_dict():
    return {1: setup_round}

class StateMachine:

    def __init__(self, player_names=None, max_rounds=36, language='en'):
        self.game_dict = create_game_dict(player_names, max_rounds, language)
        self.fun_dict = create_function_dict()

    def run(self):
        while self.game_dict["game_round"] < self.game_dict["max_round"]:
            state_fun = self.fun_dict[self.game_dict["gamestate"]]
            self.game_dict = state_fun(self.game_dict)
            break

if __name__ == "__main__":
    s = StateMachine(language='de')
    s.run()
