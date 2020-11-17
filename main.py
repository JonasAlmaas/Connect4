import pygame
import numpy as np
import sys
import random
import math

import draw


class Constants():
    def __init__(self):
        self.AI_PLAYER = True                                                   # Use if you don't have any friends to play against
        self.ALL_AI_PLAYERS = False                                             # Use if you want the AI to make all the moves
        self.AI_DEPTH = 4                                                       # How many rounds in to the future

        self.EMPTY = 0                                                          # Slots that are not filled in
        self.PLAYER_1 = 1                                                       # Default Player
        self.PLAYER_2 = 2                                                       # Default AI
        self.PLAYER_1_HOVER = 3                                                 # Player 1 hover
        self.PLAYER_2_HOVER = 4                                                 # Player 2 hover
        self.PLAYER_1_VICTORY_HEIGHTLIGHT = 5                                   # Player 1 victory
        self.PLAYER_2_VICTORY_HEIGHTLIGHT = 6                                   # Player 2 victory

        self.ROW_COUNT = 6                                                      # Default 6
        self.COLUMN_COUNT = 7                                                   # Default 7
        self.WINNING_COUNT = 4                                                  # Default 4

        self.COLOR_BACKGROUND = pygame.Color("#999999")                         # Background color, empty slots
        self.COLOR_BOARD = pygame.Color("#4a4a4a")                              # Board color
        self.COLOR_HEIGHLIGHT_COLUMN = pygame.Color("#575757")                  # Hovering color, when picking a move
        self.COLOR_HEIGHLIGHT_VICTORY = pygame.Color("#3e759c")                 # Heighlighs a victory
        self.COLOR_PLAYER_1 = pygame.Color("#eb4034")                           # Player 1 color, red
        self.COLOR_PREVIEW_PLAYER_1 = pygame.Color("#ad6b66")                   # Preview player 1 color, red ish
        self.COLOR_PLAYER_2 = pygame.Color("#ebe834")                           # Player 2 color, yellow
        self.COLOR_PREVIEW_PLAYER_2 = pygame.Color("#b3b162")                   # Preview player 2 color, yellow ish

        self.SQUARE_SIZE = 100                                                  # 100 is a nice number
        self.PIECE_RADIUS = int(self.SQUARE_SIZE/2*0.75)                        # How big the circles are in relation to the squares

        self.SCREEN_WIDTH = self.COLUMN_COUNT * self.SQUARE_SIZE                # The WIDTH of the window
        self.SCREEN_HEIGTH = self.ROW_COUNT * self.SQUARE_SIZE                  # The HEIGHT of the window
        self.WINDOW_SIZE = (self.SCREEN_WIDTH, self.SCREEN_HEIGTH)              # Combine the width and height to a vector-2 that can be used to draw the window


class Variables():
    def __init__(self):
        self.is_first_game = True
        self.screen = None
        self.board = None
        self.app_running = False
        self.game_running = False
        self.turn = None


const = Constants()
var = Variables()


# Debug tool
def print_board(board):             # Print board in console
    print(np.flip(board, 0))        # Flip the board to appeal to Sir Isaac Newton


# Create an empty board matrix
def generate_board():
    board = np.zeros((const.ROW_COUNT, const.COLUMN_COUNT))
    return board


# If the top column is not occupied
def is_valid_move(board, col):
    return board[const.ROW_COUNT-1][col] == const.EMPTY


# Return all the columns that are not full
def get_valid_moves(board):
    valid_moves=[]

    for c in range(const.COLUMN_COUNT):
        if is_valid_move(board, c):
            valid_moves.append(c)

    if valid_moves == []:
        return False
    else:
        return valid_moves


# Get the first empty row in a column
def get_next_open_row(board, col):
    for r in range(const.ROW_COUNT):
        if board[r][col] == const.EMPTY:
            return r


# Place a piece in the board
def drop_piece(board, row, col, player):
    board[row][col] = player


