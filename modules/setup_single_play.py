"""
The single Player needs to decide if he wants to take the skat and which gametype he wants to play
"""
from modules.card import Card
from modules.cards import Cards
from modules.tools import get_user_true_false, user_select_card

def setup_single_play(turn, skat, settings):
    
    if check_play_skat(settings, turn):
        turn, skat = take_skat(turn, skat, settings)

    gamemode = set_gamemode(turn, settings)
    jack_multiplicator = get_jack_multiplicator(turn.cards, settings)

    return gamemode, jack_multiplicator, skat

def check_play_skat(settings, turn):
    show_message = settings.skatmessage.format(turn.name)
    error_message = settings.yesno_errormessage.format(turn.name)
    return get_user_true_false(show_message, error_message, turn.cards)

def take_skat(turn, skat, settings):
    turn.cards += skat
    turn.cards.sort_cards()
    skat.empty_cards()

    show_message = settings.cardmessage.format(turn.name)
    error_message = settings.card_errormessage.format(turn.name)

    for _ in range(2):
        turn.cards, skat_card = user_select_card(show_message, error_message, turn.cards)
        skat.add_card(skat_card)

    return turn, skat

def set_gamemode(turn, settings):
    show_message = settings.gamemode_message.format(turn.name)
    error_message = settings.gamemode_errormessage.format(turn.name)

    gamemode = get_play_type(show_message, error_message, settings.gamemode_dict, turn.cards)
    Card.order_dict = settings.order_dicts[gamemode["order_dict"]]
    Card.trumpf = gamemode["trumpf"]
    return gamemode
    
def get_play_type(show_message, error_message, gamemode_dict, user_cards):
    user_cards.print_cards_ascii()
    print(show_message)
    for key in gamemode_dict:
        print(f"{key}: {gamemode_dict[key]['name']}")

    inp = input()
    if inp.isdigit() and inp in gamemode_dict:
        return gamemode_dict[inp]
    else:
        print(error_message)
        return get_play_type(show_message, error_message, gamemode_dict, user_cards)

def get_jack_multiplicator(cards, settings):
    """
    Get the jack multiplicator for the play
    """
    if not isinstance(cards, Cards):
        raise TypeError("table_cards need to be of Type List")
    if not all([isinstance(card, Card) for card in cards]):
        raise ValueError("Table Cards should only contain Cards")

    jacks = [card for card in cards if card.card_points == 2]
    if len(jacks) == 4 or len(jacks) == 0:
        return 5
    
    suit_list = [x[0] for x in sorted(settings.suit_dict.items(), key=lambda x: x[1], reverse=True)]
    multi = 2
    if has_card_with_suit(jacks, suit_list[0]):
        for suit in suit_list[1:]:
            if has_card_with_suit(jacks, suit):
                multi += 1
            else:
                break
    else:
        for suit in suit_list[1:]:
            if not has_card_with_suit(jacks, suit):
                multi += 1
            else:
                break
    return multi

def has_card_with_suit(cards, suit):
    if not isinstance(cards, list):
        raise TypeError("table_cards need to be of Type List")
    if not all([isinstance(card, Card) for card in cards]):
        raise ValueError("Table Cards should only contain Cards")
    if not isinstance(suit, str):
        raise TypeError("Suit needs to be of Type String")

    for card in cards:
        if card.suit_str == suit:
            return True
    return False