

class LogicManager:
    def __init__(self, board_manager):
        self.board_manager = board_manager
        self.winning_count = 4

    def get_valid_moves(self):
        empty_cols = []
        for col in range(self.board_manager.cols):
            if self.is_valid_col(col=col):
                empty_cols.append(col)
        return empty_cols

    def is_valid_col(self, col):
        if self.board_manager.matrix[0][col].type == 'blank':
            return True

        return False

    def get_first_empty_row(self, col):
        for row in reversed(range(self.board_manager.rows)):
            if self.board_manager.matrix[row][col].type == 'blank':
                return row

    def is_on_board(self, pos):
        x, y = pos

        if x <= self.board_manager.x or x >= self.board_manager.x + self.board_manager.width:
            return False

        if y <= self.board_manager.y or y >= self.board_manager.y + self.board_manager.height:
            return False

        return True

    def is_game_over(self, turn):
        # Horizontal Wins
        for row in range(self.board_manager.rows):
            for col in range(self.board_manager.cols - (self.winning_count - 1)):
                winning_pieces = []
                piece_count = 0

                for slot in range(self.winning_count):
                    if self.board_manager.matrix[row][col + slot].type == turn:
                        piece_count += 1
                        winning_pieces.append(self.board_manager.matrix[row][col + slot])
                    else:
                        break

                if piece_count == self.winning_count:
                    for piece in winning_pieces:
                        piece.is_winning_piece = True
                    return True

        # Vertical Wins
        for row in range(self.board_manager.rows - (self.winning_count - 1)):
            for col in range(self.board_manager.cols):
                winning_pieces = []
                piece_count = 0

                for slot in range(self.winning_count):
                    if self.board_manager.matrix[row + slot][col].type == turn:
                        piece_count += 1
                        winning_pieces.append(self.board_manager.matrix[row + slot][col])
                    else:
                        break
                
                if piece_count == self.winning_count:
                    for piece in winning_pieces:
                        piece.is_winning_piece = True
                    return True
        
        # Positivly Sloped Win
        for row in range(self.board_manager.rows - (self.winning_count - 1)):
            for col in range(self.board_manager.cols - (self.winning_count - 1)):
                winning_pieces = []
                piece_count = 0

                for slot in range(self.winning_count):
                    if self.board_manager.matrix[row + slot][col + slot].type == turn:
                        piece_count += 1
                        winning_pieces.append(self.board_manager.matrix[row + slot][col + slot])
                    else:
                        break

                if piece_count == self.winning_count:
                    for piece in winning_pieces:
                        piece.is_winning_piece = True
                    return True

        # Negativly Sloped Win
        for row in range(self.winning_count - 1, self.board_manager.rows):
            for col in range(self.board_manager.cols - (self.winning_count - 1)):
                winning_pieces = []
                piece_count = 0

                for slot in range(self.winning_count):
                    if self.board_manager.matrix[row - slot][col + slot].type == turn:
                        piece_count += 1
                        winning_pieces.append(self.board_manager.matrix[row - slot][col + slot])
                    else:
                        break

                if piece_count == self.winning_count:
                    for piece in winning_pieces:
                        piece.is_winning_piece = True
                    return True

        return False
