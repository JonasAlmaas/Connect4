import pygame
import numpy as np
import sys
import random
import math


class Constant():
    def __init__(self):
        self.AI_PLAYER = True                                                   # Use if you don't have any friends to play against
        self.ALL_AI_PLAYERS = False                                             # Use if you want the AI to make all the moves
        self.AI_DEPTH = 4                                                       # How many round in to the future

        self.EMPTY = 0                                                          # Slots that are not filled in
        self.PLAYER_1 = 1                                                       # Default Player
        self.PLAYER_2 = 2                                                       # Default AI

        self.ROW_COUNT = 6                                                      # Default 6
        self.COLUMN_COUNT = 7                                                   # Default 7
        self.WINNING_COUNT = 4                                                  # Default 4

        self.COLOR_BACKGROUND = pygame.Color("#999999")                         # Background color, empty slots
        self.COLOR_BOARD = pygame.Color("#4a4a4a")                              # Board color
        self.COLOR_HOVER_PLAYER = pygame.Color("#575757")                       # Hovering color, when picking a move
        self.COLOR_PLAYER_1 = pygame.Color("#eb4034")                           # Player 1 color, red
        self.COLOR_PLAYER_2 = pygame.Color("#ebe834")                           # Player 2 color, yellow

        self.SQUARE_SIZE = 100                                                  # 100 is a nice number
        self.PIECE_RADIUS = int(self.SQUARE_SIZE/2*0.75)                        # How big the circles are in relation to the squares

        self.SCREEN_WIDTH = self.COLUMN_COUNT * self.SQUARE_SIZE                # The WIDTH of the window
        self.SCREEN_HEIGTH = self.ROW_COUNT * self.SQUARE_SIZE                  # The HEIGHT of the window
        self.WINDOW_SIZE = (self.SCREEN_WIDTH, self.SCREEN_HEIGTH)              # Combine the width and height to a vector-2 that can be used to draw the window

constant = Constant()


# Create a borad matrix
def initialize_board():
    board = np.zeros((constant.ROW_COUNT,constant.COLUMN_COUNT))
    return board


# If the top column is not occupied
def is_valid_loction(borad, col):
    return borad[constant.ROW_COUNT-1][col] == 0


# Get the first empty row
def get_next_open_row(borad, col):
    for r in range(constant.ROW_COUNT):
        if borad[r][col] == 0:
            return r


# Place a piece in the board
def drop_piece(borad, row, col, player):
    borad[row][col] = player


# Rules
def win(board, player):
    # Check horizontal locations for win
    for c in range(constant.COLUMN_COUNT-(constant.WINNING_COUNT-1)):
        for r in range(constant.ROW_COUNT):
            # Temp count of how many pieces are in a row
            piece_count = 0
            for slot in range(constant.WINNING_COUNT):
                # If you find a piece add on to the piece count
                if board[r][c+slot] == player:
                    piece_count += 1
                else:
                    break
            if piece_count == constant.WINNING_COUNT:
                return True

    # Check for vertical locations for win
    for c in range(constant.COLUMN_COUNT):
        for r in range(constant.ROW_COUNT-(constant.WINNING_COUNT-1)):
            # Temp count of how many pieces are in a row
            piece_count = 0
            for slot in range(constant.WINNING_COUNT):
                # If you find a piece add on to the piece count
                if board[r+slot][c] == player:
                    piece_count += 1
                else:
                    break
            if piece_count == constant.WINNING_COUNT:
                return True

    # Check for positivly sloped diaganold
    for c in range(constant.COLUMN_COUNT-(constant.WINNING_COUNT-1)):
        for r in range(constant.ROW_COUNT-(constant.WINNING_COUNT-1)):
            # Temp count of how many pieces are in a row
            piece_count = 0
            for slot in range(constant.WINNING_COUNT):
                # If you find a piece, add to the piece count
                if board[r+slot][c+slot] == player:
                    piece_count += 1
                else:
                    break
            if piece_count == constant.WINNING_COUNT:
                return True

    # Check for negativly sloped diaganold
    for c in range(constant.COLUMN_COUNT-(constant.WINNING_COUNT-1)):
        for r in range((constant.WINNING_COUNT-1), constant.ROW_COUNT):
            # Temp count of how many pieces are in a row
            piece_count = 0
            for slot in range(constant.WINNING_COUNT):
                # If you find a piece add on to the piece count
                if board[r-slot][c+slot] == player:
                    piece_count += 1
                else:
                    break
            if piece_count == constant.WINNING_COUNT:
                return True


