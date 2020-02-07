#pylint: disable=line-too-long
"""
This File Contains the Bidding Class. Its neccessary to play the Bidding Phase
"""
from modules.tools import get_user_true_false


class Bidding():
    """
    The Bidding Class contains all Functions relevant for Bidding.
    """

    def __init__(self, settings, players):
        self.bid = None
        self.bid_player = None
        self.passed = []
        self.next_bid = 18
        self.settings = settings
        self.players = players
        self.turn = players.middlehand

    def play_bidding(self):
        """This function is the main Function of this Class. With this the Bidding Phase can be Played

        Returns:
            tuple: The Player who won Bidding or None if all passed and the new Gamestate
        """
        while not self.is_bidding_over():
            self.make_bid()
            self.get_new_turn()
        return self.end_bidding()

    def make_bid(self):
        """Main Function for bidding. Ask Player if he wants to bid, checks if bidding Phase ends and select the new turn
        """
        show_message = self.settings.bidmessage.format(
            self.turn.name, self.next_bid)
        error_message = self.settings.yesno_errormessage.format(self.turn.name)
        user_bid = get_user_true_false(
            show_message, error_message, self.turn.cards)
        self._process_user_bid(user_bid)

    def _process_user_bid(self, user_bid):
        """Check what the user has bidden and update the bidding Dictionary (bid_dict).

        Args:
            user_bid (bool): If the user passed (False) or said yes (True)
        """
        if not user_bid:
            self.passed.append(self.turn)
        else:
            self._update_bid_dict_yes_to_bid()

    def _update_bid_dict_yes_to_bid(self):
        """Updates the bid Dict if the user said Yes to the new Bid
        """
        if self.turn.position == self.settings.FORHAND_POSITION:  # Forhand can only listen
            self._bid_hear()
        elif self.turn.position == self.settings.BACKHAND_POSITION:  # Backhand can only say
            self._bid_say()
        else:  # Middlehand is playing
            self._update_bid_dict_middlehand_player()

    def _update_bid_dict_middlehand_player(self):
        """Updates the bid Dict if the user said Yes to the new Bid and was playing middlehand
        """
        if self.has_forhand_passed():  # If Forhand has passed, Middlehand is hearing
            self._bid_hear()
        else:  # Else middle hand is saying
            self._bid_say()

    def has_forhand_passed(self):
        """Checks if the Forhandplayer has allready passed

        Returns:
            bool: True if the forhand Player has passed, else False
        """
        return bool([True for player in self.passed if player.position == self.settings.FORHAND_POSITION])

    def _bid_say(self):
        """Update the bid_dict when the user needed to say
        """
        self.bid = self.next_bid
        self.bid_player = self.turn

    def _bid_hear(self):
        """Update the bid_dict when the user needed to hear
        """
        if self.settings.bid_list[-1] == self.next_bid:
            raise ValueError("Cant bid any higher")
        self.bid_player = self.turn
        self.next_bid = self.settings.bid_list[self.settings.bid_list.index(
            self.next_bid)+1]

    def get_new_turn(self):
        """Get the new turn for the next round of bidding
        """
        if self.turn in self.passed:  # Player has passed
            self._turn_if_passed()
        else:  # Player has not passed
            self._turn_if_not_passed()

    def _turn_if_passed(self):
        """Get the new turn for the next round of bidding if the player who played now passed.
        """
        if self.turn.position != self.settings.BACKHAND_POSITION:
            # If the middlehand or forhand passes backhand needs to play
            self.turn = self.players.backhand
        elif self.players.forhand not in self.passed:
            # If the Backhand and forhand is still in play, forhand needs to play
            self.turn = self.players.forhand
        else:  # self.players.middlehand not in self.passed:
            # IF Backhand passed and middlehand still in play, middlehand needs to play
            self.turn = self.players.middlehand

    def _turn_if_not_passed(self):
        """Get the new turn for the next round of bidding if the player who played now said yes.
        """
        if self.turn.position == self.settings.MIDDLEHAND_POSITION:
            self._turn_if_not_passed_middlehand()
        elif self.turn.position == self.settings.FORHAND_POSITION:
            self._turn_if_not_passed_forhand()
        else:  # self.turn.position ==  self.settings.BACKHAND_POSITION
            self._turn_if_not_passed_backhand()

    def _turn_if_not_passed_middlehand(self):
        """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the middlehand position (1).
        """
        if self.players.forhand not in self.passed:
            # If middlehand was playing and forhand is still playing, it is forhand turn
            self.turn = self.players.forhand
        else:
            # If middlehand was playing and forhand has passed, backhand is playing
            self.turn = self.players.backhand

    def _turn_if_not_passed_forhand(self):
        """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the forhand position (0).
        """
        if self.players.middlehand not in self.passed:
            # If forhand was playing and middlehand has not passed, middlehand is playing
            self.turn = self.players.middlehand
        else:
            # If forhand was playing and middlehand has passed, backhand is playing
            self.turn = self.players.backhand

    def _turn_if_not_passed_backhand(self):
        """Get the new turn for the next round of bidding if the player who played now said yes and was playing at the backhand position (2).
        """
        if self.players.middlehand not in self.passed:
            # If backhand was playing and middlehand has not passed, middlehand is playing
            self.turn = self.players.middlehand
        else:
            # If backhand was playing and forhand has not passed, forhand is playing
            self.turn = self.players.forhand

    def end_bidding(self):
        """Ends the bidding Phase, if there is an bid Player, he won the bidding, else it starts new with new cards

        Returns:
            tuple: Tuple with the the player who has the next turn and the new gamstate (turn, gamestate)
        """
        if self.bid_player is not None:
            return self.bid_player, self.settings.PLAY_ROUND

        # Ramsch not implemented, just new cards are given.
        # TODO Ramsch
        print("Everyone passed, cards get dealt again")
        return None, self.settings.START_ROUND

    def is_bidding_over(self):
        """Checks if the bidding finished

        Returns:
            bool: True if the bidding is finished, else False
        """
        return (len(self.passed) == 2 and self.bid_player is not None) or (len(self.passed) == 3)
