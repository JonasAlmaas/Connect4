import pygame


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
                pygame.draw.circle(var.screen, const.COLOR_HEIGHLIGHT_VICTORY, (c*const.SQUARE_SIZE+const.SQUARE_SIZE/2, (const.SCREEN_HEIGTH-const.SQUARE_SIZE)-r*const.SQUARE_SIZE+const.SQUARE_SIZE/2), const.PIECE_RADIUS/2)

    pygame.display.update()