from card import Card

class Game:
    MODES = ["weiter", "Sauspiel", "Wenz", "Solo"]

    def __init__(self, mode, suit=None):
        assert mode in Game.MODES
        self.mode = mode
        assert suit in Card.SUITS
        if mode == "Sauspiel":
            # for correctly ordering the cards, see Game.is_trump() for details
            self.suit = "h"
            self.called_suit = suit
        else:
            self.suit = suit

    def is_trump(self, card):
        if self.mode == "weiter":
            return False
        elif self.mode == "Wenz":
            return card.number == "U"
        else: # treat "Sauspiel" as a "Solo" with the suit "h"
            return card.number in ["O", "U"] or card.suit == self.suit

    def __gt__(self, other): # used to determine whether a game beats another
        if not other:
            return True
        return Game.MODES.index(self.mode) > Game.MODES.index(other.mode)

    def __eq__(self, other):
        if not other:
            return False
        return self.mode == other.mode