# Print the board to the console
def print_board(borad):
    # Flip the borad to appeal to Sir. Isaac Newton
    print(np.flip(borad, 0))


# Draws the board on screen with pygames
def draw_borad(board, heightlighted=None):
    for c in range(constant.COLUMN_COUNT):
        for r in range(constant.ROW_COUNT):
            if not c == heightlighted:
                # Board
                pygame.draw.rect(screen, constant.COLOR_BOARD, (c*constant.SQUARE_SIZE, r*constant.SQUARE_SIZE, constant.SQUARE_SIZE, constant.SQUARE_SIZE))

            # Hover color when droping a piece
            else:
                pygame.draw.rect(screen, constant.COLOR_HOVER_PLAYER, (c*constant.SQUARE_SIZE, r*constant.SQUARE_SIZE, constant.SQUARE_SIZE, constant.SQUARE_SIZE))

            # Empty slots
            pygame.draw.circle(screen, constant.COLOR_BACKGROUND, (c*constant.SQUARE_SIZE+constant.SQUARE_SIZE/2, r*constant.SQUARE_SIZE+constant.SQUARE_SIZE/2), constant.PIECE_RADIUS)

    for c in range(constant.COLUMN_COUNT):
        for r in range(constant.ROW_COUNT):
            if board[r][c] == constant.PLAYER_1:
                pygame.draw.circle(screen, constant.COLOR_PLAYER_1, (c*constant.SQUARE_SIZE+constant.SQUARE_SIZE/2, (constant.SCREEN_HEIGTH-constant.SQUARE_SIZE)-r*constant.SQUARE_SIZE+constant.SQUARE_SIZE/2), constant.PIECE_RADIUS)
            elif board[r][c] == constant.PLAYER_2:
                pygame.draw.circle(screen, constant.COLOR_PLAYER_2, (c*constant.SQUARE_SIZE+constant.SQUARE_SIZE/2, (constant.SCREEN_HEIGTH-constant.SQUARE_SIZE)-r*constant.SQUARE_SIZE+constant.SQUARE_SIZE/2), constant.PIECE_RADIUS)

    pygame.display.update()


# Return all the columns that are not full
def get_valid_moves(board):
    valid_moves=[]

    for c in range(constant.COLUMN_COUNT):
        if board[constant.ROW_COUNT-1][c] == constant.EMPTY:
            valid_moves.append(c)

    if not valid_moves == []:
        return valid_moves
    else:
        return False


# Give a score to a selected secton of the bord
def evaluate_window(window, player):
    score = 0
    # Get the opponent player
    if player == constant.PLAYER_1:
        opponent = constant.PLAYER_2
    else:
        opponent = constant.PLAYER_1

    # Score the player
    for i in range(0, constant.WINNING_COUNT-1):
        if window.count(player) == constant.WINNING_COUNT-i and window.count(constant.EMPTY) == i:
            score += (constant.WINNING_COUNT - i) * 2.5
    # Score the opponent
    for i in range(0, constant.WINNING_COUNT-1):
        if window.count(opponent) == constant.WINNING_COUNT-i and window.count(constant.EMPTY) == i:
            score -= (constant.WINNING_COUNT - i) * 2.25

    return score


