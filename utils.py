

ROWS, COLS = 9, 9  # Define board dimensions


def make_move_for_ai(board, start, end):
    """
    A simplified version of make_move for AI simulation.
    This function makes a move without updating history or annotations.
    :param board: The current game board
    :param start: The start position (row, col)
    :param end: The end position (row, col)
    :return: The new board after making the move
    """
    start_row, start_col = start
    end_row, end_col = end
    is_capture = abs(start_row - end_row) == 2  # Check if this is a capture

    # Make a deep copy of the board to avoid modifying the original
    new_board = [row[:] for row in board]
    
    # Make the move
    new_board[end_row][end_col] = new_board[start_row][start_col]
    new_board[start_row][start_col] = 0

    # Handle captures
    if is_capture:
        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2
        new_board[middle_row][middle_col] = 0  # Remove the captured piece

    return new_board

def get_all_valid_moves(board, current_player):
    """
    Generates all valid moves for the current player.
    :param board: The current game board
    :param current_player: The current player (1 for black, 2 for white)
    :return: A list of all valid moves
    """
    moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == current_player:
                # Check all possible moves (you may already have movement logic, so reuse it here)
                possible_moves = get_piece_valid_moves(board, (row, col), current_player)  # Implement this to get valid moves for a piece
                for move in possible_moves:
                    moves.append(((row, col), move))  # Store moves as ((start_row, start_col), (end_row, end_col))
    return moves


# Movement logic including forward captures
def is_valid_move(board, start, end, player):
    start_row, start_col = start
    end_row, end_col = end

    # Ensure the move is within bounds and the target cell is empty
    if not (0 <= end_row < ROWS and 0 <= end_col < COLS):
        return False
    if board[end_row][end_col] != 0:
        return False
    
    # Simple forward or sideways move (non-capture)
    if player == 1:  # Black moves (downwards)
        if start_row == end_row and abs(start_col - end_col) == 1:  # Sideways
            return True
        if start_col == end_col and end_row - start_row == 1:  # Forward (downwards)
            return True
    elif player == 2:  # White moves (upwards)
        if start_row == end_row and abs(start_col - end_col) == 1:  # Sideways
            return True
        if start_col == end_col and start_row - end_row == 1:  # Forward (upwards)
            return True

    # Check if a capture is possible (forward diagonal only)
    if player == 1:  # Black can capture diagonally downwards
        if end_row - start_row == 2 and abs(start_col - end_col) == 2:  # Jump two rows down
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            if board[middle_row][middle_col] == 2:  # Check if White piece is being captured
                return True
    elif player == 2:  # White can capture diagonally upwards
        if start_row - end_row == 2 and abs(start_col - end_col) == 2:  # Jump two rows up
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            if board[middle_row][middle_col] == 1:  # Check if Black piece is being captured
                return True

    return False

def get_piece_valid_moves(board, position, player):
    """
    Get all valid moves for a specific piece.
    :param board: The current game board
    :param position: The position of the piece as (row, col)
    :param player: The current player (1 for black, 2 for white)
    :return: A list of valid end positions for the piece
    """
    row, col = position
    moves = []
    
    # Check all directions (for example, forward, sideways, and capture diagonally)
    # You may reuse your existing is_valid_move() function
    for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1), (-2, -2), (-2, 2), (2, -2), (2, 2)]:  # Adjust based on your movement rules
        new_row, new_col = row + d_row, col + d_col
        if is_valid_move(board, position, (new_row, new_col), player):  # You likely have this function
            moves.append((new_row, new_col))
    
    return moves

def is_terminal(board):
    """
    Checks if the game has reached a terminal state (win/loss).
    :param board: The current game board
    :return: True if the game is over, otherwise False
    """
    winner = check_winner(board)  # Assuming you already have a check_winner function
    if winner is not None:
        return True
    return False

# Check for victory
def check_winner(board):
    if any(board[0][col] == 2 for col in range(COLS)):
        return "White"
    if any(board[8][col] == 1 for col in range(COLS)):
        return "Black"
    return None

#  for any available captures for the current player
def available_captures(board, player):
    captures = []
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                # Check forward diagonal directions for a capture
                if player == 1:  # Black (moving downwards)
                    for d_row, d_col in [(2, 2), (2, -2)]:  # Check forward-down diagonals
                        new_row, new_col = row + d_row, col + d_col
                        if is_valid_move(board, (row, col), (new_row, new_col), player):
                            captures.append(((row, col), (new_row, new_col)))
                elif player == 2:  # White (moving upwards)
                    for d_row, d_col in [(-2, 2), (-2, -2)]:  # Check forward-up diagonals
                        new_row, new_col = row + d_row, col + d_col
                        if is_valid_move(board, (row, col), (new_row, new_col), player):
                            captures.append(((row, col), (new_row, new_col)))
    return captures


