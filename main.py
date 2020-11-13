import pygame
import numpy as np
import sys
import random
import math


class Constant():
    def __init__(self):
        self.AI_PLAYER = True                                                   # Use if you don't have any friends to play against
        self.ALL_AI_PLAYERS = False                                             # Use if you want the AI to make all the moves

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
def win(board, piece):
    # Check horizontal locations for win
    for c in range(constant.COLUMN_COUNT-(constant.WINNING_COUNT-1)):
        for r in range(constant.ROW_COUNT):
            # Temp count of how many pieces are in a row
            piece_count = 0
            for slot in range(constant.WINNING_COUNT):
                # If you find a piece add on to the piece count
                if board[r][c+slot] == piece:
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
                if board[r+slot][c] == piece:
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
                if board[r+slot][c+slot] == piece:
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
                if board[r-slot][c+slot] == piece:
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


def get_valid_moves(board):
    valid_moves=[]

    for c in range(constant.COLUMN_COUNT):
        if board[constant.ROW_COUNT-1][c] == constant.EMPTY:
            valid_moves.append(c)

    if not valid_moves == []:
        return valid_moves
    else:
        return False


# Picks a random location BAD
def random_move(board):
    valid_moves = get_valid_moves(board)
    if valid_moves :
        move = random.choice(valid_moves)
        # Return as a string so the 0 index doesn't coundt as None
        return str(move)
    else:
        return False

# TODO Pls write this
# def get_winner(board):
#     if win(board, 1):
#         return "P1"
#     elif win(board, 2):
#         return "P2"


# Give a score to a selected secton of the bord
def score_window(window, player, score):
    for i in range(0, constant.WINNING_COUNT-1):
        if window.count(player) == constant.WINNING_COUNT-i and window.count(constant.EMPTY) == i:
            score += (constant.WINNING_COUNT - i) * (constant.WINNING_COUNT-i)
    return score


def score_board(board, player):
    score = 0
    # Score horizontal
    for r in range(constant.ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(constant.COLUMN_COUNT-(constant.WINNING_COUNT-1)):
            window = row_array[c:c+constant.WINNING_COUNT]
            score = score_window(window, player, score)

    # Score vertical
    for c in range(constant.COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(constant.ROW_COUNT-(constant.WINNING_COUNT-1)):
            window = col_array[r:r+constant.WINNING_COUNT]
            score = score_window(window, player, score)

    # Score positivly sloped diaganold
    for r in range(constant.ROW_COUNT-(constant.WINNING_COUNT-1)):
        for c in range(constant.COLUMN_COUNT-(constant.WINNING_COUNT-1)):
            window = [board[r+i][c+i] for i in range(constant.WINNING_COUNT)]
            score = score_window(window, player, score)

    # Score negativly sloped diaganold
    for r in range(constant.ROW_COUNT-(constant.WINNING_COUNT-1)):
        for c in range(constant.COLUMN_COUNT-(constant.WINNING_COUNT-1)):
            window = [board[r-i][c-i] for i in range(constant.WINNING_COUNT)]
            score = score_window(window, player, score)

    return score


def best_move(board, player):
    valid_moves = get_valid_moves(board)
    best_score = 0
    best_col = random.choice(valid_moves)
    for col in valid_moves:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, player)
        score = score_board(temp_board, player)
        if score > best_score:
            best_score = score
            best_col = col
    # Return as a string so the 0 index doesn't coundt as None
    return str(best_col)


def minimax(board, depth, maximizing):
    pass


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

    # move = random_move(board)
    move = best_move(board, player)
    # print(move)

    if move:
        pygame.time.wait(500)
        # Convert the sring from move to an int
        row = get_next_open_row(board, int(move))
        drop_piece(board, row, int(move), player)

        # Print matrix in console
        # print_board(board)
        draw_borad(board)
    
        if win(board, player):
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
