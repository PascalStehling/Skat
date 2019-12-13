from modules.card import Card
from itertools import product
from random import shuffle


class Cards():

    def __init__(self, settingContainer, cards=None):
        self.settings = settingContainer
        if cards:
            self.cards = cards
        else:
            self.cards = self.create_shuffled_cards()

    def create_shuffled_cards(self):
        """ 
        Creates 32 cards and returns them shuffled
        """
        card_nums = product(self.settings.value_dict.keys(), self.settings.suit_dict.keys()) # cartesian Product to get all possible card values
        cards = [Card(card[0], card[1], self.settings.value_dict,  self.settings.suit_dict) for card in card_nums]
        shuffle(cards)
        return cards

    def sort_cards(self, order_dict, trumpf):
        i = 0
        while i < len(self.cards)-1:
            k = 0
            while k < len(self.cards)-i-1:
                if not self.cards[k].ishigher(self.cards[k+1], trumpf, order_dict, True):
                    tmp = self.cards[k]
                    self.cards[k] = self.cards[k+1]
                    self.cards[k+1] = tmp
                k += 1
            i += 1

    def print_cards_ascii(self, card_delimiter=":"):        
        for i in range(len(self.cards[0].get_ascii_card())):
            pr_str = ""
            for c in self.cards:
                pr_str += c.get_ascii_card()[i]+card_delimiter
            print(pr_str[:-1])