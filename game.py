import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 500
WINDOW_WIDTH = WIDTH+200
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
screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
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

def draw_restart_button():
    button_color = (200, 0, 0)  # Red color for the button
    button_rect = pygame.Rect(WIDTH + 50, HEIGHT - 50, 100, 40)  # Position and size of the button
    pygame.draw.rect(screen, button_color, button_rect)

    # Add button text
    font = pygame.font.Font(None, 24)  # Default font
    text = font.render("Restart", True, WHITE)  # Text inside the button
    screen.blit(text, (WIDTH + 75, HEIGHT - 40))  # Position the text inside the button

    return button_rect  # Return the button rect to detect clicks later




# Check for victory
def check_winner(board):
    if any(board[0][col] == 2 for col in range(COLS)):
        return "White"
    if any(board[8][col] == 1 for col in range(COLS)):
        return "Black"
    return None

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


# Check for any available captures for the current player
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

# Convert row and column indexes to chess-style notation (columns A-I, rows 1-9)
def index_to_notation(start, end, is_capture):
    col_map = "abcdefghi"  # Column letters
    row_map = "123456789"  # Row numbers (bottom to top)

    start_col, start_row = start
    end_col, end_row = end

    # Notate positions (e.g., "a1" or "i9")
    start_pos = f"{col_map[start_row]}{row_map[8 - start_col]}"  # Row is inverted for chess notation
    end_pos = f"{col_map[end_row]}{row_map[8 - end_col]}"        # Row is inverted for chess notation

    if is_capture:
        return f"{start_pos}x{end_pos}"  # Capture notation
    return f"{start_pos}-{end_pos}"  # Normal move notation


# Perform a move and track history and annotations
def make_move(board, start, end, move_history, annotations, current_move_index, current_player):
    start_row, start_col = start
    end_row, end_col = end
    is_capture = abs(start_row - end_row) == 2  # Check if this is a capture

    # Make the move
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = 0

    # Handle captures
    if is_capture:
        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2
        board[middle_row][middle_col] = 0

    # Convert move to notation and store it
    move_annotation = index_to_notation(start, end, is_capture)

    # If we're replaying a game, remove future moves once we make a new move
    move_history = move_history[:current_move_index + 1]
    annotations = annotations[:current_move_index + 1]

    # Add new move to history and update the annotations
    move_history.append((start, end, is_capture))
    annotations.append(move_annotation)
    current_move_index += 1

    return move_history, annotations, current_move_index



# Revert the board to a previous state
def undo_move(board, move_history, current_move_index):
    if current_move_index < 0:  # No more moves to undo, prevent going below the first move
        return board, current_move_index

    # Get the move to undo
    start, end, is_capture = move_history[current_move_index]

    # Reverse the move (move the piece back to its original position)
    board[start[0]][start[1]] = board[end[0]][end[1]]  # Move piece back
    board[end[0]][end[1]] = 0  # Clear the destination square

    # Restore the captured piece if necessary
    if is_capture:
        middle_row = (start[0] + end[0]) // 2
        middle_col = (start[1] + end[1]) // 2
        # Restore the opponent's piece at the middle position
        board[middle_row][middle_col] = 3 - board[start[0]][start[1]]

    # Decrease the current move index and return the updated board and index
    current_move_index -= 1
    return board, current_move_index



# Redo a move if available
def redo_move(board, move_history, current_move_index):
    if current_move_index >= len(move_history) - 1:  # No future moves to redo
        return board

    # Get the move to redo
    start, end, is_capture = move_history[current_move_index + 1]

    # Perform the move (move the piece to its new position)
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = 0  # Clear the original square

    # Handle captures
    if is_capture:
        middle_row = (start[0] + end[0]) // 2
        middle_col = (start[1] + end[1]) // 2
        # Clear the opponent's piece that was captured
        board[middle_row][middle_col] = 0

    # Increase the current move index and return the updated board and index
    current_move_index += 1
    return board, current_move_index



