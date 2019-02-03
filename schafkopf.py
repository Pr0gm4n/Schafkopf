#!/usr/bin/python3

from random import SystemRandom as Random
from itertools import cycle

from card import Card
from hand import Hand
from player import Player

from IPython import embed


""" Model the bavarian card game Schafkopf, implementing the set of rules first
    and later potentially adding some player strategies and support for users
    to play themselves. WORK IN PROGRESS whenever I have too much time.
"""
class Schafkopf:
    def __init__(self):
        self.init_deck()
        self.deal_to_players()

        print(self.players)

        self.players = cycle(self.players)

        winner = 0
        history = []
        for _ in range(8):                                  # iterate over all 8 cards
            turn = next(self.players).start_round(history)  # play initial card
            for _ in range(3):                              # each player puts down a card
                next(self.players).play(turn, history)
            for _ in range(turn.winner):                    # scroll to winner of the round
                next(self.players)
            history.append(turn)

            input()                                         # wait for a keypress


        embed() # start debugging in this context

    def init_deck(self):
        self.deck = []
        for suit in Card.SUITS.keys():
            for number in Card.NUMBERS:
                self.deck.append(Card(suit, number))
        Random().shuffle(self.deck)

    def deal_to_players(self):
        self.players = []
        for player in range(4):
            cards = []
            for card in range(8):
                cards.append(self.deck[8 * player + card])
            cards.sort()
            self.players.append(Player(str(player), Hand(cards)))


if __name__ == "__main__":
    # execute only if run as a script
    Schafkopf()
