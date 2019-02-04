class Game:
    MODES = ["weiter", "Sauspiel", "Wenz", "Solo"]

    def __init__(self, mode, suit=None):
        self.mode = mode

    def __gt__(self, other): # used to determine whether a game beats another
        if not other:
            return True
        return Game.MODES.index(self.mode) > Game.MODES.index(other.mode)

    def __eq__(self, other):
        if not other:
            return False
        return self.mode == other.mode
