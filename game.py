import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 500
ROWS, COLS = 9, 9
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)
BROWN = (139, 69, 19)

# Load assets
WHITE_PIECE = pygame.transform.scale(pygame.image.load('white_piece.png'), (SQUARE_SIZE, SQUARE_SIZE))
BLACK_PIECE = pygame.transform.scale(pygame.image.load('black_piece.png'), (SQUARE_SIZE, SQUARE_SIZE))

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fianco')

# Board setup from the given image
START_POSITION = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 2, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 2, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 2, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2]
]

# Draw the board
def draw_board():
    screen.fill(BROWN)
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, GREY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces
def draw_pieces(board, selected_piece):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 1 and (row, col) != selected_piece:
                screen.blit(BLACK_PIECE, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif board[row][col] == 2 and (row, col) != selected_piece:
                screen.blit(WHITE_PIECE, (col * SQUARE_SIZE, row * SQUARE_SIZE))



# Check for victory
def check_winner(board):
    if any(board[0][col] == 2 for col in range(COLS)):
        return "White"
    if any(board[8][col] == 1 for col in range(COLS)):
        return "Black"
    return None

# Movement logic
def is_valid_move(board, start, end, player):
    start_row, start_col = start
    end_row, end_col = end

    # Ensure the move is within bounds and the target cell is empty
    if not (0 <= end_row < ROWS and 0 <= end_col < COLS):
        return False
    if board[end_row][end_col] != 0:
        return False
    
    # Simple forward or sideways move
    if player == 1:  # Black moves
        if start_row == end_row and abs(start_col - end_col) == 1:  # Sideways
            return True
        if start_col == end_col and end_row - start_row == 1:  # Forward
            return True
    elif player == 2:  # White moves
        if start_row == end_row and abs(start_col - end_col) == 1:  # Sideways
            return True
        if start_col == end_col and start_row - end_row == 1:  # Forward
            return True

    # Check if a capture is possible (diagonal forward move)
    if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2
        if board[middle_row][middle_col] in (1, 2) and board[middle_row][middle_col] != player:
            return True

    return False

# Check for any available captures for the current player
def available_captures(board, player):
    captures = []
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                # Check all diagonal directions for a capture
                for d_row, d_col in [(2, 2), (2, -2), (-2, 2), (-2, -2)]:
                    new_row, new_col = row + d_row, col + d_col
                    if is_valid_move(board, (row, col), (new_row, new_col), player):
                        captures.append(((row, col), (new_row, new_col)))
    return captures


# Perform a move
def make_move(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = 0

    # Check for captures
    if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2
        board[middle_row][middle_col] = 0

# Main game loop
def main():
    clock = pygame.time.Clock()
    board = [row[:] for row in START_POSITION]  # Deep copy the starting board
    selected_piece = None
    current_player = 2  # Black starts
    dragging_piece = False  # Track whether a piece is being dragged
    piece_drag_offset = (0, 0)  # Offset to keep piece centered on mouse
    dragged_pos = None  # Keep track of where the piece is being dragged

    while True:
        draw_board()
        draw_pieces(board, selected_piece)  # Pass selected_piece here

        # If dragging, draw the selected piece following the mouse
        if dragging_piece and dragged_pos:
            pygame.draw.rect(screen, GREY, (dragged_pos[0] - piece_drag_offset[0], dragged_pos[1] - piece_drag_offset[1], SQUARE_SIZE, SQUARE_SIZE))

            # Draw the dragged piece on the mouse position
            piece_image = WHITE_PIECE if current_player == 2 else BLACK_PIECE
            screen.blit(piece_image, (dragged_pos[0] - piece_drag_offset[0], dragged_pos[1] - piece_drag_offset[1]))

        # Check for winner
        winner = check_winner(board)
        if winner:
            print(f"{winner} wins!")
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                if not dragging_piece and board[row][col] == current_player:
                    selected_piece = (row, col)
                    dragging_piece = True
                    piece_drag_offset = (pos[0] % SQUARE_SIZE, pos[1] % SQUARE_SIZE)  # Store the offset to center piece on cursor
                    dragged_pos = pos  # Start dragging from current mouse position

            if event.type == pygame.MOUSEMOTION and dragging_piece:
                # Update dragged position
                dragged_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP and dragging_piece:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                if selected_piece:
                    if is_valid_move(board, selected_piece, (row, col), current_player):
                        make_move(board, selected_piece, (row, col))
                        current_player = 3 - current_player  # Switch players
                    selected_piece = None
                dragging_piece = False  # Stop dragging after the drop

        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()
