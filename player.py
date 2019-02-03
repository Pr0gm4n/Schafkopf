from random import SystemRandom as Random

from turn import Turn
from game import Game

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
        self.stack = []
        self.game = Game("Sauspiel") #TODO: properly select game you want to play

    def __repr__(self):
        return "Player " + self.name + ": " + self.hand.__repr__()

    def start_round(self, history):
        turn = Turn(self.name)
        self.play(turn, history)
        return turn

    def play(self, turn, history):
        print("Player", self.name, "may put down", self.hand.get_playable_cards(turn.get_suit()))

        choice = Random().choice(self.hand.get_playable_cards(turn.get_suit()))
        self.hand.play(choice)
        turn.add_card(choice)
