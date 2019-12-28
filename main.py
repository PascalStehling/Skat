"""
This is the main File with starts the skat App
"""
from modules.Bidding import Bidding
from modules.Round import Round
from modules.SettingContainer import SettingContainer
from modules.Players import Players
from modules.Card import Card

class StateMachine:

    def __init__(self, **settings):
        self.game_round = 1
        self.max_rounds = settings.get("max_rounds", 36)
        self.gamestate = 1
        self.settings = SettingContainer.create_SettingContainer_from_file(settings.get("language"))
        self.players = Players(self.settings, kwargs=settings)

    def run(self):
        while self.game_round <= self.max_rounds:
            if self.gamestate == self.settings.START_ROUND:
                self.round = Round(self.players, self.settings)
                self.gamestate = self.round.start_bidding()
            elif self.gamestate == self.settings.PLAY_ROUND:
                self.round.setup().play_round().end_round()
                self.gamestate = self.settings.START_ROUND
                self.game_round += 1
            

if __name__ == "__main__":
    s = StateMachine(language='de', max_rounds=2, auto_play_cards=True)
    s.run()
