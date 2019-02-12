from card import Card

class Game:
    MODES = ["weiter", "Sauspiel", "Wenz", "Solo"]

    def __init__(self, mode, suit=None):
        assert mode in Game.MODES
        assert not suit or suit in Card.SUITS

        self.mode = mode
        if self.mode == "Sauspiel":
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

    def __str__(self):
        if self.mode == "Sauspiel":
            return self.mode + " mit der " + Card.SUITS[self.called_suit] + " Sau"
        elif self.suit:
            return Card.SUITS[self.suit] + " " + self.mode
        else:
            return self.mode

    def __repr__(self):
        if self.suit:
            return self.mode + "+" + self.suit
        return self.mode
