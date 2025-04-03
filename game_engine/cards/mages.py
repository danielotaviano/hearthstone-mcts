

import random
from game_engine.game import Game
from game_engine.state import Card, CardType


class ArcaneExplosion(Card):
    def __init__(self):
        super().__init__(name="Arcane Explosion", mana_cost=2, card_type=CardType.SPELL, attack=0, health=0)
        self.description = "Deal 1 damage to all enemy minions."

    def spell(self, game: Game):
        enemy_board = game.opponent.board
        for card in enemy_board:
            card.health -= 1
            if card.health <= 0:
                game.opponent.board.remove(card)
        return True
        
class ArcaneIntellect(Card):
    def __init__(self):
        super().__init__(name="Arcane Intellect", mana_cost=3, card_type=CardType.SPELL, attack=0, health=0)
        self.description = "Draw 2 cards."

    def spell(self, game: Game):
        for _ in range(2):
            if not game.current_player.draw_card():
                break
        return True
    

class ArcaneMissile(Card):
    def __init__(self):
        super().__init__(name="Arcane Missile", mana_cost=1, card_type=CardType.SPELL, attack=0, health=0)
        self.description = "Deal 3 damage to the enemy hero or minion."

    def spell(self, game: Game):
        enemies = game.opponent.board + [game.opponent]

        choosed_enemies = random.choices(enemies, k=3)
        for enemy in choosed_enemies:
            if isinstance(enemy, Card):
                enemy.health -= 1
                if enemy.health <= 0:
                    game.opponent.board.remove(enemy)
            else:
                game.opponent.health -= 1
        return True
    

class Fireball(Card):
    def __init__(self):
        super().__init__(name="Fireball", mana_cost=4, card_type=CardType.SPELL, attack=0, health=0)
        self.description = "Deal 6 damage to a target."

    def spell(self, game: Game, target: int):
        if target == -1:
            game.opponent.health -= 6
        else:
            card = game.opponent.board[target]
            card.health -= 6
            if card.health <= 0:
                game.opponent.board.remove(card)
        return True
        