from modules.Cards import Cards
from modules.Player import Player
class Players():

    def __init__(self, settingContainer, **kwargs):
        player_name_list = kwargs.get("player_names", ["Player 1", "Player 2", "Player 3"])
        self.players = [Player(name, settings=kwargs["kwargs"]) for name in player_name_list]

        self.forhand = self.players[0]
        self.middlehand = self.players[1]
        self.backhand = self.players[2]

        self.settings = settingContainer

    def __iter__(self):
        return iter(self.players)

    def get_next_player(self, player):
        index = self.players.index(player)
        index = (index+1)%3
        return self.players[index]

    def players_on_next_position(self):
        tmp = self.forhand
        self.forhand = self.middlehand
        self.middlehand = self.backhand
        self.backhand = tmp

    def get_player_by_num(self, num):
        for player in self.players:
            if player.num == num:
                return player
        raise Exception("No Player with this num")

    def sort_cards(self):
        for player in self.players:
            player.cards.sort_cards()

    def reset(self):
        for player in self.players:
            player.won_cards = Cards(self.settings)
            player.cards = Cards(self.settings)