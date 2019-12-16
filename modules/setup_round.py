"""
In this file all Functions are located which are needed to setup a new round
"""
from modules.cards import Cards
from modules.card import Card
from modules.round_class import Round

def setup_round(players, settings):
    game_round = Round(players, settings)
    players, skat = give_cards(players, settings)
    game_round.skat = skat
    return game_round, players

def give_cards(players, settings):
    cards = Cards(settings)
    cards.create_shuffled_cards()
    for i, player in enumerate(players):
        player.cards = Cards(settings, cards.cards[10*i:10*(i+1)])
        player.cards.sort_cards()

    skat = Cards(settings, cards.cards[-2:])
    return players, skat
