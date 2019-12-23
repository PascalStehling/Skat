"""
This is the main File with starts the skat App
"""
from modules.setup_round import start_new_round
from modules.bidding_class import Bidding
from modules.round_class import Round
from modules.setup_single_play import setup_single_play
from modules.create_settings import create_game_objects
from modules.play_round import play_card_user
from modules.card import Card

class StateMachine:

    def __init__(self, **settings):
        self.game_round = 1
        self.max_rounds = settings.get("max_rounds", 36)
        self.gamestate = 1
        self.players, self.settings = create_game_objects(settings)
        self.bidding = None
        self.skat = None
        self.turn = None

    def run(self):
        while self.game_round <= self.max_rounds:
            if self.gamestate == 1:
                self.players, self.skat = start_new_round(self.players, self.settings)
                self.bidding = Bidding(self.settings, self.players)
                self.turn, self.gamestate = self.bidding.play_bidding()
            elif self.gamestate == 3:
                gamemode, jack_multiplicator, self.skat = setup_single_play(self.turn,self.skat, self.settings)
                self.round = Round(self.players, self.settings, self.bidding, jack_multiplicator, gamemode)
                self.round.play_round()
                self.round.end_round()
                self.gamestate = 1
                self.max_rounds += 1
            

if __name__ == "__main__":
    s = StateMachine(language='de', max_rounds=2, auto_play_cards=True)
    s.run()
