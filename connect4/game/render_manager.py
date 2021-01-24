import pygame
import math
import copy

from ..engine.window_manager import WindowManager
from .turn_manager import TurnManager
from .board_manager import BoardManager


class RenderManager:
    def __init__(self, window_manager: WindowManager, turn_manager: TurnManager):
        self.window_manager = window_manager
        self.turn_manager = turn_manager
        self.display = window_manager.display

        self.color_board = pygame.Color('#4a4a4a')
        self.color_hover = pygame.Color('#606060')
        self.color_victory = pygame.Color('#3e759c')

    def board(self, board_manager: BoardManager):
        board_manager = board_manager
        board_manager.calculate_dimentions(surface_size=(self.window_manager.width, self.window_manager.height))

        board_manager = copy.deepcopy(board_manager)

        self.display.fill(self.color_board)

        square_size = board_manager.height // board_manager.rows

        if not self.turn_manager.is_ai_turn():
            mouse_pos = pygame.mouse.get_pos()
            if board_manager.logic_manager.is_on_board(pos=mouse_pos):
                col = board_manager.get_coords(pos=mouse_pos)[1]
                x = board_manager.x + col * square_size
                pygame.draw.rect(self.display, self.color_hover, (x, board_manager.y, square_size, board_manager.height))

                if board_manager.logic_manager.is_valid_col(col=col):
                    type = self.turn_manager.turn + '_preview'
                    board_manager.drop_piece(col=col, type=type)

        piece_radius = square_size // 2 - square_size // 12

        for row in range(board_manager.rows):
            for col in range(board_manager.cols):
                x = board_manager.x + (col * square_size) + square_size // 2
                y = board_manager.y + (row * square_size) + square_size // 2

                color = board_manager.matrix[row][col].color

                pygame.draw.circle(self.display, color, (x, y), piece_radius)

                if board_manager.matrix[row][col].is_winning_piece:
                    self.star(board_manager, row, col, piece_radius - piece_radius // 4, piece_radius - piece_radius * 0.7 , 5)

        pygame.display.update()

    def star(self, board_manager: BoardManager, row, col, outer_radius, inner_radius, steps):
        steps = steps * 2
        step_size = 360 /  steps
        points = []

        square_size = board_manager.height // board_manager.rows

        for step in range(1, steps + 1):
            angle = step_size * step
            if step % 2:
                point = self.get_radial_pos(outer_radius, angle)
            else:
                point = self.get_radial_pos(inner_radius, angle)

            x = board_manager.x + col * square_size + square_size // 2 + point[0]
            y = board_manager.y + row * square_size + square_size // 2 + point[1]
            points.append((x, y))

        pygame.draw.polygon(self.display, self.color_victory, points)

    def get_radial_pos(self, radius, angle):
        x = radius * math.sin(math.pi * 2 * angle / 360)
        y = radius * math.cos(math.pi * 2 * angle / 360)
        return (x, y)