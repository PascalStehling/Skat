#pylint: disable=line-too-long
"""The File with the Round Class
"""
from modules.Card import Card
from modules.Cards import Cards
from modules.Bidding import Bidding
from modules.tools import get_user_true_false, user_select_card
from modules.Stich import Stich


class Round():
    """The Round Class has all Functions for Playing and Evaluating a Played Round
    """

    def __init__(self, players, settingContainer):
        self.turn = None
        self.settings = settingContainer
        self.players = players
        self.bidding = None
        self.jack_multiplicator = None
        self.gamemode = None
        self.skat = None

        self.start_new_round()

    def start_bidding(self):
        """Start and play the bidding phase

        Returns:
            int: the new gamstate after the bidding Phase
        """
        self.bidding = Bidding(self.settings, self.players)
        self.turn, gamestate = self.bidding.play_bidding()
        return gamestate

    def play_round(self):
        """Play a round

        Returns:
            Rround: return its own object
        """
        while len(self.turn.cards) != 0:
            self.turn = Stich(self.players, self.turn, self.settings
                              ).play_stich(
                              ).assign_stich_to_winner(
                              ).get_winner()
            print(self.settings.winner_message.format(self.turn.name))
        return self

    def end_round(self):
        """Calculates all Points and ends the played round

        Returns:
            Round: returns itself
        """
        self.bidding.bid_player.cards += self.skat
        single_player_card_points = self._calculate_single_player_points()
        score = self._calculate_score(single_player_card_points)
        self.bidding.bid_player.score += score
        print(self.settings.end_round_message.format(
            self.bidding.bid_player, single_player_card_points, score))
        self._print_player_scores()

        self.players.set_players_on_next_position()

        return self

    def _print_player_scores(self):
        """Prints the Scores of the Players
        """
        for p in self.players:
            print(self.settings.point_message.format(p.name, p.score))

    def _calculate_score(self, single_player_card_points):
        """Calculate the score points of the single_player

        Returns:
            int: the score points the player achieved
        """
        if self._has_won_round(single_player_card_points):
            return self._calc_score_points_won(single_player_card_points)

        return self._calc_score_points_lost(single_player_card_points)

    def _calc_score_points_won(self, single_player_card_points):
        """Get the Score points if the player won
        Returns:
            int: the score points the player achieved
        """
        return (self._get_win_level(single_player_card_points)+self.jack_multiplicator)*self.gamemode["points"]

    def _calc_score_points_lost(self, single_player_card_points):
        """Get the Score points if the player Lost

        Returns:
            int: the score points the player achieved
        """
        return (self._get_win_level(120-single_player_card_points)+self.jack_multiplicator)*self.gamemode["points"]*-2

    @staticmethod
    def _get_win_level(card_points):
        """Get the win states the Player has.

        Returns:
            int: 0 for playing, 1 for Schneider and 2 for Schwarz
        """
        if card_points == 120:
            return 2
        if card_points > 90:
            return 1

        return 0

    def _calculate_single_player_points(self):
        """Claculates the Points for the single Player

        Returns:
            int: the Points the single Player achieved
        """
        points = 0
        for card in self.bidding.bid_player.cards:
            points += card.card_points
        return points

    def _has_won_round(self, card_points):
        """Checks if the Player has won this round. If he has over 90 he always wins, under 60 allways loose and between 60 and 90 it depends if he overbidded

        Returns:
            bool: True if the Player won, else False
        """
        if card_points >= 90:
            return True

        if card_points <= 60:
            return False

        return not self._has_over_bidded()

    def _has_over_bidded(self):
        """Checks is the Player has overbidden

        Returns:
            bool: True if the player has overbidded, else False
        """
        if Card.trumpf is not None:
            return (self.gamemode["points"]*self.jack_multiplicator) < self.bidding.bid

        return self.gamemode["points"] < self.bidding.bid

    def setup(self):
        """Starts the Setup, in which the single Player can take the Skat and choose the gamemode

        Returns:
            Round: returns itself
        """
        self.turn = self.bidding.bid_player
        if self._check_take_skat():
            self._take_skat()
        self.set_gamemode()
        self.jack_multiplicator = self._get_jack_multiplicator()
        self.turn = self.players.forhand
        return self

    def _check_take_skat(self):
        """Asks if the Single Player wants to take the Skat

        Returns:
            bool: True if he wats to take the Skat, else Flase
        """
        show_message = self.settings.skatmessage.format(self.turn.name)
        error_message = self.settings.yesno_errormessage.format(self.turn.name)
        return get_user_true_false(show_message, error_message, self.turn.cards)

    def _take_skat(self):
        """Take the Skat and let the single Player decide, which one he wants to put away
        """
        self.turn.cards += self.skat
        self.turn.cards.sort_cards()
        self.skat.empty_cards()

        show_message = self.settings.cardmessage.format(self.turn.name)
        error_message = self.settings.card_errormessage.format(self.turn.name)

        for _ in range(2):
            self.turn.cards, skat_card = user_select_card(
                show_message, error_message, self.turn.cards)
            self.skat.add_card(skat_card)

    def set_gamemode(self):
        """Ask the SIngle Player which play Types he wants to chose and sets it
        """
        self.gamemode = self._get_play_type()
        Card.order_dict = self.settings.order_dicts[self.gamemode["order_dict"]]
        Card.trumpf = self.gamemode["trumpf"]

    def _get_play_type(self):
        """Get the Play Type from the single Player

        Returns:
            int: The Gamemode the Single Player Chooses
        """
        self.turn.cards.print_cards_ascii()
        print(self.settings.gamemode_message.format(self.turn.name))
        for key in self.settings.gamemode_dict:
            print(f"{key}: {self.settings.gamemode_dict[key]['name']}")

        inp = input()
        if inp.isdigit() and inp in self.settings.gamemode_dict:
            return self.settings.gamemode_dict[inp]

        print(self.settings.gamemode_errormessage.format(self.turn.name))
        return self._get_play_type()

    def _get_jack_multiplicator(self):
        """Get the jack multiplicator for the play

        Returns:
            int: the Multiplier
        """
        jack_cards = self.turn.cards.get_jacks()
        if len(jack_cards) == 4 or len(jack_cards) == 0:
            return 5

        multi = 2
        if self._is_club_jack_in_cards(jack_cards):
            multi += self._count_cards_with_jacks(jack_cards)
        else:
            multi += self._count_cards_without_jacks(jack_cards)
        return multi

    def _is_club_jack_in_cards(self, cards):
        """Checks if the Club Jack is in the Cards object

        Args:
            cards (Cards): A Cards Object

        Returns:
            bool: True if the club Jack is in Cards, else False
        """
        return self._has_card_with_suit(cards, self.settings.sorted_suit_list[0])

    def _count_cards_without_jacks(self, cards):
        """Get a Multiplier, if the Club Jack is not in Cards

        Args:
            cards (Cards): a Cards Object

        Returns:
            int: the Number of not appearing Jacks
        """
        multi = 0
        for suit in self.settings.sorted_suit_list[1:]:
            if not self._has_card_with_suit(cards, suit):
                multi += 1
            else:
                break
        return multi

    def _count_cards_with_jacks(self, cards):
        """Get a Multiplier, if the Club Jack is not in Cards

        Args:
            cards (Cards): a Cards Object

        Returns:
            int: the Number of appearing Jacks
        """
        multi = 0
        for suit in self.settings.sorted_suit_list[1:]:
            if self._has_card_with_suit(cards, suit):
                multi += 1
            else:
                break
        return multi

    @staticmethod
    def _has_card_with_suit(cards, suit):
        """Checks if the Cards object has atleast one Card with the given suit

        Args:
            cards (Cards): the Cards in which the suit will be searched
            suit (str): the Suit which is searched

        Returns:
            bool: True if the suit was found, else False
        """
        for card in cards:
            if card.suit_str == suit:
                return True
        return False

    def start_new_round(self):
        """Starts a new round
        """
        self.set_card_default_values()
        self.players.reset()
        self.give_cards()

    def set_card_default_values(self):
        """sets the static Values of Card to its default
        """
        Card.value_dict = self.settings.value_dict
        Card.suit_dict = self.settings.suit_dict
        Card.order_dict = self.settings.standart_order_dict
        Card.trumpf = self._get_clubs_string()

    def give_cards(self):
        """give Cards to every Player and put 2 into the Skat
        """
        cards = Cards(self.settings)
        cards.create_shuffled_cards()
        for i, player in enumerate(self.players):
            player.cards = Cards(self.settings, cards.cards[10*i:10*(i+1)])
            player.cards.sort_cards()

        self.skat = Cards(self.settings, cards.cards[-2:])

    def _get_clubs_string(self):
        """Get the suit name of Clubs (because of Multi language)

        Raises:
            Exception: If there are no Clubs

        Returns:
            str: the name of Clubs in the game
        """
        for tup in self.settings.suit_dict.items():
            if tup[1] == 12:
                return tup[0]
        raise Exception("No Clubs found")
