from classes.cards import Cards
from classes.card import EmptyCard, Card
from classes.tools import user_select_card
from copy import deepcopy

class PlayRound():

    def __init__(self, settings, players, bidding):
        self.settings = settings
        self.single_player_stack = Cards(self.settings)
        self.bidding = bidding
        self.players = players
        self.turn = players.forhand

    def every_player_plays_card(self):
        move = PlayerMove(self.settings)

        for _ in range(3):
            move.play_card(self.turn)
            self.turn = self.players.get_next_player(self.turn)

        self.turn = move.winner
        move.cards_on_table.print_cards_ascii()
        print(self.settings.winner_message.format(self.turn.name))
        
        self.add_cards_single_player_stack(move)
    
    def has_single_player_won(self):
        return self.turn == self.bidding.bid_player

    def add_cards_single_player_stack(self, move):
        if self.has_single_player_won():
            self.single_player_stack += move.cards_on_table
            print(self.single_player_stack)
        
    def play_round(self):
        while self.turn.has_cards():
            self.every_player_plays_card()
    
class PlayerMove():

    def __init__(self, settings):
        self.settings = settings
        self.cards_on_table = Cards(settings)
        self.single_player_stack = []
        self.winner = None

    def play_card(self, turn):
        self.turn = turn
        self.print_card_table()
        self.user_play_card()
        self.check_winner()

    def check_winner(self):
        if len(self.cards_on_table) == 1:
            self.winner = self.turn
        else:
            if all([True if self.cards_on_table[-1].ishigher(card) else False for card in self.cards_on_table[:-1]]):
                self.winner = self.turn

    def user_play_card(self):
        card_message = self.settings.cardmessage.format(self.turn.name)
        card_errormessage = self.settings.card_errormessage.format(self.turn.name)
        self.turn.cards, played_card = user_select_card(card_message, card_errormessage, self.turn.cards)

        if not self.is_valid_card(played_card):
            self.turn.cards.add_card_and_sort(played_card)
            print(self.settings.play_errormessage.format(self.turn.name))
            self.user_play_card()
        else:
            self.cards_on_table.add_card(played_card)

    def is_valid_card(self, played_card):
        """Checks if the Card that was played is valid. It checks if the played card has the same suit or trumpf as the first played card. 
        If this isnt the case it checks if any of the user card has the same suit or trumpf as the first played card. If this is true the its not a valid card.
        
        Args:
            played_card (Card): the Card the user wants to play
        
        Returns:
            bool: True if the play was valid, else False
        """
        if not self.cards_on_table:
            return True
        if self.same_suit_or_trumpf(self.cards_on_table[0], played_card):
            return True
        if not self.same_suit_in_cards(self.cards_on_table[0]):
            return True

        return False

    def same_suit_in_cards(self, check_card):
        """Checks if there is an card with the same suit or trumpf in the cards of the user.
        
        Args:
            check_card (Card): Card to check for in the list
        
        Returns:
            bool: True if there if a card in the list has the same suit or both are trumpf in user_cards, else False
        """
        return any(self.same_suit_or_trumpf(check_card, card) for card in self.turn.cards)

    def same_suit_or_trumpf(self, card1, card2):
        """Check if 2 Cards have the same Suit or both are trumpf. 
        
        Args:
            card1 (Card): First Card to Compare
            card2 (Card): Second Card to Compare
        
        Returns:
            boolean: True If the 2 Cards have the same suit or are both trumpf, else False
        """
        
        # If there is an Trumpf, it need to be checked if the card is trumpf, because the jacks are diffrent color but are trumpf
        if card1.istrumpf():
            return card2.istrumpf() # If Both ar Trumpf they are equal, if card 1 is trumpf and card2 not its not equal
        
        if card2.istrumpf(): # if card2 is trumpf and card1 not, its not equal
            return False

        return card1.equal_suit(card2) # if they are both not trumpf, just the suit matters

    def print_card_table(self):
        """Prints the Cards that were Played plus empty cards to show how many need to be played
        """
        cards_on_table = deepcopy(self.cards_on_table)
        while len(cards_on_table) < 3:
            cards_on_table.add_card(EmptyCard())

        print(self.settings.tablecard_message)
        cards_on_table.print_cards_ascii()