# Main game loop
def main():
    clock = pygame.time.Clock()
    
    def reset_game():
        # Reset the game state
        board = [row[:] for row in START_POSITION]  # Reset the board to the starting position
        selected_piece = None
        current_player = 2  # White starts
        dragging_piece = False  # Reset dragging state
        piece_drag_offset = (0, 0)  # Reset offset
        dragged_pos = None  # Reset dragged position
        move_history = []  # Clear move history
        annotations = []  # Clear annotations
        current_move_index = -1  # Reset move index
        return board, selected_piece, current_player, dragging_piece, piece_drag_offset, dragged_pos, move_history, annotations, current_move_index

    # Initialize game state
    board, selected_piece, current_player, dragging_piece, piece_drag_offset, dragged_pos, move_history, annotations, current_move_index = reset_game()

    def draw_moves():
        font = pygame.font.Font(None, 24)  # Use a default font
        text_start_x = WIDTH + 30  # Position text to the right of the board
        text_start_y = 20
        screen.fill(BROWN, (WIDTH, 0, 200, HEIGHT))  # Background for moves area

        # Loop through all the move annotations
        for i, annotation in enumerate(annotations):
            move_text = font.render(f"{i + 1}. {annotation}", True, BLACK)
            screen.blit(move_text, (text_start_x, text_start_y + i * 20))  # Display moves with spacing

            # If this is the current move, draw a small circle next to it
            if i == current_move_index:
                # Draw a small black circle next to the current move
                pygame.draw.circle(screen, BLACK, (text_start_x - 15, text_start_y + i * 20 + 10), 5)  # (x, y) coordinates and radius

    while True:
        draw_board()
        draw_pieces(board, selected_piece)  # Pass selected_piece here
        draw_moves()  # Draw the move list with current move indicator

        # Draw the restart button
        restart_button_rect = draw_restart_button()

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
            sys.exit()  # This stays for quitting the game

        # Check if the current player has any available captures
        captures = available_captures(board, current_player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the game only if the user closes the window
                sys.exit()

            # Handle button clicks for restart
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):  # Check if restart button was clicked
                    board, selected_piece, current_player, dragging_piece, piece_drag_offset, dragged_pos, move_history, annotations, current_move_index = reset_game()

            # Handle mouse button down for piece selection and movement
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

                # Check if the click is within the bounds of the board
                if 0 <= row < ROWS and 0 <= col < COLS:
                    # If not dragging and selecting the current player's piece
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

                # Check if the release is within the bounds of the board
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if selected_piece:
                        # If captures are available, restrict to capturing moves only
                        if captures:
                            for start, end in captures:
                                if selected_piece == start and (row, col) == end:
                                    move_history, annotations, current_move_index = make_move(
                                        board, selected_piece, (row, col), move_history, annotations, current_move_index, current_player
                                    )
                                    current_player = 3 - current_player  # Switch players
                                    break
                        else:
                            # If no captures are available, allow regular moves
                            if is_valid_move(board, selected_piece, (row, col), current_player):
                                move_history, annotations, current_move_index = make_move(
                                    board, selected_piece, (row, col), move_history, annotations, current_move_index, current_player
                                )
                                current_player = 3 - current_player  # Switch players
                        selected_piece = None
                dragging_piece = False  # Stop dragging after the drop

            # Navigate move history with arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Go back one move
                    if current_move_index >= 0:
                        board, current_move_index = undo_move(board, move_history, current_move_index)
                        current_player = 3 - current_player  # Switch turns after undo
                elif event.key == pygame.K_RIGHT:  # Go forward one move
                    if current_move_index < len(move_history) - 1:
                        board, current_move_index = redo_move(board, move_history, current_move_index)
                        current_player = 3 - current_player  # Switch turns after redo

        pygame.display.flip()
        clock.tick(60)





if __name__ == "__main__":
    main()
