from .board_handler import BoardHandler


class EvaluationHandler:
    def evaluate_board(self, board_handler: BoardHandler, team):
        score = 0
        matrix = board_handler.matrix
        self.winning_count = board_handler.logic_handler.winning_count

        # Evaluate Horizontal
        for row in range(board_handler.rows):
            for col in range(board_handler.cols - (self.winning_count - 1)):
                window = [(matrix[row][col + i].type) for i in range(self.winning_count)]
                score += self.evaluate_window(window=window, team=team)

        # Evaluate Vertical
        for row in range(board_handler.rows - (self.winning_count - 1)):
            for col in range(board_handler.cols):
                window = [(matrix[row + i][col].type) for i in range(self.winning_count)]
                score += self.evaluate_window(window=window, team=team)

        # Evaluate Positivly Sloped
        for row in range(board_handler.rows - (self.winning_count - 1)):
            for col in range(board_handler.cols - (self.winning_count - 1)):
                window = [(matrix[row + i][col + i].type) for i in range(self.winning_count)]
                score += self.evaluate_window(window=window, team=team)

        # Evaluate Negativly Sloped
        for row in range(board_handler.rows - (self.winning_count - 1)):
            for col in range(board_handler.cols - (self.winning_count - 1)):
                window = [(matrix[row - i][col + i].type) for i in range(self.winning_count)]
                score += self.evaluate_window(window=window, team=team)

        return score

    def evaluate_window(self, window, team):
        score = 0

        if team == 'p1':
            opponent = 'p2'
        else:
            opponent = 'p1'

        for i in range(self.winning_count - 1):
            if window.count(team) == self.winning_count - i and window.count('blank') == i:
                score += self.winning_count - i

                if i == 0:
                    score += 10000

            if window.count(opponent) == self.winning_count - i and window.count('blank') == i:
                score -= self.winning_count - i

                if i == 0:
                    score -= 10000

        return score
