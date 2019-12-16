from modules.card import Card
from itertools import product
from random import shuffle


class Cards():

    def __init__(self, settingContainer, cards=None):
        self.settings = settingContainer
        if cards:
            self.cards = cards
        else:
            self.cards = []

    def __add__(self, other_cards):
        self.cards += other_cards.cards
        self.sort_cards()
        return self

    def create_shuffled_cards(self):
        """ 
        Creates 32 cards and returns them shuffled
        """
        card_nums = product(self.settings.value_dict.keys(), self.settings.suit_dict.keys()) # cartesian Product to get all possible card values
        self.cards = [Card(card[0], card[1]) for card in card_nums]
        shuffle(self.cards)

    def sort_cards(self):
        i = 0
        while i < len(self.cards)-1:
            k = 0
            while k < len(self.cards)-i-1:
                if not self.cards[k].ishigher(self.cards[k+1], True):
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

    def index(self, card):
        return self.cards.index(card)

    def remove(self, card_to_remove):
        self.cards.remove(card_to_remove)

    def add_card_and_sort(self, card):
        self.add_card(card)
        self.sort_cards()

    def add_card(self, card):
        self.cards.append(card)

    def empty_cards(self):
        self.cards = []

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, indieces):
        return self.cards[indieces]

    def __repr__(self):
        self.print_cards_ascii()
        return ""