from modules.Card import Card
from modules.Cards import Cards
from modules.Bidding import Bidding
from modules.tools import get_user_true_false, user_select_card
from modules.Stich import Stich


class Round():

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
        self.bidding = Bidding(self.settings, self.players)
        self.turn, gamestate = self.bidding.play_bidding()
        return gamestate

    def play_round(self):
        while len(self.turn.cards) != 0:
            self.turn = Stich(self.players, self.turn, self.settings).play_stich(
            ).assign_stich_to_winner().get_winner()
            print(self.settings.winner_message.format(self.turn.name))
        return self

    def end_round(self):
        """The main function to end the round   
        """
        self.bidding.bid_player.cards += self.skat
        single_player_card_points = self.calculate_single_player_points()
        score = self.calculate_score(single_player_card_points)
        self.bidding.bid_player.score += score
        print(self.settings.end_round_message.format(
            self.bidding.bid_player, single_player_card_points, score))
        self.print_player_scores()

        self.players.set_players_on_next_position()

        return self

    def print_player_scores(self):
        for p in self.players:
            print(self.settings.point_message.format(p.name, p.score))

    def calculate_score(self, single_player_card_points):
        """Calculate the score points of the single_player

        Returns:
            int: the score points the player achieved
        """
        if self.has_won_round(single_player_card_points):
            return self.calc_score_points_won(single_player_card_points)
        else:
            return self.calc_score_points_lost(single_player_card_points)

    def calc_score_points_won(self, single_player_card_points):
        """Get the Score points if the player won
        Returns:
            int: the score points the player achieved
        """
        return (self.get_win_level(single_player_card_points)+self.jack_multiplicator)*self.gamemode["points"]

    def calc_score_points_lost(self, single_player_card_points):
        """Get the Score points if the player Lost

        Returns:
            int: the score points the player achieved
        """
        return (self.get_win_level(120-single_player_card_points)+self.jack_multiplicator)*self.gamemode["points"]*-2

    @staticmethod
    def get_win_level(card_points):
        """Get the win states the Player has.

        Returns:
            int: 0 for playing, 1 for Schneider and 2 for Schwarz
        """
        if card_points == 120:
            return 2
        if card_points > 90:
            return 1

        return 0

    def calculate_single_player_points(self):
        points = 0
        for card in self.bidding.bid_player.cards:
            points += card.card_points
        return points

    def has_won_round(self, card_points):
        """Checks if the Player has won this round. If he has over 90 he always wins, under 60 allways loose and between 60 and 90 it depends if he overbidded

        Returns:
            bool: True if the Player won, else False
        """
        if card_points >= 90:
            return True

        if card_points <= 60:
            return False

        return not self.has_over_bidded()

    def has_over_bidded(self):
        """Checks is the Player has overbidden

        Returns:
            bool: True if the player has overbidded, else False
        """
        if Card.trumpf is not None:
            return (self.gamemode["points"]*self.jack_multiplicator) < self.bidding.bid
        else:
            return self.gamemode["points"] < self.bidding.bid

    def setup(self):
        self.turn = self.bidding.bid_player
        if self.check_take_skat():
            self.take_skat()
        self.set_gamemode()
        self.jack_multiplicator = self.get_jack_multiplicator()
        self.turn = self.players.forhand
        return self

    def check_take_skat(self):
        show_message = self.settings.skatmessage.format(self.turn.name)
        error_message = self.settings.yesno_errormessage.format(self.turn.name)
        return get_user_true_false(show_message, error_message, self.turn.cards)

    def take_skat(self):
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
        self.gamemode = self.get_play_type()
        Card.order_dict = self.settings.order_dicts[self.gamemode["order_dict"]]
        Card.trumpf = self.gamemode["trumpf"]

    def get_play_type(self):
        self.turn.cards.print_cards_ascii()
        print(self.settings.gamemode_message.format(self.turn.name))
        for key in self.settings.gamemode_dict:
            print(f"{key}: {self.settings.gamemode_dict[key]['name']}")

        inp = input()
        if inp.isdigit() and inp in self.settings.gamemode_dict:
            return self.settings.gamemode_dict[inp]
        else:
            print(self.settings.gamemode_errormessage.format(self.turn.name))
            return get_play_type()

    def get_jack_multiplicator(self):
        """
        Get the jack multiplicator for the play
        """
        jack_cards = self.turn.cards.get_jacks()
        if len(jack_cards) == 4 or len(jack_cards) == 0:
            return 5

        multi = 2
        if self.is_club_jack_in_cards(jack_cards):
            multi += self._count_cards_with_jacks(jack_cards)
        else:
            multi += self._count_cards_without_jacks(jack_cards)
        return multi

    def is_club_jack_in_cards(self, cards):
        return self.has_card_with_suit(cards, self.settings.sorted_suit_list[0])

    def _count_cards_without_jacks(self, cards):
        multi = 0
        for suit in self.settings.sorted_suit_list[1:]:
            if not self.has_card_with_suit(cards, suit):
                multi += 1
            else:
                break
        return multi

    def _count_cards_with_jacks(self, cards):
        multi = 0
        for suit in self.settings.sorted_suit_list[1:]:
            if self.has_card_with_suit(cards, suit):
                multi += 1
            else:
                break
        return multi

    @staticmethod
    def has_card_with_suit(cards, suit):
        for card in cards:
            if card.suit_str == suit:
                return True
        return False

    def start_new_round(self):
        self.set_card_default_values()
        self.players.reset()
        self.give_cards()

    def set_card_default_values(self):
        Card.value_dict = self.settings.value_dict
        Card.suit_dict = self.settings.suit_dict
        Card.order_dict = self.settings.standart_order_dict
        Card.trumpf = self.get_clubs_string()

    def give_cards(self):
        cards = Cards(self.settings)
        cards.create_shuffled_cards()
        for i, player in enumerate(self.players):
            player.cards = Cards(self.settings, cards.cards[10*i:10*(i+1)])
            player.cards.sort_cards()

        self.skat = Cards(self.settings, cards.cards[-2:])

    def get_clubs_string(self):
        for tup in self.settings.suit_dict.items():
            if tup[1] == 12:
                return tup[0]
        raise Exception("No Clubs found")
