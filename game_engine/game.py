import random
from .state import PlayerState, Card

def generateDeck(deck_size=30):
    """Gera um deck de cartas com atributos aleatórios."""
    # A soma dos atributos devem ser igual a mana_cost
    # Menos cartas de mana_cost 1, que podem atributos somados igual a 2 

    deck = []

    for i in range(deck_size):
        mana_cost = random.randint(1, 10)
        attack = random.randint(mana_cost-2, mana_cost+2)
        health = random.randint(mana_cost-3, mana_cost+3)

        deck.append(Card(f"Minion {i}", mana_cost=mana_cost, attack=attack, health=health))
    
    #shuffle the deck
    random.shuffle(deck)
    return deck


class Game:
    """Gerencia o jogo completo com dois jogadores e turnos."""
    def __init__(self):


        self.player1 = PlayerState(player_mana=1, health=30, deck=generateDeck())
        self.player2 = PlayerState(player_mana=1, health=30, deck=generateDeck())
        self.current_player = self.player1  
        self.opponent = self.player2
        self.turn = 1

        for _ in range(3):
            self.current_player.draw_card()
            
        for _ in range(4):
            self.opponent.draw_card()


    def switch_turn(self):
        self.current_player.max_mana = min(self.current_player.max_mana + 1, 10)
        self.current_player.player_mana = self.current_player.max_mana

        self.current_player, self.opponent = self.opponent, self.current_player
        self.turn += 1

        self.current_player.draw_card()
        for card in self.current_player.board:
            card.can_attack = True

    def play_card(self, card_index):
        return self.current_player.play_card(card_index)
    
    def attack(self, attacker_index, target):
        card = self.current_player.board[attacker_index]
        target_card = self.opponent.board[target] if target != -1 else None

        
        if target == -1:
            self.opponent.health -= card.attack
        else:
            target_card.health -= card.attack
            if target_card.health <= 0:
                self.opponent.board.pop(target)
            if card.health <= 0:
                self.current_player.board.pop(attacker_index)

        card.can_attack = False
    
    def is_game_over(self):
        return self.current_player.health <= 0 or self.opponent.health <= 0

    def copy(self):
      new_game = Game()
      new_game.player1 = self.player1.copy()
      new_game.player2 = self.player2.copy()
      new_game.current_player = new_game.player1 if self.current_player == self.player1 else new_game.player2
      new_game.opponent = new_game.player2 if self.opponent == self.player2 else new_game.player1
      new_game.turn = self.turn
      return new_game

    def __str__(self):
        return (f"Turno: {self.turn}\n"
                f"Jogador Ativo:\n{self.current_player}\n"
                f"Oponente:\n{self.opponent}")
    

