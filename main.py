import pygame
import numpy as np
import sys

# Constants
ROW_COUNT = 6           #Default 6
COLUMN_COUNT = 7        #Default 7
WINNING_AMOUNT = 4      #Default 4

COLOR_TEXT = pygame.Color("#d9d9d9")
COLOR_BACKGROUND = pygame.Color("#999999")
COLOR_BOARD = pygame.Color("#4a4a4a")
COLOR_HOVER_PLAYER = pygame.Color("#575757")
COLOR_PLAYER_1 = pygame.Color("#eb4034")
COLOR_PLAYER_2 = pygame.Color("#ebe834")

SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2*0.75)


# Create a borad matrix
def initialize_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board


# If the top column is not occupied
def is_valid_loction(borad, col):
    return borad[ROW_COUNT-1][col] == 0


# Get the first empty row
def get_next_open_row(borad, col):
    for r in range(ROW_COUNT):
        if borad[r][col] == 0:
            return r


# Place a piece in the board
def drop_piece(borad, row, col, piece):
    borad[row][col] = piece


# Rules
def win(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-(WINNING_AMOUNT-1)):
        for r in range(ROW_COUNT):
            # Temp count of how many pieces are in a row
            piece_count = 0
            for slot in range(WINNING_AMOUNT):
                # If you find a piece add on to the piece count
                if board[r][c+slot] == piece:
                    piece_count += 1
                else:
                    break
            if piece_count == WINNING_AMOUNT:
                return True

    # Check for vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-(WINNING_AMOUNT-1)):
            # Temp count of how many pieces are in a row
            piece_count = 0
            for slot in range(WINNING_AMOUNT):
                # If you find a piece add on to the piece count
                if board[r+slot][c] == piece:
                    piece_count += 1
                else:
                    break
            if piece_count == WINNING_AMOUNT:
                return True

    # Check for positivly sloped diaganold
    for c in range(COLUMN_COUNT-(WINNING_AMOUNT-1)):
        for r in range(ROW_COUNT-(WINNING_AMOUNT-1)):
            # Temp count of how many pieces are in a row
            piece_count = 0
            for slot in range(WINNING_AMOUNT):
                # If you find a piece, add to the piece count
                if board[r+slot][c+slot] == piece:
                    piece_count += 1
                else:
                    break
            if piece_count == WINNING_AMOUNT:
                return True

    # Check for negativly sloped diaganold
    for c in range(COLUMN_COUNT-(WINNING_AMOUNT-1)):
        for r in range((WINNING_AMOUNT-1), ROW_COUNT):
            # Temp count of how many pieces are in a row
            piece_count = 0
            for slot in range(WINNING_AMOUNT):
                # If you find a piece add on to the piece count
                if board[r-slot][c+slot] == piece:
                    piece_count += 1
                else:
                    break
            if piece_count == WINNING_AMOUNT:
                return True


# Print the board to the console
def print_board(borad):
    # Flip the borad to appeal to Sir. Isaac Newton
    print(np.flip(borad, 0))


# Draws the board on screen with pygames
def draw_borad(board, heightlighted=None):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if not c == heightlighted:
                # Board
                pygame.draw.rect(screen, COLOR_BOARD, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Hover color when droping a piece
            else:
                pygame.draw.rect(screen, COLOR_HOVER_PLAYER, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Empty slots
            pygame.draw.circle(screen, COLOR_BACKGROUND, (c*SQUARE_SIZE+SQUARE_SIZE/2, r*SQUARE_SIZE+SQUARE_SIZE/2), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, COLOR_PLAYER_1, (c*SQUARE_SIZE+SQUARE_SIZE/2, (height-SQUARE_SIZE)-r*SQUARE_SIZE+SQUARE_SIZE/2), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, COLOR_PLAYER_2, (c*SQUARE_SIZE+SQUARE_SIZE/2, (height-SQUARE_SIZE)-r*SQUARE_SIZE+SQUARE_SIZE/2), RADIUS)

    pygame.display.update()


board = initialize_board()
game_running = True
turn = 0

# Initialize Pygames
pygame.init()

# Window dimentions
width = COLUMN_COUNT * SQUARE_SIZE
height = ROW_COUNT * SQUARE_SIZE
window_size = (width, height)
# Draw the window
screen = pygame.display.set_mode(window_size)


def play(turn, col):
    global game_running

    player = turn+1

    if is_valid_loction(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player)

        if win(board, player):
            print("Player " + str(player) + " wins")
            game_running = False
    else:
        pass

    draw_borad(board)

    # Debuging
    # print_board(board)


while game_running:
    # Event listeners
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            col = int(event.pos[0] / SQUARE_SIZE)
            draw_borad(board, col)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            col = int(event.pos[0] / SQUARE_SIZE)
            play(turn, col)

            # Bump the turn number
            turn += 1
            turn = turn % 2
        
        if game_running == False:
            pygame.time.wait(1000)
