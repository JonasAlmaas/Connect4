import random
import sys
import copy

from numpy.matrixlib.defmatrix import matrix

from .board_handler import BoardHandler
from .evaluation_handler import EvaluationHandler


class AIHandler:
    def __init__(self, game_handler):
        self.game_handler = game_handler
        self.evaluation_handler = EvaluationHandler()

        self.all_boards = {}

        self.opponent = True
        self.all_player = False

        self.depth = 5

    def make_move(self):
        self.best_move()
        # self.random_move()
        self.game_handler.next_round()

    def random_move(self):
        empty_cols = self.game_handler.board_handler.logic_handler.get_valid_moves()

        if empty_cols == []:
            self.game_handler.game_over = True
            return

        col = random.choice(empty_cols)
        team = self.game_handler.turn_handler.turn
        self.game_handler.board_handler.drop_piece(col=col, type=team)

    def best_move(self):
        board_handler = self.game_handler.board_handler
        team = self.game_handler.turn_handler.turn
        col = self.minimax(board_handler=board_handler, depth=self.depth, alpha=-sys.maxsize, beta=sys.maxsize, is_maximizing=True, team=team)[0]

        if col == None:
            print("This shouldn't happen, EVER!")
            return
        self.game_handler.board_handler.drop_piece(col=col, type=team)

    def minimax(self, board_handler: BoardHandler, depth: int, alpha, beta, is_maximizing: bool, team: str):
        if team == 'p1':
            opponent = 'p2'
        else:
            opponent = 'p1'
        
        valid_moves = board_handler.logic_handler.get_valid_moves()
        is_terminal = valid_moves == [] or board_handler.logic_handler.is_game_over(turn=team) or board_handler.logic_handler.is_game_over(turn=opponent)

        if depth == 0 or is_terminal:
            if is_terminal:
                if board_handler.logic_handler.is_game_over(turn=team):
                    return (None, sys.maxsize)
                elif board_handler.logic_handler.is_game_over(turn=opponent):
                    return (None, -sys.maxsize)
                else:
                    return (None, 0)
            else:
                return (None, self.evaluation_handler.evaluate_board(board_handler=board_handler, team=team))

        if is_maximizing:
            value = -sys.maxsize
            column = None
            for col in valid_moves:
                board_handler_copy = copy.deepcopy(board_handler)
                board_handler_copy.drop_piece(col=col, type=team)
                new_score = self.minimax(board_handler=board_handler_copy, depth=depth-1, alpha=alpha, beta=beta, is_maximizing=False, team=team)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return (column, value)
        else:
            value = sys.maxsize
            column = None
            for col in valid_moves:
                board_handler_copy = copy.deepcopy(board_handler)
                board_handler_copy.drop_piece(col=col, type=opponent)
                new_score = self.minimax(board_handler=board_handler_copy, depth=depth-1, alpha=alpha, beta=beta, is_maximizing=True, team=team)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return (column, value)
