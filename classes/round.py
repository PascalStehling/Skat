from classes.cards import Cards
from classes.bidding_class import Bidding

class Round():

    def __init__(self, players, settingContainer):
        self.players = players
        self.settings = settingContainer
        self.skat = []
        self.single_player_stack = []
        self.jacks_multiplicator = None
        self.cards_on_table = []
        self.gamemode = None
        self.turn = self.players.middlehand
        self.bidding = None
        self.order_dict = None

        self.give_cards()

    def give_cards(self):
        cards = Cards(self.settings)
        for i, player in enumerate(self.players):
            player.cards = Cards(self.settings, cards.cards[10*i:10*(i+1)])
            player.cards.sort_cards(self.settings.standart_order_dict, self.get_clubs_string())

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