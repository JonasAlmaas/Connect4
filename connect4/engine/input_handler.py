import pygame


class InputHandler:
    '''Input handler for the application'''

    def __init__(self, app_handler):
        self.app_handler = app_handler

    def think(self):
        if pygame.event.peek(pygame.QUIT):
            self.app_handler.should_close = True
