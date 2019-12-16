
from modules.card import EmptyCard, Card
from modules.cards import Cards
from modules.tools import user_select_card
from copy import deepcopy

def play_card_user(game_round, settings, players):

    gamestate = 4
    player_name = game_round.turn.name
    card_message = settings.cardmessage.format(player_name)
    card_errormessage = settings.card_errormessage.format(player_name)
    play_errormessage = settings.play_errormessage.format(player_name)
    table_card_message = settings.tablecard_message

    print_card_table(game_round.cards_on_table, table_card_message)

    game_round, game_round.turn.cards = user_play_card(game_round, card_message, card_errormessage, play_errormessage)

    if len(game_round.cards_on_table) < 3:
        game_round.turn = players.get_next_player(game_round.turn)
        return game_round, gamestate
    
    winner = get_winner(game_round, players)
    game_round.turn = winner

    game_round.cards_on_table.print_cards_ascii()
    print(settings.winner_message.format(winner.name))

    game_round.single_player_stack += update_single_player_stack(winner, game_round, settings)
    game_round.cards_on_table = Cards(settings)

    if len(winner.cards) == 0:
        gamestate = 5

    return game_round, gamestate

def user_play_card(game_round, card_message, card_errormessage, play_errormessage):

    cards, played_card = user_select_card(card_message, card_errormessage, game_round.turn.cards)

    if not is_valid_card(game_round, played_card):
        cards.add_card(played_card)
        cards.sort_cards()
        print(play_errormessage)
        return user_play_card(game_round, card_message, card_errormessage, play_errormessage)
    
    game_round.cards_on_table.add_card(played_card)
    return game_round, cards

def is_valid_card(game_round, played_card):
    """Checks if the Card that was played is valid. It checks if the played card has the same suit or trumpf as the first played card. 
    If this isnt the case it checks if any of the user card has the same suit or trumpf as the first played card. If this is true the its not a valid card.
    
    Returns:
        bool: True if the play was valid, else False
    """
    if not game_round.cards_on_table.cards:
        return True
    if same_suit_or_trumpf(game_round.cards_on_table[0], played_card):
        return True
    if not same_suit_in_cards(game_round.cards_on_table[0], game_round.turn.cards):
        return True

    return False

def same_suit_in_cards(check_card, user_cards):
    """Checks if there is an card with the same suit or trumpf in an list of cards.
    
    Args:
        check_card (Card): Card to check for in the list
        trumpf (str): the trumpf witch is played
        user_cards (list): List of cards whitch will be checked
    
    Returns:
        bool: True if there if a card in the list has the same suit or both are trumpf in user_cards, else False
    """
    return any(same_suit_or_trumpf(check_card, card) for card in user_cards)


def same_suit_or_trumpf(card1, card2):
    """Check if 2 Cards have the same Suit or both are trumpf. 
    
    Args:
        card1 (Card): First Card to Compare
        card2 (Card): Second Card to Compare
        trumpf (str): the trumpf which is played
    
    Returns:
        boolean: True If the 2 Cards have the same suit or are both trumpf, else False
    """

    if Card.trumpf is None:
        return card1.equal_suit(card2) # if there is no trumpf, just the coller matters
    
    # If there is an Trumpf, it need to be checked if the card is trumpf, because the jacks are diffrent color but are trumpf
    if card1.istrumpf():
        return card2.istrumpf() # If Both ar Trumpf they are equal, if card 1 is trumpf and card2 not its not equal
    
    if card2.istrumpf(): # if card2 is trumpf and card1 not, its not equal
        return False

    return card1.equal_suit(card2) # if they are both not trumpf, just the suit matters

def get_winning_card(table_cards):
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
        if not winner.ishigher(card):
            winner = card
    
    return table_cards.index(winner)

def get_winner(game_round, players):
    """Gets the cards that were Played and returns the number of the Player who won
    """
    return players.get_player_by_num((game_round.turn.num+1+get_winning_card(game_round.cards_on_table))%3)

def print_card_table(table_cards, table_card_message):
    """Prints the Cards that were Played plus empty cards to show how many need to be played
    
    Args:
        table_cards (list): List of Cards that were played
        table_card_message (str): MessAGE that will be printed befor the cards
    """
    cards_on_table = deepcopy(table_cards)
    while len(cards_on_table) < 3:
        cards_on_table.add_card(EmptyCard())

    print(table_card_message)
    cards_on_table.print_cards_ascii()

def update_turn(turn):
    """updates the turn to the next player
    
    Args:
        turn (int): Number of the Player which has his turn
    
    Returns:
        int: Number of the Player who has next round his turn
    """
    return (turn + 1)%3

def update_single_player_stack(winner, game_round, settings):
    """Checks if the single_player has won, if so returns a list with the cards, else an empty list
    
    Args:
        winner (int): number of the player who won
        single_player (int): number of the single Player
        table_cards (list): [List of Cards that were Played
    
    Returns:
        list: empty list, if the winner is not the single player, else table cards
    """
    if winner == game_round.bidding.bid_player:
        return deepcopy(game_round.cards_on_table)
    
    return Cards(settings)