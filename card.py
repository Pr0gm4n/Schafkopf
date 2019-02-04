""" Models a single card of a bavarian deck of cards. Supports 
"""
class Card:
    SUITS = {
        "e": "Eichel",
        "g": "Gras",
        "h": "Herz",
        "s": "Schellen"
    }
    NUMBERS = ["A", "X", "K", "O", "U", "9", "8", "7"]

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
        self.binding_suit = suit # used to determine which cards may be chosen in this round

        # initially order as if hearts were trump
        if number in ["O", "U"] or suit == "h":
            self.binding_suit = "t"

    def __repr__(self):
        return self.suit + "+" + self.number

    def __str__(self):
        return self.suit + "-" + self.number

    # using lexical ordering
    def order(self):
        return self.suit + "-" + str(Card.NUMBERS.index(self.number))

    # using lexical ordering
    def binding_order(self):
        return self.binding_suit + "-" + str(Card.NUMBERS.index(self.number))

    def adapt_to(self, game):
        if game.is_trump(self):
            self.binding_suit = "t"
        else:
            self.binding_suit = self.suit

    def __lt__(self, other): # used for sorting
        if (self.binding_suit == "t") ^ (other.binding_suit == "t"): # exactly one trump
            return self.binding_suit == "t"

        elif self.binding_suit == "t": # both trump
            if (self.number == "O") ^ (other.number == "O"): # exactly one Ober
                return self.number == "O"
            elif (self.number == "U") ^ (other.number == "U"): # exactly one Unter
                return self.number == "U"
            return self.order() < other.order() # order by the original suit names

        else: # no trump involved
            return self.binding_order() < other.binding_order()

    def __gt__(self, other): # used to determine whether a card beats another
        if (self.binding_suit == "t") or (other.binding_suit == "t") or (self.binding_suit == other.binding_suit): # trump involved or same (binding) suit
            return self < other # use sorting comparison
        else: # otherwise a card cannot beat another
            return False

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other
