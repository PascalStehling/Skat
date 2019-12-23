from modules.Card import Card
from modules.Cards import Cards
from modules.Bidding import Bidding
from modules.tools import user_select_card
from modules.Stich import Stich
from copy import deepcopy

class Round():

    def __init__(self, players, settingContainer, bidding, jack_multiplicator, gamemode):
        self.turn = players.forhand
        self.settings = settingContainer
        self.players = players
        self.bidding = bidding
        self.jack_multiplicator = jack_multiplicator
        self.gamemode = gamemode


    def play_round(self):
        while len(self.turn.cards) != 0:
            self.turn = Stich(self.players, self.turn, self.settings).play_stich().assign_stich_to_winner().get_winner()
            print(self.settings.winner_message.format(self.turn.name))

    def end_round(self):
        """The main function to end the round   
        """
        
        single_player_card_points = self.calc_card_points()
        score = self.calculate_score(single_player_card_points)
        self.bidding.bid_player.score += score

        print(self.settings.end_round_message.format(self.bidding.bid_player, single_player_card_points, score))
        for p in self.players:
            print(self.settings.point_message.format(p.name, p.score))

        self.players.players_on_next_position()

        return self

    def calculate_score(self, single_player_card_points):
        """Calculate the score points of the single_player
        
        Returns:
            int: the score points the player achieved
        """
        if self.has_won_round(single_player_card_points):
            return self.calc_score_points_won(single_player_card_points)
        else:
            return self.calc_score_points_lost(single_player_card_points)

    def calc_score_points_won(self, single_player_card_points):
        """Get the Score points if the player won
        Returns:
            int: the score points the player achieved
        """
        return (self.get_win_level(single_player_card_points)+self.jack_multiplicator)*self.gamemode["points"]

    def calc_score_points_lost(self, single_player_card_points):
        """Get the Score points if the player Lost

        Returns:
            int: the score points the player achieved
        """
        return (self.get_win_level(120-single_player_card_points)+self.jack_multiplicator)*self.gamemode["points"]*-2

    @staticmethod
    def get_win_level(card_points):
        """Get the win states the Player has.

        Returns:
            int: 0 for playing, 1 for Schneider and 2 for Schwarz
        """
        if card_points == 120:
            return 2
        if card_points > 90:
            return 1
        
        return 0

    def calc_card_points(self):
        """Calculate the points from a list of Cards

        Returns:
            int: number of points the Player got
        """
        points = 0
        for card in self.turn.cards:
            points += card.card_points
        return points

    def has_won_round(self, card_points):
        """Checks if the Player has won this round. If he has over 90 he always wins, under 60 allways loose and between 60 and 90 it depends if he overbidded

        Returns:
            bool: True if the Player won, else False
        """
        if card_points >= 90:
            return True

        if card_points <= 60:
            return False

        return not self.has_over_bidded()
        

    def has_over_bidded(self):
        """Checks is the Player has overbidden

        Returns:
            bool: True if the player has overbidded, else False
        """
        if Card.trumpf is not None:
            return (self.gamemode["points"]*self.jack_multiplicator) < self.bidding.bid
        else:
            return self.gamemode["points"] < self.bidding.bid