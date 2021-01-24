import pygame


colors = {
    'blank': pygame.Color('#999999'),
    'p1': pygame.Color('#e8f53d'),
    'p1_preview': pygame.Color('#bcc775'),
    'p2': pygame.Color('#e63939'),
    'p2_preview': pygame.Color('#cc9191')
    }


class PieceManager:
    def __init__(self, type):
        self.set_type(type)
        self.is_winning_piece = False

    def set_type(self, type):
        self.type = type
        self.color = colors[self.type]
