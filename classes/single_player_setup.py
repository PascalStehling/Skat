from classes.card import Card
from classes.tools import user_select_card, get_user_true_false
from classes.cards import Cards

def single_player_setup(round_object):
    show_message = round_object.settings.skatmessage.format(round_object.turn.name)
    error_message = round_object.settings.yesno_errormessage.format(round_object.turn.name)
    if get_user_true_false(show_message, error_message, round_object.turn.cards):
        show_message = round_object.settings.cardmessage.format(round_object.turn.name)
        error_message = round_object.settings.card_errormessage.format(round_object.turn.name)
        round_object.turn.cards += round_object.skat
        round_object.skat.empty_cards()
        round_object.turn.cards.sort_cards()

        for _ in range(2):
            round_object.turn.cards, skat_card = user_select_card(show_message, error_message, round_object.turn.cards)
            round_object.skat.add_card_and_sort(skat_card)

    show_message = round_object.settings.gamemode_message.format(round_object.turn.name)
    error_message = round_object.settings.gamemode_errormessage.format(round_object.turn.name)
    round_object.gamemode = get_play_type(round_object, show_message, error_message)
    
    Card.order_dict = round_object.settings.order_dicts[round_object.gamemode.get("order_dict")]
    Card.trumpf = round_object.gamemode.get("trumpf")

    round_object.jack_multiplicator = get_jack_multiplicator(round_object)

    for player in round_object.players:
        player.cards.sort_cards()

    round_object.turn = round_object.players.forhand
    return round_object

def get_play_type(round_object, show_message, error_message):
    round_object.turn.cards.print_cards_ascii()
    print(show_message)
    for key in round_object.settings.gamemode_dict:
        print(f"{key}: {round_object.settings.gamemode_dict[key]['name']}")

    inp = input()
    if inp in round_object.settings.gamemode_dict:
        return round_object.settings.gamemode_dict[inp]
    else:
        print(error_message)
        return get_play_type(round_object, show_message, error_message)

def get_jack_multiplicator(round_object):
    """
    Get the jack multiplicator for the play
    """
    cards = round_object.turn.cards
    if not isinstance(cards, Cards):
        raise TypeError("table_cards need to be of Type List")
    if not all([isinstance(card, Card) for card in cards]):
        raise ValueError("Table Cards should only contain Cards")

    jacks = [card for card in cards if card.card_points == 2]
    if len(jacks) == 4 or len(jacks) == 0:
        return 5
    
    suit_list = [x[0] for x in sorted(round_object.settings.suit_dict.items(), key=lambda x: x[1], reverse=True)]
    jack_name = [x[0] for x in round_object.settings.value_dict.items() if x[1] == 2][0]
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
