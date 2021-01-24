import pygame


class InputManager:
    '''Input manager for the game'''

    def __init__(self, game_manager):
        self.game_manager = game_manager

    def think(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_manager.new_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                if self.game_manager.game_over:
                    self.game_manager.new_game()

                if self.game_manager.turn_manager.is_ai_turn():
                    return

                else:
                    if not self.game_manager.board_manager.logic_manager.is_on_board(pos=pos):
                        return

                    col = self.game_manager.board_manager.get_coords(pos)[1]

                    if not self.game_manager.board_manager.logic_manager.is_valid_col(col=col):
                        return

                    self.game_manager.board_manager.drop_piece(col=col, type=self.game_manager.turn_manager.turn)

                    self.game_manager.next_round()
