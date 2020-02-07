#pylint: disable=line-too-long
"""This File contains the Player CLass. which is a container for Player objects
"""
from modules.Cards import Cards
from modules.Player import Player


class Players():
    """The Player Class is an container for multible Player Objects
    """
    NUMBER_OF_PLAYERS = 3

    def __init__(self, settingContainer, **kwargs):
        kwargs = kwargs.get("kwargs", kwargs)
        player_name_list = kwargs.get(
            "player_names", ["Player 1", "Player 2", "Player 3"])
        if len(player_name_list) != self.NUMBER_OF_PLAYERS:
            raise ValueError("There need to be exactly 3 Players")
        self.players = [Player(name, settings=kwargs)
                        for name in player_name_list]

        self.forhand = self.players[0]
        self.middlehand = self.players[1]
        self.backhand = self.players[2]

        self.settings = settingContainer

    def __iter__(self):
        return iter(self.players)

    def get_next_player(self, player):
        """Get the next Player in the List, if the list is at the End, it starts from the beginning

        Args:
            player (Player): The Player at the moment

        Returns:
            Player: the Player, after the Player which was given as input
        """
        index = self.players.index(player)
        index = (index+1) % 3
        return self.players[index]

    def set_players_on_next_position(self):
        """Change the positions of all Players. Forhand --> Middlehand, Middlehand --> Backhand, Backhand --> Forhand
        """
        tmp = self.backhand
        self.backhand = self.middlehand
        self.middlehand = self.forhand
        self.forhand = tmp

    def get_player_by_num(self, num):
        """Get a Player by its num which was assigned when creating a Player object

        Args:
            num (Int): The num of the Player

        Raises:
            Exception: If a Player with this num doesen't exist

        Returns:
            Player: The Player with the corresponding num
        """
        for player in self.players:
            if player.num == num:
                return player
        raise Exception("No Player with this num")

    def sort_cards(self):
        """Sort all Cards of all Players
        """
        for player in self.players:
            player.cards.sort_cards()

    def reset(self):
        """Reset the Player for a new Round.
        """
        for player in self.players:
            player.won_cards = Cards(self.settings)
            player.cards = Cards(self.settings)
