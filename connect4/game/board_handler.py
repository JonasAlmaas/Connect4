from .piece_handler import PieceHandler
from .logic_handler import LogicHandler


class BoardHandler:
    def __init__(self, rows: int = 6, cols: int = 7):
        self.rows = rows
        self.cols = cols

        self.logic_handler = LogicHandler(board_handler=self)

        self.margin_top = 15
        self.matrix = [[PieceHandler(type='blank') for _ in range(self.cols)] for _ in range(self.rows)]

        self.width = 0
        self.hight = 0
        self.x = 0
        self.y = 0

    def drop_piece(self, col, type):
        row = self.logic_handler.get_first_empty_row(col=col)
        self.matrix[row][col].set_type(type)

    def get_coords(self, pos):
        x, y= pos
        x = x - self.x
        y = y - self.y

        square_size = self.height // self.rows

        row = y // square_size
        col = x // square_size

        return (row, col)

    def calculate_dimentions(self, surface_size):
        surface_width, surface_hight = surface_size

        size_min = min(surface_width // self.cols, surface_hight // self.rows)

        if size_min == surface_hight // self.rows:
            self.height = surface_hight - self.margin_top * 2
            self.width = self.height // self.rows * self.cols
            self.y = self.margin_top
        else:
            self.width = surface_width - surface_width // 20
            self.height = self.width // self.cols * self.rows
            self.y = surface_hight // 2 - self.height // 2

        self.x = (surface_width - self.width) // 2
