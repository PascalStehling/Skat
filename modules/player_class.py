
class Player():

    player_count = 0
    def __init__(self, player_name, **settings):

        self.name = player_name
        self.num = self.player_count
        self.position = self.player_count
        Player.player_count += 1

        self.cards = []
        self.score = 0
        self.auto_play = settings["settings"].get("auto_play_cards", False)

    def __eq__(self, other_player):
        return self.num == other_player.num

    def __repr__(self):
        return f"{self.num}: {self.name}"

    def has_cards(self):
        return bool(self.cards)


class Players():

    def __init__(self, **settings):
        player_name_list = settings.get("player_names", ["Player 1", "Player 2", "Player 3"])
        self.players = [Player(name, settings=settings["settings"]) for name in player_name_list]

        self.forhand = self.players[0]
        self.middlehand = self.players[1]
        self.backhand = self.players[2]

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