def evaluate_board(board, player):
    score = 0

    # Score center col
    if constant.COLUMN_COUNT % 2: # If the column count is odd
        center_array = [int(i) for i in list(board[:,(constant.COLUMN_COUNT+1)//2])]
    else: # If the column count is eaven
        center_array = [int(i) for i in list(board[:,constant.COLUMN_COUNT//2])]

    center_count = center_array.count(player)
    score += center_count * 2

    # Score horizontal
    for r in range(constant.ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(constant.COLUMN_COUNT-(constant.WINNING_COUNT-1)):
            window = row_array[c:c+constant.WINNING_COUNT]
            score += evaluate_window(window, player)

    # Score vertical
    for c in range(constant.COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(constant.ROW_COUNT-(constant.WINNING_COUNT-1)):
            window = col_array[r:r+constant.WINNING_COUNT]
            score += evaluate_window(window, player)

    # Score positivly sloped diaganold
    for r in range(constant.ROW_COUNT-(constant.WINNING_COUNT-1)):
        for c in range(constant.COLUMN_COUNT-(constant.WINNING_COUNT-1)):
            window = [board[r+i][c+i] for i in range(constant.WINNING_COUNT)]
            score += evaluate_window(window, player)

    # Score negativly sloped diaganold
    for r in range(constant.ROW_COUNT-(constant.WINNING_COUNT-1)):
        for c in range(constant.COLUMN_COUNT-(constant.WINNING_COUNT-1)):
            window = [board[r+(constant.WINNING_COUNT-1)-i][c+i] for i in range(constant.WINNING_COUNT)]
            score += evaluate_window(window, player)

    return score


def minimax(board, depth, alpha, beta, maximizing, player):
    # Get the opponent player
    if player == constant.PLAYER_1:
        opponent = constant.PLAYER_2
    else:
        opponent = constant.PLAYER_1

    valid_moves = get_valid_moves(board)
    is_terminal = win(board, constant.PLAYER_1) or win(board, constant.PLAYER_2) or valid_moves == False
    if depth == 0 or is_terminal:
        if is_terminal:
            if win(board, player):
                return (None, 100000000)
            elif win(board, opponent):
                return (None, -100000000)
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


board = initialize_board()                                              # Make an empty matrix
game_running = True                                                     # Set the game state to running
turn = random.choice([constant.PLAYER_1-1, constant.PLAYER_2-1])      # Randomly pick what player starts. PLAYER_#-1 so 1 and 2 is 0 and 1

pygame.init()                                                           # Initialize Pygames
pygame.display.set_caption('Connect 4')                                 # Title bar message
screen = pygame.display.set_mode(constant.WINDOW_SIZE)                 # Draw the window as screen


def end_game():
    global game_running

    pygame.time.wait(1000)
    game_running = False


def ai_move(turn):
    player = turn+1

    move, minimax_score = minimax(board, constant.AI_DEPTH, -math.inf, math.inf, True, player)

    if not move == None:
        row = get_next_open_row(board, int(move))
        drop_piece(board, row, int(move), player)

        # Print matrix in console
        # print_board(board)
        draw_borad(board)
    
        if win(board, player):
            if constant.ALL_AI_PLAYERS:
                print("Player " + str(player) + " wins")
            else:
                print("You lost to an AI")
            end_game()
            return False
        else:
            return True
    else:
        print("THE AI SUCKS!")
        return False


def player_move(turn, col):
    player = turn+1

    if is_valid_loction(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player)

        # Print matrix in console
        # print_board(board)
        draw_borad(board)

        if win(board, player):
            print("Player " + str(player) + " wins")
            end_game()
        else:
            return True
    else:
        return False


def bumpTurn():
    global turn

    turn += 1
    turn = turn % 2


while game_running:
    # Event listeners (No mater what)
    for event in pygame.event.get():
        # System exiter
        if event.type == pygame.QUIT:
            sys.exit()

        # Mouse movement, pos of the cursor
        if event.type == pygame.MOUSEMOTION:
            if not constant.ALL_AI_PLAYERS:
                col = int(event.pos[0] / constant.SQUARE_SIZE)
                draw_borad(board, col)

        # Mosue 1 click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not constant.ALL_AI_PLAYERS:
                col = int(event.pos[0] / constant.SQUARE_SIZE)
                moved = player_move(turn, col)
                if moved:
                    bumpTurn()

    # If all players are AI players
    if constant.ALL_AI_PLAYERS:                          
        moved = ai_move(turn)
        if moved:
            bumpTurn()
    # If player 1 is an AI player
    elif constant.AI_PLAYER:
        if turn == constant.PLAYER_1:
            moved = ai_move(turn)
            if moved:
                bumpTurn()

    # Kill window if there cant be any made any more moves
    if not get_valid_moves(board):
        end_game()
