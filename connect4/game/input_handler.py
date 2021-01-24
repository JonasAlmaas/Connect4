import pygame


class InputHandler:
    '''Input handler for the game'''

    def __init__(self, game_handler):
        self.game_handler = game_handler

    def think(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_handler.new_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                if self.game_handler.game_over:
                    self.game_handler.new_game()

                if self.game_handler.turn_handler.is_ai_turn():
                    return

                else:
                    if not self.game_handler.board_handler.logic_handler.is_on_board(pos=pos):
                        return

                    col = self.game_handler.board_handler.get_coords(pos)[1]

                    if not self.game_handler.board_handler.logic_handler.is_valid_col(col=col):
                        return

                    self.game_handler.board_handler.drop_piece(col=col, type=self.game_handler.turn_handler.turn)

                    self.game_handler.next_round()
