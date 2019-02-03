class Turn:
    def __init__(self, initiator, suit = None):
        self.initiator = initiator
        self.suit = suit
        self.cards = []
        self.winner_card = None
        self.winner = -1

    def get_suit(self):
        return self.suit

    def add_card(self, card):
        assert len(self.cards) < 4
        if self.suit is None:
            self.suit = card.binding_suit
        if self.winner_card is None or card > self.winner_card:
            self.winner_card = card
            self.winner = len(self.cards)
        self.cards.append(card)
