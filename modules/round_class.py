from modules.card import Card
from modules.cards import Cards
from modules.bidding_class import Bidding

class Round():

    def __init__(self, players, settingContainer, skat=None):
        self.skat = skat
        self.jack_multiplicator = None
        self.gamemode = None
        self.turn = players.middlehand
        self.bidding = Bidding()
        self.single_player_stack = Cards(settingContainer)
        self.cards_on_table = Cards(settingContainer)

        Card.value_dict = settingContainer.value_dict
        Card.suit_dict = settingContainer.suit_dict
        Card.order_dict = settingContainer.standart_order_dict
        Card.trumpf = self.get_clubs_string(settingContainer)

    def get_clubs_string(self, settings):
        for tup in settings.suit_dict.items():
            if tup[1] == 12:
                return tup[0]
        raise Exception("No Clubs found")