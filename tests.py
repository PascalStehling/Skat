
from tests import bidding_test, card_test, main_test, play_round_test,tools_test, end_round_test
import unittest

test_classes = [bidding_test, card_test, main_test, play_round_test, tools_test, end_round_test]

suit_list = []
loader = unittest.TestLoader()
for test in test_classes:
    suit = loader.loadTestsFromModule(test)
    suit_list.append(suit)


unittest.TextTestRunner(verbosity=1).run(unittest.TestSuite(suit_list))