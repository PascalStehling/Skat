from classes.tools import get_user_true_false

class Bidding():

    def __init__(self, settings):
        self.settings = settings

        self.bid = None
        self.bid_player = None
        self.passed = []
        self.next_bid = 18

    def make_bid(self, bidding_player):
        show_message = self.settings.bidmessage.format(bidding_player.name, self.next_bid)
        error_message = self.settings.yesno_errormessage.format(bidding_player.name)

        user_bid = get_user_true_false(show_message, error_message, bidding_player.cards)
        self.update_bid_values(bidding_player, user_bid)

    def update_bid_values(self, bidding_player, user_bid):
        if not user_bid:
            self.passed.append(bidding_player)
        else:
            self.update_bid_values_positiv_bid(bidding_player)

    def update_bid_values_positiv_bid(self, bidding_player):
        """Updates the bid Dict if the user said Yes to the new Bid
        """
        if bidding_player.position == 0: # Forhand can only listen
            self.bid_hear(bidding_player)
        elif bidding_player.position == 2: # Backhand can only say
            self.bid_say(bidding_player)
        else: # Middlehand is playing
            self.update_bid_values_middlehand_player(bidding_player)

    def update_bid_values_middlehand_player(self, bidding_player):
        """Updates the bid Dict if the user said Yes to the new Bid and was playing middlehand
        """
        if [True for player in self.passed if player.position == 0]: # If Forhand has passed, Middlehand is hearing
            self.bid_hear(bidding_player)
        else:  # Else middle hand is saying
            self.bid_say(bidding_player)

    def bid_say(self, bidding_player):
        """Update the bid_dict when the user needed to say
        """
        self.bid = self.next_bid
        self.bid_player = bidding_player

    def bid_hear(self, bidding_player):
        """Update the bid_dict when the user needed to hear
        """

        if self.settings.bid_list[-1] == self.bid:
            raise ValueError("Cant bid any higher") 
        self.bid_player = bidding_player
        self.next_bid = self.settings.bid_list[self.settings.bid_list.index(self.bid)+1]

    def get_new_turn(self, bidding_player, players):
        """Get the new turn for the next round of bidding
        """
        if bidding_player in self.passed: # Player has passed
            return self.turn_if_passed(bidding_player, players)
        else: # Player has not passed
            return self.turn_if_not_passed(bidding_player, players)

    def turn_if_passed(self, bidding_player, players):
        """Get the new turn for the next round of bidding if the player who played now passed.
        """
        if bidding_player.position != 2:
            # If the middlehand or forhand passes backhand needs to play
            return players.backhand
        elif players.forhand not in self.passed:
            # If the Backhand and forhand is still in play, forhand needs to play
            return players.forhand
        elif players.middlehand not in self.passed:
            # IF Backhand passed and middlehand still in play, middlehand needs to play
            return players.middlehand
        else:
            raise Exception("Somthing wrong happend in turn_if_passed")

    def turn_if_not_passed(self, bidding_player, players):
        """Get the new turn for the next round of bidding if the player who played now said yes.
        """
        if bidding_player.position == 1:
            return self.turn_if_not_passed_middlehand(players)
        if bidding_player.position == 0:
            return self.turn_if_not_passed_forhand(players)
        if bidding_player.position == 2 :
            return self.turn_if_not_passed_backhand(players)
        else:
            raise Exception("Somthing wrong happend in turn_if_not_passed")

    def turn_if_not_passed_middlehand(self, players):
        """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the middlehand position (1).
        """
        if players.forhand not in self.passed:
            # If middlehand was playing and forhand is still playing, it is forhand turn
            return players.forhand
        else:
            # If middlehand was playing and forhand has passed, backhand is playing
            return players.backhand

    def turn_if_not_passed_forhand(self, players):
        """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the forhand position (0).
        
        Args:
            middlehand_player (int): Number of the Player who is plays middlehand
            backhand_player (int): Number of the Player who is plays backhand
            passed (list): List of Numbers of the Players who passed
        
        Returns:
            int: The Number of the Player who plays next round
        """
        if players.middlehand not in self.passed:
            # If forhand was playing and middlehand has not passed, middlehand is playing
            return players.middlehand
        else:
            # If forhand was playing and middlehand has passed, backhand is playing
            return players.backhand

    def turn_if_not_passed_backhand(self, players):
        """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the backhand position (2).
        """
        if players.middlehand not in self.passed:
            # If backhand was playing and middlehand has not passed, middlehand is playing
            return players.middlehand
        else:
            # If backhand was playing and forhand has not passed, forhand is playing
            return players.forhand

    def end_bidding(self, forhand_player):
        """Ends the bidding Phase, if there is an bid Player, he won the bidding, else it starts new with new cards
        
        Args:
            bid_player (int): the Number of the Player who set the highest bid. It can also be None
            forhand_player_num (int): the number of the player who plays forhand
        
        Returns:
            tuple: Tuple with the the player who has the next turn and the new gamstate (turn, gamestate)
        """
        if self.bid_player is not None:
            return self.bid_player, 2
        else:
            # Ramsch not implemented, just new cards are given.
            # TODO Ramsch
            print("Everyone passed, cards get dealt again")
            return forhand_player, 1

    def is_end_bidding(self):
        """Checks if the bidding finished
        
        Args:
            passed_player_list (list): List of Players who passed
            bid_player (int): Number of the Player who is highest at bidding, can be None
        
        Returns:
            bool: True if the bidding is finished, else False
        """
        return (len(self.passed) == 2 and self.bid_player is not None) or (len(self.passed) == 3)