class Card:
    """Creates a card object. This has a suit as string, as Unicode character and the value of the suit. 
    It also includes the value of the card (7-10, J, Q, K ,A) and the points of the card value.
    
    Returns:
        card: A Card Object
    """
    def __init__(self,value, suit, value_dict, suit_dict):
        if not isinstance(suit, str):
            raise TypeError("suit needs to be an str between 0 and 3")
        elif not isinstance(value, str):
            raise TypeError("value needs to be an string")
        elif not isinstance(value_dict, dict):
            raise TypeError("value needs to be an dict")
        elif not isinstance(suit_dict, dict):
            raise TypeError("value needs to be an dict")
        elif suit not in suit_dict:
            raise ValueError("Enter a Valid suit")
        elif value not in value_dict:
            raise ValueError("Enter a Valid Card Value")

        self.value = value
        self.suit_val = suit_dict[suit] # The Suit Value for skat
        self.suit = '♣♠♥♦'[12-self.suit_val] # 0,1,2,3 = ♥♦♣♠
        self.suit_str = suit
        self.card_points = value_dict[value]
    
    def __repr__(self):
        return f"{self.value} {self.suit_str}"

    def get_ascii_card(self):
        """Returns the Card as Ascii Art, where each element of the list is one line of the picture.
        
        Returns:
            list: list with the elements of the Ascii Art Card
        """
        return ['┌───────┐',f'| {self.value:<2}    |','|       |',f'|   {self.suit}   |','|       |',f'|    {self.value:>2} |','└───────┘', f' {self.suit_str:<2} {self.value:>2}   ']

    def print(self):
        """Prints the Ascii Art Card
        """
        for e in self.get_ascii_card():
            print(e)

    def get_card_tuple(self):
        """Get the suit value and the card value
        
        Returns:
            tuple: tuple with suit value and card value
        """
        return (self.suit_val, self.value)

    def __eq__(self, other_card):
        """Checks if the card is equal to another
        
        Args:
            other_card (Card): Card to check if equal
        
        Raises:
            TypeError: if other_card is not of Type Card
        
        Returns:
            bool: True if the 2 Cards are equal, else False
        """
        if not isinstance(other_card, Card):
            raise TypeError("The other Object need to be of Type Card")
        
        if self.value == other_card.value and self.suit_val == other_card.suit_val:
            return True
        else:
            return False

    def equal_suit(self, other_card):
        """Checks if the Card has the same suit as another Card
        
        Args:
            other_card (Card): Card to check if equal suit
        
        Raises:
            TypeError: if other_card is not of Type Card
        
        Returns:
            bool: True if the Cards have the same suit
        """
        if not isinstance(other_card, Card):
            raise TypeError("The other Object need to be of Type Card")

        if self.suit_val == other_card.suit_val:
            return True
        else:
            return False

    def istrumpf(self, trumpf):
        """Checks if the Card is Trumpf
        
        Args:
            trumpf (str): the trumpf which is played at the moment
        
        Raises:
            TypeError: if trumpf not None or not string
        
        Returns:
            bool: True if card is trumpf
        """
        if trumpf is not None and not isinstance(trumpf, str):
            raise TypeError("Trumpf need to be of Type None or String")

        if (self.card_points == 2 or self.suit_str == trumpf) and trumpf is not None:
            return True
            
        return False

    def ishigher(self, other_card, trumpf, order_dict, check_suit_val=False):
        """Checks if the card is higher than other_card
        
        Args:
            other_card (Card): Card to check with
            trumpf (str): Trumpf which is played at the moment
            order_dict (dict): dictionary with the ranking order of the cards
            check_suit_val (bool, optional): If the higher suit wins, if no card is Trumpf and there are not equal suit. If False the main card (self) is winning. Defaults to False.
        
        Raises:
            TypeError: if other Card is not of Type Card
        
        Returns:
            bool: True if the main Card (self) is higher, False if other_card is higher
        """
        if not isinstance(other_card, Card):
            raise TypeError("Other Card needs to be of Type Card")

        other_card_trumpf = other_card.istrumpf(trumpf)
        if self.istrumpf(trumpf):
            return self._ishigher_self_is_trumpf(other_card, other_card_trumpf, order_dict)
        
        return self._ishigher_self_not_trumpf(other_card, other_card_trumpf, order_dict, check_suit_val)
            

    def _ishigher_self_not_trumpf(self, other_card, other_card_trumpf, order_dict, check_suit_val=False):
        """Checks if the card is higher than other_card, if the main card (self) is not trumpf
        
        Args:
            other_card (Card): Card to check with
            other_card_trumpf (bool): if the other card is Trumpf
            order_dict (dict): dictionary with the ranking order of the cards
            check_suit_val (bool, optional): If the higher suit wins, if no card is Trumpf and there are not equal suit. If False the main card (self) is winning. Defaults to False.
        
        Returns:
            bool: True if the main Card (self) is higher, False if other_card is higher
        """
        if other_card_trumpf:
            return False
        if self.suit_val != other_card.suit_val: # If none is Trumpf and they have diffrent suits
            return self._ishigher_no_trumpf(other_card, check_suit_val)
            
        return self.has_higher_value(other_card, order_dict)

    def _ishigher_self_is_trumpf(self, other_card, other_card_trumpf, order_dict):
        """Checks if the card is higher than other_card, if the main card (self) is trumpf
        
        Args:
            other_card (Card): Card to check with
            other_card_trumpf (bool): if the other card is Trumpf
            order_dict (dict): dictionary with the ranking order of the cards
        
        Returns:
            bool: True if the main Card (self) is higher, False if other_card is higher
        """
        if not other_card_trumpf:
            return True
        else:
            return self._ishigher_both_trumpf(other_card, order_dict)

    def _ishigher_no_trumpf(self, other_card, check_suit_val=False):
        """Checks if the card is higher than other_card, if both cards are not trumpf
        
        Args:
            other_card (Card): Card to check with
            check_suit_val (bool, optional): If the higher suit wins, if no card is Trumpf and there are not equal suit. If False the main card (self) is winning. Defaults to False.
        
        Returns:
            bool: True if the main Card (self) is higher, False if other_card is higher
        """
        if check_suit_val:
            return self._ishigher_no_trumpf_check_suit_val(other_card)
        else:
            return True

    def _ishigher_no_trumpf_check_suit_val(self, other_card):
        """Checks if the card is higher than other_card, if both cards are not trumpf and the higher suit value wins
        Args:
            other_card (Card): Card to check with
        
        Returns:
            bool: True if the main Card (self) is higher, False if other_card is higher
        """
        if self.suit_val > other_card.suit_val:
            return True
        else:
            return False

    def _ishigher_both_trumpf(self, other_card, order_dict):
        """Checks if the card is higher than other_card, if both cards are trumpf
        
        Args:
            other_card (Card): Card to check with
            order_dict (dict): dictionary with the ranking order of the cards
        
        Returns:
            bool: True if the main Card (self) is higher, False if other_card is higher
        """
        if self.card_points == 2: # If self is Jack
            return self._ishigher_both_trump_self_is_jack(other_card)
        else:  # self is no Jack
            return self._ishigher_both_trump_self_not_jack(other_card, order_dict)
            
    def _ishigher_both_trump_self_not_jack(self, other_card, order_dict):
        """Checks if the card is higher than other_card, if both cards are trumpf and the main card (self) is not a Jack
        
        Args:
            other_card (Card): Card to check with
            order_dict (dict): dictionary with the ranking order of the cards
        
        Returns:
            bool: True if the main Card (self) is higher, False if other_card is higher
        """
        if other_card.card_points == 2: # other_card is Jack
            return False
        else: # No Card is Jack, higher Value wins
            return self.has_higher_value(other_card, order_dict)

    def _ishigher_both_trump_self_is_jack(self, other_card):
        """Checks if the card is higher than other_card, if both cards are trumpf and the main card (self) is a Jack
        
        Args:
            other_card (Card): Card to check with
        
        Returns:
            bool: True if the main Card (self) is higher, False if other_card is higher
        """
        if other_card.card_points != 2: # If smaller Card is not Jack
            return True
        return self._ishigher_both_trump_both_jack(other_card)

    def _ishigher_both_trump_both_jack(self, other_card):
        """Checks if the card is higher than other_card, if both cards are trumpf and both cards are Jacks
        
        Args:
            other_card (Card): Card to check with
        
        Returns:
            bool: True if the main Card (self) is higher, False if other_card is higher
        """
        if self.suit_val > other_card.suit_val: # Jack with higher Suit value is Higher
            return True
        else: # Normally there cant bee 2 Times the same Card, so the vals cant be equal
            return False

    def has_higher_value(self, other_card, order_dict):
        """Checks if the main card (self) has an higher value than other_card
        
        Args:
            other_card (Card): Card to check with
            order_dict (dict): dictionary with the ranking order of the cards
        
        Returns:
            bool: True if the main card (self) is higher
        """
        if order_dict[self.value] > order_dict[other_card.value]:
            return True
        else:
            return False

class EmptyCard(Card):
    """Creates an Empty card, with no text
    """

    def __init__(self):
        self.value = " "
        self.suit_val = -1
        self.suit = " "
        self.suit_str = " "
        self.card_points = -1