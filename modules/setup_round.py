"""
In this file all Functions are located which are needed to setup a new round
"""
from modules.cards import Cards
from modules.card import Card
from modules.round_class import Round

def start_new_round(players, settings):
    set_card_default_values(settings)
    players.reset()
    return give_cards(players, settings)

def set_card_default_values(settings):
    Card.value_dict = settings.value_dict
    Card.suit_dict = settings.suit_dict
    Card.order_dict = settings.standart_order_dict
    Card.trumpf = get_clubs_string(settings)

def give_cards(players, settings):
    cards = Cards(settings)
    cards.create_shuffled_cards()
    for i, player in enumerate(players):
        player.cards = Cards(settings, cards.cards[10*i:10*(i+1)])
        player.cards.sort_cards()

    skat = Cards(settings, cards.cards[-2:])
    return players, skat

def get_clubs_string(settings):
    for tup in settings.suit_dict.items():
        if tup[1] == 12:
            return tup[0]
    raise Exception("No Clubs found")