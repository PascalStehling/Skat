    
import unittest
import sys

sys.path.append('../')
from modules import card
from modules.tools import print_multiple_cards, sort_cards
from random import sample


class Test_tools(unittest.TestCase):

    value_dict = {'7': 0, '8': 0, '9': 0, '10': 10, 'B': 2, 'D': 3, 'K': 4, 'A': 11}
    suit_dict = {"Kr": 12, "P": 11, "H": 10, "Ka": 9}
    standart_order_dict = {'7': 0, '8': 1, '9': 2, '10': 5, 'B': 7, 'D': 3, 'K': 4, 'A': 6}

    def test_print_multiple_cards_type(self):
        c1 = card.Card('7', 'Kr', self.value_dict, self.suit_dict)
        c2 = card.Card('K', 'H', self.value_dict, self.suit_dict)
        c3 = card.Card('A', 'P', self.value_dict, self.suit_dict)
        c4 = card.Card('10', 'Ka', self.value_dict, self.suit_dict)
        cards = [c1,c2,c3,c4]
        with self.assertRaises(TypeError):
            print_multiple_cards("cards")
        with self.assertRaises(TypeError):
            print_multiple_cards(cards+["asd"])

        print()
        print_multiple_cards(cards) # Test if its looks right

    def create_sorted_list(self, order_dict, trumpf):
        sort_value_list = [x[0] for x in sorted(order_dict.items(), key=lambda x:x[1], reverse=True)]
        del sort_value_list[0]
        sort_suit_list = [x[0] for x in sorted(self.suit_dict.items(), key=lambda x:x[1], reverse=True)]
        
        # At the beginning allways the Jacks
        sort_card_list = [card.Card('B', suit, self.value_dict, self.suit_dict) for suit in sort_suit_list]
        
        # Add the Trumpf Cards
        for val in sort_value_list:
            sort_card_list.append(card.Card(val, trumpf, self.value_dict, self.suit_dict))

        # Add the other Cards from Top to Bottom without Trumpf
        for suit in sort_suit_list:
            if suit != trumpf:
                for val in sort_value_list:
                    sort_card_list.append(card.Card(val, suit, self.value_dict, self.suit_dict))
        return sort_card_list


    def test_sort_cards(self):
        sort_list_kr = self.create_sorted_list(self.standart_order_dict, "Kr")
        sort_list_p = self.create_sorted_list(self.standart_order_dict, "P")
        sort_list_h = self.create_sorted_list(self.standart_order_dict, "H")
        sort_list_ka = self.create_sorted_list(self.standart_order_dict, "Ka")

        with self.assertRaises(TypeError):
            sort_cards("a", self.standart_order_dict, "Kr")
        with self.assertRaises(TypeError):
            sort_cards(sort_list_h, "self.standart_order_dict", "Kr")
        with self.assertRaises(TypeError):
            sort_cards(sort_list_h, self.standart_order_dict, 1)

        self.assertListEqual(sort_list_kr, sort_cards(sort_list_kr[::-1], self.standart_order_dict, "Kr"))
        self.assertListEqual(sort_list_p, sort_cards(sort_list_p[::-1], self.standart_order_dict, "P"))
        self.assertListEqual(sort_list_h, sort_cards(sort_list_h[::-1], self.standart_order_dict, "H"))
        self.assertListEqual(sort_list_ka, sort_cards(sort_list_ka[::-1], self.standart_order_dict, "Ka"))

if __name__ == "__main__":
    unittest.main()