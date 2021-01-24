import pygame
import math
import copy

from ..engine.window_handler import WindowHandler
from .turn_handler import TurnHandler
from .board_handler import BoardHandler


class RenderHandler:
    def __init__(self, window_handler: WindowHandler, turn_handler: TurnHandler):
        self.window_handler = window_handler
        self.turn_handler = turn_handler
        self.display = window_handler.display

        self.color_board = pygame.Color('#4a4a4a')
        self.color_hover = pygame.Color('#606060')
        self.color_victory = pygame.Color('#3e759c')

    def board(self, board_handler: BoardHandler):
        board_handler = board_handler
        board_handler.calculate_dimentions(surface_size=(self.window_handler.width, self.window_handler.height))

        board_handler = copy.deepcopy(board_handler)

        self.display.fill(self.color_board)

        square_size = board_handler.height // board_handler.rows

        if not self.turn_handler.is_ai_turn():
            mouse_pos = pygame.mouse.get_pos()
            if board_handler.logic_handler.is_on_board(pos=mouse_pos):
                col = board_handler.get_coords(pos=mouse_pos)[1]
                x = board_handler.x + col * square_size
                pygame.draw.rect(self.display, self.color_hover, (x, board_handler.y, square_size, board_handler.height))

                if board_handler.logic_handler.is_valid_col(col=col):
                    type = self.turn_handler.turn + '_preview'
                    board_handler.drop_piece(col=col, type=type)

        piece_radius = square_size // 2 - square_size // 12

        for row in range(board_handler.rows):
            for col in range(board_handler.cols):
                x = board_handler.x + (col * square_size) + square_size // 2
                y = board_handler.y + (row * square_size) + square_size // 2

                color = board_handler.matrix[row][col].color

                pygame.draw.circle(self.display, color, (x, y), piece_radius)

                if board_handler.matrix[row][col].is_winning_piece:
                    self.star(board_handler, row, col, piece_radius - piece_radius // 4, piece_radius - piece_radius * 0.7 , 5)

        pygame.display.update()

    def star(self, board_handler: BoardHandler, row, col, outer_radius, inner_radius, steps):
        steps = steps * 2
        step_size = 360 /  steps
        points = []

        square_size = board_handler.height // board_handler.rows

        for step in range(1, steps + 1):
            angle = step_size * step
            if step % 2:
                point = self.get_radial_pos(outer_radius, angle)
            else:
                point = self.get_radial_pos(inner_radius, angle)

            x = board_handler.x + col * square_size + square_size // 2 + point[0]
            y = board_handler.y + row * square_size + square_size // 2 + point[1]
            points.append((x, y))

        pygame.draw.polygon(self.display, self.color_victory, points)

    def get_radial_pos(self, radius, angle):
        x = radius * math.sin(math.pi * 2 * angle / 360)
        y = radius * math.cos(math.pi * 2 * angle / 360)
        return (x, y)