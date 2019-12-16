"""
This is the main File with starts the skat App
"""
from modules.setup_round import setup_round
from modules.bidding import make_bid
from modules.setup_single_play import setup_single_play
from modules.create_settings import create_game_objects
from modules.play_round import play_card_user
#from modules.end_round import end_round

class StateMachine:

    def __init__(self, **settings):
        self.game_round = 1
        self.max_rounds = settings.get("max_rounds", 36)
        self.gamestate = 1
        self.round = None
        self.players, self.settings = create_game_objects(settings)

        # self.fun_dict = {1: setup_round, 2:make_bid, 3:setup_single_play, 4:play_card_user, 5:end_round}

    def run(self):
        while self.game_round <= self.max_rounds:
            if self.gamestate == 1:
                self.round, self.players = setup_round(self.players, self.settings)
                self.gamestate += 1
            elif self.gamestate == 2:
                self.round, self.gamestate = make_bid(self.round, self.settings, self.players)
            elif self.gamestate == 3:
                self.round = setup_single_play(self.round, self.settings, self.players)
                self.gamestate += 1
            elif self.gamestate == 4:
                self.round, self.gamestate = play_card_user(self.round, self.settings, self.players)
            

if __name__ == "__main__":
    s = StateMachine(language='de', max_rounds=2)
    s.run()
