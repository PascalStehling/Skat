

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