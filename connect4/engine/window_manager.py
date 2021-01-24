import pygame


class WindowManager:
    def __init__(self, title: str = 'Title', width: int = 900, height: int = 700):
        pygame.init()

        pygame.display.set_caption(title)

        self.display = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def think(self):
        self.width = self.display.get_size()[0]
        self.height = self.display.get_size()[1]
