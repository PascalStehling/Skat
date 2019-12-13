from classes.cards import Cards
from classes.bidding_class import Bidding
from classes.tools import get_user_true_false, user_select_card
from classes.card import Card

class Round():

    def __init__(self, players, settingContainer):
        self.players = players
        self.settings = settingContainer
        self.skat = []
        self.single_player_stack = []
        self.jack_multiplicator = None
        self.cards_on_table = []
        self.gamemode = None
        self.turn = self.players.middlehand
        self.bidding = None
        self.order_dict = None

        Card.set_value_dict(Card, self.settings.value_dict)
        Card.set_suit_dict(Card, self.settings.suit_dict)
        Card.set_order_dict(Card, self.settings.standart_order_dict)
        Card.set_trumpf(Card, self.get_clubs_string())

        self.give_cards()

    def give_cards(self):
        cards = Cards(self.settings)
        for i, player in enumerate(self.players):
            player.cards = Cards(self.settings, cards.cards[10*i:10*(i+1)])
            player.cards.sort_cards()

        self.skat = Cards(self.settings, cards.cards[-2:])

    def get_clubs_string(self):
        for tup in self.settings.suit_dict.items():
            if tup[1] == 12:
                return tup[0]
        raise Exception("No Clubs found")

    def start_bidding(self):
        bidding = Bidding(self.settings)
        while True:
            bidding.make_bid(self.turn)
            if bidding.is_end_bidding():
                self.turn, gamestate = bidding.end_bidding(self.players.forhand)
                return gamestate
            self.turn = bidding.get_new_turn(self.turn, self.players)

    def single_player_setup(self):
        show_message = self.settings.skatmessage.format(self.turn.name)
        error_message = self.settings.yesno_errormessage.format(self.turn.name)
        if get_user_true_false(show_message, error_message, self.turn.cards):
            show_message = self.settings.cardmessage.format(self.turn.name)
            error_message = self.settings.card_errormessage.format(self.turn.name)
            self.turn.cards += self.skat
            self.skat.empty_cards()
            self.turn.cards.sort_cards()

            for _ in range(2):
                self.turn.cards, skat_card = user_select_card(show_message, error_message, self.turn.cards)
                self.skat.add_card_and_sort(skat_card)

        show_message = self.settings.gamemode_message.format(self.turn.name)
        error_message = self.settings.gamemode_errormessage.format(self.turn.name)
        self.gamemode = self.get_play_type(show_message, error_message, self.turn.cards)
        Card.set_order_dict(Card,self.settings.order_dicts[self.gamemode.get("order_dict")])
        Card.set_trumpf(Card,self.gamemode.get("trumpf"))

        self.jack_multiplicator = self.get_jack_multiplicator(self.turn.cards)

        for player in self.players:
            player.cards.sort_cards()

        self.turn = self.players.forhand
    
    def get_play_type(self, show_message, error_message, user_cards):
        user_cards.print_cards_ascii()
        print(show_message)
        for key in self.settings.gamemode_dict:
            print(f"{key}: {self.settings.gamemode_dict[key]['name']}")

        inp = input()
        if inp in self.settings.gamemode_dict:
            return self.settings.gamemode_dict[inp]
        else:
            print(error_message)
            return self.get_play_type(show_message, error_message, user_cards)

    def get_jack_multiplicator(self, cards):
        """
        Get the jack multiplicator for the play
        """
        if not isinstance(cards, Cards):
            raise TypeError("table_cards need to be of Type List")
        if not all([isinstance(card, Card) for card in cards]):
            raise ValueError("Table Cards should only contain Cards")

        jacks = [card for card in cards if card.card_points == 2]
        if len(jacks) == 4 or len(jacks) == 0:
            return 5
        
        suit_list = [x[0] for x in sorted(self.settings.suit_dict.items(), key=lambda x: x[1], reverse=True)]
        jack_name = [x[0] for x in self.settings.value_dict.items() if x[1] == 2][0]
        multi = 2
        if self.has_card_with_suit(jacks, suit_list[0]):
            for suit in suit_list[1:]:
                if self.has_card_with_suit(jacks, suit):
                    multi += 1
                else:
                    break
        else:
            for suit in suit_list[1:]:
                if not has_card_with_suit(jacks, suit):
                    multi += 1
                else:
                    break
        return multi

    def has_card_with_suit(self, cards, suit):
        if not isinstance(cards, list):
            raise TypeError("table_cards need to be of Type List")
        if not all([isinstance(card, Card) for card in cards]):
            raise ValueError("Table Cards should only contain Cards")
        if not isinstance(suit, str):
            raise TypeError("Suit needs to be of Type String")

        for card in cards:
            if card.suit_str == suit:
                return True
        return False
