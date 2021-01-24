import random

from .ai_manager import AIManager


class TurnManager:
    def __init__(self, ai_manager: AIManager):
        self.ai_manager = ai_manager

    def swap(self):
        if self.turn == 'p1':
            self.turn = 'p2'
        else:
            self.turn = 'p1'

    def pick_random(self):
        self.turn = random.choice(('p1', 'p2'))
    
    def is_ai_turn(self):
        if self.ai_manager.all_player:
            return True

        if self.ai_manager.opponent and self.turn == 'p2':
            return True

        return False
