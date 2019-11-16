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

    def print(self):
        print('┌───────┐')
        print(f'| {self.value:<2}    |')
        print('|       |')
        print(f'|   {self.suit}   |')
        print('|       |')
        print(f'|    {self.value:>2} |')
        print('└───────┘') 

    def get_print_vals(self):
        return ['┌───────┐',f'| {self.value:<2}    |','|       |',f'|   {self.suit}   |','|       |',f'|    {self.value:>2} |','└───────┘', f' {self.value:<2} {self.suit_str:>2}   ']


def print_multiple_cards(cards):
    if not isinstance(cards, list):
        raise TypeError("cards need to be of type list")
    elif not all(isinstance(c, Card) for c in cards):
        raise TypeError("All elements need to be of Type Card")
    
    for i in range(len(cards[0].get_print_vals())):
        pr_str = ""
        for c in cards:
            pr_str += c.get_print_vals()[i]+":"
        print(pr_str[:-1])
        
