from asyncio import sleep
import random
import time

from game_engine.game import Game
from game_engine.state import Card


class MCTSNode:
  def __init__(self, game_state, parent=None, action=None):
    self.game_state = game_state
    self.parent = parent
    self.children = []
    self.action = action
    self.visits = 0
    self.wins = 0

  def generate_possible_actions(self):
        """Gera todas as ações possíveis com base no estado do jogo e nas heurísticas."""
        game = self.game_state
        possible_actions = []

        # sem heurísticas
        for i, card in enumerate(game.current_player.hand):
            if card.mana_cost <= game.current_player.player_mana:
                if card.attack > 0 and card.health > 0:
                    if len(game.current_player.board) >= 7:
                        continue
                    possible_actions.append(('play', i, None))  # Lacaio
        for i, attacker in enumerate(game.current_player.board):
            if attacker.can_attack == False:
                continue
            for j, defender in enumerate(game.opponent.board):
                possible_actions.append(('attack', i, j))
            possible_actions.append(('attack', i, -1))

        # # Heurística 1: Não jogar lacaios que morrem imediatamente:
        # for i, card in enumerate(game.current_player.hand):
        #     if card.mana_cost <= game.current_player.player_mana:
        #         if card.attack > 0 and card.health > 0:
        #             if len(game.current_player.board) >= 7:  # Lacaio
        #                 continue
        #             dies_immediately = False
        #             for enemy in game.opponent.board:
        #                 if enemy.attack >= card.health and enemy.health > card.attack:
        #                     dies_immediately = True
        #                     break
        #             if not dies_immediately:
        #                 possible_actions.append(('play', i, None))
        #         else:  # Feitiço
        #             possible_actions.append(('play', i, None))

      
        # # Heurística 2: Priorizar trocas favoráveis no ataque
        # for i, attacker in enumerate(game.current_player.board):
        #     if attacker.can_attack == False:
        #         continue
        #     for j, defender in enumerate(game.opponent.board):
        #         if attacker.attack >= defender.health and defender.attack < attacker.health:
        #             possible_actions.append(('attack', i, j))  # Troca favorável
        #     possible_actions.append(('attack', i, -1))  # Ataque ao herói

        return possible_actions

  def is_fully_expanded(self):
    """Verifica se todas as ações possíveis foram exploradas."""
    explored_actions = {child.action for child in self.children}
    possible_actions = self.generate_possible_actions()

    # Verificar se todas as ações possíveis já foram exploradas
    for action in possible_actions:
        if action not in explored_actions:
            return False  # Ainda há ações não exploradas

    return True  # Todas as ações possíveis foram exploradas
  

  def best_child(self, exploration_weight=1.41):
    best_score = float('-inf')
    best_child = None
    for child in self.children:
      if child.visits == 0:
        return child
      score = (child.wins / child.visits) + exploration_weight * (
        (2*(self.visits**0.5)) / child.visits
      ) ** 0.5

      if score > best_score:
        best_score = score
        best_child = child

    return best_child
  

class MCTS:
  def __init__(self, game):
    self.root = MCTSNode(game)

  def select(self):
    current = self.root
    while current.children and current.is_fully_expanded():
      current = current.best_child()

    return current
  

  def expand(self, node):
    untried_actions = [
        action for action in node.generate_possible_actions()
        if action not in {child.action for child in node.children}
    ]


    if not untried_actions:
        return node

    # Escolher uma ação aleatória entre as não tentadas
    action = random.choice(untried_actions)
    new_game = node.game_state.copy()

    if action[0] == 'play':
        new_game.play_card(action[1])
    elif action[0] == 'attack':
        if action[2] == -1:
            new_game.attack(action[1], -1)
        else:
            new_game.attack(action[1], action[2])

    child = MCTSNode(new_game, parent=node, action=action)
    node.children.append(child)
    return child

  def simulate(self, node):
    game_copy = node.game_state.copy()
    for _ in range(20):
        node = MCTSNode(game_copy)
        if game_copy.is_game_over():
            break

        actions = node.generate_possible_actions()
        if actions:
            action = random.choice(actions)
            if action[0] == 'play':
              game_copy.play_card(action[1])
            elif action[0] == 'attack':
              if action[2] == -1:
                game_copy.attack(action[1], -1)
              else:
                game_copy.attack(action[1], action[2])

        game_copy.switch_turn()

    return 1 if game_copy.player2.health <= 0 else 0

    
  def backpropagate(self, node, result):
    current = node
    while current:
      current.visits += 1
      current.wins += result
      current = current.parent

  def run(self, iterations=100):
    for _ in range(iterations):
        node = self.select()
        if not node.is_fully_expanded():
            node = self.expand(node)
        result = self.simulate(node)
        self.backpropagate(node, result)

  def best_action(self):
    if not self.root.children:
      return None
  
    return max(self.root.children, key=lambda c: c.visits).action