# Winning condition
def win(board, player):
    # Check horizontal locations for win
    for c in range(const.COLUMN_COUNT-(const.WINNING_COUNT-1)):
        for r in range(const.ROW_COUNT):
            winning_window = []
            piece_count = 0
            for slot in range(const.WINNING_COUNT):
                # If you find a piece add on to the piece count
                if board[r][c+slot] == player:
                    piece_count += 1
                    winning_window.append([r, c+slot])
                else:
                    break
            if piece_count == const.WINNING_COUNT:
                return (True, winning_window)

    # Check for vertical locations for win
    for c in range(const.COLUMN_COUNT):
        for r in range(const.ROW_COUNT-(const.WINNING_COUNT-1)):
            winning_window = []
            piece_count = 0
            for slot in range(const.WINNING_COUNT):
                # If you find a piece add on to the piece count
                if board[r+slot][c] == player:
                    piece_count += 1
                    winning_window.append([r+slot, c])
                else:
                    break
            if piece_count == const.WINNING_COUNT:
                return (True, winning_window)

    # Check for positivly sloped diaganold
    for c in range(const.COLUMN_COUNT-(const.WINNING_COUNT-1)):
        for r in range(const.ROW_COUNT-(const.WINNING_COUNT-1)):
            winning_window = []
            piece_count = 0
            for slot in range(const.WINNING_COUNT):
                # If you find a piece, add to the piece count
                if board[r+slot][c+slot] == player:
                    piece_count += 1
                    winning_window.append([r+slot, c+slot])
                else:
                    break
            if piece_count == const.WINNING_COUNT:
                return (True, winning_window)

    # Check for negativly sloped diaganold
    for c in range(const.COLUMN_COUNT-(const.WINNING_COUNT-1)):
        for r in range((const.WINNING_COUNT-1), const.ROW_COUNT):
            winning_window = []
            piece_count = 0
            for slot in range(const.WINNING_COUNT):
                # If you find a piece add on to the piece count
                if board[r-slot][c+slot] == player:
                    piece_count += 1
                    winning_window.append([r-slot, c+slot])
                else:
                    break
            if piece_count == const.WINNING_COUNT:
                return (True, winning_window)

    # Return this if there are no winners
    return (False, None)


# Give a score to a selected secton of the bord
def evaluate_window(window, player):
    score = 0
    # Get the opponent player
    if player == const.PLAYER_1:
        opponent = const.PLAYER_2
    else:
        opponent = const.PLAYER_1

    # Score the player
    for i in range(1, const.WINNING_COUNT-1):
        if window.count(player) == const.WINNING_COUNT-i and window.count(const.EMPTY) == i:
            score += (const.WINNING_COUNT - i) * 2.5

    # Score the opponent
    for i in range(1, const.WINNING_COUNT-1):
        if window.count(opponent) == const.WINNING_COUNT-i and window.count(const.EMPTY) == i:
            score -= (const.WINNING_COUNT - i) * 2.25

    return score


