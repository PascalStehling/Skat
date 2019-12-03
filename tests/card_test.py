import unittest
import sys

sys.path.insert(0, r"C:/Users/Pascal/Desktop/Skat")
from modules import card

class Test_card(unittest.TestCase):

    value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'B': 2, 'D': 3, 'K': 4, 'A': 11}
    suit_dict = {"Kr": 12, "P": 11, "H": 10, "Ka": 9}

    def test_card_wrong_input_types(self):
        with self.assertRaises(TypeError):
            c = card.Card(7, 'Kr', self.value_dict, self.suit_dict)

        with self.assertRaises(TypeError):
            c = card.Card('7', 23, self.value_dict, self.suit_dict)

        with self.assertRaises(TypeError):
            c = card.Card('7', 'Kr', [], self.suit_dict)

        with self.assertRaises(TypeError):
            c = card.Card('7', 'Kr', self.value_dict, [])

    def test_card_wrong_input_values(self):
        with self.assertRaises(ValueError):
            c = card.Card('5', 'Kr', self.value_dict, self.suit_dict)

        with self.assertRaises(ValueError):
            c = card.Card('7', '23', self.value_dict, self.suit_dict)

    def equal_suit_test(self):
        a = card.Card("7", 'Kr', self.value_dict, self.suit_dict)
        b = card.Card("7", 'H', self.value_dict, self.suit_dict)
        c = card.Card("8", 'Kr', self.value_dict, self.suit_dict)

        self.assertTrue(a.equal_suit(c))
        with self.assertRaises(TypeError):
            a.equal_suit("a")
        self.assertFalse(a.equal_suit(b))

    def test_istrumpf(self):
        a = card.Card("7", 'Kr', self.value_dict, self.suit_dict)
        b = card.Card("B", 'H', self.value_dict, self.suit_dict)

        with self.assertRaises(TypeError):
            a.istrumpf(1)
        
        self.assertTrue(a.istrumpf("Kr"))
        self.assertTrue(b.istrumpf("H"))
        self.assertTrue(b.istrumpf("Kr"))
        self.assertFalse(a.istrumpf("H"))
        self.assertFalse(a.istrumpf(None))

    def test_ishigher(self):
        a = card.Card("7", 'Kr', self.value_dict, self.suit_dict)
        b = card.Card("8", 'Kr', self.value_dict, self.suit_dict)
        c = card.Card("8", 'H', self.value_dict, self.suit_dict)
        d = card.Card("B", 'H', self.value_dict, self.suit_dict)
        e = card.Card("B", 'Kr', self.value_dict, self.suit_dict)

        order_dict = {'7': 0, '8': 1, '9': 2, '10': 5, 'J': 7, 'Q': 3, 'K': 4, 'A': 6}

        with self.assertRaises(TypeError):
            a.ishigher(1, "Kr", order_dict)
        with self.assertRaises(TypeError):
            a.ishigher(b, 2, order_dict)
        with self.assertRaises(TypeError):
            a.ishigher(b, "Kr", 2)

        self.assertTrue(b.ishigher(a, "H", order_dict)) # 2 Cards not Trumpf
        self.assertTrue(b.ishigher(c, "P", order_dict)) # 2 Cards not Trumpf
        self.assertFalse(a.ishigher(b, "P", order_dict)) # 2 Cards not Trumpf

        self.assertTrue(b.ishigher(c, "P", order_dict, True)) # 2 Cards not Trumpf, suit_val check
        self.assertFalse(c.ishigher(b, "P", order_dict, True)) # 2 Cards not Trumpf, suit_val check

        self.assertTrue(d.ishigher(b, "P", order_dict, True)) # Jack and not Trumpf, suit_val check
        self.assertFalse(b.ishigher(d, "P", order_dict, True)) # not Trumpf and Jack, suit_val check

        self.assertTrue(d.ishigher(a, "P", order_dict))
        self.assertFalse(a.ishigher(d, "P", order_dict))

        self.assertTrue(d.ishigher(a, "Kr", order_dict))
        self.assertFalse(a.ishigher(d, "Kr", order_dict))

        self.assertTrue(e.ishigher(d, "P", order_dict))
        self.assertFalse(d.ishigher(e, "P", order_dict))

        self.assertTrue(b.ishigher(a, "Kr", order_dict)) # 2 Cards Trumpf
        self.assertFalse(a.ishigher(b, "Kr", order_dict)) # 2 Cards Trumpf

        self.assertTrue(b.ishigher(a, "Kr", order_dict)) # 2 Cards Trumpf

    def test_has_higher_value(self):
        a = card.Card("7", 'Kr', self.value_dict, self.suit_dict)
        b = card.Card("8", 'Kr', self.value_dict, self.suit_dict)
        order_dict = {'7': 0, '8': 1, '9': 2, '10': 5, 'J': 7, 'Q': 3, 'K': 4, 'A': 6}

        with self.assertRaises(TypeError):
            a.has_higher_value("a", order_dict)
        with self.assertRaises(TypeError):
            a.has_higher_value(b, "order_dict")
        
        self.assertFalse(a.has_higher_value(b, order_dict))
        self.assertTrue(b.has_higher_value(a, order_dict))