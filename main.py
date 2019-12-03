"""
This is the main File with starts the skat App
"""
from modules.setup_round import setup_round
from modules.bidding import make_bid
from modules.setup_single_play import setup_single_play
from modules.create_settings import create_game_dict
from modules.play_round import play_card_user
from modules.end_round import end_round

class StateMachine:

    def __init__(self, player_names=None, max_rounds=36, language='en'):
        self.game_dict = create_game_dict(player_names, max_rounds, language)
        self.fun_dict = {1: setup_round, 2:make_bid, 3:setup_single_play, 4:play_card_user, 5:end_round}

    def run(self):
        while self.game_dict["game_round"] <= self.game_dict["max_round"]:
            state_fun = self.fun_dict[self.game_dict["gamestate"]]
            self.game_dict = state_fun(self.game_dict)
            

if __name__ == "__main__":
    s = StateMachine(language='de', max_rounds=2)
    s.run()
