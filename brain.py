from utils import make_move_for_ai, get_all_valid_moves, is_terminal, available_captures


def negamax(board, depth, alpha, beta, color):
    """
    NegaMax with Alpha-Beta pruning.
    :param board: The current game board
    :param depth: The depth of the search
    :param alpha: The alpha value for pruning
    :param beta: The beta value for pruning
    :param color: 1 for maximizing player, -1 for minimizing player
    :return: The best score for the current player
    """
    if depth == 0 or is_terminal(board):
        return color * evaluate(board)  # Return the evaluation of the board for the current player

    max_score = float('-inf')

    # Generate all possible valid moves
    for move in get_all_valid_moves(board, color):
        new_board = make_move_for_ai(board, move[0], move[1])
        score = -negamax(new_board, depth - 1, -beta, -alpha, -color)  # Switch player and negate score
        max_score = max(max_score, score)
        alpha = max(alpha, score)
        if alpha >= beta:
            break  # Beta cutoff (prune branch)

    return max_score


def ai_move(board, current_player, depth=3, rows=9, cols=9):
    best_score = float('-inf')
    best_move = None

    color = 1 if current_player == 2 else -1  # White is maximizing, Black is minimizing

    # First, check if any captures are available
    captures = available_captures(board, current_player)

    # Generate all possible moves (restrict to captures if they exist)
    if captures:
        possible_moves = captures  # AI must make a capture move
    else:
        possible_moves = get_all_valid_moves(board, current_player)  # Regular moves if no captures

    # Iterate over possible moves
    for move in possible_moves:
        new_board = make_move_for_ai(board, move[0], move[1])
        score = -negamax(new_board, depth - 1, float('-inf'), float('inf'), -color)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def evaluate(board):
    white_score = 0
    black_score = 0
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 1:  # Black pieces
                black_score += (ROWS - row)  # Reward advancing towards opponent's row
            elif board[row][col] == 2:  # White pieces
                white_score += row  # Reward advancing towards opponent's row
    return white_score - black_score  # Higher score is better for White
