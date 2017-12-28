#!/usr/bin/python3


from random import SystemRandom as Random
from itertools import cycle


SUITS = {
  "e": "Eichel",
  "g": "Gras",
  "h": "Herz",
  "s": "Schellen"
}
NUMBERS = ["A", "X", "K", "O", "U", "9", "8", "7"]


class Card:
  def __init__(self, suit, number):
    self.suit = suit
    self.number = number
    self.binding_suit = suit # used to determine which cards may be chosen in this round

    # initially order as if hearts were trump
    if number in ["U", "O"] or suit is "h":
      self.binding_suit = "t"

  def __repr__(self):
    return self.suit + "+" + self.number

  def __str__(self):
    return self.suit + "-" + self.number

  def order(self):
    return self.suit + "-" + str(NUMBERS.index(self.number))

  def binding_order(self):
    return self.binding_suit + "-" + str(NUMBERS.index(self.number))

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


class Hand:
  def __init__(self, cards):
    self.cards = cards

  # TODO: make sure that game mode "Sauspiel" is incorporated correctly
  def get_cards(self, suit):
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
    repr = ""
    for card in self.cards:
      repr += str(card) + " "
    return repr[:-1]


class Player:
  def __init__(self, name, hand):
    self.name = name
    self.hand = hand
    self.stack = []
    #self.game = 

  def __repr__(self):
    return "Player " + self.name + "\n" \
         + "---------------"     + "\n" \
         + self.hand.__repr__()  + "\n"

  def play(self, turn = None):
    if turn is None:
      turn = Turn()
    print("Player", self.name, "may put down", self.hand.get_cards(turn.get_suit()))

    global rand
    choice = rand.choice(self.hand.get_cards(turn.get_suit()))
    self.hand.play(choice)
    turn.add_card(choice)
    return turn


class Turn:
  def __init__(self, suit = None):
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


def main():
  global SUITS
  global NUMBERS
  # for interactive shell
  global deck
  global players

  deck = []
  for suit in SUITS.keys():
    for number in NUMBERS:
      deck.append(Card(suit, number))

  global rand
  rand = Random()
  rand.shuffle(deck)

  players = []
  for player in range(4):
    cards = []
    for card in range(8):
      cards.append(deck[8 * player + card])
    cards.sort()
    players.append(Player(str(player), Hand(cards)))

  print(players)

  players = cycle(players)

  turn = next(players).play()
  for i in range(3):
    next(players).play(turn)

if __name__ == "__main__":
  # execute only if run as a script
  main()
