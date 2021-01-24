from .ai_handler import AIHandler
from .board_handler import BoardHandler
from .input_handler import InputHandler
from .render_handler import RenderHandler
from .turn_handler import TurnHandler
from ..engine.window_handler import WindowHandler


class GameHandler:
    def __init__(self, window_handler: WindowHandler):
        self.input_handler = InputHandler(game_handler=self)
        self.ai_handler = AIHandler(game_handler=self)
        self.turn_handler = TurnHandler(ai_handler=self.ai_handler)
        self.render_handler = RenderHandler(window_handler=window_handler, turn_handler=self.turn_handler)

        self.new_game()

    def think(self):
        self.input_handler.think()
        self.render_handler.board(board_handler=self.board_handler)

        if self.turn_handler.is_ai_turn() and not self.game_over:
            self.ai_handler.make_move()

    def next_round(self):
        lh = self.board_handler.logic_handler
        if lh.is_game_over(turn=self.turn_handler.turn) or lh.get_valid_moves == []:
            self.game_over = True
            return

        self.turn_handler.swap()

    def new_game(self):
        self.game_over = False
        self.turn_handler.pick_random()
        self.board_handler = BoardHandler()
