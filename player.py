from random import SystemRandom as Random

from turn import Turn
from game import Game

class Player:
    def __init__(self, name, player_id, hand):
        self.name = name
        self.player_id = player_id
        self.hand = hand
        self.stack = []
        self.init_game()

    def __repr__(self):
        return "Player " + self.name + ": " + self.hand.__repr__()

    def init_game(self):
        self.game = Game("weiter") #TODO: properly select game you want to play

    def start_round(self, history):
        turn = Turn(self.name)
        self.play(turn, history)
        return turn

    def play(self, turn, history):
        print("Player", self.name, "may put down", self.hand.get_playable_cards(turn.get_suit()))

        choice = Random().choice(self.hand.get_playable_cards(turn.get_suit()))
        self.hand.play(choice)
        turn.add_card(choice)

    def set_game(self, game, announcer):
        self.hand.sort(game)
        self.announcer = announcer
        self.game = game