def make_action(action, game):
    if action[0] == 'play':
        card = game.current_player.hand[action[1]]
        game.play_card(action[1])
        return f"Jogar {card.name} ({card.attack}/{card.health})"
    elif action[0] == 'attack':
        attacker = game.current_player.board[action[1]]
        if action[2] == -1:
            game.attack(action[1], -1)
            return f"Atacar o herói do oponente com {attacker.name} ({attacker.attack}/{attacker.health})"
        else:
            defender = game.opponent.board[action[2]]
            game.attack(action[1], action[2])
            return f"Atacar {defender.name} ({defender.attack}/{defender.health}) com {attacker.name} ({attacker.attack}/{attacker.health})"

if __name__ == "__main__":
    game = Game()

#     Estado do jogo após a ação:
# Turno: 6
# Jogador Ativo:
# Health: 26, Mana: 0/3, Hand: ['Minion 3 (Cost: 4, ATK: 1, HP: 1) WAKED: False)', 'Minion 4 (Cost: 5, ATK: 2, HP: 2) WAKED: False)', 'Minion 5 (Cost: 1, ATK: 3, HP: 3) WAKED: False)'], Board: ['Minion 0 (Cost: 1, ATK: 1, HP: -1) WAKED: False)', 'Minion 1 (Cost: 2, ATK: 2, HP: 1) WAKED: False)', 'Minion 2 (Cost: 3, ATK: 3, HP: 3) WAKED: False)'], Deck: 24 cards
# Oponente:
# Health: 28, Mana: 4/4, Hand: ['Minion 3 (Cost: 4, ATK: 1, HP: 1) WAKED: False)', 'Minion 4 (Cost: 5, ATK: 2, HP: 2) WAKED: False)', 'Minion 5 (Cost: 1, ATK: 3, HP: 3) WAKED: False)'], Board: ['Minion 1 (Cost: 2, ATK: 2, HP: 1) WAKED: False)', 'Minion 2 (Cost: 3, ATK: 3, HP: 3) WAKED: False)'], Deck: 24 cards

    # Testar troca favorável

    # game.player1.hand = [
    #     Card("Minion 3", mana_cost=4, attack=1, health=1),
    #     Card("Minion 4", mana_cost=5, attack=2, health=2),
    #     Card("Minion 5", mana_cost=1, attack=3, health=3)
    # ]

    # game.player2.hand = [
    #   Card("Minion 3", mana_cost=4, attack=1, health=1),
    #   Card("Minion 4", mana_cost=5, attack=2, health=2),
    #   Card("Minion 5", mana_cost=1, attack=3, health=3)
    # ]

    # game.player1.board = [
    #     Card("Minion 0", mana_cost=1, attack=1, health=-1),
    #     Card("Minion 1", mana_cost=2, attack=2, health=1),
    #     Card("Minion 2", mana_cost=3, attack=3, health=3)
    # ]

    # game.player2.board = [
    # ]

    # # print("Estado inicial:")
    # # print(game)
    # mcts = MCTS(game.copy())
    # mcts.run(iterations=1)
    # best_action = mcts.best_action()

    
    # print(f"\nMelhor ação: {best_action}")
  

      

    while not game.is_game_over():
        while True:
            mcts = MCTS(game.copy())
            mcts.run(iterations=10000)
            best_action = mcts.best_action()

            if best_action is None:
                print("\nNenhuma ação possível. Encerrando turno.")
                break  # Sai do loop interno para trocar o turno
            else:
                print(f"\nMelhor ação: {best_action}")
                action_description = make_action(best_action, game)
                print(f"Ação executada: {action_description}")

            print("\nEstado do jogo após a ação:")
            print(game)

            # Verifica se o jogo acabou após a ação
            if game.is_game_over():
                break

        # Troca de turno
        if not game.is_game_over():
            game.switch_turn()
            print("\nApós troca de turno:")
            print(game)

    # Fim do jogo
    print("\nFim do jogo!")
    if game.player1.health <= 0:
        print("Jogador 2 venceu!")
    elif game.player2.health <= 0:
        print("Jogador 1 venceu!")
    else:
        print("Empate!")


    # while not game.is_game_over():
    #     mcts.run(iterations=100)
    #     best_action = mcts.best_action()
    #     while best_action is not None:
    #         print(f"\nMelhor ação: {best_action}")
    #         if best_action:
    #             if best_action[0] == 'play':
    #                 print(f"Jogando carta: {game.current_player.hand[best_action[1]]}")
    #                 game.play_card(best_action[1])
    #             elif best_action[0] == 'attack':
    #                 game.attack(best_action[1], best_action[2])
            
    #         print("Após executar a melhor ação:")
    #         print(game)
    #         mcts = MCTS(game.copy())
    #         mcts.run(iterations=100)
    #         best_action = mcts.best_action()
    #         time.sleep(5)
    
    #     print("\nApós executar todas as melhores ações:")
    #     print(game)
    #     game.switch_turn()
        


    # print("Após fim do jogo:")
    # print(game)

    # mcts.run(iterations=100)
    # best_action = mcts.best_action()
    # print(f"\nMelhor ação: {best_action}")
    # if best_action:
    #     if best_action[0] == 'play':
    #         print(f"Jogando carta: {game.current_player.hand[best_action[1]]}")
    #         game.play_card(best_action[1])
    #     elif best_action[0] == 'attack':
    #         game.attack(best_action[1], best_action[2])
    
    
    # print("Após executar a melhor ação:")
    # print(game)