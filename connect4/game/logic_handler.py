

class LogicHandler:
    def __init__(self, board_handler):
        self.board_handler = board_handler
        self.winning_count = 4

    def get_valid_moves(self):
        empty_cols = []
        for col in range(self.board_handler.cols):
            if self.is_valid_col(col=col):
                empty_cols.append(col)
        return empty_cols

    def is_valid_col(self, col):
        if self.board_handler.matrix[0][col].type == 'blank':
            return True

        return False

    def get_first_empty_row(self, col):
        for row in reversed(range(self.board_handler.rows)):
            if self.board_handler.matrix[row][col].type == 'blank':
                return row

    def is_on_board(self, pos):
        x, y = pos

        if x <= self.board_handler.x or x >= self.board_handler.x + self.board_handler.width:
            return False

        if y <= self.board_handler.y or y >= self.board_handler.y + self.board_handler.height:
            return False

        return True

    def is_game_over(self, turn):
        # Horizontal Wins
        for row in range(self.board_handler.rows):
            for col in range(self.board_handler.cols - (self.winning_count - 1)):
                winning_pieces = []
                piece_count = 0

                for slot in range(self.winning_count):
                    if self.board_handler.matrix[row][col + slot].type == turn:
                        piece_count += 1
                        winning_pieces.append(self.board_handler.matrix[row][col + slot])
                    else:
                        break

                if piece_count == self.winning_count:
                    for piece in winning_pieces:
                        piece.is_winning_piece = True
                    return True

        # Vertical Wins
        for row in range(self.board_handler.rows - (self.winning_count - 1)):
            for col in range(self.board_handler.cols):
                winning_pieces = []
                piece_count = 0

                for slot in range(self.winning_count):
                    if self.board_handler.matrix[row + slot][col].type == turn:
                        piece_count += 1
                        winning_pieces.append(self.board_handler.matrix[row + slot][col])
                    else:
                        break
                
                if piece_count == self.winning_count:
                    for piece in winning_pieces:
                        piece.is_winning_piece = True
                    return True
        
        # Positivly Sloped Win
        for row in range(self.board_handler.rows - (self.winning_count - 1)):
            for col in range(self.board_handler.cols - (self.winning_count - 1)):
                winning_pieces = []
                piece_count = 0

                for slot in range(self.winning_count):
                    if self.board_handler.matrix[row + slot][col + slot].type == turn:
                        piece_count += 1
                        winning_pieces.append(self.board_handler.matrix[row + slot][col + slot])
                    else:
                        break

                if piece_count == self.winning_count:
                    for piece in winning_pieces:
                        piece.is_winning_piece = True
                    return True

        # Negativly Sloped Win
        for row in range(self.winning_count - 1, self.board_handler.rows):
            for col in range(self.board_handler.cols - (self.winning_count - 1)):
                winning_pieces = []
                piece_count = 0

                for slot in range(self.winning_count):
                    if self.board_handler.matrix[row - slot][col + slot].type == turn:
                        piece_count += 1
                        winning_pieces.append(self.board_handler.matrix[row - slot][col + slot])
                    else:
                        break

                if piece_count == self.winning_count:
                    for piece in winning_pieces:
                        piece.is_winning_piece = True
                    return True

        return False
