import pygame
from concurrent.futures import ThreadPoolExecutor
import threading
import random
import time
from copy import deepcopy


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
        # Heatmap values for each piece type
        self.heatmap = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 999  # King has no value in terms of material
        }
        self.max_depth = 2  # Maximum depth for recursive search
        print(f"Using a recursion depth of {self.max_depth}({round(self.max_depth/2)} moves deep)")
        self.time_limit = 99995  # Time limit in seconds for move calculation

    def evaluate_board(self, board):
        """Evaluate the board and return a score."""
        score = 0

        #Positional heatmap for pawns (encourages central control)
        pawn_position_bonus = {
            "a1": 0, "b1": 0, "c1": 0, "d1": 0, "e1": 0, "f1": 0, "g1": 0, "h1": 0,
            "a2": 1, "b2": 1, "c2": 1, "d2": 1, "e2": 1, "f2": 1, "g2": 1, "h2": 1,
            "a3": 2, "b3": 3, "c3": 3, "d3": 4, "e3": 4, "f3": 3, "g3": 3, "h3": 2,
            "a4": 3, "b4": 4, "c4": 5, "d4": 7, "e4": 7, "f4": 5, "g4": 4, "h4": 3,
            "a5": 3, "b5": 4, "c5": 5, "d5": 7, "e5": 7, "f5": 5, "g5": 4, "h5": 3,
            "a6": 2, "b6": 3, "c6": 3, "d6": 4, "e6": 4, "f6": 3, "g6": 3, "h6": 2,
            "a7": 1, "b7": 1, "c7": 1, "d7": 1, "e7": 1, "f7": 1, "g7": 1, "h7": 1,
            "a8": 0, "b8": 0, "c8": 0, "d8": 0, "e8": 0, "f8": 0, "g8": 0, "h8": 0
        }

        for position, piece in board.items():
            piece_type = piece.split("_")[1]
            piece_value = self.heatmap.get(piece_type, 0)

            # Adjust pawn scores based on position
            # Positive means white is winning
            if piece.startswith('white'):
                if piece_type == "pawn":
                    piece_value += pawn_position_bonus.get(position, 0)
                score += piece_value
            else:
                piece_value -= pawn_position_bonus.get(position, 0)
                score -= piece_value
        #print(f"Score {score} found for player {self.player} on board {board}")
        return score


    def calculate_best_move(self, board, player, turn):
        """Calculate the best move for the player using threading."""
        start_time = time.time()
        best_move = None
        best_score = float('inf') if player == 'black' else float('-inf')
        legal_moves = self.generate_legal_moves(board, player)
        is_maximising = (player == 'white')

        # Function to evaluate a single move
        def evaluate_move(move):
            new_board = self.make_move(deepcopy(board), *move, legal_moves)
            score = self.minimax(new_board, self.max_depth,float('-inf'), float('inf'), is_maximising, start_time)
            return move, score

        # Use ThreadPoolExecutor to evaluate moves in parallel
        with ThreadPoolExecutor() as executor:
            results = executor.map(evaluate_move, legal_moves)

        # Find the best move from results
        for move, score in results:
            if (player == 'black' and score < best_score) or (player == 'white' and score > best_score):
                best_score = score
                best_move = move
                print(f"New best move {move}, giving a score of {score}")

        print(f"best move returned: {best_move}")
        return best_move

    #@measure_time
    def minimax(self, board, depth, alpha, beta, is_maximizing, start_time):
        """Minimax algorithm with time limit."""
        if depth == 0 or time.time() - start_time > self.time_limit:
            return self.evaluate_board(board)

        if is_maximizing: # If emulated player is white
            max_eval = float('-inf')
            legal_moves = self.generate_legal_moves(board, 'black')
            for move in legal_moves:
                new_board = self.make_move(deepcopy(board), *move, legal_moves)
                eval = self.minimax(new_board, depth - 1, alpha, beta, False, start_time)
                max_eval = max(max_eval, eval)
                alpha = max_eval
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = float('inf')
            legal_moves = self.generate_legal_moves(board, 'white')
            for move in legal_moves:
                new_board = self.make_move(deepcopy(board), *move, 'white')
                eval = self.minimax(new_board, depth - 1, alpha, beta,True, start_time)
                min_eval = min(min_eval, eval)

                beta = min_eval
                if beta <= alpha:
                    break
            return min_eval

    #@measure_time
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
                    if 0 <= target_col < 8 and 0 <= target_row < 8:
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
                    if 0 <= target_col < 8 and 0 <= target_row < 8:
                        target_square = f"{chr(target_col + ord('a'))}{target_row + 1}"
                        if target_square not in board or board[target_square].split("_")[0] != player:
                            moves.append((square, target_square))

            elif piece_type in {"bishop", "rook", "queen"}:
                for direction in directions[piece_type]:
                    for step in range(1, 8):
                        target_col, target_row = col + direction[0] * step, row + direction[1] * step
                        if 0 <= target_col < 8 and 0 <= target_row < 8:
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
                    if 0 <= target_col < 8 and 0 <= target_row < 8:
                        target_square = f"{chr(target_col + ord('a'))}{target_row + 1}"
                        if target_square not in board or board[target_square].split("_")[0] != player:
                            moves.append((square, target_square))
        return moves

    #@measure_time
    def make_move(self, board, from_square, to_square, legal_moves):
        """Move a piece from one square to another."""
        if from_square in board:
            board[to_square] = board[from_square]  # Move the piece to the new square
            del board[from_square]  # Remove the piece from its old square
        return board


class ChessGame:
    def __init__(self):
        pygame.init()
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
        with open('res/initial_position.txt', 'r') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    position, piece = line.strip().split()
                    board[position] = piece
        return board

    def reset(self):
        self.board = self.load_initial_position()
        self.current_turn = random.choice(['white', 'black'])
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
                colour = colours[(row + col) % 2]
                pygame.draw.rect(
                    self.screen,
                    colour,
                    pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size))

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
                move = self.bot.calculate_best_move(self.board, self.bot_colour, self.current_turn)
                self.make_move(*move)
                self.swap_turn()

            else:
                move = self.bot.calculate_best_move(self.board, self.player_colour, self.current_turn)
                self.make_move(*move)
                self.swap_turn()

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
                    if 0 <= target_col < 8 and 0 <= target_row < 8:
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
                    if 0 <= target_col < 8 and 0 <= target_row < 8:
                        target_square = f"{chr(target_col + ord('a'))}{target_row + 1}"
                        if target_square not in board or board[target_square].split("_")[0] != player:
                            moves.append((square, target_square))

            elif piece_type in {"bishop", "rook", "queen"}:
                for direction in directions[piece_type]:
                    for step in range(1, 8):
                        target_col, target_row = col + direction[0] * step, row + direction[1] * step
                        if 0 <= target_col < 8 and 0 <= target_row < 8:
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
                    if 0 <= target_col < 8 and 0 <= target_row < 8:
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
    game = ChessGame()
    game.run()