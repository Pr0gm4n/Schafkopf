#!/usr/bin/python3

from random import SystemRandom as Random
from itertools import cycle

from card import Card
from hand import Hand
from player import AIPlayer, HumanPlayer

from IPython import embed


""" Model the bavarian card game Schafkopf, implementing the set of rules first
    and later potentially adding some player strategies and support for users
    to play themselves. WORK IN PROGRESS whenever I have too much time.
"""
class Schafkopf:
    def __init__(self):
        self.init_deck()
        self.deal_to_players()

        from game import Game # TODO: for testing only! remove!
        self.players[2].game = Game("Solo")

        print(self.players)

        game = None
        announcer = -1
        for i, player in enumerate(self.players):
            # TODO: possibly might not play a game if another player already
            # announces a game
            if player.game > game:
                game = player.game
                announcer = i

        # update card ordering according to selected game
        for player in self.players:
            player.set_game(game, announcer)

        self.players = cycle(self.players)

        winner = 0
        history = []
        # iterate 8 turns / rounds
        for _ in range(8):
            # turn initiation
            turn = next(self.players).start_round(history)
            # each player puts down a card
            for _ in range(3):
                next(self.players).play(turn, history)
            # scroll to winner of the round
            for _ in range(turn.winner):
                next(self.players)
            # memorize outcome
            history.append(turn)

            # wait for a keypress
            input()


        embed() # start debugging in this context

    def init_deck(self):
        self.deck = []
        for suit in Card.SUITS.keys():
            for number in Card.NUMBERS:
                self.deck.append(Card(suit, number))
        Random().shuffle(self.deck)

    def deal_to_players(self):
        self.players = []
        for player_id in range(4):
            cards = []
            for card in range(8):
                cards.append(self.deck[8 * player_id + card])
            cards.sort()
            self.players.append(AIPlayer(str(player_id), player_id, Hand(cards)))


if __name__ == "__main__":
    # execute only if run as a script
    Schafkopf()
