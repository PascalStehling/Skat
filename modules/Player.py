class Player():

    player_count = 0
    def __init__(self, player_name, **settings):

        self.name = player_name
        self.num = self.player_count
        self.position = self.player_count
        Player.player_count += 1

        self.cards = None
        self.score = 0
        self.auto_play = settings["settings"].get("auto_play_cards", False)
        self.won_cards = None

    def __eq__(self, other_player):
        return self.num == other_player.num

    def __repr__(self):
        return f"{self.num}: {self.name}"

    def has_cards(self):
        return bool(self.cards)