def evaluate_board(board, player):
    score = 0

    # Score center col
    if const.COLUMN_COUNT % 2: # If the column count is odd
        center_array = [int(i) for i in list(board[:,(const.COLUMN_COUNT+1)//2])]
    else: # If the column count is eaven
        center_array = [int(i) for i in list(board[:,const.COLUMN_COUNT//2])]

    center_count = center_array.count(player)
    score += center_count * 2

    # Score horizontal
    for r in range(const.ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(const.COLUMN_COUNT-(const.WINNING_COUNT-1)):
            window = row_array[c:c+const.WINNING_COUNT]
            score += evaluate_window(window, player)

    # Score vertical
    for c in range(const.COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(const.ROW_COUNT-(const.WINNING_COUNT-1)):
            window = col_array[r:r+const.WINNING_COUNT]
            score += evaluate_window(window, player)

    # Score positivly sloped diaganold
    for r in range(const.ROW_COUNT-(const.WINNING_COUNT-1)):
        for c in range(const.COLUMN_COUNT-(const.WINNING_COUNT-1)):
            window = [board[r+i][c+i] for i in range(const.WINNING_COUNT)]
            score += evaluate_window(window, player)

    # Score negativly sloped diaganold
    for r in range(const.ROW_COUNT-(const.WINNING_COUNT-1)):
        for c in range(const.COLUMN_COUNT-(const.WINNING_COUNT-1)):
            window = [board[r+(const.WINNING_COUNT-1)-i][c+i] for i in range(const.WINNING_COUNT)]
            score += evaluate_window(window, player)

    return score


def minimax(board, depth, alpha, beta, maximizing, player):
    # Get the opponent player
    if player == const.PLAYER_1:
        opponent = const.PLAYER_2
    else:
        opponent = const.PLAYER_1

    valid_moves = get_valid_moves(board)
    is_terminal = win(board, const.PLAYER_1)[0] or win(board, const.PLAYER_2)[0] or valid_moves == False
    if depth == 0 or is_terminal:
        if is_terminal:
            if win(board, player)[0]:
                return (None, sys.maxsize)
            elif win(board, opponent)[0]:
                return (None, -sys.maxsize-1)
            else: # No more valid moves
                return (None, 0)
        else: # If the depth is 0
            return (None, evaluate_board(board, player))
    # Maximizing player
    if maximizing:
        value = -math.inf
        column = random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, player)
            new_score = minimax(b_copy, depth-1, alpha, beta, False, player)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (column, value)
    # Minimizing player
    else:
        value = math.inf
        column = random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, opponent)
            new_score = minimax(b_copy, depth-1, alpha, beta, True, player)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (column, value)


def end_game(board, won, player=0):
    if won:
        winning_window = win(board, player)[1]
        if player == const.PLAYER_1:
            for piece in winning_window:
                drop_piece(board, piece[0], piece[1], const.PLAYER_1_VICTORY_HEIGHTLIGHT)
        elif player == const.PLAYER_2:
            for piece in winning_window:
                drop_piece(board, piece[0], piece[1], const.PLAYER_2_VICTORY_HEIGHTLIGHT)

        draw.board(board, const, var)

    if var.is_first_game == True:
        var.is_first_game = False
    var.game_running = False


def ai_move(board, turn):
    player = turn+1

    move, minimax_score = minimax(board, const.AI_DEPTH, -math.inf, math.inf, True, player)

    if not move == None:
        row = get_next_open_row(board, int(move))
        drop_piece(board, row, int(move), player)

        # Print matrix in console
        # print_board(board)
        draw.board(board, const, var)
    
        if win(board, player)[0]:
            if const.ALL_AI_PLAYERS:
                print("Player " + str(player) + " wins")
            # else:
            #     print("You lost to an AI")

            end_game(board, True, player)
            return False
        else:
            return True
    else:
        print("THE AI SUCKS!")
        return False


def player_move(board, turn, col):
    player = turn+1

    if is_valid_move(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player)

        # Print matrix in console
        # print_board(board)
        draw.board(board, const, var)

        if win(board, player)[0]:
            print("Player " + str(player) + " wins")
            end_game(board, True, player)
        else:
            return True
    else:
        return False


# Swapp turn
def bump_turn():
    var.turn += 1
    var.turn = var.turn % 2


if __name__ == "__main__":
    pygame.init()                                                               # Initialize Pygames
    pygame.display.set_caption('Connect 4')                                     # Title bar message
    var.screen = pygame.display.set_mode(const.WINDOW_SIZE)                     # Draw the window as var.screen
    var.app_running = True                                                      # Set the app to be running


def new_game():
    var.board = generate_board()                                                # Make an empty matrix
    var.turn = random.choice([const.PLAYER_1, const.PLAYER_2]) - 1              # Randomly pick what player starts. -1 so 1 and 2 is 0 and 1
    var.game_running = True                                                     # Set game running to true

    while var.game_running:
        # Event listeners
        for event in pygame.event.get():
            # System exiter
            if event.type == pygame.QUIT:
                sys.exit()
            # Mouse movement, pos of the cursor
            if event.type == pygame.MOUSEMOTION:
                if not const.ALL_AI_PLAYERS:
                    # Make a copy of the board and place it
                    b_copy = var.board.copy()
                    # Get the column the mouse is hovering over
                    col = int(event.pos[0] / const.SQUARE_SIZE)
                    player = None
                    # Set the player whoever is making the move
                    if var.turn == const.PLAYER_1 -1:           # -1 since players are 1 and 2 and turns are 0 and 1
                        player = const.PLAYER_1_HOVER
                    elif var.turn == const.PLAYER_2 -1:         # -1 since players are 1 and 2 and turns are 0 and 1
                        player = const.PLAYER_2_HOVER
                    if is_valid_move(b_copy, col):           # If the column has any valid locations to dopor a pice
                        row = get_next_open_row(b_copy,col)     # Get the row that pice will land at
                        drop_piece(b_copy, row, col, player)    # Drop the piece in the copied board
                    draw.board(b_copy, const, var, col)                     # Draw the copied board on screen

            # Mosue 1 click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not const.ALL_AI_PLAYERS:
                    col = int(event.pos[0] / const.SQUARE_SIZE)
                    moved = player_move(var.board, var.turn, col)
                    if moved:
                        bump_turn()

        # If all players are AI players
        if const.ALL_AI_PLAYERS:                          
            moved = ai_move(var.board, var.turn)
            if moved:
                bump_turn()
        # If player 1 is an AI player
        elif const.AI_PLAYER:
            if var.turn == const.PLAYER_1:
                moved = ai_move(var.board, var.turn)
                if moved:
                    bump_turn()

        # Kill window if there cant be any made any more moves
        if not get_valid_moves(var.board):
            end_game(var.board, False)


# Main while loop, KEEP at the bottom
while var.app_running:
    if var.is_first_game == True:
        new_game()
    # Event listeners
    for event in pygame.event.get():
        # System exiter
        if event.type == pygame.QUIT:
            sys.exit()
        # Mouse 1 click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            new_game()
