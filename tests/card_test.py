import unittest
import sys

sys.path.append('../')
from modules.Card import Card

class Test_card(unittest.TestCase):

    value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'B': 2, 'D': 3, 'K': 4, 'A': 11}
    suit_dict = {"Kr": 12, "P": 11, "H": 10, "Ka": 9}
    order_dict = {'7': 0, '8': 1, '9': 2, '10': 5, 'B': 7, 'D': 3, 'K': 4, 'A': 6}

    Card.value_dict = value_dict
    Card.suit_dict = suit_dict
    Card.order_dict = order_dict
    def test_init(self):
        with self.assertRaises(TypeError):
            Card(7, 'Kr')

        with self.assertRaises(TypeError):
            Card('7', 23)

        with self.assertRaises(TypeError):
            Card.value_dict = []
            Card('7', 'Kr')

        Card.value_dict = self.value_dict

        with self.assertRaises(TypeError):
            Card.suit_dict = []
            Card('7', 'Kr')
        Card.suit_dict = self.suit_dict
        
        with self.assertRaises(ValueError):
            Card('5', 'Kr')

        with self.assertRaises(ValueError):
            Card('7', '23')
        

    def test_equal_suit_test(self):
        a = Card("7", 'Kr')
        b = Card("7", 'H')
        c = Card("8", 'Kr')

        self.assertTrue(a.equal_suit(c))
        with self.assertRaises(TypeError):
            a.equal_suit("a")
        self.assertFalse(a.equal_suit(b))

    def test_istrumpf(self):
        a = Card("7", 'Kr')
        b = Card("B", 'H')

        Card.trumpf = 1
        with self.assertRaises(TypeError):
            a.istrumpf()
        
        Card.trumpf = "Kr"
        self.assertTrue(a.istrumpf())
        Card.trumpf = "H"
        self.assertTrue(b.istrumpf())
        Card.trumpf = "Kr"
        self.assertTrue(b.istrumpf())
        Card.trumpf = "H"
        self.assertFalse(a.istrumpf())
        Card.trumpf = None
        self.assertFalse(a.istrumpf())

    def test_has_higher_value(self):
        a = Card("B", 'Kr')
        b = Card("B", 'H')

        self.assertTrue(a.has_higher_suit_val(b))
        self.assertFalse(b.has_higher_suit_val(a))

    def test_ishigher_both_trump_self_is_jack(self):
        a = Card("B", 'Kr')
        b = Card("B", 'H')
        c = Card("D", 'H')

        self.assertTrue(a._ishigher_both_trump_self_is_jack(c))
        self.assertFalse(b._ishigher_both_trump_self_is_jack(a))

    def test_ishigher_both_trump_self_not_jack(self):
        a = Card("D", 'Kr')
        b = Card("K", 'Kr')

        self.assertFalse(a._ishigher_both_trump_self_not_jack(b))
        self.assertTrue(b._ishigher_both_trump_self_not_jack(a))

    def test_ishigher_both_trumpf(self):
        a = Card("B", 'Kr')
        b = Card("K", 'Kr')

        self.assertTrue(a._ishigher_both_trumpf(b))
        self.assertFalse(b._ishigher_both_trumpf(a))

    def test_ishigher_no_trumpf(self):
        a = Card("D", 'Kr')
        b = Card("K", 'H')

        self.assertTrue(a._ishigher_no_trumpf(b))
        self.assertFalse(b._ishigher_no_trumpf(a, check_suit_val=True))
        self.assertTrue(a._ishigher_no_trumpf(b, check_suit_val=True))

    def test_ishigher_self_is_trumpf(self):
        a = Card("D", 'Kr')
        b = Card("K", 'H')
        c = Card("K", 'Kr')

        self.assertTrue(a._ishigher_self_is_trumpf(b))
        self.assertFalse(a._ishigher_self_is_trumpf(c))

    def test_ishigher_self_not_trumpf(self):
        a = Card("D", 'Kr')
        b = Card("K", 'H')
        c = Card("K", 'Kr')

        Card.trumpf = "H"
        self.assertFalse(a._ishigher_self_not_trumpf(b))
        Card.trumpf = "P"
        self.assertTrue(a._ishigher_self_not_trumpf(b))
        self.assertFalse(a._ishigher_self_not_trumpf(c))


    def test_ishigher(self):
        a = Card("7", 'Kr')
        b = Card("8", 'Kr')
        c = Card("8", 'H')
        d = Card("B", 'H')
        e = Card("B", 'Kr')

        with self.assertRaises(TypeError):
            a.ishigher(1)

        Card.trumpf = "H"
        self.assertTrue(b.ishigher(a)) # 2 Cards not Trumpf
        Card.trumpf = "P"
        self.assertTrue(b.ishigher(c)) # 2 Cards not Trumpf
        self.assertFalse(a.ishigher(b)) # 2 Cards not Trumpf

        self.assertTrue(b.ishigher(c, True)) # 2 Cards not Trumpf, suit_val check
        self.assertFalse(c.ishigher(b, True)) # 2 Cards not Trumpf, suit_val check

        self.assertTrue(d.ishigher(b, True)) # Jack and not Trumpf, suit_val check
        self.assertFalse(b.ishigher(d, True)) # not Trumpf and Jack, suit_val check

        self.assertTrue(d.ishigher(a))
        self.assertFalse(a.ishigher(d))

        self.assertTrue(e.ishigher(d))
        self.assertFalse(d.ishigher(e))

        Card.trumpf = "Kr"
        self.assertTrue(d.ishigher(a))
        self.assertFalse(a.ishigher(d))

        self.assertTrue(b.ishigher(a)) # 2 Cards Trumpf
        self.assertFalse(a.ishigher(b)) # 2 Cards Trumpf

        self.assertTrue(b.ishigher(a)) # 2 Cards Trumpf

    def test_has_higher_value(self):
        a = Card("7", 'Kr')
        b = Card("8", 'Kr')
        
        self.assertFalse(a.has_higher_value(b))
        self.assertTrue(b.has_higher_value(a))

if __name__ == "__main__":
    unittest.main()