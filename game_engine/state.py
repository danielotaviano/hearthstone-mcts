from enum import Enum
from nanoid import generate


class CardType(Enum):
  MINION = "MINION"
  SPELL = "SPELL"
  WEAPON = "WEAPON"

class Card:
  def __init__(self, name, mana_cost, card_type: CardType, attack=0, health=0,  can_attack=False):
    self.id = generate(size=5)
    self.name = name
    self.mana_cost = mana_cost
    self.attack = attack
    self.health = health
    self.can_attack = can_attack
    self.card_type = card_type

  def battlecry(self, game):
    return
  
  def spell(self):
    return
  
  def copy(self):
    return Card(self.name, self.mana_cost, self.attack, self.health, self.can_attack)

  def __str__(self):
    return (f"({self.id}) {self.name} (Cost: {self.mana_cost}, ATK: {self.attack}, HP: {self.health}) WAKED: {self.can_attack})")


class PlayerState:
  def __init__(self, player_mana=1, health=30, deck=None, hand=None, board=None):
    self.player_mana = player_mana
    self.max_mana = player_mana
    self.health = health
    self.deck = deck if deck is not None else []
    self.hand = hand if hand is not None else []
    self.board = board if board is not None else []
    

  def draw_card(self):
    card = self.deck.pop(0)
    if self.deck and len(self.hand) < 10:
      self.hand.append(card)
      return True
    return False
  
  def play_card(self, card_index):
    if card_index < 0 or card_index >= len(self.hand) or len(self.board) >= 7:
      return False
    
    card = self.hand[card_index]
    if card.mana_cost > self.player_mana:
      return False
    
    self.hand.pop(card_index)
    self.player_mana -= card.mana_cost
    if card.attack > 0 and card.health > 0: 
      self.board.append(card)
    return True
    
  def copy(self):
    new_player = PlayerState(
        player_mana=self.player_mana,
        health=self.health,
        deck=[card.copy() for card in self.deck],
        hand=[card.copy() for card in self.hand],
        board=[card.copy() for card in self.board]
    )
    return new_player

  
  def __str__(self):
        return (f"Health: {self.health}, Mana: {self.player_mana}/{self.max_mana}, "
                f"Hand: {[str(c) for c in self.hand]}, "
                f"Board: {[str(c) for c in self.board]}, "
                f"Deck: {len(self.deck)} cards")
  



