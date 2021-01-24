import random
import sys
import copy

from numpy.matrixlib.defmatrix import matrix

from .board_manager import BoardManager
from .evaluation_manager import EvaluationManager


class AIManager:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.evaluation_manager = EvaluationManager()

        self.all_boards = {}

        self.opponent = True
        self.all_player = False

        self.depth = 5

    def make_move(self):
        self.best_move()
        # self.random_move()
        self.game_manager.next_round()

    def random_move(self):
        empty_cols = self.game_manager.board_manager.logic_manager.get_valid_moves()

        if empty_cols == []:
            self.game_manager.game_over = True
            return

        col = random.choice(empty_cols)
        team = self.game_manager.turn_manager.turn
        self.game_manager.board_manager.drop_piece(col=col, type=team)

    def best_move(self):
        board_manager = self.game_manager.board_manager
        team = self.game_manager.turn_manager.turn
        col = self.minimax(board_manager=board_manager, depth=self.depth, alpha=-sys.maxsize, beta=sys.maxsize, is_maximizing=True, team=team)[0]

        if col == None:
            print("This shouldn't happen, EVER!")
            return
        self.game_manager.board_manager.drop_piece(col=col, type=team)

    def minimax(self, board_manager: BoardManager, depth: int, alpha, beta, is_maximizing: bool, team: str):
        if team == 'p1':
            opponent = 'p2'
        else:
            opponent = 'p1'
        
        valid_moves = board_manager.logic_manager.get_valid_moves()
        is_terminal = valid_moves == [] or board_manager.logic_manager.is_game_over(turn=team) or board_manager.logic_manager.is_game_over(turn=opponent)

        if depth == 0 or is_terminal:
            if is_terminal:
                if board_manager.logic_manager.is_game_over(turn=team):
                    return (None, sys.maxsize)
                elif board_manager.logic_manager.is_game_over(turn=opponent):
                    return (None, -sys.maxsize)
                else:
                    return (None, 0)
            else:
                return (None, self.evaluation_manager.evaluate_board(board_manager=board_manager, team=team))

        if is_maximizing:
            value = -sys.maxsize
            column = None
            for col in valid_moves:
                board_manager_copy = copy.deepcopy(board_manager)
                board_manager_copy.drop_piece(col=col, type=team)
                new_score = self.minimax(board_manager=board_manager_copy, depth=depth-1, alpha=alpha, beta=beta, is_maximizing=False, team=team)[1]
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
                board_manager_copy = copy.deepcopy(board_manager)
                board_manager_copy.drop_piece(col=col, type=opponent)
                new_score = self.minimax(board_manager=board_manager_copy, depth=depth-1, alpha=alpha, beta=beta, is_maximizing=True, team=team)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return (column, value)
