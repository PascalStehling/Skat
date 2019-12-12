import unittest
import sys

sys.path.insert(0, r"C:/Users/Pascal/Desktop/Skat")
from modules.card import *

class Test_card(unittest.TestCase):

    value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'B': 2, 'D': 3, 'K': 4, 'A': 11}
    suit_dict = {"Kr": 12, "P": 11, "H": 10, "Ka": 9}
    order_dict = {'7': 0, '8': 1, '9': 2, '10': 5, 'B': 7, 'D': 3, 'K': 4, 'A': 6}

    def test_init(self):
        with self.assertRaises(TypeError):
            Card(7, 'Kr', self.value_dict, self.suit_dict)

        with self.assertRaises(TypeError):
            Card('7', 23, self.value_dict, self.suit_dict)

        with self.assertRaises(TypeError):
            Card('7', 'Kr', [], self.suit_dict)

        with self.assertRaises(TypeError):
            Card('7', 'Kr', self.value_dict, [])
        
        with self.assertRaises(ValueError):
            Card('5', 'Kr', self.value_dict, self.suit_dict)

        with self.assertRaises(ValueError):
            Card('7', '23', self.value_dict, self.suit_dict)
        

    def test_equal_suit_test(self):
        a = Card("7", 'Kr', self.value_dict, self.suit_dict)
        b = Card("7", 'H', self.value_dict, self.suit_dict)
        c = Card("8", 'Kr', self.value_dict, self.suit_dict)

        self.assertTrue(a.equal_suit(c))
        with self.assertRaises(TypeError):
            a.equal_suit("a")
        self.assertFalse(a.equal_suit(b))

    def test_istrumpf(self):
        a = Card("7", 'Kr', self.value_dict, self.suit_dict)
        b = Card("B", 'H', self.value_dict, self.suit_dict)

        with self.assertRaises(TypeError):
            a.istrumpf(1)
        
        self.assertTrue(a.istrumpf("Kr"))
        self.assertTrue(b.istrumpf("H"))
        self.assertTrue(b.istrumpf("Kr"))
        self.assertFalse(a.istrumpf("H"))
        self.assertFalse(a.istrumpf(None))

    def test_has_higher_value(self):
        a = Card("B", 'Kr', self.value_dict, self.suit_dict)
        b = Card("B", 'H', self.value_dict, self.suit_dict)

        self.assertTrue(a.has_higher_suit_val(b))
        self.assertFalse(b.has_higher_suit_val(a))

    def test_ishigher_both_trump_self_is_jack(self):
        a = Card("B", 'Kr', self.value_dict, self.suit_dict)
        b = Card("B", 'H', self.value_dict, self.suit_dict)
        c = Card("D", 'H', self.value_dict, self.suit_dict)

        self.assertTrue(a._ishigher_both_trump_self_is_jack(c))
        self.assertFalse(b._ishigher_both_trump_self_is_jack(a))

    def test_ishigher_both_trump_self_not_jack(self):
        a = Card("D", 'Kr', self.value_dict, self.suit_dict)
        b = Card("K", 'Kr', self.value_dict, self.suit_dict)

        self.assertFalse(a._ishigher_both_trump_self_not_jack(b, self.order_dict))
        self.assertTrue(b._ishigher_both_trump_self_not_jack(a, self.order_dict))

    def test_ishigher_both_trumpf(self):
        a = Card("B", 'Kr', self.value_dict, self.suit_dict)
        b = Card("K", 'Kr', self.value_dict, self.suit_dict)

        self.assertTrue(a._ishigher_both_trumpf(b, self.order_dict))
        self.assertFalse(b._ishigher_both_trumpf(a, self.order_dict))

    def test_ishigher_no_trumpf(self):
        a = Card("D", 'Kr', self.value_dict, self.suit_dict)
        b = Card("K", 'H', self.value_dict, self.suit_dict)

        self.assertTrue(a._ishigher_no_trumpf(b))
        self.assertFalse(b._ishigher_no_trumpf(a, check_suit_val=True))
        self.assertTrue(a._ishigher_no_trumpf(b, check_suit_val=True))

    def test_ishigher_self_is_trumpf(self):
        a = Card("D", 'Kr', self.value_dict, self.suit_dict)
        b = Card("K", 'H', self.value_dict, self.suit_dict)
        c = Card("K", 'Kr', self.value_dict, self.suit_dict)

        self.assertTrue(a._ishigher_self_is_trumpf(b, False, self.order_dict))
        self.assertFalse(a._ishigher_self_is_trumpf(c, True, self.order_dict))

    def test_ishigher_self_not_trumpf(self):
        a = Card("D", 'Kr', self.value_dict, self.suit_dict)
        b = Card("K", 'H', self.value_dict, self.suit_dict)
        c = Card("K", 'Kr', self.value_dict, self.suit_dict)

        self.assertFalse(a._ishigher_self_not_trumpf(b, True, self.order_dict))
        self.assertTrue(a._ishigher_self_not_trumpf(b, False, self.order_dict))
        self.assertFalse(a._ishigher_self_not_trumpf(c, False, self.order_dict))


    def test_ishigher(self):
        a = Card("7", 'Kr', self.value_dict, self.suit_dict)
        b = Card("8", 'Kr', self.value_dict, self.suit_dict)
        c = Card("8", 'H', self.value_dict, self.suit_dict)
        d = Card("B", 'H', self.value_dict, self.suit_dict)
        e = Card("B", 'Kr', self.value_dict, self.suit_dict)

        with self.assertRaises(TypeError):
            a.ishigher(1, "Kr", self.order_dict)
        with self.assertRaises(TypeError):
            a.ishigher(b, 2, self.order_dict)
        with self.assertRaises(TypeError):
            a.ishigher(b, "Kr", 2)

        self.assertTrue(b.ishigher(a, "H", self.order_dict)) # 2 Cards not Trumpf
        self.assertTrue(b.ishigher(c, "P", self.order_dict)) # 2 Cards not Trumpf
        self.assertFalse(a.ishigher(b, "P", self.order_dict)) # 2 Cards not Trumpf

        self.assertTrue(b.ishigher(c, "P", self.order_dict, True)) # 2 Cards not Trumpf, suit_val check
        self.assertFalse(c.ishigher(b, "P", self.order_dict, True)) # 2 Cards not Trumpf, suit_val check

        self.assertTrue(d.ishigher(b, "P", self.order_dict, True)) # Jack and not Trumpf, suit_val check
        self.assertFalse(b.ishigher(d, "P", self.order_dict, True)) # not Trumpf and Jack, suit_val check

        self.assertTrue(d.ishigher(a, "P", self.order_dict))
        self.assertFalse(a.ishigher(d, "P", self.order_dict))

        self.assertTrue(d.ishigher(a, "Kr", self.order_dict))
        self.assertFalse(a.ishigher(d, "Kr", self.order_dict))

        self.assertTrue(e.ishigher(d, "P", self.order_dict))
        self.assertFalse(d.ishigher(e, "P", self.order_dict))

        self.assertTrue(b.ishigher(a, "Kr", self.order_dict)) # 2 Cards Trumpf
        self.assertFalse(a.ishigher(b, "Kr", self.order_dict)) # 2 Cards Trumpf

        self.assertTrue(b.ishigher(a, "Kr", self.order_dict)) # 2 Cards Trumpf

    def test_has_higher_value(self):
        a = Card("7", 'Kr', self.value_dict, self.suit_dict)
        b = Card("8", 'Kr', self.value_dict, self.suit_dict)
        order_dict = {'7': 0, '8': 1, '9': 2, '10': 5, 'J': 7, 'Q': 3, 'K': 4, 'A': 6}
        
        self.assertFalse(a.has_higher_value(b, order_dict))
        self.assertTrue(b.has_higher_value(a, order_dict))

if __name__ == "__main__":
    unittest.main()