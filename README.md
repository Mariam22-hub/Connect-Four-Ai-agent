
# Ai-agent

# Connect4-Python
Connect 4 programmed in python using pygame.

## Features

### Connect Four Game Mechanics
- Standard Connect Four gameplay where two players (one human and one AI) drop pieces into a 7-column, 6-row vertically suspended grid.
- The game continues until one player forms a horizontal, vertical, or diagonal line of four of their own pieces.

### Graphical User Interface
- Custom graphical user interface using Pygame for rendering the game board and interactive elements.
- Visual indications for player actions and game status updates.

### AI Opponent
- AI opponent implementing Minimax algorithm with enhancements like alpha-beta pruning for efficient decision making.
- Difficulty levels for the AI, providing varying levels of challenge.

### Interactive Game States
- Different game states such as main menu, difficulty selection, game play, and game over, each with its own interactive interface.
- Options to select AI algorithm and difficulty level.

### Board Initialization and Management
- `create_board()`: Initializes and returns a new game board.
- `drop_piece(board, row, col, piece)`: Drops a piece into the game board.
- `is_valid_location(board, col)`: Checks if a column in the board is available for dropping a piece.
- `get_next_open_row(board, col)`: Finds the next open row in a given column.
- `winning_move(board, piece)`: Checks if the last move was a winning move.

### AI Logic
- `evaluate_window(window, piece)`: Evaluates a window of four slots in the board for scoring.
- `score_position(board, piece)`: Scores the board position based on the current placement of pieces.
- `minimax(board, depth, alpha, beta, maximizingPlayer)`: Implements the Minimax algorithm with alpha-beta pruning.
- `get_valid_locations(board)`: Retrieves columns that can accept new pieces.
- `pick_best_move(board, piece)`: Picks the best move for the AI.

### Rendering and Event Handling
- `draw_board(board)`: Renders the game board and pieces on the screen.
- `handle_menu_events()`: Handles user inputs in the menu state.
- `handle_difficulty_selection_events()`: Handles user inputs in the difficulty selection state.
