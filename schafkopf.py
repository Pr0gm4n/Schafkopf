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
    self.binding_suit = suit

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

  def __lt__(self, other):
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

  def __eq__(self, other):
    return self.__repr__() == other.__repr__()

  def __le__(self, other):
    return self < other or self == other

  def __ge__(self, other):
    return self > other or self == other


class Hand:
  def __init__(self, cards):
    self.cards = cards

  def get_cards(self, suit):
    cards = []
    for card in self.cards:
      if card.suit == suit:
        cards.append(card)
    if len(cards) == 0:
      return self.cards
    return cards

  def play(self, card):
    self.cards.remove(card)

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

  Random().shuffle(deck)

  players = []
  for player in range(4):
    cards = []
    for card in range(8):
      cards.append(deck[8 * player + card])
    cards.sort()
    players.append(Player(str(player), Hand(cards)))

  print(players)

  players = cycle(players)

if __name__ == "__main__":
  # execute only if run as a script
  main()
