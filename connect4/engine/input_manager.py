import pygame


class InputManager:
    '''Input manager for the application'''

    def __init__(self, app_manager):
        self.app_manager = app_manager

    def think(self):
        if pygame.event.peek(pygame.QUIT):
            self.app_manager.should_close = True
