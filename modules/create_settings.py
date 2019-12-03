
from itertools import product

def create_settings(language='en'):
    """
    Choose the settings for the game
    language: Change the Language in which you play the game

    returns dict with:
    TODO Put everything in JSON files with "settings_DE.json" name (DE or EN or other language) and load Dynamically so that new files can be created
        Mybe Checksum by standart, so that no errors occure or other kind of Check
    """
    if not isinstance(language, str):
        raise TypeError("language needs to be of type str")
    if language == 'en':
        value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'J': 2, 'Q': 3, 'K': 4, 'A': 11}
        suit_dict = {"C": 12, "S": 11, "H": 10, "D": 9}
        standart_order_dict = {'7': 0, '8': 1, '9': 2, '10': 5, 'J': 7, 'Q': 3, 'K': 4, 'A': 6}
        null_order_dict = {'7': 0, '8': 1, '9': 2, '10': 3, 'J': 4, 'Q': 5, 'K': 6, 'A': 7}

        position_dict = {0: "Forhand", 1: "Middlehand", 2: "Backhand"}
        gamemode_dict = {0: {"name": "Color Game: Clubs", "trumpf": "C", "order_dict": "standart_order_dict", "points": 12},
                         1: {"name": "Color Game: Spade", "trumpf": "S", "order_dict": "standart_order_dict", "points": 11},
                         2: {"name": "Color Game: Hearts", "trumpf": "H", "order_dict": "standart_order_dict", "points": 10}, 
                         3: {"name": "Color Game: Diamonds", "trumpf": "D", "order_dict": "standart_order_dict", "points": 9},
                         4: {"name": "Grand", "trumpf": "J", "order_dict": "standart_order_dict", "points": 24},
                         5: {"name": "Zero", "trumpf": None, "order_dict": "null_order_dict", "points": 23}}

        bidmessage = "{}: Do you want to bid {}? With Yes you accept the bid, with No you pass."
        skatmessage = "{} Do you want to take the Skat? Yes or No"
        cardmessage = "{} Please Play a Card from your Cards. Please write the Cards as written under the Cards"
        gamemode_message = "{} Please choose a Gamemode from the ones beneeth. Just enter the Number"
        tablecard_message = "Cards on the Table"
        winner_message = "{} won this round"
        end_round_message="{} scored {} Points. {} get added to his Score Board"
        point_message = "{}| Points: {}"

        yesno_errormessage = "{}: Please enter Yes or No!"
        card_errormessage = "{} Please enter a Real Card which is in your Cards!"
        gamemode_errormessage = "{}Please Enter a valid number of the Gamemode"
        play_errormessage = "{} Play a Card with the same Suit as the first that was Played"
        
    elif language == 'de':
        value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'B': 2, 'D': 3, 'K': 4, 'A': 11}
        suit_dict = {"Kr": 12, "P": 11, "H": 10, "Ka": 9}
        standart_order_dict = {'7': 0, '8': 1, '9': 2, '10': 5, 'B': 7, 'D': 3, 'K': 4, 'A': 6}
        null_order_dict = {'7': 0, '8': 1, '9': 2, '10': 3, 'B': 4, 'D': 5, 'K': 6, 'A': 7}

        position_dict = {0: "Vorhand", 1: "Mittelhand", 2: "Rückhand"}
        gamemode_dict = {0: {"name": "Farbspiel: Kreuz", "trumpf": "Kr", "order_dict": "standart_order_dict", "points": 12},
                         1: {"name": "Farbspiel: Pik", "trumpf": "P", "order_dict": "standart_order_dict", "points": 11},
                         2: {"name": "Farbspiel: Herz", "trumpf": "H", "order_dict": "standart_order_dict", "points": 10}, 
                         3: {"name": "Farbspiel: Karo", "trumpf": "Ka", "order_dict": "standart_order_dict", "points": 9},
                         4: {"name": "Grand", "trumpf": "B", "order_dict": "standart_order_dict", "points": 24},
                         5: {"name": "Null", "trumpf": None, "order_dict": "null_order_dict", "points": 23}}

        bidmessage = "{}: Willst du {} bieten? Mit Yes akzeptierst du, mit No Passt du."
        skatmessage = "{} Willst du den Skat aufnehmen? Yes(ja)/No(Nein)"
        cardmessage = "{} Spiele eine Karte aus deinem Blatt. Bitte Schreib die Karte so, wie unter den oben angezeigten Karten zu sehen"
        gamemode_message = "{} Wähle einen Spielart von den darunterligenden aus. Bitte gebe nur die Nummer ein"
        tablecard_message = "Karten auf dem Tisch"
        winner_message = "{} hat die Runde gewonnen"
        point_message = "{}| Punkte: {}"
        end_round_message="{} hat {} Punkte. {} werden zu seinen Punktewerte dazugerechnet"

        yesno_errormessage = "{}: Bitte geb Yes(ja) oder No(nein) ein!"
        card_errormessage = "{} Bitte geben sie eine echte Karte ein, die sich auch in ihrem Blatt befindet!"
        gamemode_errormessage = "{} Bitte gebe nur eine Zahl der Spielarten ein."
        play_errormessage = "{} Spiele eine Karte mit der selben Farbe wie der ersten"
    else:
        raise ValueError("Please choose Between english (en) and german (de)")
    
    # Create Bid list
    # Get all Values except Null for bidding, Null is added afterwards, the Number of Jacks dont care for that
    point_list = [mode["points"] for mode in gamemode_dict.values() if mode["trumpf"] is not None]
    bid_list = [x[0]*x[1] for x in product(point_list, range(2, 6))]
    bid_list.append(23) # Add Null Value
    bid_list.sort()
    return {"value_dict": value_dict,
            "suit_dict": suit_dict,
            "position_dict": position_dict,
            "bid_list": bid_list,
            "bidmessage": bidmessage,
            "yesno_errormessage": yesno_errormessage,
            "skatmessage":skatmessage,
            "cardmessage": cardmessage,
            "card_errormessage": card_errormessage, 
            "gamemode_dict": gamemode_dict,
            "gamemode_message": gamemode_message,
            "gamemode_errormessage": gamemode_errormessage,
            "tablecard_message": tablecard_message,
            "play_errormessage": play_errormessage,
            "standart_order_dict": standart_order_dict,
            "null_order_dict": null_order_dict,
            "winner_message": winner_message,
            "point_message": point_message,
            "end_round_message":end_round_message}

def create_player(player_name, player_num, player_position):
    """
    Creates a dict with all Information for one Player
    name: Name of the Player
    num: fixed number of the player
    cards: the cards of the Player
    points: the Points of the Player
    position: the position in the game (0 For-, 1 middle-, 2 Backhand)
    bid: the bid of the player. None if he hasn't bid yet, int if he bid, false if he passed
    """
    return {"name": player_name,"num": player_num,"cards": [],"points": 0,"position": player_position}

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
    order_dict: The dictionary with the order of witch card is is higher than the other
    """
    return {"players": create_players(player_names), 
            "gamestate": 1, 
            "skat": [], 
            "single_player_stack": [],
            "jack_multiplicator": None,
            "table_cards": [],
            "game_round": 1, 
            "max_round": max_rounds,
            "settings": create_settings(language),
            "gamemode": None,
            "turn": None,
            "bidding": None,
            "order_dict": None}