#main game logic
import pygame, random
#minimax modules
import threading, time
from copy import deepcopy
#efficiency modules
from functools import lru_cache
import ctypes
#file modules
import os, sys, atexit, json

sys.setrecursionlimit(1000000000)

dll_path = "C:\\Users\\kamil\\OneDrive\\Desktop\\Github\\Python_Chess_Project\\mylibrary.dll"
mylib = ctypes.CDLL(dll_path)
mylib.king_dead.argtypes = [ctypes.py_object]  # Pointer to array of C strings
mylib.king_dead.restype = ctypes.c_bool




def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # Convert seconds to milliseconds
        print(f"{func.__name__} took {execution_time:.5f} ms to run.")
        return result
    return wrapper

class ChessBot:
    def __init__(self):

        turn_depth = 3 # 3 moves into the future
        self.max_depth = turn_depth * 2  # How many plies to look into (half moves)
        self.time_limit = 999999999 # Time limit in seconds for move calculation
        print(f"Using a recursion depth of {self.max_depth} ({round(self.max_depth/2)} moves deep)")

        self.max_threads = os.cpu_count()
        print(f"{self.max_threads} cpu cores found")

    def clear_all_caches(self):
        self.generate_piece_attacks.cache_clear()


    #@measure_time
    # ~ 0.002 ms
    def king_dead(self, board):
        """
        Check if both kings are present on the board.
        :param board: Dictionary representing the board state. Keys are positions (e.g., "e1"),
                      values are pieces (e.g., "white_king").
        :return: True if either king is missing; False otherwise.
        """
        result = mylib.king_dead(board)
        return result



    #@measure_time
    def evaluate_board(self, board, is_maximizing, depth):
        """Evaluate the board and return a score."""

        if self.king_dead(board):
            return float('10_000') - depth if is_maximizing else float('-inf') + depth

        # Heatmap values for each piece type
        heatmap = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 0}  # King has no value in terms of material}

        #Positional heatmap for pawns (encourages central control)
        pawn_position_bonus = {
            "a1": 0.0, "b1": 0.0, "c1": 0.0, "d1": 0.0, "e1": 0.0, "f1": 0.0, "g1": 0.0, "h1": 0.0,
            "a2": 0.1, "b2": 0.1, "c2": 0.1, "d2": 0.1, "e2": 0.1, "f2": 0.1, "g2": 0.1, "h2": 0.1,
            "a3": 0.2, "b3": 0.3, "c3": 0.3, "d3": 0.4, "e3": 0.4, "f3": 0.3, "g3": 0.3, "h3": 0.2,
            "a4": 0.3, "b4": 0.4, "c4": 0.5, "d4": 0.7, "e4": 0.7, "f4": 0.5, "g4": 0.4, "h4": 0.3,
            "a5": 0.3, "b5": 0.4, "c5": 0.5, "d5": 0.7, "e5": 0.7, "f5": 0.5, "g5": 0.4, "h5": 0.3,
            "a6": 0.2, "b6": 0.3, "c6": 0.3, "d6": 0.4, "e6": 0.4, "f6": 0.3, "g6": 0.3, "h6": 0.2,
            "a7": 0.1, "b7": 0.1, "c7": 0.1, "d7": 0.1, "e7": 0.1, "f7": 0.1, "g7": 0.1, "h7": 0.1,
            "a8": 0.0, "b8": 0.0, "c8": 0.0, "d8": 0.0, "e8": 0.0, "f8": 0.0, "g8": 0.0, "h8": 0.0
        }

        score = 0

        for position, piece in board.items():
            piece_type = piece.split("_")[1]
            piece_value = heatmap.get(piece_type, 0)

            # Adjust pawn scores based on position
            # Positive means white is winning
            if piece.startswith('white'):
                if piece_type == "pawn":
                    piece_value += pawn_position_bonus.get(position, 0)
                score += piece_value
            else:
                if piece_type == "pawn":
                    piece_value -= pawn_position_bonus.get(position, 0)
                score -= piece_value
        #print(f"Score {score} found for player {self.player} on board {board}")

        return score

    def iterative_deepening(self, board, player):
        """Iterative deepening minimax."""
        global positions

        start_time = time.time()
        best_move = None


        for depth in range(1, self.max_depth ):
            positions = 0
            self.depth_time = time.time()
            try:
                move, score = self.search_with_depth(board, player, depth, start_time)
                if move is not None:
                    best_move = move
            except TimeoutError:
                print("Time limit reached during search.")
                print(f"{('{:,}'.format(positions)) } positions searched in {self.time_limit} seconds for an average of {('{:,}'.format(positions / (time.time() - start_time) / 1000))} kNps")
                break

        print(f"Best move: {best_move} with score {score} found at depth: {depth}")
        return best_move

    #@measure_time
    def search_with_depth(self, board, player, depth, start_time):
        """Perform minimax search to a fixed depth."""
        legal_moves = self.generate_legal_moves(board, player)
        is_maximizing = player == 'white'
        best_score = float('-9999') if is_maximizing else float('9999')
        alpha = float('-9999')
        beta = float('9999')
        best_move = None

        for move in legal_moves:
            if depth == 5:
                if (move == ("c2", "g6")):
                    if board == {'c2': 'white_bishop', 'd7': 'white_king', 'f6': 'black_pawn', 'f7': 'black_king',
                                 'g7': 'black_pawn', 'e1': 'white_rook', 'h5': 'white_pawn'}:
                        new_board = self.make_move(board, *move)  # Apply the move
                        eval = self.minimax(new_board, alpha, beta, depth - 1, False, start_time)  # Recursively evaluate
                        print(eval)

            score = self.minimax(self.make_move(board, *move), alpha, beta, depth, is_maximizing, start_time)
            if (is_maximizing and score > best_score) or (not is_maximizing and score < best_score):
                best_score = score
                best_move = move

        global positions
        print(f"minimax function searched {positions:,} positions at depth {depth} for {(time.time() - self.depth_time):.3f} seconds ({((positions / (time.time() - self.depth_time+1))/1000):.3f}KNps)")
        return best_move, best_score


    #@measure_time
    def minimax(self, board, alpha, beta, depth, is_maximizing, start_time):
        """Minimax algorithm with transposition table and timeout."""
        global positions
        positions += 1

        # Check for timeout
        if time.time() - start_time > self.time_limit:
            raise TimeoutError

        # Base case: Evaluate board when the depth is 0
        if depth == 0:
            return self.evaluate_board(board, is_maximizing, depth)

        # Generate legal moves for the current player
        legal_moves = self.generate_legal_moves(board, 'white' if is_maximizing else 'black')

        if is_maximizing:  # White's turn to maximize the score
            max_eval = -5000

            for move in legal_moves:
                if depth >= 5:
                    if board == {'g6': 'white_bishop', 'd7': 'white_king', 'f6': 'black_pawn', 'f7': 'black_king',
                                 'g7': 'black_pawn', 'e1': 'white_rook', 'h5': 'white_pawn'}:
                        if move == ("g6", "f7"):
                            print("mating move simulated")
                            new_board = self.make_move(board, *move)  # Apply the move
                            eval = self.minimax(new_board, alpha, beta, depth - 1, False,
                                                start_time)  # Recursively evaluate

                            print(depth)
                            print(eval)
                new_board = self.make_move(board, *move)  # Apply the move
                eval = self.minimax(new_board, alpha, beta, depth - 1, False, start_time)  # Recursively evaluate
                max_eval = max(max_eval, eval)  # Maximise the score
                alpha = max(alpha, eval)  # Update alpha value (maximize alpha)

                if beta <= alpha:  # Beta cut-off
                    break  # Prune the branch as further exploration won't improve the score
            return max_eval

        elif not is_maximizing:  # Black's turn to minimize the score
            min_eval = 5000
            for move in legal_moves:
                new_board = self.make_move(board, *move)  # Apply the move
                eval = self.minimax(new_board, alpha, beta, depth - 1, True, start_time)  # Recursively evaluate
                min_eval = min(min_eval, eval)  # Minimize the score
                beta = min(beta, eval)  # Update beta value (minimize beta)

                if beta <= alpha:  # Alpha cut-off
                    break  # Prune the branch as further exploration won't improve the score

            return min_eval

    #@measure_time
    def find_king(self, board, player):
        king_position = None
        for square, piece in board.items():
            if piece == f"{player}_king":
                king_position = square
                break
        return king_position

    @lru_cache(maxsize=None)
    #@measure_time
    def generate_piece_attacks(self, simulated_board, square, piece_type):
        """Generate all squares a piece can attack."""
        attack_squares = set()
        row, col = self.get_coordinates_from_square(square)

        if piece_type == "knight":
            knight_offsets = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
            for offset in knight_offsets:
                new_row, new_col = row + offset[0], col + offset[1]
                new_square = self.get_square_from_coordinates(new_row, new_col)
                if self.is_valid_square(new_square, simulated_board):
                    attack_squares.add(new_square)
        elif piece_type in ["queen", "rook", "bishop"]:
            directions = []
            if piece_type == "queen":
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
            elif piece_type == "rook":
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            elif piece_type == "bishop":
                directions = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

            for direction in directions:
                while True:
                    row, col = row + direction[0], col + direction[1]
                    new_square = self.get_square_from_coordinates(row, col)
                    if not self.is_valid_square(new_square, simulated_board):
                        break
                    attack_squares.add(new_square)
                    if simulated_board.get(new_square):
                        break  # Stop sliding if we hit a piece

        elif piece_type == "pawn":
            # Pawns attack diagonally, based on their direction
            direction = 1 if self.is_white(piece) else -1
            attack_squares.add(self.get_square_from_coordinates(row + direction, col - 1))
            attack_squares.add(self.get_square_from_coordinates(row + direction, col + 1))

        return attack_squares

    # @measure_time
    def is_within_bounds(self, col, row):
        """Check if the given coordinates are within the board."""
        return 0 <= col < 8 and 0 <= row < 8

    # @measure_time
    def has_pawn_moved(self, player, row):
        """Check if a pawn has already moved."""
        if player == "white" and row != 1:
            return True
        if player == "black" and row != 6:
            return True
        return False

    # @measure_time
    def is_empty_square(self, board, square):
        """Check if a square is empty."""
        return square not in board

    # @measure_time
    def is_opponent_piece(self, board, square, player):
        """Check if a square contains an opponent's piece."""
        if square not in board:
            return False
        return board[square].split("_")[0] != player

    # @measure_time
    def generate_pawn_moves(self, board, square, col, row, player):
        """Generate pawn moves (including double move and captures)."""
        moves = []
        directions = [(0, 1), (0, 2), (-1, 1), (1, 1)] if player == "white" else [(0, -1), (0, -2), (-1, -1), (1, -1)]
        has_moved = self.has_pawn_moved(player, row)

        for direction in directions:
            target_col, target_row = col + direction[0], row + direction[1]
            target_square = f"{chr(target_col + ord('a'))}{target_row + 1}"

            # Single moves
            if direction in [(0, 1), (0, -1)]:
                if self.is_empty_square(board, target_square):  # Empty square
                    moves.append((square, target_square))

            # Double moves (only if pawn hasn't moved yet)
            elif direction in [(0, 2), (0, -2)] and not has_moved:
                middle_square = f"{chr(col + ord('a'))}{row + 2 if player == 'white' else row - 2 + 1}"
                if self.is_empty_square(board, target_square) and self.is_empty_square(board, middle_square):
                    moves.append((square, target_square))

            # Captures
            elif self.is_opponent_piece(board, target_square, player):
                moves.append((square, target_square))

        return moves

    # @measure_time
    def generate_knight_moves(self, board, square, col, row, player):
        """Generate knight moves."""
        moves = []
        directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

        for direction in directions:
            target_col, target_row = col + direction[0], row + direction[1]
            if self.is_within_bounds(target_col, target_row):
                target_square = f"{chr(target_col)}{target_row}"
                if self.is_empty_square(board, target_square) or self.is_opponent_piece(board, target_square, player):
                    moves.append((square, target_square))

        return moves
    # @measure_time
    def generate_sliding_piece_moves(self, board, square, col, row, directions, player):
        """Generate moves for sliding pieces (rook, bishop, queen, king)."""
        moves = []

        for direction in directions:
            for step in range(1, 8):
                target_col, target_row = col + direction[0] * step, row + direction[1] * step
                if not self.is_within_bounds(target_col, target_row):
                    break

                target_square = f"{chr(target_col + ord('a'))}{target_row + 1}"
                if self.is_empty_square(board, target_square):
                    moves.append((square, target_square))  # Free move
                elif self.is_opponent_piece(board, target_square, player):
                    moves.append((square, target_square))  # Capture
                    break  # Blocked by opponent piece
                else:
                    break  # Blocked by own piece
        return moves

    def generate_king_moves(self, board, square, col, row, directions, player):
        moves = []
        for direction in directions:
            target_col, target_row = col + direction[0], row + direction[1]
            if not self.is_within_bounds(target_col, target_row):
                break

            target_square = f"{chr(target_col + ord('a'))}{target_row + 1}"
            if self.is_empty_square(board, target_square):
                moves.append((square, target_square))  # Free move
            elif self.is_opponent_piece(board, target_square, player):
                moves.append((square, target_square))  # Capture
                break  # Blocked by opponent piece
            else:
                break  # Blocked by own piece

        return moves

    def sort_moves_by_piece_priority(self, board, moves):
        """
        Sorts legal moves based on the priority of the piece making the move.
        Priority order: queen > rook > bishop > knight > pawn > king.
        """

        # Define piece priorities (lower numbers = higher priority)
        piece_priority = {
            "queen": 2,
            "rook": 3,
            "bishop": 4,
            "knight": 5,
            "pawn": 7,
            "king": 6
        }

        def move_priority(move):
            from_square, to_square = move
            piece = self.get_piece_at(board, from_square)
            # Get the type of piece and fetch its priority
            piece_type = self.get_piece_type(piece)
            return piece_priority.get(piece_type.lower())

        # Sort the moves by the priority of the piece making the move
        return sorted(moves, key=move_priority)

    def get_piece_at(self, board, square):
        return board[square]

    def get_piece_type(self, piece):
        piece_colour, piece_type = piece.split("_")
        return piece_type  # Assuming piece has a `type` attribute

    #@measure_time
    def generate_legal_moves(self, board, player):
        """Generate all pseudo-legal moves for the given player."""
        moves = []
        sliding_directions = {
            "bishop": [(1, 1), (1, -1), (-1, 1), (-1, -1)],
            "rook": [(1, 0), (-1, 0), (0, 1), (0, -1)],
            "queen": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        }
        king_directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        # Iterate through all pieces on the board
        for square, piece in board.items():
            piece_colour, piece_type = piece.split("_")
            if piece_colour != player:
                continue  # Skip opponent's pieces

            col, row = ord(square[0]) - ord('a'), int(square[1]) - 1  # Convert board notation to indices

            if piece_type == "pawn":
                moves.extend(self.generate_pawn_moves(board, square, col, row, player))

            elif piece_type == "knight":
                moves.extend(self.generate_knight_moves(board, square, col, row, player))

            elif piece_type == "king":
                moves.extend(self.generate_king_moves(board, square, col, row, king_directions, player))

            elif piece_type in {"bishop", "rook", "queen"}:
                sliding_direction = sliding_directions[piece_type]
                moves.extend(self.generate_sliding_piece_moves(board, square, col, row, sliding_direction, player))

        moves = self.sort_moves_by_piece_priority(board, moves)
        return moves

    def make_move(self, board, from_square, to_square):
        """Move a piece from one square to another."""
        new_board = deepcopy(board)
        if from_square in new_board:
            new_board[to_square] = new_board[from_square]  # Move the piece to the new square
            del new_board[from_square]  # Remove the piece from its old square
        return new_board


