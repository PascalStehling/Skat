
from modules.card import EmptyCard, Card
from modules.tools import print_multiple_cards, user_select_card, sort_cards
from copy import copy

def play_card_user(game_dict):

    player_name = game_dict["players"][game_dict["turn"]]["name"]
    card_message = game_dict["settings"]["cardmessage"].format(player_name)
    card_errormessage = game_dict["settings"]["card_errormessage"].format(player_name)
    play_errormessage = game_dict["settings"]["play_errormessage"].format(player_name)
    table_card_message = game_dict["settings"]["tablecard_message"]
    cards = game_dict["players"][game_dict["turn"]]["cards"]
    value_dict = game_dict["settings"]["value_dict"]
    suit_dict = game_dict["settings"]["suit_dict"]
    trumpf = game_dict["gamemode"]["trumpf"]
    previous_played_cards = game_dict["table_cards"]
    order_dict = game_dict["order_dict"]
    turn = game_dict["turn"]

    print_card_table(previous_played_cards, table_card_message)

    game_dict["table_cards"], game_dict["players"][turn]["cards"] = user_play_card(cards, previous_played_cards, trumpf, value_dict, suit_dict, order_dict, card_message, card_errormessage, play_errormessage)

    if len(game_dict["table_cards"]) < 3:
        game_dict["turn"] =  update_turn(turn)
        return game_dict
    
    winner = get_winner(game_dict["table_cards"], trumpf, order_dict, turn)
    game_dict["turn"] = winner

    print_multiple_cards(game_dict["table_cards"])
    print(game_dict["settings"]["winner_message"].format(game_dict["players"][winner]["name"]))

    game_dict["single_player_stack"] += update_single_player_stack(winner, game_dict["bidding"]["bid_player"], game_dict["table_cards"])
    game_dict["table_cards"] = []

    if len(game_dict["players"][winner]["cards"]) == 0:
        game_dict["gamestate"] = 5

    return game_dict

def user_play_card(cards, previous_played_cards, trumpf, value_dict, suit_dict, order_dict, card_message, card_errormessage, play_errormessage):

    cards, played_card = user_select_card(card_message, card_errormessage, cards, value_dict, suit_dict)

    if not is_valid_card():
        cards.append(played_card)
        cards = sort_cards(cards, order_dict, trumpf)
        print(play_errormessage)
        return user_play_card(cards, previous_played_cards, trumpf, value_dict, suit_dict, order_dict, card_message, card_errormessage, play_errormessage)
    
    previous_played_cards.append(played_card)
    return previous_played_cards, cards

def is_valid_card(previous_played_cards, played_card, trumpf, user_cards):
    if previous_played_cards:
        if not same_suit_or_trumpf(previous_played_cards[0], played_card, trumpf):
            if same_suit_in_cards(previous_played_cards[0], trumpf, user_cards):
                return False
    return True

def same_suit_in_cards(check_card, trumpf, user_cards):
    return any(same_suit_or_trumpf(check_card, card, trumpf) for card in user_cards)


def same_suit_or_trumpf(card1, card2, trumpf):
    """Check if 2 Cards have the same Suit or both are trumpf. 
    
    Args:
        card1 (Card): First Card to Compare
        card2 (Card): Second Card to Compare
        trumpf (str): the trumpf which is played
    
    Returns:
        boolean: True If the 2 Cards have the same suit or are both trumpf, else False
    """

    if trumpf is None:
        return card1.equal_suit(card2) # if there is no trumpf, just the coller matters
    
    # If there is an Trumpf, it need to be checked if the card is trumpf, because the jacks are diffrent color but are trumpf
    if card1.istrumpf(trumpf):
        return card2.istrumpf(trumpf) # If Both ar Trumpf they are equal, if card 1 is trumpf and card2 not its not equal
    
    if card2.istrumpf(trumpf): # if card2 is trumpf and card1 not, its not equal
        return False

    return card1.equal_suit(card2) # if they are both not trumpf, just the suit matters

def get_winning_card(table_cards, trumpf, order_dict):
    """Checks which is the winning card, from all Cards that were played
    
    Args:
        table_cards (list): List of Cards that were Played
        trumpf (str): the trumpf at the moment
        order_dict (dict): the dictionary with the ranking for all cards
    
    Returns:
        int: the number of that card that won
    """

    winner = table_cards[0]
    for card in table_cards[1:]:
        if not winner.ishigher(card, trumpf, order_dict):
            winner = card
    
    return table_cards.index(winner)

def get_winner(table_cards, trumpf, order_dict, turn):
    """Gets the cards that were Played and returns the number of the Player who won
    
    Args:
        table_cards (list): List of Cards that were Played
        trumpf (str): the trumpf at the moment
        order_dict (dict): the dictionary with the ranking for all cards
        turn (int): The Number of the Player who is playing
    
    Returns:
        int: number of the player who won
    """
    return (turn+1+get_winning_card(table_cards, trumpf, order_dict))%3

def print_card_table(table_cards, table_card_message):
    """Prints the Cards that were Played plus empty cards to show how many need to be played
    
    Args:
        table_cards (list): List of Cards that were played
        table_card_message (str): MessAGE that will be printed befor the cards
    """
    cards_on_table = copy(table_cards)
    while len(cards_on_table) < 3:
        cards_on_table.append(EmptyCard())

    print(table_card_message)
    print_multiple_cards(cards_on_table)

def update_turn(turn):
    """updates the turn to the next player
    
    Args:
        turn (int): Number of the Player which has his turn
    
    Returns:
        int: Number of the Player who has next round his turn
    """
    return (turn + 1)%3

def update_single_player_stack(winner, single_player, table_cards):
    """Checks if the single_player has won, if so returns a list with the cards, else an empty list
    
    Args:
        winner (int): number of the player who won
        single_player (int): number of the single Player
        table_cards (list): [List of Cards that were Played
    
    Returns:
        list: empty list, if the winner is not the single player, else table cards
    """
    if winner == single_player:
        return copy(table_cards)
    
    return []