from classes.card import Card

def get_user_true_false(show_message, error_message, cards):
    """
    Get True or False if user wants to take the bid
    """
    cards.print_cards_ascii()
    print("\n", show_message)
    inp = input()

    if inp.lower() == "yes" or inp.lower() == "y":
        return True
    if inp.lower() == "no" or inp.lower() == "n":
        return False
    
    print(error_message)
    return get_user_true_false(show_message, error_message, cards)

def get_user_card(show_message, error_message, cards):
    """
    Get a Card from a Userinput
    """
    cards.print_cards_ascii()
    print("\n", show_message)
    inp = input()

    if isinstance(inp, str):
        inp = inp.split()
    
    if isinstance(inp, list) and len(inp) == 2:
        try:
            return Card(inp[1], inp[0])
        except (TypeError, ValueError):
            pass
    print(error_message)
    return get_user_card(show_message, error_message, cards)
            
def user_select_card(show_message, error_message, cards):
    card = get_user_card(show_message, error_message, cards)

    if card in cards:
        cards.remove(card)
        return cards, card
    else:
        print(error_message)
        return user_select_card(show_message, error_message, cards)