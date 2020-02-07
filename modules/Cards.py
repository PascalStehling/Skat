#pylint: disable=line-too-long
"""This File contains the Cards object. This is a container CLass for Multible Card Objects
"""
from itertools import product
from random import shuffle
from modules.Card import Card


class Cards():
    """Creates a Cards object, which is a container for multible Card objects. It has functions to manipulate multible Card objects.
    """
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
        """Creates 32 cards and returns them shuffled
        """
        # cartesian Product to get all possible card values
        card_nums = product(self.settings.value_dict.keys(),
                            self.settings.suit_dict.keys())
        self.cards = [Card(card[0], card[1]) for card in card_nums]
        shuffle(self.cards)

    def sort_cards(self):
        """Sorts all Card objects with a simple Bubble sort. There can only be 12 Cards at your Hand,
        so Performance isnt that important
        """
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
        """Prints all Card objects as Ascii-Art in the Terminal.

        Args:
            card_delimiter (str, optional): The Symbols which are used between 2 Cards. Defaults to ":".
        """
        for i in range(len(self.cards[0].get_ascii_card())):
            pr_str = ""
            for c in self.cards:
                pr_str += c.get_ascii_card()[i]+card_delimiter
            print(pr_str[:-1])

    def index(self, card):
        """Reeturns the Index of the Card in the list of all Cards

        Args:
            card (Card): The Card, where the Index should be found

        Returns:
            int: The index of the Card in the Cards Object list of all Cards
        """
        return self.cards.index(card)

    def remove(self, card_to_remove):
        """Remove a Card from the List

        Args:
            card_to_remove (Card): The Card the should be removed
        """
        self.cards.remove(card_to_remove)

    def add_card_and_sort(self, card):
        """Add a new Card to the List and sort the List afterwards

        Args:
            card (Card): The new Card the should be Added
        """
        self.add_card(card)
        self.sort_cards()

    def add_card(self, card):
        """Add a new Card to the Cards object

        Args:
            card (Card): The Card that should be added
        """
        self.cards.append(card)

    def empty_cards(self):
        """Remove all Cards from the Cards Object
        """
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

    def get_jacks(self):
        """Get all Jacks from the Cards Object

        Returns:
            List: A List with all Jack Card objects
        """
        return [card for card in self.cards if card.card_points == 2]
