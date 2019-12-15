from classes.cards import Cards
from classes.bidding_class import Bidding
from classes.tools import get_user_true_false, user_select_card
from classes.card import Card
from classes.single_player_setup import single_player_setup
from classes.play_round import PlayRound

class Round():

    def __init__(self, players, settingContainer):
        self.players = players
        self.settings = settingContainer
        self.skat = []
        self.jack_multiplicator = None
        self.gamemode = None
        self.gamestate = 1
        self.turn = players.middlehand
        self.bidding = None
        self.play_round = None

        Card.value_dict = self.settings.value_dict
        Card.suit_dict = self.settings.suit_dict
        Card.order_dict = self.settings.standart_order_dict
        Card.trumpf = self.get_clubs_string()

        self.give_cards()

    def give_cards(self):
        cards = Cards(self.settings)
        cards.create_shuffled_cards()
        for i, player in enumerate(self.players):
            player.cards = Cards(self.settings, cards.cards[10*i:10*(i+1)])
            player.cards.sort_cards()

        self.skat = Cards(self.settings, cards.cards[-2:])

    def get_clubs_string(self):
        for tup in self.settings.suit_dict.items():
            if tup[1] == 12:
                return tup[0]
        raise Exception("No Clubs found")

    def start_bidding(self):
        self.bidding = Bidding(self.settings)
        while True:
            self.bidding.make_bid(self.turn)
            if self.bidding.is_end_bidding():
                self.turn, self.gamestate = self.bidding.end_bidding(self.players.forhand)
                break
            else:
                self.turn = self.bidding.get_new_turn(self.turn, self.players)

    def start_single_player_setup(self):
        self = single_player_setup(self)

    def start_play_cards(self):
        self.play_round = PlayRound(self.settings, self.players, self.bidding)
        self.play_round.play_round()

    def finish_round(self):
        card_points = self.calc_card_points()
        score = self.calculate_score(card_points)
        self.bidding.bid_player.points += score

        print(self.settings.end_round_message.format(self.bidding.bid_player.name, card_points, score))
        for player in self.players:
            print(self.settings.point_message.format(player.name, player.points))

    def play(self):
        self.start_bidding()
        if self.gamestate == 2:
            self.start_single_player_setup()
            self.start_play_cards()
            self.finish_round()

    def calculate_score(self, single_player_card_points):
        """Calculate the score points of the single_player
        
        Args:
            single_player_card_points (int): number of Card-Points the single_player got
            trumpf (str): None or String of the trumpf thatz is played
            bid (int): the bid of the single player
            jack_multiplicator (int): the multiplicator of the jacks (play with/without jacks plus 1 (take game))
            gamemode_points (int): points of the gamemode
        
        Returns:
            int: the score points the player achieved
        """
        if self.has_won_round(single_player_card_points):
            return self.calc_score_points_won(single_player_card_points)
        else:
            return self.calc_score_points_lost(single_player_card_points)

    def calc_score_points_won(self, single_player_card_points):
        """Get the Score points if the player won
        
        Args:
            single_player_card_points (int): number of Card-Points the single_player got
        
        Returns:
            int: the score points the player achieved
        """
        return (self.get_win_level(single_player_card_points)+self.jack_multiplicator)*self.gamemode.get("points")

    def calc_score_points_lost(self, single_player_card_points):
        """Get the Score points if the player Lost
        
        Args:
            single_player_card_points (int): number of Card-Points the single_player got
        
        Returns:
            int: the score points the player achieved
        """
        return (self.get_win_level(120-single_player_card_points)+self.jack_multiplicator)*self.gamemode.get("points")*-2


    def get_win_level(self, card_points):
        """Get the win states the Player has.
        
        Args:
            card_points (int): number of Points the single_player got
        
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
        
        Args:
            cards (list): A List of Card Objects
        
        Returns:
            int: number of points the Player got
        """
        points = 0
        for card in self.play_round.single_player_stack:
            points += card.card_points
        return points

    def has_won_round(self, card_points):
        """Checks if the Player has won this round. If he has over 90 he always wins, under 60 allways loose and between 60 and 90 it depends if he overbidded
        
        Args:
            card_points (int): number of Points the single_player got
        
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
        
        Args:
            trumpf (str): None or String of the trumpf thatz is played
            bid (int): the bid of the single player
            jack_multiplicator (int): the multiplicator of the jacks (play with/without jacks plus 1 (take game))
            gamemode_points (int): points of the gamemode
        
        Returns:
            bool: True if the player has overbidded, else False
        """
        if Card.trumpf is not None:
            return (self.gamemode.get("points")*self.jack_multiplicator) < self.bidding.bid
        else:
            return self.gamemode.get("points") < self.bidding.bid