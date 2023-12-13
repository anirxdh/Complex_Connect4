import pygame
import sys
import numpy as np
import random
import math

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return None

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 3:
                pygame.draw.circle(screen, GREEN, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def main_menu():
    pygame.init()  # Initialize Pygame here
    print("Welcome to Connect 4")
    print("1. Player vs Player")
    print("2. Player vs AI Bots")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        player_vs_player_menu()
    elif choice == "2":
        player_vs_ai_menu()

def player_vs_player_menu():
    print("Player vs Player")
    print("1. 1v1")
    print("2. 1v1v1")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        player_vs_player_1v1()
    elif choice == "2":
        player_vs_player_1v1v1()

def player_vs_ai_menu():
    print("Player vs AI Bots")
    print("1. 1v1")
    print("2. 1v1v1")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        player_vs_ai_1v1()
    elif choice == "2":
        player_vs_ai_1v1v1()


def player_vs_player_1v1():
    board = create_board()
    game_over = False
    turn = 0

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    draw_board(board,screen)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Player 1
                if turn == 0:
                    col = int(event.pos[0] // SQUARESIZE)
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myfont.render("Player 1 wins!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                # Player 2
                else:
                    col = int(event.pos[0] // SQUARESIZE)
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                draw_board(board,screen)
                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)
                
                if check_draw(board):
                    label = myfont.render("Game Draw!", 1, GREEN)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(2000)
                    retry = input("Draw! Retry? (yes/no): ")
                    if retry.lower() == 'yes':
                        player_vs_player_1v1()
                    else:
                        sys.exit()

def player_vs_player_1v1v1():
    board = create_board()
    game_over = False
    turn = 0

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    draw_board(board,screen)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Determine column from mouse position
                col = int(event.pos[0] // SQUARESIZE)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, turn + 1)

                    if winning_move(board, turn + 1):
                        color = RED if turn == 0 else YELLOW if turn == 1 else GREEN
                        label = myfont.render(f"Player {turn + 1} wins!", 1, color)
                        screen.blit(label, (40, 10))
                        game_over = True

                    draw_board(board, screen)
                    turn += 1
                    turn = turn % 3

                    if game_over:
                        pygame.time.wait(3000)
                    
                    if check_draw(board):
                        label = myfont.render("Game Draw!", 1, GREEN)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        pygame.time.wait(2000)
                        retry = input("Draw! Retry? (yes/no): ")
                        if retry.lower() == 'yes':
                            player_vs_player_1v1v1()
                        else:
                            sys.exit()

def evaluate_window(window, piece):
    score = 0
    opp_piece = 1 if piece == 2 else 2
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, 2):
                return (None, 100000000000000)
            elif winning_move(board, 1):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, 2))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 2)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 1)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

def player_vs_ai_1v1():
    board = create_board()
    game_over = False
    turn = random.randint(0, 1)

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    draw_board(board,screen)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 0:  # Player's turn
                    col = int(event.pos[0] // SQUARESIZE)
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myfont.render("Player wins!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        draw_board(board,screen)

                        if check_draw(board):
                            label = myfont.render("Game Draw!", 1, GREEN)
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            pygame.time.wait(2000)
                            retry = input("Draw! Retry? (yes/no): ")
                            if retry.lower() == 'yes':
                                player_vs_ai_1v1()
                            else:
                                sys.exit()

        # AI's turn
        if turn == 1 and not game_over:
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    label = myfont.render("AI wins!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                draw_board(board,screen)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)

# Player vs Two AI Players
def player_vs_ai_1v1v1():
    board = create_board()
    game_over = False
    turn = 0  # Player starts first

    pygame.display.set_caption('Connect 4')
    screen = pygame.display.set_mode(SIZE)
    draw_board(board,screen)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:  # Player's turn
                col = int(event.pos[0] // SQUARESIZE)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player wins!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn = (turn + 1) % 3
                    draw_board(board,screen)

                    if check_draw(board):
                        label = myfont.render("Game Draw!", 1, GREEN)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        pygame.time.wait(2000)
                        retry = input("Draw! Retry? (yes/no): ")
                        if retry.lower() == 'yes':
                            player_vs_ai_1v1v1()
                        else:
                            sys.exit()

        # AI Turn
        if turn != 0 and not game_over:
            # Choose the AI's piece based on the turn
            ai_piece = 2 if turn == 1 else 3

            col = ai_move(board, ai_piece)
            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, ai_piece)

                if winning_move(board, ai_piece):
                    color = YELLOW if ai_piece == 2 else GREEN
                    label = myfont.render(f"AI {turn} wins!", 1, color)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn = (turn + 1) % 3
                draw_board(board,screen)

        if game_over:
            pygame.time.wait(3000)


# AI Function
def ai_move(board, piece):
    valid_locations = [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

def check_draw(board):
    return all(board[r][c] != 0 for r in range(ROW_COUNT) for c in range(COLUMN_COUNT))


main_menu()