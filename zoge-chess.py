import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ZOGE Chess")

# Colors
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT = (255, 255, 0, 100)  # Semi-transparent yellow
PIECE_COLORS = {"w": (255, 255, 255), "b": (0, 0, 0)}  # White and Black pieces

# Initial board state (8x8, "wp" = white pawn, "bp" = black pawn, etc.)
board = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
]

# Selected piece and valid moves
selected_piece = None
valid_moves = []

# Function to draw the board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            piece = board[row][col]
            if piece:
                color = PIECE_COLORS[piece[0]]  # Use piece color based on 'w' or 'b'
                if piece[1] == "p":  # Pawn
                    pygame.draw.circle(screen, color, (col * CELL_SIZE + CELL_SIZE//2, row * CELL_SIZE + CELL_SIZE//2), CELL_SIZE//4)
                elif piece[1] in "rnbq":  # Rook, Knight, Bishop, Queen
                    pygame.draw.rect(screen, color, (col * CELL_SIZE + CELL_SIZE//4, row * CELL_SIZE + CELL_SIZE//4, CELL_SIZE//2, CELL_SIZE//2))
                elif piece[1] == "k":  # King
                    pygame.draw.polygon(screen, color, [
                        (col * CELL_SIZE + CELL_SIZE//2, row * CELL_SIZE + CELL_SIZE//4),
                        (col * CELL_SIZE + CELL_SIZE//4, row * CELL_SIZE + 3*CELL_SIZE//4),
                        (col * CELL_SIZE + 3*CELL_SIZE//4, row * CELL_SIZE + 3*CELL_SIZE//4)
                    ])
    # Highlight selected piece and valid moves
    if selected_piece:
        row, col = selected_piece
        pygame.draw.rect(screen, HIGHLIGHT, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
        for move in valid_moves:
            pygame.draw.circle(screen, HIGHLIGHT, (move[1] * CELL_SIZE + CELL_SIZE//2, move[0] * CELL_SIZE + CELL_SIZE//2), 10)

# Function to get valid moves (basic for now)
def get_valid_moves(row, col):
    piece = board[row][col]
    moves = []
    if not piece:
        return moves
    # Simple pawn movement (white)
    if piece.startswith("w") and piece.endswith("p"):
        if row > 0 and not board[row-1][col]:  # Move forward
            moves.append((row-1, col))
            if row == 6 and not board[4][col]:  # Double move from start
                moves.append((4, col))
        if row > 0 and col > 0 and board[row-1][col-1] and board[row-1][col-1].startswith("b"):  # Capture left
            moves.append((row-1, col-1))
        if row > 0 and col < 7 and board[row-1][col+1] and board[row-1][col+1].startswith("b"):  # Capture right
            moves.append((row-1, col+1))
    return moves

# Game loop
turn = "w"  # White starts
running = True
clock = pygame.time.Clock()

while running:
    draw_board()
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            col, row = x // CELL_SIZE, y // CELL_SIZE
            if 0 <= row < 8 and 0 <= col < 8:
                if selected_piece and (row, col) in valid_moves:
                    board[row][col] = board[selected_piece[0]][selected_piece[1]]
                    board[selected_piece[0]][selected_piece[1]] = ""
                    selected_piece = None
                    valid_moves = []
                    turn = "b" if turn == "w" else "w"
                elif board[row][col] and board[row][col].startswith(turn):
                    selected_piece = (row, col)
                    valid_moves = get_valid_moves(row, col)

    if not any("" in row for row in board):  # Check draw
        print("Game is a draw!")
        running = False

pygame.quit()
sys.exit()
