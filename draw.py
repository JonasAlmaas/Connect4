import pygame
import utils


def draw_star(var, const, r, c, outer_radius, inner_radius, steps):
    steps = steps * 2
    step_size = 360 /  steps
    points = []
    for step in range(1, steps + 1):
        angle = step_size * step
        if step % 2:
            point = utils.get_radial_pos(outer_radius, angle)
        else:
            point = utils.get_radial_pos(inner_radius, angle)
        x = c * const.SQUARE_SIZE + const.SQUARE_SIZE / 2 + point[0]
        y = (const.SCREEN_HEIGTH-const.SQUARE_SIZE) - r * const.SQUARE_SIZE + const.SQUARE_SIZE / 2 + point[1]
        points.append((x, y))
    pygame.draw.polygon(var.screen, const.COLOR_HEIGHLIGHT_VICTORY, points)


def board(board, const, var, heightlighted=None):
    for c in range(const.COLUMN_COUNT):
        for r in range(const.ROW_COUNT):
            if c == heightlighted:
                # Hover color when droping a piece
                pygame.draw.rect(var.screen, const.COLOR_HEIGHLIGHT_COLUMN, (c*const.SQUARE_SIZE, r*const.SQUARE_SIZE, const.SQUARE_SIZE, const.SQUARE_SIZE))
            else:
                # Board
                pygame.draw.rect(var.screen, const.COLOR_BOARD, (c*const.SQUARE_SIZE, r*const.SQUARE_SIZE, const.SQUARE_SIZE, const.SQUARE_SIZE))

            # Empty slots
            pygame.draw.circle(var.screen, const.COLOR_BACKGROUND, (c*const.SQUARE_SIZE+const.SQUARE_SIZE/2, r*const.SQUARE_SIZE+const.SQUARE_SIZE/2), const.PIECE_RADIUS)

    for c in range(const.COLUMN_COUNT):
        for r in range(const.ROW_COUNT):
            if board[r][c] == const.PLAYER_1 or board[r][c] == const.PLAYER_1_VICTORY_HEIGHTLIGHT:
                pygame.draw.circle(var.screen, const.COLOR_PLAYER_1, (c*const.SQUARE_SIZE+const.SQUARE_SIZE/2, (const.SCREEN_HEIGTH-const.SQUARE_SIZE)-r*const.SQUARE_SIZE+const.SQUARE_SIZE/2), const.PIECE_RADIUS)
            elif board[r][c] == const.PLAYER_2 or board[r][c] == const.PLAYER_2_VICTORY_HEIGHTLIGHT:
                pygame.draw.circle(var.screen, const.COLOR_PLAYER_2, (c*const.SQUARE_SIZE+const.SQUARE_SIZE/2, (const.SCREEN_HEIGTH-const.SQUARE_SIZE)-r*const.SQUARE_SIZE+const.SQUARE_SIZE/2), const.PIECE_RADIUS)
            elif board[r][c] == const.PLAYER_1_HOVER:
                pygame.draw.circle(var.screen, const.COLOR_PREVIEW_PLAYER_1, (c*const.SQUARE_SIZE+const.SQUARE_SIZE/2, (const.SCREEN_HEIGTH-const.SQUARE_SIZE)-r*const.SQUARE_SIZE+const.SQUARE_SIZE/2), const.PIECE_RADIUS)
            elif board[r][c] == const.PLAYER_2_HOVER:
                pygame.draw.circle(var.screen, const.COLOR_PREVIEW_PLAYER_2, (c*const.SQUARE_SIZE+const.SQUARE_SIZE/2, (const.SCREEN_HEIGTH-const.SQUARE_SIZE)-r*const.SQUARE_SIZE+const.SQUARE_SIZE/2), const.PIECE_RADIUS)
            # Draw victory markings
            if board[r][c] == const.PLAYER_1_VICTORY_HEIGHTLIGHT or board[r][c] == const.PLAYER_2_VICTORY_HEIGHTLIGHT:
                draw_star(var, const, r, c, 25, 10, 5)


            # if board[r][c] == const.PLAYER_1_VICTORY_HEIGHTLIGHT or board[r][c] == const.PLAYER_2_VICTORY_HEIGHTLIGHT:
            #     pygame.draw.circle(var.screen, const.COLOR_HEIGHLIGHT_VICTORY, (c*const.SQUARE_SIZE+const.SQUARE_SIZE/2, (const.SCREEN_HEIGTH-const.SQUARE_SIZE)-r*const.SQUARE_SIZE+const.SQUARE_SIZE/2), const.PIECE_RADIUS/2)

    pygame.display.update()
