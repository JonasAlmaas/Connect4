import time

from ..game.game_manager import GameManager
from .input_manager import InputManager
from .window_manager import WindowManager


class ApplicationManager:
    def __init__(self):
        self.refresh_rate = 128
        self.last_refresh = 0

        self.input_manager = InputManager(app_manager=self)
        self.window_manager = WindowManager(title='Connect 4', width=1200, height=1000)
        self.game_manager = GameManager(window_manager=self.window_manager)

        self.should_close = False
        while not self.should_close:
            self.think()

    def think(self):
        if time.time() - self.last_refresh < 1 / self.refresh_rate:
            wait_time = (1 / self.refresh_rate) - (time.time() - self.last_refresh)
            time.sleep(wait_time)

        self.last_refresh = time.time()

        self.input_manager.think()
        self.window_manager.think()
        self.game_manager.think()
