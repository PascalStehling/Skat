import sys
sys.path.insert(0, r"C:/Users/Pascal/Desktop/Skat")

from modules.play_round import same_suit_or_trumpf
from modules.card import Card
import unittest

class Test_same_suit_or_trumpf(unittest.TestCase):

    value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'B': 2, 'D': 3, 'K': 4, 'A': 11}
    suit_dict = {"Kr": 12, "P": 11, "H": 10, "Ka": 9}

    a = Card("7", 'Kr', value_dict, suit_dict)
    b = Card("B", 'Kr', value_dict, suit_dict)
    c = Card("7", 'H', value_dict, suit_dict)
    d = Card("B", 'H', value_dict, suit_dict)
    e = Card("9", 'Kr', value_dict, suit_dict)

    def test_cards_are_equal(self): # 2 Cards have the same Suit and none is a Jack
        self.assertTrue(same_suit_or_trumpf(self.a,self.e, "P",self.suit_dict))

    def test_cards_not_equal_no_trumpf(self): # 2 Cards dont have the same Suit and there is no trumpf
        self.assertFalse(same_suit_or_trumpf(self.a,self.c,None, self.suit_dict))

    def test_cards_are_equal_no_trumpf_card_jack(self): # 2 Cards have the same Suit and there is no trumpf and one is JAck and one is a normal card
        self.assertTrue(same_suit_or_trumpf(self.a,self.b,None, self.suit_dict))

    def test_cards_not_equal_trumpf_kr_cards(self): # 2 Cards dont have the same suit and trumpf is Kr and both cards are normal cards
        self.assertFalse(same_suit_or_trumpf(self.a,self.c,"Kr", self.suit_dict))

    def test_cards_not_equal_trumpf_kr_jack(self): # 2 Cards dont have the same suit and trumpf is Kr and one card is a jack
        self.assertFalse(same_suit_or_trumpf(self.b,self.c,"Kr", self.suit_dict))

    def test_cards_are_equal_trumpf_kr_card_jack(self): # 2 Cards dont have the same suit and trumpf is Kr and one card is a suit Kr and the other one is a jack
        self.assertTrue(same_suit_or_trumpf(self.a,self.d,"Kr", self.suit_dict))

    def test_cards_are_equal_trumpf_kr_jack_jack(self): # 2 Cards dont have the same suit and trumpf is Kr and both are jacks
        self.assertTrue(same_suit_or_trumpf(self.b,self.d,"Kr", self.suit_dict))

    def test_cards_are_equal_trumpf_J_jack_jack(self): # 2 Cards dont have the same suit and trumpf is Jack and both are jacks
        self.assertTrue(same_suit_or_trumpf(self.b,self.d,"B", self.suit_dict))

    def test_cards_are_equal_trumpf_J_card_jack(self): # 2 Cards dont have the same suit and trumpf is Jack and only one is Jack
        self.assertFalse(same_suit_or_trumpf(self.b,self.c,"B", self.suit_dict))


if __name__ == "__main__":
    unittest.main()