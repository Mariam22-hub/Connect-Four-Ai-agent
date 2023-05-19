import numpy as np
import pygame
import sys
import math
import random

burgundy = (128, 0, 32)
blue = (173, 216, 230)
silver = (169, 169, 169)
violet = (143, 0, 255)

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

# Game states
MENU = "menu"
DIFFICULTY_SELECTION = "difficulty_selection"
GAME = "game"
GAME_OVER = "game_over"

# AI algorithms
MINIMAX = "minimax"
ALPHA_BETA = "alpha_beta"

# Menu options
DIFFICULTY_LEVELS = {
    1: "Easy",
    2: "Medium",
    3: "Hard"
}

ALGORITHM_OPTIONS = {
    1: MINIMAX,
    2: ALPHA_BETA
}

# Game settings
DEFAULT_DIFFICULTY_LEVEL = 2
DEFAULT_ALGORITHM_OPTION = 1

# Initialize game settings
current_difficulty_level = DEFAULT_DIFFICULTY_LEVEL
current_algorithm_option = DEFAULT_ALGORITHM_OPTION

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


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

    return False


def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(
        get_valid_locations(board)
    ) == 0


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)


	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col	

			if alpha != None and beta != None:
				print("alpha pruning")
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
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col

			if beta != None and alpha != None:
				print("alpha pruning")
				beta = min(beta, value)
				if alpha >= beta:
					break
		return column, value

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -math.inf
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


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                blue,
                (
                    c * SQUARESIZE,
                    (r + 1) * SQUARESIZE,
                    SQUARESIZE,
                    SQUARESIZE,
                ),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    c * SQUARESIZE + SQUARESIZE // 2,
                    (r + 1) * SQUARESIZE + SQUARESIZE // 2,
                ),
                RADIUS,
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(
                    screen,
                    burgundy,
                    (
                        c * SQUARESIZE + SQUARESIZE // 2,
                        height - r * SQUARESIZE - SQUARESIZE // 2,
                    ),
                    RADIUS,
                )
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(
                    screen,
                    violet,
                    (
                        c * SQUARESIZE + SQUARESIZE // 2,
                        height - r * SQUARESIZE - SQUARESIZE // 2,
                    ),
                    RADIUS,
                )
    pygame.display.update()


def draw_menu():
    screen.fill(BLACK)
    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("Connect Four", True, BLUE)
    screen.blit(
        title_text,
        (
            (width - title_text.get_width()) // 2,
            (height - title_text.get_height()) // 2 - 100,
        ),
    )

    levels_font = pygame.font.Font(None, 50)
    levels_text = levels_font.render("Choose Difficulty Level:", True, silver)
    screen.blit(
        levels_text,
        (
            (width - levels_text.get_width()) // 2,
            (height - levels_text.get_height()) // 2,
        ),
    )

    level_options = [levels_font.render(DIFFICULTY_LEVELS[i], True, BLUE) for i in DIFFICULTY_LEVELS]
    for i, option_text in enumerate(level_options):
        screen.blit(
            option_text,
            (
                (width - option_text.get_width()) // 2,
                (height - option_text.get_height()) // 2 + 50 + i * 50,
            ),
        )

    pygame.display.update()


def draw_difficulty_selection():
    screen.fill(BLACK)
    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("Connect Four", True, BLUE)
    screen.blit(
        title_text,
        (
            (width - title_text.get_width()) // 2,
            (height - title_text.get_height()) // 2 - 100,
        ),
    )

    algorithm_font = pygame.font.Font(None, 50)
    algorithm_text = algorithm_font.render("Choose AI Algorithm:", True, silver)
    screen.blit(
        algorithm_text,
        (
            (width - algorithm_text.get_width()) // 2,
            (height - algorithm_text.get_height()) // 2,
        ),
    )

    algorithm_options = [algorithm_font.render(ALGORITHM_OPTIONS[i], True, BLUE) for i in ALGORITHM_OPTIONS]
    for i, option_text in enumerate(algorithm_options):
        screen.blit(
            option_text,
            (
                (width - option_text.get_width()) // 2,
                (height - option_text.get_height()) // 2 + 50 + i * 50,
            ),
        )

    pygame.display.update()


def draw_game_over(winning_player):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 80)
    if winning_player == PLAYER:
        text = font.render("Computer Wins!", True, BLUE)
    elif winning_player == AI:
        text = font.render("Ai agent Wins!", True, BLUE)
    else:
        text = font.render("It's a Tie!", True, BLUE)

    screen.blit(
        text,
        (
            (width - text.get_width()) // 2,
            (height - text.get_height()) // 2 - 100,
        ),
    )
    pygame.display.update()


def initialize_game():
    global board, game_state
    board = create_board()
    game_state = GAME


def handle_menu_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return 1
            elif event.key == pygame.K_2:
                return 2
            elif event.key == pygame.K_3:
                return 3
    return None


def handle_difficulty_selection_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return 1
            elif event.key == pygame.K_2:
                return 2
    return None


def handle_game_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == GAME:
                
                # Player's turn
                col = event.pos[0] // SQUARESIZE
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    
                    if winning_move(board, PLAYER_PIECE):
                        game_state = GAME_OVER
                        draw_game_over(PLAYER)
                        break

                    # AI's turn
                    col = pick_best_move(board, AI_PIECE)
                    if is_valid_location(board, col):
                        pygame.time.wait(500)
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, AI_PIECE)
                        
                        if winning_move(board, AI_PIECE):
                            game_state = GAME_OVER
                            draw_game_over(AI)
                            break

                    if len(get_valid_locations(board)) == 0:
                        game_state = GAME_OVER
                        draw_game_over(None)

                    draw_board(board)

    return None


pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

RADIUS = SQUARESIZE // 2 - 5

screen = pygame.display.set_mode(size)
draw_menu()
menu_selected_level = None
difficulty_selection_selected_algorithm = None
game_state = MENU

while True:
    if game_state == MENU:
        menu_selected_level = handle_menu_events()
        
        if menu_selected_level is not None:
            game_state = DIFFICULTY_SELECTION
            current_difficulty_level = menu_selected_level
            draw_difficulty_selection()

    elif game_state == DIFFICULTY_SELECTION:
        
        difficulty_selection_selected_algorithm = handle_difficulty_selection_events()
        
        if difficulty_selection_selected_algorithm is not None:
            game_state = GAME
            current_algorithm_option = difficulty_selection_selected_algorithm
            initialize_game()

    elif game_state == GAME:
        handle_game_events()

    pygame.display.update()
