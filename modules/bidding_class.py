from classes.tools import get_user_true_false

class Bidding():

    def __init__(self):
        self.bid = None
        self.bid_player = None
        self.passed = []
        self.next_bid = 18