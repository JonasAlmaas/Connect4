import random

from .ai_handler import AIHandler


class TurnHandler:
    def __init__(self, ai_handler: AIHandler):
        self.ai_handler = ai_handler

    def swap(self):
        if self.turn == 'p1':
            self.turn = 'p2'
        else:
            self.turn = 'p1'

    def pick_random(self):
        self.turn = random.choice(('p1', 'p2'))
    
    def is_ai_turn(self):
        if self.ai_handler.all_player:
            return True

        if self.ai_handler.opponent and self.turn == 'p2':
            return True

        return False
