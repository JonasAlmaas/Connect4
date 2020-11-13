import pygame
import numpy as np
import sys
import random

# Constants
AI_PLAYER = True

ROW_COUNT = 6           #Default 6
COLUMN_COUNT = 7        #Default 7
WINNING_AMOUNT = 40      #Default 4

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


def get_possible_moves():
    moves=[]

    for c in range(COLUMN_COUNT):
        if board[ROW_COUNT-1][c] == 0:
            moves.append(c)

    if not moves == []:
        return moves
    else:
        return False


def randomMove():
    list = get_possible_moves()
    if list :
        move = random.choice(list)
        # Return as a string so the 0 index doesn coundt as None
        return str(move)
    else:
        return False


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


def ai_move(turn):
    global game_running

    player = turn+1

    move = randomMove()
    if move:
        # Convert the sring from move to an int
        row = get_next_open_row(board, int(move))
        drop_piece(board, row, int(move), player)

        if win(board, player):
            print("You loset to AI")
            game_running = False

        # Debuging
        # print_board(board)
        draw_borad(board)
        return True
    else:
        print("THE AI SUCKS!")
        return False


def make_move(turn, col):
    global game_running

    player = turn+1

    if is_valid_loction(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player)

        if win(board, player):
            print("Player " + str(player) + " wins")
            game_running = False
        
        # Debuging
        # print_board(board)
        draw_borad(board)
        return True
    else:
        return False


def bumpTurn():
    global turn

    turn += 1
    turn = turn % 2


while game_running:
    # Event listeners
    for event in pygame.event.get():
        # System exiter
        if event.type == pygame.QUIT:
            sys.exit()

        # Mouse movement, pos of the cursor
        if event.type == pygame.MOUSEMOTION:
            col = int(event.pos[0] / SQUARE_SIZE)
            draw_borad(board, col)

        # Mosue 1 click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            col = int(event.pos[0] / SQUARE_SIZE)
            moved = make_move(turn, col)
            if moved:
                bumpTurn()

        # Sleep a bit before shitting down
        if game_running == False:
            pygame.time.wait(1000)

    # Make a play if ther is an AI and its the "1" turn
    if AI_PLAYER and turn == 1:
        moved = ai_move(turn)
        if moved:
            bumpTurn()

    # Kill window if there cant be any made any more moves
    if not get_possible_moves():
        pygame.time.wait(1000)
        game_running = False
