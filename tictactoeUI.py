import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 15

# Colors (Hex to RGB)
BACKGROUND_COLOR = (26, 28, 30)    # #1a1c1e
BUTTON_COLOR = (44, 62, 80)        # #2c3e50
BUTTON_TEXT_COLOR = (236, 240, 241) # #ecf0f1
X_COLOR = (231, 76, 60)            # #e74c3c
O_COLOR = (52, 152, 219)           # #3498db
GRID_LINES_COLOR = (149, 165, 166) # #95a5a6

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe by mohditachi")
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Global variables
player = 1
game_over = False
winner = None
game_mode = None

def draw_lines():
    # Vertical lines
    pygame.draw.line(screen, GRID_LINES_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, GRID_LINES_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # Horizontal lines
    pygame.draw.line(screen, GRID_LINES_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, GRID_LINES_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, O_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + 30, row * SQUARE_SIZE + 30), (col * SQUARE_SIZE + SQUARE_SIZE - 30, row * SQUARE_SIZE + SQUARE_SIZE - 30), CROSS_WIDTH)
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + 30, row * SQUARE_SIZE + SQUARE_SIZE - 30), (col * SQUARE_SIZE + SQUARE_SIZE - 30, row * SQUARE_SIZE + 30), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    return not any(0 in row for row in board)

def check_win(player):
    # Check rows
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return True
    if all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True
    return False

def setup():
    screen.fill(BACKGROUND_COLOR)
    draw_lines()
    pygame.display.update()

def ai_move():
    global player
    # Check for AI win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(row, col):
                board[row][col] = player
                if check_win(player):
                    return
                board[row][col] = 0
    # Block Player 1 win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(row, col):
                board[row][col] = 1
                if check_win(1):
                    board[row][col] = player
                    return
                board[row][col] = 0
    # Random move
    while True:
        ai_row = random.randint(0, 2)
        ai_col = random.randint(0, 2)
        if available_square(ai_row, ai_col):
            mark_square(ai_row, ai_col, player)
            return

def update_loop():
    global player, game_over, winner, game_mode
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            if game_mode is None:  # Welcome screen
                single_button = pygame.Rect(200, 200, 200, 60)
                if single_button.collidepoint(mouseX, mouseY):
                    game_mode = "single"
                    player = 1
                    setup()
                multi_button = pygame.Rect(200, 280, 200, 60)
                if multi_button.collidepoint(mouseX, mouseY):
                    game_mode = "multi"
                    player = 1
                    setup()
            elif not game_over:
                if game_mode == "single" and player == 1:
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE
                    if 0 <= clicked_row < BOARD_ROWS and 0 <= clicked_col < BOARD_COLS and available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, player)
                        if check_win(player):
                            game_over = True
                            winner = player
                            print(f"Player {player} wins!")
                        elif is_board_full():
                            game_over = True
                            winner = 0
                            print("It's a tie!")
                        else:
                            player = 2
                            pygame.time.wait(500)
                            ai_move()
                            if check_win(2):
                                game_over = True
                                winner = 2
                                print("AI wins!")
                            elif is_board_full():
                                game_over = True
                                winner = 0
                                print("It's a tie!")
                            else:
                                player = 1
                        screen.fill(BACKGROUND_COLOR)
                        draw_lines()
                        draw_figures()
                        pygame.display.update()
                elif game_mode == "multi":
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE
                    if 0 <= clicked_row < BOARD_ROWS and 0 <= clicked_col < BOARD_COLS and available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, player)
                        if check_win(player):
                            game_over = True
                            winner = player
                            print(f"Player {player} wins!")
                        elif is_board_full():
                            game_over = True
                            winner = 0
                            print("It's a tie!")
                        else:
                            player = player % 2 + 1
                        screen.fill(BACKGROUND_COLOR)
                        draw_lines()
                        draw_figures()
                        pygame.display.update()
            elif game_over:
                retry_button = pygame.Rect(200, 400, 100, 50)
                if retry_button.collidepoint(mouseX, mouseY):
                    board.fill(0)
                    game_over = False
                    winner = None
                    player = 1
                    game_mode = None
                    screen.fill(BACKGROUND_COLOR)
                    pygame.display.update()
                exit_button = pygame.Rect(320, 400, 100, 50)
                if exit_button.collidepoint(mouseX, mouseY):
                    return False

    # Draw screens
    if game_mode is None:  # Welcome screen
        screen.fill(BACKGROUND_COLOR)
        try:
            font = pygame.font.SysFont("segoeui", 35)  # Reduced from 40 to 35
        except:
            try:
                font = pygame.font.SysFont("roboto", 35)
            except:
                font = pygame.font.SysFont(None, 35)
        welcome_text = font.render("Welcome to Tic Tac Toe!", True, BUTTON_TEXT_COLOR)
        screen.blit(welcome_text, (150, 100))

        # Draw Single Player button
        single_button = pygame.Rect(200, 200, 200, 60)
        pygame.draw.rect(screen, BUTTON_COLOR, single_button)
        single_text = font.render("Single Player", True, BUTTON_TEXT_COLOR)
        single_text_rect = single_text.get_rect(center=single_button.center)
        screen.blit(single_text, single_text_rect.topleft)

        # Draw Multiplayer button
        multi_button = pygame.Rect(200, 280, 200, 60)
        pygame.draw.rect(screen, BUTTON_COLOR, multi_button)
        multi_text = font.render("Multiplayer", True, BUTTON_TEXT_COLOR)
        multi_text_rect = multi_text.get_rect(center=multi_button.center)
        screen.blit(multi_text, multi_text_rect.topleft)

        pygame.display.update()
    elif game_over:
        try:
            font = pygame.font.SysFont("segoeui", 36)
        except:
            try:
                font = pygame.font.SysFont("roboto", 36)
            except:
                font = pygame.font.SysFont(None, 36)
        if winner == 1:
            text = font.render("Player 1 wins!", True, BUTTON_TEXT_COLOR)
        elif winner == 2:
            text = font.render("AI wins!" if game_mode == "single" else "Player 2 wins!", True, BUTTON_TEXT_COLOR)
        else:
            text = font.render("It's a tie!", True, BUTTON_TEXT_COLOR)
        screen.blit(text, (WIDTH // 4, HEIGHT // 2 - 50))
        pygame.draw.rect(screen, BUTTON_COLOR, (200, 400, 100, 50))
        retry_text = font.render("Retry", True, BUTTON_TEXT_COLOR)
        retry_text_rect = retry_text.get_rect(center=(250, 425))
        screen.blit(retry_text, retry_text_rect.topleft)
        pygame.draw.rect(screen, BUTTON_COLOR, (320, 400, 100, 50))
        exit_text = font.render("Exit", True, BUTTON_TEXT_COLOR)
        exit_text_rect = exit_text.get_rect(center=(370, 425))
        screen.blit(exit_text, exit_text_rect.topleft)
        pygame.display.update()
    return True

# Game loop
setup()
running = True
while running:
    running = update_loop()
    pygame.display.update()

pygame.quit()