class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Chess Game')
        self.clock = pygame.time.Clock()
        self.board = self.load_initial_position()
        self.square_size = 100
        self.current_turn = None
        self.bot = ChessBot()
        self.running = True
        self.font = pygame.font.SysFont("calibri", 20)
        self.piece_images = {}

    def load_initial_position(self):
        board = {}
        with open('res/test_position.txt', 'r') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    position, piece = line.strip().split()
                    board[position] = piece
        return board

    def reset(self):
        self.board = self.load_initial_position()
        self.current_turn = "white" # random.choice(['white', 'black'])
        print(f"{self.current_turn} goes first.")
        self.player_colour = self.current_turn
        if self.player_colour == 'white':
            self.bot_colour = 'black'
        else:
            self.bot_colour = 'white'

    #@measure_time
    def draw_board(self):
        colours = [(240, 217, 181), (181, 136, 99)]  # Light and dark squares
        for row in range(8):
            for col in range(8):
                x = col * self.square_size
                y = row * self.square_size
                colour = colours[(row + col) % 2]
                pygame.draw.rect(
                    self.screen,
                    colour,
                    pygame.Rect(x, y, self.square_size, self.square_size))

                square_name = f"{chr(ord('a') + col)}{8 - row}"
                text_surface = self.font.render(square_name, True, (0,0,0))
                text_x = x + 5  # Padding from the top-left corner of the square
                text_y = y + 5
                self.screen.blit(text_surface, (text_x, text_y))

    def load_piece_image(self, piece):
        """Load a piece image, cache it, and return the cached image."""
        if piece not in self.piece_images:
            try:
                image = pygame.image.load(f"Pictures/{piece}.png")
                self.piece_images[piece] = pygame.transform.scale(image, (self.square_size, self.square_size))
            except pygame.error:
                print(f"Error loading image for {piece}. Ensure the file exists.")
                return None
        return self.piece_images[piece]

    #@measure_time
    def draw_pieces(self, position):
        for square, piece in position.items():
            piece_image = self.load_piece_image(piece)
            if piece_image:
                col = ord(square[0]) - ord('a')  # Convert 'a'-'h' to 0-7
                row = 8 - int(square[1])  # Convert '1'-'8' to 7-0
                self.screen.blit(piece_image, (col * self.square_size, row * self.square_size))

    def display_fps(self):  # Displays current FPS
        fps_counter = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps_counter, True, pygame.Color("coral"))
        (self.screen.blit(fps_text, (780, 0)))

    def display_update(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw_board()
            self.draw_pieces(self.board.copy())
            self.display_fps()
            pygame.display.flip()
            self.clock.tick(60)

    def swap_turn(self):
        if self.current_turn == 'white':
            self.current_turn = 'black'
        else:
            self.current_turn = 'white'

    def play_turn(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

            if self.player_colour != self.current_turn:
                move = self.bot.iterative_deepening(self.board, self.bot_colour)
                self.make_move(*move)
                if mylib.king_dead(self.board):
                    winner = self.current_turn
                    break
                self.swap_turn()


            else:
                move = self.bot.iterative_deepening(self.board, self.player_colour)
                self.make_move(*move)
                if mylib.king_dead(self.board):
                    winner = self.current_turn
                    break
                self.swap_turn()

        print(f"{winner} is the winner")

    def player_move_piece(board, player):
        """
        Handles the player's move by prompting for a piece and a destination,
        validating the move, and updating the board state if the move is legal.

        :param board: The current state of the chess board
        :param player: The current player ('white' or 'black')
        :return: Updated board state after a legal move
        """
        while True:
            # Prompt the player to select a piece and a destination
            piece = input(f"{player.capitalize()}, select a piece to move (e.g., 'e2'): ")
            destination = input(f"{player.capitalize()}, select a destination (e.g., 'e4'): ")

            # Generate all legal moves for the current player
            legal_moves = generate_legal_moves(board, player)

            # Validate the player's move
            move = (piece, destination)
            if move in legal_moves:
                # Update the board state with the legal move
                board = make_move(board, *move)
                print(f"Move successful: {piece} to {destination}")
                break
            else:
                print("Illegal move. Please try again.")

        return board

    def generate_legal_moves(self, board, player):
        """Generate all pseudo-legal moves for the given player."""
        moves = []

        # Define movement rules for each piece
        directions = {
            "pawn": {"white": [(0, 1), (0, 2), (-1, 1), (1, 1)], "black": [(0, -1), (0, -2), (-1, -1), (1, -1)]},
            "knight": [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)],
            "bishop": [(1, 1), (1, -1), (-1, 1), (-1, -1)],
            "rook": [(1, 0), (-1, 0), (0, 1), (0, -1)],
            "queen": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],
            "king": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],
        }

        # Iterate through all pieces on the board
        for square, piece in board.items():
            piece_colour, piece_type = piece.split("_")
            if piece_colour != player:
                continue  # Skip opponent's pieces

            col, row = ord(square[0]) - ord('a'), int(square[1]) - 1  # Convert board notation to indices

            if piece_type == "pawn":
                move_directions = directions["pawn"][player]
                for direction in move_directions:
                    target_col, target_row = col + direction[0], row + direction[1]

                    # Ensure move is within the board boundaries
                    if self.is_within_bounds(col, row):
                        target_square = f"{chr(target_col + ord('a'))}{target_row + 1}"

                        # Handle forward moves
                        if direction in [(0, 1), (0, -1), (0, 2), (0, -2)]:
                            if target_square not in board:
                                moves.append((square, target_square))

                        # Handle captures
                        elif target_square in board and board[target_square].split("_")[0] != player:
                            moves.append((square, target_square))

            elif piece_type == "knight":
                for direction in directions["knight"]:
                    target_col, target_row = col + direction[0], row + direction[1]
                    if self.is_within_bounds(col, row):
                        target_square = f"{chr(target_col + ord('a'))}{target_row + 1}"
                        if target_square not in board or board[target_square].split("_")[0] != player:
                            moves.append((square, target_square))

            elif piece_type in {"bishop", "rook", "queen"}:
                for direction in directions[piece_type]:
                    for step in range(1, 8):
                        target_col, target_row = col + direction[0] * step, row + direction[1] * step
                        if self.is_within_bounds(col, row):
                            target_square = f"{chr(target_col + ord('a'))}{target_row + 1}"
                            if target_square in board:
                                if board[target_square].split("_")[0] != player:
                                    moves.append((square, target_square))  # Capture
                                break  # Blocked by another piece
                            else:
                                moves.append((square, target_square))  # Free move
                        else:
                            break  # Out of bounds

            elif piece_type == "king":
                for direction in directions["king"]:
                    target_col, target_row = col + direction[0], row + direction[1]
                    if self.is_within_bounds(col, row):
                        target_square = f"{chr(target_col + ord('a'))}{target_row + 1}"
                        if target_square not in board or board[target_square].split("_")[0] != player:
                            moves.append((square, target_square))
        return moves

    def make_move(self, from_square, to_square):
        """Move a piece from one square to another."""

        if from_square in self.board:
            self.board[to_square] = self.board[from_square]  # Move the piece to the new square
            del self.board[from_square]  # Remove the piece from its old square
        else:
            print(f"No piece at {from_square} to move. from chess.py")

    def run(self):
        self.reset()
        bot = threading.Thread(target=self.play_turn)
        bot.start()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

            self.display_update()





        bot.join()


if __name__ == '__main__':
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    pygame.init()
    game = ChessGame()
    game.run()
