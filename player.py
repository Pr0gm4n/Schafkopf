from random import SystemRandom as Random

from turn import Turn
from game import Game
from card import Card

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
        self.game = Game("weiter") # dummy player

    def play(self, turn, history):
        print("Player", self.name, "may put down", self.hand.get_playable_cards(turn.get_suit()))

        choice = Random().choice(self.hand.get_playable_cards(turn.get_suit()))
        self.hand.play(choice)
        turn.add_card(choice)

    def set_game(self, game, announcer):
        self.hand.sort(game)
        self.announcer = announcer
        self.game = game

class AIPlayer(Player):
    def __init__(self, name, player_id, hand):
        Player.__init__(self, name, player_id, hand)

    def init_game(self):
        print("Estimating hand: " + str(self.hand))
        solo, solo_suit = self.solo_probability()
        wenz = self.wenz_probability()
        sauspiel, sauspiel_suit = self.sauspiel_probability()

        if solo > wenz and solo > 0.6:
            self.game = Game("Solo", solo_suit)
        elif wenz > 0.6:
            self.game = Game("Wenz")
        elif sauspiel > 0.6:
            self.game = Game("Sauspiel", sauspiel_suit)
        else:
            self.game = Game("weiter")

    def solo_probability(self):
        max_probability = -1.0
        max_probability_suit = None

        for suit in Card.SUITS:
            game = Game("Solo", suit) # get suit from context
            def solo_card_estimator(card):
                if game.is_trump(card):
                    return { # TODO: test and tweak these values
                        "O": 0.13,
                        "U": 0.12,
                        "A": 0.10,
                        "X": 0.09,
                        "K": 0.06,
                        "9": 0.05,
                        "8": 0.05,
                        "7": 0.05
                    }[card.number]
                else:
                    return {
                        "A": 0.05,
                        "X": 0.03,
                        "K": 0.01,
                        "9": 0.00,
                        "8": 0.00,
                        "7": 0.00
                    }[card.number]

            probability = self.hand.evaluate(solo_card_estimator)
            print("Estimating " + str(game) + ": " + str(probability))

            if probability > max_probability:
                max_probability = probability
                max_probability_suit = suit
        return max_probability, max_probability_suit

    def wenz_probability(self):
        def wenz_card_estimator(card):
            return {
                "U": 0.18,
                "A": 0.07,
                "X": 0.03,
                "K": 0.01,
                "O": 0.00,
                "9": 0.00,
                "8": 0.00,
                "7": 0.00
            }[card.number]

        probability = self.hand.evaluate(wenz_card_estimator)
        print("Estimating Wenz: " + str(probability))
        return probability

    def sauspiel_probability(self):
        max_probability = -1.0
        max_probability_called_suit = None

        for suit in Card.SUITS:
            game = Game("Sauspiel", suit) # get suit from context
            def sauspiel_card_estimator(card):
                if game.is_trump(card):
                    return { # TODO: test and tweak these values
                        "O": 0.12,
                        "U": 0.12,
                        "A": 0.10,
                        "X": 0.10,
                        "K": 0.07,
                        "9": 0.07,
                        "8": 0.07,
                        "7": 0.07
                    }[card.number]
                else:
                    return {
                        "A": 0.05,
                        "X": 0.03,
                        "K": 0.01,
                        "9": 0.00,
                        "8": 0.00,
                        "7": 0.00
                    }[card.number]

            probability = self.hand.evaluate(sauspiel_card_estimator)
            print("Estimating " + str(game) + ": " + str(probability))

            if probability > max_probability:
                max_probability = probability
                max_probability_called_suit = suit
        return max_probability, max_probability_called_suit

    def start_round(self, history):
        turn = Turn(self.name)
        self.play(turn, history)
        return turn

class HumanPlayer(Player):
    def __init__(self, name, player_id, hand):
        Player.__init__(self, name, player_id, hand)
