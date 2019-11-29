class Card:
    def __init__(self,value, suit, value_dict, suit_dict):

        if not isinstance(suit, str):
            raise TypeError("suit needs to be an int between 0 and 3")
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
        return ['┌───────┐',f'| {self.value:<2}    |','|       |',f'|   {self.suit}   |','|       |',f'|    {self.value:>2} |','└───────┘', f' {self.suit_str:<2} {self.value:>2}   ']

    def print(self):
        for e in self.get_ascii_card():
            print(e)

    def get_card_tuple(self):
        return (self.suit_val, self.value)

    def __eq__(self, other_card):
        if isinstance(other_card, Card):
            if self.value == other_card.value and self.suit_val == other_card.suit_val:
                return True
            else:
                return False
        else:
            raise TypeError("The other Object need to be of Type Card")

    def equal_suit(self, other_card):
        if isinstance(other_card, Card):
            if self.suit_val == other_card.suit_val:
                return True
            else:
                return False
        else:
            raise TypeError("The other Object need to be of Type Card")

    def istrumpf(self, trumpf):
        if trumpf is not None and not isinstance(trumpf, str):
            raise TypeError("Trumpf need to be of Type None or String")

        if trumpf is not None:
            if self.card_points == 2:
                return True
            elif self.suit_str == trumpf:
                return True
            
        return False

    def ishigher(self, smaller_card, trumpf, order_dict, check_suit_val=False):
        if not isinstance(smaller_card, Card):
            raise TypeError("Other Card needs to be of Type Card")

        card_trumpf = self.istrumpf(trumpf)
        smaller_card_trumpf = smaller_card.istrumpf(trumpf)

        if card_trumpf and not smaller_card:
            return True
        elif smaller_card_trumpf and not card_trumpf:
            return False
        elif card_trumpf and smaller_card_trumpf:
            if self.card_points == 2 and smaller_card.card_points != 2:
                return True
            elif self.card_points != 2 and smaller_card.card_points == 2:
                return False
            elif self.card_points == 2 and smaller_card.card_points == 2:
                if self.suit_val > smaller_card.suit_val: # JAck with higher Suit value is Higher
                    return True
                else: # Normally there cant bee 2 Times the same Card, so the vals cant be equal
                    return False
            else:
                return self.has_higher_value(smaller_card, order_dict)
        elif self.suit_val != smaller_card.suit_val: # If none is Trumpf and they have diffrent suits, the first Card is Higher
            if check_suit_val:
                if self.suit_val > smaller_card.suit_val:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return self.has_higher_value(smaller_card, order_dict)

    def has_higher_value(self, smaller_card, order_dict):
        if not isinstance(order_dict, dict):
            raise TypeError("order_dict needs to be of Type dict")
        if not isinstance(smaller_card, Card):
            raise TypeError("smaller card needs to be of Type Card")
        if order_dict[self.value] > order_dict[smaller_card.value]:
            return True
        else:
            return False

class EmptyCard(Card):

    def __init__(self):
        self.value = " "
        self.suit_val = -1
        self.suit = " "
        self.suit_str = " "
        self.card_points = -1