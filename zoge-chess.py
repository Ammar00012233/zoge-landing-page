import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 168, 82)

# Board settings
CELL_SIZE = 100
ROWS, COLS = 3, 3
WIDTH, HEIGHT = CELL_SIZE * COLS, CELL_SIZE * ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cat vs Computer")

# Load move sound
move_sound = pygame.mixer.Sound("move.wav")

# Board
board = [["" for _ in range(COLS)] for _ in range(ROWS)]

def draw_board():
    screen.fill(GREEN)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 2)
            if board[row][col] == "P":
                pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE//3)
            elif board[row][col] == "C":
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE//3)

def player_move(pos):
    x, y = pos
    row, col = y // CELL_SIZE, x // CELL_SIZE
    if board[row][col] == "":
        board[row][col] = "P"
        move_sound.play()
        return True
    return False

def computer_move():
    # Harder AI: choose winning move, block player, or random
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == "":
                board[row][col] = "C"
                if check_winner("C"):
                    move_sound.play()
                    return
                board[row][col] = ""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == "":
                board[row][col] = "P"
                if check_winner("P"):
                    board[row][col] = "C"
                    move_sound.play()
                    return
                board[row][col] = ""
    empty_cells = [(r, c) for r in range(ROWS) for c in range(COLS) if board[r][c] == ""]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = "C"
        move_sound.play()

def check_winner(player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(COLS):
        if all(board[row][col] == player for row in range(ROWS)):
            return True
    if all(board[i][i] == player for i in range(ROWS)):
        return True
    if all(board[i][ROWS-i-1] == player for i in range(ROWS)):
        return True
    return False

# Game loop
turn = "P"
running = True
while running:
    draw_board()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and turn == "P":
            if player_move(event.pos):
                if check_winner("P"):
                    print("Player wins!")
                    running = False
                else:
                    turn = "C"
    if turn == "C" and running:
        pygame.time.wait(500)
        computer_move()
        if check_winner("C"):
            print("Computer wins!")
            running = False
        else:
            turn = "P"

pygame.quit()
sys.exit()
