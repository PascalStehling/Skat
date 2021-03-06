# pylint: disable=line-too-long,
"""This File Contains the Stich Class
"""
from copy import deepcopy
from modules.tools import user_select_card
from modules.Card import EmptyCard
from modules.Cards import Cards


class Stich():
    """The Stich CLass contains all functions which are neccessary to play a single Stich
    """

    def __init__(self, players, turn, settings):
        self.settings = settings
        self.players = players
        self.turn = turn
        self.cards_on_table = Cards(settings)

    def play_stich(self):
        """Play a single Stich

        Returns:
            Stich: returns itself
        """
        for _ in range(3):
            self.print_card_table()
            self._play_card()
            self.turn = self.players.get_next_player(self.turn)
        print(self.cards_on_table)
        self.cards_on_table.print_cards_ascii()
        return self

    def _play_card(self):
        """Plays a card
        """
        if not self.turn.auto_play:
            self._user_play_card()
        else:
            self._auto_play_card()

    def _auto_play_card(self):
        """Function for automatic playing cards with an AI
        """
        for card in self.turn.cards:
            if self._is_valid_card(card):
                self.turn.cards.remove(card)
                self.cards_on_table.add_card(card)

    def _user_play_card(self):
        """Playing a card as a user
        """
        card_message = self.settings.cardmessage.format(self.turn.name)
        card_errormessage = self.settings.card_errormessage.format(
            self.turn.name)
        play_errormessage = self.settings.play_errormessage.format(
            self.turn.name)

        self.turn.cards, played_card = user_select_card(
            card_message, card_errormessage, self.turn.cards)

        if not self._is_valid_card(played_card):
            self.turn.cards.add_card(played_card)
            self.turn.cards.sort_cards()
            print(play_errormessage)
            self._user_play_card()
        else:
            self.cards_on_table.add_card(played_card)

    def _is_valid_card(self, played_card):
        """Checks if the Card that was played is valid. It checks if the played card has the same suit or trumpf as the first played card.
        If this isnt the case it checks if any of the user card has the same suit or trumpf as the first played card. If this is true the its not a valid card.

        Returns:
            bool: True if the play was valid, else False
        """
        if not self.cards_on_table.cards:
            return True
        if self.cards_on_table[0].same_suit_or_trumpf(played_card):
            return True
        if not self._same_suit_in_cards(self.cards_on_table[0]):
            return True

        return False

    def _same_suit_in_cards(self, check_card):
        """Checks if there is an card with the same suit or trumpf in an list of cards.

        Args:
            check_card (Card): Card to check for in the list

        Returns:
            bool: True if there if a card in the list has the same suit or both are trumpf in user_cards, else False
        """
        return any(check_card.same_suit_or_trumpf(card) for card in self.turn.cards)

    def print_card_table(self):
        """Prints the Cards that were Played plus empty cards to show how many need to be played
        """
        cards_on_table = deepcopy(self.cards_on_table)
        while len(cards_on_table) < 3:
            cards_on_table.add_card(EmptyCard())

        table_card_message = self.settings.tablecard_message
        print(table_card_message)
        cards_on_table.print_cards_ascii()

    def _get_winning_card_index(self):
        """Checks which is the winning card, from all Cards that were played
        Returns:
            int: the number of that card that won
        """

        winner = self.cards_on_table[0]
        for card in self.cards_on_table[1:]:
            if not winner.ishigher(card):
                winner = card

        return self.cards_on_table.index(winner)

    def get_winner(self):
        """Gets the cards that were Played and returns the number of the Player who won
        """
        return self.players.get_player_by_num((self.turn.num+1+self._get_winning_card_index()) % 3)

    def assign_stich_to_winner(self):
        """assign the Cards of the Stich to the winner

        Returns:
            Stich: retunrs itself
        """
        self.get_winner().won_cards += self.cards_on_table
        return self
