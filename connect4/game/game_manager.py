from .ai_manager import AIManager
from .board_manager import BoardManager
from .input_manager import InputManager
from .render_manager import RenderManager
from .turn_manager import TurnManager
from ..engine.window_manager import WindowManager


class GameManager:
    def __init__(self, window_manager: WindowManager):
        self.input_manager = InputManager(game_manager=self)
        self.ai_manager = AIManager(game_manager=self)
        self.turn_manager = TurnManager(ai_manager=self.ai_manager)
        self.render_manager = RenderManager(window_manager=window_manager, turn_manager=self.turn_manager)

        self.new_game()

    def think(self):
        self.input_manager.think()
        self.render_manager.board(board_manager=self.board_manager)

        if self.turn_manager.is_ai_turn() and not self.game_over:
            self.ai_manager.make_move()

    def next_round(self):
        lh = self.board_manager.logic_manager
        if lh.is_game_over(turn=self.turn_manager.turn) or lh.get_valid_moves == []:
            self.game_over = True
            return

        self.turn_manager.swap()

    def new_game(self):
        self.game_over = False
        self.turn_manager.pick_random()
        self.board_manager = BoardManager()
