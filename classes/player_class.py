
class Player():

    player_count = 0
    def __init__(self, player_name):

        self.name = player_name
        self.num = self.player_count
        self.position = self.player_count
        Player.player_count += 1

        self.cards = []
        self.points = 0

    def __eq__(self, other_player):
        return self.num == other_player.num

    def __repr__(self):
        return f"{self.num}: {self.name}"


class Players():

    def __init__(self, player_name_list):
        self.players = [Player(name) for name in player_name_list]

        self.forhand = self.players[0]
        self.middlehand = self.players[1]
        self.backhand = self.players[2]

    def __iter__(self):
        return iter(self.players)