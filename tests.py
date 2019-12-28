
from tests import player_test, settingContainer_test, Players_test, bidding_test, card_test
import unittest

test_classes = [player_test, settingContainer_test, Players_test, bidding_test, card_test]

suit_list = []
loader = unittest.TestLoader()
for test in test_classes:
    suit = loader.loadTestsFromModule(test)
    suit_list.append(suit)


unittest.TextTestRunner(verbosity=1).run(unittest.TestSuite(suit_list))