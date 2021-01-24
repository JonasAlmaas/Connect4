import time

from ..game.game_handler import GameHandler
from .input_handler import InputHandler
from .window_handler import WindowHandler


class ApplicationHandler:
    def __init__(self):
        self.refresh_rate = 128
        self.last_refresh = 0

        self.input_handler = InputHandler(app_handler=self)
        self.window_handler = WindowHandler(title='Connect 4', width=1200, height=1000)
        self.game_handler = GameHandler(window_handler=self.window_handler)

        self.should_close = False
        while not self.should_close:
            self.think()

    def think(self):
        if time.time() - self.last_refresh < 1 / self.refresh_rate:
            wait_time = (1 / self.refresh_rate) - (time.time() - self.last_refresh)
            time.sleep(wait_time)

        self.last_refresh = time.time()

        self.input_handler.think()
        self.window_handler.think()
        self.game_handler.think()
