from game_engine.state import Card, CardType


class BloodfenRaptor(Card):
    def __init__(self):
        super().__init__(name="Bloodfen Raptor", mana_cost=2, attack=3, health=2)
        self.description = "A 3/2 beast minion."
        self.card_type = CardType.MINION



class BoulderfistOgre(Card):
    def __init__(self):
        super().__init__(name="Boulderfist Ogre", mana_cost=6, attack=6, health=7)
        self.description = "A 6/7 ogre minion."
        self.card_type = CardType.MINION
        
    