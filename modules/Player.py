
class Player():

    player_count = 0
    def __init__(self, player_name, **settings):
        settings = settings.get("settings", settings)
        if not isinstance(player_name, str):
            raise TypeError("player_name need to be a string")
        self.name = player_name
        self.num = self.player_count
        self.position = self.player_count
        Player.player_count += 1

        self.cards = None
        self.score = 0
        self.auto_play = settings.get("auto_play_cards", False)
        self.won_cards = None

    def __eq__(self, other_player):
        if not isinstance(other_player, Player):
            raise TypeError("other_player needs to be of Type Player")
        return self.num == other_player.num

    def __repr__(self):
        return f"{self.num}: {self.name}"

    def has_cards(self):
        return bool(self.cards)