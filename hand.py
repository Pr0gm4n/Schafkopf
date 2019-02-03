class Hand:
    def __init__(self, cards):
        self.cards = cards

    # TODO: make sure that game mode "Sauspiel" is incorporated correctly
    def get_playable_cards(self, suit):
        if suit is None: # first player has (almost) free choice
            return self.cards
        cards = []
        for card in self.cards:
            if card.binding_suit == suit:
                cards.append(card)
        if len(cards) == 0: # if no card of the given suit is available, we are not bound by any rules
            return self.cards
        return cards

    def play(self, card):
        self.cards.remove(card)
        print("played card", card)

    def __repr__(self):
        return " ".join([str(x) for x in self.cards])
