# pygame module
import pygame
import threading
import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # Convert seconds to milliseconds
        print(f"{func.__name__} took {execution_time:.5f} ms to run.")
        return result
    return wrapper

class Chess():
    import pygame

    def __init__(self, dimensions=960, fps=9999999):
        self.event_list = None
        self.piece_image = None
        self.mouse_x, self.mouse_y = None, None
        pygame.init()
        self.Dimensions = dimensions
        self.font = pygame.font.SysFont("calibri", 30)

        # setting up the font for text
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.cyan = (0, 255, 255)
        self.grey = (150, 150, 150)
        self.brown = (139, 69, 19)
        self.lBrown = (235, 188, 128)
        self.peach = (255, 211, 129)
        self.green = (0, 0, 255)

        self.game_display = pygame.display.set_mode((self.Dimensions, self.Dimensions))
        pygame.display.set_caption("Chess")

        self.FPS = fps

        # self.boxL means the diameter of a singular chess piece location.
        self.boxL = int((self.Dimensions - 40) / 8)  # will be 115
        # minus 40 so there is a white self.boarder outline on the edge of the self.board, divide by 8 because
        # self.board is 8 by 8
        try:
            from board import board
            self.board = board
        except:
            print("Starting Board could not be found ")

        self.true_username = ""
        self.true_password = ""
        self.username = ""
        self.password = ""
        self.hidden_password = ""
        self.typing_username = False
        self.typing_password = False

        self.clock = pygame.time.Clock()

        # Typing Variables

        self.pygame.event.set_blocked(771)
        self.selected_colour_username = self.get_selected_colour_username()

        # ## Scene Variables

        self.Credits = False
        self.soloMode = False  # will display the normal chess game when True
        self.mainPage = True  # will display the mainpage of the application when True

        # ## moving Piece Variables
        self.movingPiece = False
        self.piece_moving = 100
        self.moving_multiple = 0
        self.colour_moving_white = True
        self.circle_radius = 15
        self.moving = False
        self.chosen_piece = []
        self.blocked_x = 0
        self.blocked_y = 0
        self.check_ghost = False

        # ## Loading Images
        self.loading = True

        # Chess self.board Display variables
        self.Turn = "White"
        self.gameRunning = True
        self.event = []

    # Functions
    # #### colours
    # colour binary codes:

    def get_mouse(self):
        return pygame.mouse.get_pos()

    def clickableButton(self, x_starting_pos, x_length, y_starting_pos, y_length):  # detects if click inside area
        self.mouse_x, self.mouse_y = self.get_mouse()
        if (x_starting_pos <= self.mouse_x <= x_starting_pos + x_length) and (
                y_starting_pos <= self.mouse_y <= y_starting_pos + y_length):
            for self.event in self.event_list:
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    return True

    def exclusiveButton(self, x_starting_pos, x_length, y_starting_pos, y_length):  # detects if click is not in an area
        self.mouse_x, self.mouse_y = self.get_mouse()
        if (self.mouse_x <= x_starting_pos or self.mouse_x >= x_starting_pos + x_length) or (
                self.mouse_y <= y_starting_pos or self.mouse_y >= y_starting_pos + y_length):
            for self.event in self.event_list:
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    return True

    def DrawButton(self, colour, x_starting_pos, x_length, y_starting_pos, y_length,
                   text):  # draws a rectangle on locations
        pygame.draw.rect(self.game_display, colour, (x_starting_pos, y_starting_pos, x_length, y_length))
        self.game_display.blit(self.font.render(text, True, self.cyan), (x_starting_pos, y_starting_pos))

    #@measure_time
    def display_fps(self):  # Displays current FPS
        fps_counter = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps_counter, True, pygame.Color("coral"))
        self.game_display.blit(fps_text, (910, 0))

    #@measure_time
    def DrawBoard(self):
        for X in range(4):
            for Y in range(4):
                box_x = self.boxL * 2 * (X + 1)
                box_y = self.boxL * 2 * Y
                pygame.draw.rect(self.game_display, self.lBrown, (box_x - 210, box_y + 20, self.boxL, self.boxL))
                pygame.draw.rect(self.game_display, self.brown, (box_x - 95, box_y + 20, self.boxL, self.boxL))

                pygame.draw.rect(self.game_display, self.lBrown, (box_x - 95, box_y + 135, self.boxL, self.boxL))
                pygame.draw.rect(self.game_display, self.brown, (box_x - 210, box_y + 135, self.boxL, self.boxL))

        pygame.draw.rect(self.game_display, self.black, (20, 20, 920, 920), 1)

    # format for piece = [colour, rank, picture, x, y, life?]

    #@measure_time
    def loadPictures(self):  # loads, resizes and blits active chess pieces
        # Cache images during initialisation or when needed
        if not hasattr(self, "image_cache"):
            self.image_cache = {}

        for i in range(64):
            if self.board[i][2] == "noPicture":
                continue

            if self.board[i][5] == "life":
                piece_name = self.board[i][2]

                # Load and cache the image if it's not already cached
                if piece_name not in self.image_cache:
                    image = pygame.image.load(f"Pictures/{piece_name}")
                    image = pygame.transform.scale(image, (self.boxL, self.boxL))
                    self.image_cache[piece_name] = image

                # Use the cached image
                self.piece_image = self.image_cache[piece_name]
                x_coord, y_coord = self.selected_to_x_y(i)
                self.game_display.blit(self.piece_image, (x_coord * self.boxL + 20, y_coord * self.boxL + 20))

    def input_text(self, eventLists, name):
        try:
            # I don't even know why this works but returns letter pressed
            backspace = False
            for self.event in eventLists:
                if self.event.type == pygame.KEYDOWN:
                    if self.event.key == pygame.K_BACKSPACE:
                        backspace = True
                    name = str(chr(self.event.key))
                if backspace:
                    return "backspace"
                else:
                    return name
        except ValueError:
            print("Value error. most likely shift or caps lock pressed ")
        except:
            print("Unknown Error ")

    def selected(self):  # returns value of 0-64 based on chess self.board
        mouse_x, mouse_y = self.get_mouse()
        for horizontal_squares in range(9):
            for vertical_squares in range(9):
                if ((horizontal_squares - 1) * self.boxL) + 20 <= mouse_x <= (horizontal_squares * self.boxL) + 20 and (
                        (vertical_squares - 1) * self.boxL) + 20 <= mouse_y <= (vertical_squares * self.boxL + 20):
                    piece_position = (horizontal_squares + ((vertical_squares - 1) * 8))
                    return piece_position - 1  # -1 cause of indexing
        return None  # essentially an else return

    def selected_to_x_y(self, selected):  # converts 0-63 to x and y coord
        try:
            selected = int(selected)
            y = selected // 8
            x = selected % 8
            return x, y
        except:
            return 1000, 1000  # values that will never be used.

    def get_selected_colour_username(self):
        selected_colour_username = (0, 0, 0)
        return selected_colour_username

    def get_selected_colour_password(self):
        selected_colour_password = (0, 0, 0)
        return selected_colour_password

    def get_selected_colour(self):
        selected_colour = (0, 0, 0)
        return selected_colour

    def ischeckmate(self, board):  # ###if they are both alive, game still in progress else returns whoever won
        balive = False
        walive = False
        for i in range(64):
            if self.board[i][1] == "King":
                if self.board[i][0] == "White":
                    walive = True
                if self.board[i][0] == "Black":
                    balive = True
        if balive and walive:
            return False
        elif balive:
            return "black "
        elif walive:
            return "white"

    def promote(self, event):

        if self.Turn[0] == "W":
            #  ## Due to the loop, the self.Turn has changed before checking if pawn has promoted so need to inverse it here
            lower_turn = "b"
        else:
            lower_turn = "w"
            #  #### don't need to check for "B" as there are only 2 options

        knight = pygame.image.load("Pictures/" + str(lower_turn) + "_knight.png")
        knight = pygame.transform.scale(knight, (self.boxL, self.boxL))

        queen = pygame.image.load("Pictures/" + str(lower_turn) + "_queen.png")
        queen = pygame.transform.scale(queen, (self.boxL, self.boxL))

        rook = pygame.image.load("Pictures/" + str(lower_turn) + "_rook.png")
        rook = pygame.transform.scale(rook, (self.boxL, self.boxL))

        bishop = pygame.image.load("Pictures/" + str(lower_turn) + "_bishop.png")
        bishop = pygame.transform.scale(bishop, (self.boxL, self.boxL))
        promoted = False

        while not promoted:
            self.event_list = pygame.event.get()
            for self.event in self.event_list:
                if self.event.type == pygame.QUIT:
                    return None

            pygame.display.flip()
            self.game_display.fill(self.white)
            self.loadPictures()
            self.DrawBoard()

            mouse_x, mouse_y = self.get_mouse()
            pygame.draw.rect(self.game_display, self.black,
                             (self.height / 2 - self.boxL, self.height / 2 - self.boxL, 2 * self.boxL, 2 * self.boxL))

            self.game_display.blit(knight, ((self.Dimensions / 2) - self.boxL, (self.Dimensions / 2) - self.boxL))
            self.game_display.blit(rook, ((self.Dimensions / 2), (self.Dimensions / 2) - self.boxL))
            self.game_display.blit(queen, ((self.Dimensions / 2) - self.boxL, (self.Dimensions / 2)))
            self.game_display.blit(bishop, ((self.Dimensions / 2), (self.Dimensions / 2)))

            if ((self.Dimensions / 2) <= mouse_x <= (self.Dimensions / 2) + self.boxL) and (
                    (self.Dimensions / 2) <= mouse_y <= (self.Dimensions / 2) + self.boxL):
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    #  print("Bishop selected")
                    #  print("Bishop")
                    return "Bishop"

            if ((self.Dimensions / 2) - self.boxL <= mouse_x <= (self.Dimensions / 2)) and (
                    (self.Dimensions / 2) <= mouse_y <= (self.Dimensions / 2) + self.boxL):
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    #  print("Queen selected")
                    #  print("Queen")
                    return "Queen"

            if ((self.Dimensions / 2) <= mouse_x <= (self.Dimensions / 2) + self.boxL) and (
                    (self.Dimensions / 2) - self.boxL <= mouse_y <= (self.Dimensions / 2)):
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    # print("Rook selected")
                    #  print("Rook")
                    return "Rook"

            if ((self.Dimensions / 2) - self.boxL <= mouse_x <= (self.Dimensions / 2)) and (
                    (self.Dimensions / 2) - self.boxL <= mouse_y <= (self.Dimensions / 2)):
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    #  print("Knight selected")
                    #  print("Knight")
                    return "Knight"

    def emulate_position(self, selected, offset):
        new_position = selected + offset
        if 0 <= new_position < 64:
            return new_position
        return None

    def highlight_rook(self, selected):
        directions = [8, -8, 1, -1]  # down, up, right, left
        for direction in directions:
            for i in range(1, 8):
                new_position = self.emulate_position(selected, direction * i)
                if new_position is None:
                    break
                piece = self.board[new_position]
                if piece[0] == "Null":
                    pygame.draw.circle(self.game_display, self.cyan, (
                        (self.selected_to_x_y(new_position)[0] * self.boxL) + 20 + self.boxL / 2,
                        (self.selected_to_x_y(new_position)[1] * self.boxL) + 20 + self.boxL / 2),
                                       self.circle_radius)
                elif piece[0] != self.Turn:
                    pygame.draw.circle(self.game_display, self.red, (
                        (self.selected_to_x_y(new_position)[0] * self.boxL) + 20 + self.boxL / 2,
                        (self.selected_to_x_y(new_position)[1] * self.boxL) + 20 + self.boxL / 2),
                                       self.circle_radius)
                    break
                else:
                    break

    def highlight_pawn(self, selected, piece_colour):
        direction = -8 if piece_colour == "White" else 8
        start_row = 6 if piece_colour == "White" else 1
        try:
            if selected // 8 == start_row:
                if self.board[selected + direction][1] == "Null" and self.board[selected + 2 * direction][1] == "Null":
                    for offset in [direction, 2 * direction]:
                        new_position = self.emulate_position(selected, offset)
                        if new_position is not None:
                            pygame.draw.circle(self.game_display, self.cyan, (
                                (selected % 8 * self.boxL) + 20 + self.boxL / 2,
                                (self.selected_to_x_y(new_position)[1] * self.boxL) + 20 + self.boxL / 2),
                                               self.circle_radius)

            if self.board[selected + direction][1] == "Null":
                new_position = self.emulate_position(selected, direction)
                if new_position is not None:
                    pygame.draw.circle(self.game_display, self.cyan, (
                        (selected % 8 * self.boxL) + 20 + self.boxL / 2,
                        (self.selected_to_x_y(new_position)[1] * self.boxL) + 20 + self.boxL / 2),
                                       self.circle_radius)

            for capture_offset in [-1, 1]:
                new_position = self.emulate_position(selected, direction + capture_offset)
                if new_position is not None and self.board[new_position][0] != self.Turn and self.board[new_position][
                    0] != "Null":
                    pygame.draw.circle(self.game_display, self.red, (
                        (self.selected_to_x_y(new_position)[0] * self.boxL) + 20 + self.boxL / 2,
                        (self.selected_to_x_y(new_position)[1] * self.boxL) + 20 + self.boxL / 2),
                                       self.circle_radius)
        except IndexError:
            pass

    def highlight_bishop(self, selected):
        directions = [9, -9, 7, -7]  # up-right, down-left, up-left, down-right
        for direction in directions:
            for i in range(1, 8):
                new_position = self.emulate_position(selected, direction * i)
                if new_position is None:
                    break
                piece = self.board[new_position]
                if piece[0] == "Null":
                    pygame.draw.circle(self.game_display, self.cyan, (
                        (self.selected_to_x_y(new_position)[0] * self.boxL) + 20 + self.boxL / 2,
                        (self.selected_to_x_y(new_position)[1] * self.boxL) + 20 + self.boxL / 2),
                                       self.circle_radius)
                elif piece[0] != self.Turn:
                    pygame.draw.circle(self.game_display, self.red, (
                        (self.selected_to_x_y(new_position)[0] * self.boxL) + 20 + self.boxL / 2,
                        (self.selected_to_x_y(new_position)[1] * self.boxL) + 20 + self.boxL / 2),
                                       self.circle_radius)
                    break
                else:
                    break

    def highlight_queen(self, selected):
        self.highlight_rook(selected)
        self.highlight_bishop(selected)

    def highlight_king(self, selected):
        offsets = [-9, -8, -7, -1, 1, 7, 8, 9]
        for offset in offsets:
            new_position = self.emulate_position(selected, offset)
            if new_position is not None:
                piece = self.board[new_position]
                if piece[0] == "Null":
                    pygame.draw.circle(self.game_display, self.cyan, (
                        (self.selected_to_x_y(new_position)[0] * self.boxL) + 20 + self.boxL / 2,
                        (self.selected_to_x_y(new_position)[1] * self.boxL) + 20 + self.boxL / 2),
                                       self.circle_radius)
                elif piece[0] != self.Turn:
                    pygame.draw.circle(self.game_display, self.red, (
                        (self.selected_to_x_y(new_position)[0] * self.boxL) + 20 + self.boxL / 2,
                        (self.selected_to_x_y(new_position)[1] * self.boxL) + 20 + self.boxL / 2),
                                       self.circle_radius)

    def highlight_knight(self, selected):
        offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
        for offset in offsets:
            new_position = self.emulate_position(selected, offset)
            if new_position is not None:
                piece = self.board[new_position]
                if piece[0] == "Null":
                    pygame.draw.circle(self.game_display, self.cyan, (
                        (self.selected_to_x_y(new_position)[0] * self.boxL) + 20 + self.boxL / 2,
                        (self.selected_to_x_y(new_position)[1] * self.boxL) + 20 + self.boxL / 2),
                                       self.circle_radius)
                elif piece[0] != self.Turn:
                    pygame.draw.circle(self.game_display, self.red, (
                        (self.selected_to_x_y(new_position)[0] * self.boxL) + 20 + self.boxL / 2,
                        (self.selected_to_x_y(new_position)[1] * self.boxL) + 20 + self.boxL / 2),
                                       self.circle_radius)

    def highlighted(self, selected, Turn):
        if selected is None:
            return

        piece_colour = self.board[selected][0]
        piece_name = self.board[selected][1]
        life = self.board[selected][5]

        if life != "life" or piece_colour != self.Turn:
            return

        if piece_name == "Rook":
            self.highlight_rook(selected)
        elif piece_name == "Pawn":
            self.highlight_pawn(selected, piece_colour)
        elif piece_name == "Bishop":
            self.highlight_bishop(selected)
        elif piece_name == "Queen":
            self.highlight_queen(selected)
        elif piece_name == "King":
            self.highlight_king(selected)
        elif piece_name == "Knight":
            self.highlight_knight(selected)

    def x_y_to_selected(self, x, y):
        if x >= 8 or x < 0 or y >= 8 or y < 0:
            return 10000
        return ((y * 8) + x)

    def swap_colour(self):
        if self.Turn == "White":
            return "Black"
        elif self.Turn == "Black":
            return "White"

    def set_blocked_typing(self):
        pygame.event.set_blocked(1025)  # blocks mouse clicks from being detected
        pygame.event.set_blocked(1026)
        pygame.event.set_blocked(1024)  # blocks mouse movement to be detected
        pygame.event.set_blocked(769)

    def solo_mode_display(self):
        while self.gameRunning:
            self.game_display.fill(self.white)
            self.DrawBoard()#
            self.loadPictures()#
            self.display_fps()#
            # Refreshes the screen
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def solo_mode_logic(self):
        while self.gameRunning:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.gameRunning = False


            self.chosen = self.selected()
            # print(self.chosen)
            x, y = self.selected_to_x_y(self.chosen)
            mouse_x, mouse_y = self.get_mouse()

            if self.moving:
                self.highlighted(self.chosen_index, self.Turn)
            else:
                self.highlighted(self.chosen, self.Turn)

            if self.ischeckmate(self.board) == "white":
                print("white won")
            elif self.ischeckmate(self.board) == "black":
                print("black won")

            for i in range(64):
                if self.board[i][1] == "Pawn":
                    if i // 8 == 0 or i // 8 == 7:
                        print("pawn about to be promoted")
                        self.promoted_piece = self.promote(self.event)
                        self.promoted_piece = str(self.promoted_piece)

                        if self.promoted_piece is None:
                            self.gameRunning = False
                            print("Quitting")
                        else:
                            self.promoted_picture = (self.promoted_piece + ".png")
                            self.board[self.x_y_to_selected(self.board[i][3], self.board[i][4])][1] == str(
                                self.promoted_piece)
                            self.board[i][1] = self.promoted_piece

                            self.promoted_piece = self.promoted_piece.lower()
                            print(self.x_y_to_selected(self.board[i][3], self.board[i][4]))
                            self.board[self.chosen_index][0] == str(self.Turn)

                            self.board[i][3] == self.selected_to_x_y(self.board[i][3])
                            self.board[i][4] == self.selected_to_x_y(self.board[i][4])

                            self.picture = (self.swap_colour(self.Turn)[0].lower() + "_" + self.promoted_picture)
                            self.board[i][2] = self.picture.lower()
                            break

            if not self.moving:
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    if self.chosen is None:
                        pass
                    elif self.board[self.chosen][0] == self.Turn:
                        self.chosen_piece = self.board[self.chosen]
                        self.choice = self.chosen
                        print("Chosen", self.chosen_piece[1])
                        self.chosen_index = self.chosen
                        self.moving = True

            self.check_ghost = True

            for i in range(64):
                if self.check_ghost:
                    if self.board[i][5] == "ghost":
                        if self.board[i][0] == self.Turn:
                            self.board[i][0] = "Null"
                            self.board[i][1] = "Null"
                            self.board[i][2] = "noPicture"
                            self.board[i][5] = "dead"
                            print(self.board[i])
                            self.check_ghost = False
                            print("getting rid of ghost at", i)

            if self.moving:
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    if self.event.button == 3 or (mouse_x < 20 or mouse_x > 940) or (mouse_y > 940 or mouse_y < 20):
                        self.chosen_piece = ["", "", ""]
                        self.moving = False
                        print("Deselected")

                if self.chosen is None:
                    pass
                elif self.chosen_piece[0] == self.Turn:
                    if self.chosen_piece[5] == "life":
                        if self.chosen_piece[1] == "Queen":

                            #  ###Bishop half of queen

                            if self.board[self.chosen][0] == self.Turn:  # Cant take my own piece
                                pass  # don't wanna take my own piece
                            elif self.event.type == pygame.MOUSEBUTTONDOWN:  # #### taking the initial click as me wanting to move piece to its own location
                                if self.board[
                                    self.chosen] == self.chosen_piece:  # so it doesnt swap to its own location
                                    pass

                                self.allow_move = True

                                if abs(self.selected_to_x_y(self.chosen)[0] -
                                       self.selected_to_x_y(self.chosen_index)[0]) == abs(
                                    self.selected_to_x_y(self.chosen)[1] -
                                    self.selected_to_x_y(self.chosen_index)[
                                        1]):  # ### to ensure along a diagonal as the change in y and change in x shld be equal
                                    try:
                                        for i in range(1, self.selected_to_x_y(self.chosen)[0] -
                                                          self.selected_to_x_y(self.chosen_index)[
                                                              0]):  # could have chosen y. doesnt matter

                                            if self.Turn in self.board[
                                                self.x_y_to_selected(self.selected_to_x_y(self.chosen)[0] + i,
                                                                     self.selected_to_x_y(self.chosen)[1] + i)]:
                                                self.allow_move = False
                                                break
                                            elif self.Turn in self.board[
                                                self.x_y_to_selected(self.selected_to_x_y(self.chosen)[0] + i,
                                                                     self.selected_to_x_y(self.chosen)[1] - i)]:
                                                self.allow_move = False
                                                break
                                            elif self.Turn in self.board[
                                                self.x_y_to_selected(self.selected_to_x_y(self.chosen)[0] - i,
                                                                     self.selected_to_x_y(self.chosen)[1] + i)]:
                                                self.allow_move = False
                                                break
                                            elif self.Turn in self.board[
                                                self.x_y_to_selected(self.selected_to_x_y(self.chosen)[0] - i,
                                                                     self.selected_to_x_y(self.chosen)[1] - i)]:
                                                self.allow_move = False
                                                break
                                    except:
                                        pass
                                    if self.allow_move:
                                        #  ########################## afaik, this works perfectly fine
                                        if self.selected_to_x_y(self.chosen)[0] == self.chosen_piece[
                                            3]:  # if the x coordinate is the same as the moving to where the mouse is
                                            if self.board[self.chosen][0] == self.Turn:  # Cant take my own piece
                                                pass  # don't wanna take my own piece
                                            elif self.event.type == pygame.MOUSEBUTTONDOWN:  # #### taking the initial click as me wanting to move piece to its own location
                                                if self.board[
                                                    self.chosen] == self.chosen_piece:  # so it doesnt swap to its own location
                                                    pass

                                                self.allow_move = True
                                                for i in range(1, self.selected_to_x_y(self.chosen)[1] -
                                                                  self.chosen_piece[
                                                                      4]):  # ##### to find the the the distance between original and place i want to move
                                                    if self.Turn in self.board[self.chosen_index + 8 * i][0]:
                                                        self.allow_move = False
                                                        break

                                                if self.allow_move:
                                                    print("taking " + str(self.board[self.chosen]))
                                                    self.board[
                                                        self.chosen] = self.chosen_piece  # ### making where the mouse is, the piece selected
                                                    self.board[self.chosen][3] = self.selected_to_x_y(self.chosen)[
                                                        0]  # #### correcting values within the self.board[self.chosen]
                                                    self.board[self.chosen][4] = self.selected_to_x_y(self.chosen)[
                                                        1]  # #### correcting values within the self.board[self.chosen]
                                                    self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                                     self.selected_to_x_y(
                                                                                         self.chosen_index)[0],
                                                                                     self.selected_to_x_y(
                                                                                         self.chosen_index)[1],
                                                                                     "dead"]  # ### setting the old square to empty
                                                    self.moving = False
                                                    self.allow_move = False
                                                    self.Turn = self.swap_colour()

                            # #################### Rook half of Queen is done

                            # print(self.chosen_piece)
                            # print(self.selected_to_x_y(self.chosen)[1], self.chosen_piece[4])

                            #  ########################## afaik, this works perfectly fine
                            if self.selected_to_x_y(self.chosen)[0] == self.chosen_piece[
                                3]:  # if the x coordinate is the same as the moving to where the mouse is
                                if self.board[self.chosen][0] == self.Turn:  # Cant take my own piece
                                    pass  # don't wanna take my own piece
                                elif self.event.type == pygame.MOUSEBUTTONDOWN:  # #### taking the initial click as me wanting to move piece to its own location
                                    if self.board[
                                        self.chosen] == self.chosen_piece:  # so it doesnt swap to its own location
                                        pass

                                    self.allow_move = True
                                    for i in range(1, self.selected_to_x_y(self.chosen)[1] - self.chosen_piece[
                                        4]):  # ##### to find the the the distance between original and place i want to move
                                        if self.Turn in self.board[self.chosen_index + 8 * i][0]:
                                            self.allow_move = False
                                            break

                                    if self.allow_move:
                                        print("taking " + str(self.board[self.chosen]))
                                        self.board[
                                            self.chosen] = self.chosen_piece  # ### making where the mouse is, the piece selected
                                        self.board[self.chosen][3] = self.selected_to_x_y(self.chosen)[
                                            0]  # #### correcting values within the self.board[self.chosen]
                                        self.board[self.chosen][4] = self.selected_to_x_y(self.chosen)[
                                            1]  # #### correcting values within the self.board[self.chosen]
                                        self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                         self.selected_to_x_y(self.chosen_index)[0],
                                                                         self.selected_to_x_y(self.chosen_index)[1],
                                                                         "dead"]  # ### setting the old square to empty
                                        self.moving = False
                                        self.allow_move = False
                                        self.Turn = self.swap_colour()

                            if self.selected_to_x_y(self.chosen)[1] == self.chosen_piece[
                                4]:  # if the y coordinate is the same as the moving to where the mouse is
                                if self.board[self.chosen][0] == self.Turn:  # Cant take my own piece
                                    pass  # don't wanna take my own piece

                                elif self.event.type == pygame.MOUSEBUTTONDOWN:  # #### taking the initial click as me wanting to move piece to its own location
                                    if self.board[
                                        self.chosen] == self.chosen_piece:  # so it doesnt swap to its own location
                                        pass

                                    self.allow_move = True
                                    for i in range(1, self.selected_to_x_y(self.chosen)[0] - self.chosen_piece[
                                        3]):  # ###### to find the the the distance between original and place i want to move
                                        if self.Turn in self.board[self.chosen_index + i][0]:
                                            self.allow_move = False
                                            break

                                    if self.allow_move:
                                        print("taking " + str(self.board[self.chosen]))
                                        self.board[self.chosen] = self.chosen_piece
                                        self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                         self.selected_to_x_y(self.chosen_index)[0],
                                                                         self.selected_to_x_y(self.chosen_index)[1],
                                                                         "dead"]
                                        self.moving = False

                                        self.allow_move = False
                                        self.Turn = self.swap_colour(self.Turn)

                        if self.chosen_piece[1] == "Bishop":

                            if self.board[self.chosen][0] == self.Turn:  # Cant take my own piece
                                pass  # don't wanna take my own piece
                            elif self.event.type == pygame.MOUSEBUTTONDOWN:  # #### taking the initial click as me wanting to move piece to its own location
                                if self.board[
                                    self.chosen] == self.chosen_piece:  # so it doesnt swap to its own location
                                    pass

                                self.allow_move = True

                                if abs(self.selected_to_x_y(self.chosen)[0] -
                                       self.selected_to_x_y(self.chosen_index)[0]) == abs(
                                    self.selected_to_x_y(self.chosen)[1] -
                                    self.selected_to_x_y(self.chosen_index)[
                                        1]):  # ### to ensure along a diaganol
                                    try:
                                        for i in range(1, self.selected_to_x_y(self.chosen)[0] -
                                                          self.selected_to_x_y(self.chosen_index)[0]):

                                            if self.Turn in self.board[
                                                self.x_y_to_selected(self.selected_to_x_y(self.chosen)[0] + i,
                                                                     self.selected_to_x_y(self.chosen)[1] + i)]:
                                                self.allow_move = False
                                                break
                                            elif self.Turn in self.board[
                                                self.x_y_to_selected(self.selected_to_x_y(self.chosen)[0] + i,
                                                                     self.selected_to_x_y(self.chosen)[1] - i)]:
                                                self.allow_move = False
                                                break
                                            elif self.Turn in self.board[
                                                self.x_y_to_selected(self.selected_to_x_y(self.chosen)[0] - i,
                                                                     self.selected_to_x_y(self.chosen)[1] + i)]:
                                                self.allow_move = False
                                                break
                                            elif self.Turn in self.board[
                                                self.x_y_to_selected(self.selected_to_x_y(self.chosen)[0] - i,
                                                                     self.selected_to_x_y(self.chosen)[1] - i)]:
                                                self.allow_move = False
                                                break
                                    except:
                                        pass
                                    if self.allow_move:
                                        print("taking " + str(self.board[self.chosen]))
                                        self.board[
                                            self.chosen] = self.chosen_piece  # ### making where the mouse is, the piece selected
                                        self.board[self.chosen][3] = self.selected_to_x_y(self.chosen)[
                                            0]  # #### correcting values within the self.board[self.chosen]
                                        self.board[self.chosen][4] = self.selected_to_x_y(self.chosen)[
                                            1]  # #### correcting values within the self.board[self.chosen]
                                        self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                         self.selected_to_x_y(self.chosen_index)[0],
                                                                         self.selected_to_x_y(self.chosen_index)[1],
                                                                         "dead"]  # ### setting the old square to empty
                                        moving = False
                                        allow_move = False
                                        self.Turn = self.swap_colour(self.Turn)

                        if self.chosen_piece[1] == "Rook":  # ### DONE ROOK

                            #  ########################## afaik, this works perfectly fine
                            if self.selected_to_x_y(self.chosen)[0] == self.chosen_piece[
                                3]:  # if the x coordinate is the same as the moving to where the mouse is
                                if self.board[self.chosen][0] == self.Turn:  # Cant take my own piece
                                    pass  # don't wanna take my own piece
                                elif self.event.type == pygame.MOUSEBUTTONDOWN:  # #### taking the initial click as me wanting to move piece to its own location
                                    if self.board[
                                        self.chosen] == self.chosen_piece:  # so it doesnt swap to its own location
                                        pass

                                    self.allow_move = True
                                    for i in range(1, self.selected_to_x_y(self.chosen)[1] - self.chosen_piece[
                                        4]):  # ##### to find the the the distance between original and place i want to move
                                        if self.Turn in self.board[self.chosen_index + 8 * i][0]:
                                            self.allow_move = False
                                            break

                                    if self.allow_move:
                                        print("taking " + str(self.board[self.chosen]))
                                        self.board[
                                            self.chosen] = self.chosen_piece  # ### making where the mouse is, the piece selected
                                        self.board[self.chosen][3] = self.selected_to_x_y(self.chosen)[
                                            0]  # #### correcting values within the self.board[self.chosen]
                                        self.board[self.chosen][4] = self.selected_to_x_y(self.chosen)[
                                            1]  # #### correcting values within the self.board[self.chosen]
                                        self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                         self.selected_to_x_y(self.chosen_index)[0],
                                                                         self.selected_to_x_y(self.chosen_index)[1],
                                                                         "dead"]  # ### setting the old square to empty
                                        self.moving = False
                                        self.allow_move = False
                                        self.Turn = self.swap_colour(self.Turn)

                            # #################### AFAIK, Done

                            # print(self.chosen_piece)
                            # print(self.selected_to_x_y(self.chosen)[1], self.chosen_piece[4])

                            if self.selected_to_x_y(self.chosen)[1] == self.chosen_piece[
                                4]:  # if the y coordinate is the same as the moving to where the mouse is
                                if self.board[self.chosen][0] == self.Turn:  # Cant take my own piece
                                    pass  # don't wanna take my own piece

                                elif self.event.type == pygame.MOUSEBUTTONDOWN:  # #### taking the initial click as me wanting to move piece to its own location
                                    if self.board[
                                        self.chosen] == self.chosen_piece:  # so it doesnt swap to its own location
                                        pass

                                    self.allow_move = True
                                    for i in range(1, self.selected_to_x_y(self.chosen)[0] - self.chosen_piece[
                                        3]):  # ###### to find the the the distance between original and place i want to move
                                        if self.Turn in self.board[self.chosen_index + i][0]:
                                            allow_move = False
                                            break

                                    if self.allow_move:
                                        print("taking " + str(self.board[self.chosen]))
                                        self.board[self.chosen] = self.chosen_piece
                                        self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                         self.selected_to_x_y(self.chosen_index)[0],
                                                                         self.selected_to_x_y(self.chosen_index)[1],
                                                                         "dead"]
                                        self.moving = False
                                        self.allow_move = False
                                        self.Turn = self.swap_colour(self.Turn)

                        if self.chosen_piece[1] == "King":  # AFAIK, WORKING PERFECTLY FINE
                            if self.board[self.chosen][0] == self.Turn:  # Cant take my own piece
                                pass  # don't wanna take my own piece
                            elif self.event.type == pygame.MOUSEBUTTONDOWN:  # #### taking the initial click as me wanting to move piece to its own location
                                if self.board[
                                    self.chosen] == self.chosen_piece:  # so it doesnt swap to its own location
                                    pass

                                if self.chosen == self.chosen_index + 1:  # to the right
                                    print("taking " + str(self.board[self.chosen]))
                                    self.board[self.chosen] = self.chosen_piece
                                    self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                     self.selected_to_x_y(self.chosen_index)[0],
                                                                     self.selected_to_x_y(self.chosen_index)[1],
                                                                     "dead"]
                                    self.board[self.chosen][6] = False  # it has now moved
                                    self.moving = False
                                    self.Turn = self.swap_colour(self.Turn)

                                if self.chosen == self.chosen_index - 1:  # to the left
                                    print("taking " + str(self.board[self.chosen]))
                                    self.board[self.chosen] = self.chosen_piece
                                    self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                     self.selected_to_x_y(self.chosen_index)[0],
                                                                     self.selected_to_x_y(self.chosen_index)[1],
                                                                     "dead"]
                                    self.board[self.chosen][6] = False  # it has now moved
                                    self.moving = False
                                    self.Turn = self.swap_colour(self.Turn)

                                if self.chosen == self.chosen_index - 7:  # top right
                                    print("taking " + str(self.board[self.chosen]))
                                    self.board[self.chosen] = self.chosen_piece
                                    self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                     self.selected_to_x_y(self.chosen_index)[0],
                                                                     self.selected_to_x_y(self.chosen_index)[1],
                                                                     "dead"]
                                    self.board[self.chosen][6] = False  # it has now moved
                                    self.moving = False

                                if self.chosen == self.chosen_index - 8:  # above
                                    print("taking " + str(self.board[self.chosen]))
                                    self.board[self.chosen] = self.chosen_piece
                                    self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                     self.selected_to_x_y(self.chosen_index)[0],
                                                                     self.selected_to_x_y(self.chosen_index)[1],
                                                                     "dead"]
                                    self.board[self.chosen][6] = False  # it has now moved
                                    self.moving = False
                                    self.Turn = self.swap_colour(self.Turn)

                                if self.chosen == self.chosen_index - 9:  # top left
                                    print("taking " + str(self.board[self.chosen]))
                                    self.board[self.chosen] = self.chosen_piece
                                    self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                     self.selected_to_x_y(self.chosen_index)[0],
                                                                     self.selected_to_x_y(self.chosen_index)[1],
                                                                     "dead"]
                                    self.board[self.chosen][6] = False  # it has now moved
                                    self.moving = False
                                    self.Turn = self.swap_colour(self.Turn)

                                if self.chosen == self.chosen_index + 7:  # bottom left
                                    print("taking " + str(self.board[self.chosen]))
                                    self.board[self.chosen] = self.chosen_piece
                                    self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                     self.selected_to_x_y(self.chosen_index)[0],
                                                                     self.selected_to_x_y(self.chosen_index)[1],
                                                                     "dead"]
                                    self.board[self.chosen][6] = False  # it has now moved
                                    self.moving = False
                                    self.Turn = self.swap_colour(self.Turn)

                                if self.chosen == self.chosen_index + 8:  # down
                                    print("taking " + str(self.board[self.chosen]))
                                    self.board[self.chosen] = self.chosen_piece
                                    self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                     self.selected_to_x_y(self.chosen_index)[0],
                                                                     self.selected_to_x_y(self.chosen_index)[1],
                                                                     "dead"]
                                    self.board[self.chosen][6] = False  # it has now moved
                                    self.moving = False
                                    self.Turn = self.swap_colour(self.Turn)

                                if self.chosen == self.chosen_index + 9:  # bottom right
                                    print("taking " + str(self.board[self.chosen]))
                                    self.board[self.chosen] = self.chosen_piece
                                    self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                     self.selected_to_x_y(self.chosen_index)[0],
                                                                     self.selected_to_x_y(self.chosen_index)[1],
                                                                     "dead"]
                                    self.board[self.chosen][6] = False  # it has now moved
                                    self.moving = False
                                    self.Turn = self.swap_colour(self.Turn)

                                if self.chosen == self.chosen_index + 2:  # castling rules to right
                                    print("Castling right")
                                    try:
                                        if self.board[self.chosen_index][6] and self.board[self.chosen_index + 3][
                                            6]:  # if neither rook or king has moved before
                                            if self.board[self.chosen][0] == "Null" and self.board[self.chosen - 1][
                                                0] == "Null":  # if both spaces empty to castle to right
                                                self.board[self.chosen] = self.board[self.chosen_index]
                                                self.board[self.chosen][6] = False
                                                self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                                 self.selected_to_x_y(
                                                                                     self.chosen + 1)[0],
                                                                                 self.selected_to_x_y(
                                                                                     self.chosen + 1)[1], "dead"]
                                                self.board[self.chosen - 1] = self.board[self.chosen + 1]
                                                self.board[self.chosen - 1][6] = False
                                                self.board[self.chosen + 1] = ["Null", "Null", "noPicture",
                                                                               self.selected_to_x_y(
                                                                                   self.chosen + 1)[0],
                                                                               self.selected_to_x_y(
                                                                                   self.chosen + 1)[1], "dead"]
                                                self.Turn = self.swap_colour(self.Turn)
                                                self.moving = False
                                    except:
                                        pass

                                if self.chosen == self.chosen_index - 2:
                                    print("Castling Left")
                                    try:
                                        if self.board[self.chosen_index][6] and self.board[self.chosen_index - 4][
                                            6]:  # if neither rook or king has moved before
                                            if self.board[self.chosen][0] == "Null" and self.board[self.chosen - 1][
                                                0] == "Null" and self.board[self.chosen + 1][
                                                0] == "Null":  # if both spaces empty to castle to right
                                                self.board[self.chosen] = self.board[self.chosen_index]
                                                self.board[self.chosen][6] = False
                                                self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                                 self.selected_to_x_y(
                                                                                     self.chosen + 2)[0],
                                                                                 self.selected_to_x_y(
                                                                                     self.chosen + 2)[1], "dead"]
                                                self.board[self.chosen + 1] = self.board[self.chosen - 2]
                                                self.board[self.chosen + 1][6] = False
                                                self.board[self.chosen - 2] = ["Null", "Null", "noPicture",
                                                                               self.selected_to_x_y(
                                                                                   self.chosen - 2)[0],
                                                                               self.selected_to_x_y(
                                                                                   self.chosen - 2)[1], "dead"]

                                                self.Turn = self.swap_colour(self.Turn)
                                                self.moving = False
                                    except:
                                        pass

                        if self.chosen_piece[1] == "Knight":  # ###DONE

                            if self.board[self.chosen][0] == self.Turn:  # Cant take my own piece
                                pass  # don't wanna take my own piece
                            elif self.event.type == pygame.MOUSEBUTTONDOWN:  # #### taking the initial click as me wanting to move piece to its own location
                                if self.board[
                                    self.chosen] == self.chosen_piece:  # so it doesnt swap to its own location
                                    pass

                                if self.selected_to_x_y(self.chosen)[0] == self.selected_to_x_y(self.chosen_index)[
                                    0] + 2 or \
                                        self.selected_to_x_y(self.chosen)[0] == \
                                        self.selected_to_x_y(self.chosen_index)[0] - 2:
                                    if self.selected_to_x_y(self.chosen)[1] == \
                                            self.selected_to_x_y(self.chosen_index)[1] + 1:
                                        print("taking " + str(self.board[self.chosen]))
                                        self.board[self.chosen] = self.chosen_piece
                                        self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                         self.selected_to_x_y(self.chosen_index)[0],
                                                                         self.selected_to_x_y(self.chosen_index)[1],
                                                                         "dead"]
                                        self.moving = False
                                        self.Turn = self.swap_colour(self.Turn)

                                    elif self.selected_to_x_y(self.chosen)[1] == \
                                            self.selected_to_x_y(self.chosen_index)[1] - 1:
                                        print("taking " + str(self.board[self.chosen]))
                                        self.board[self.chosen] = self.chosen_piece
                                        self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                         self.selected_to_x_y(self.chosen_index)[0],
                                                                         self.selected_to_x_y(self.chosen_index)[1],
                                                                         "dead"]
                                        self.moving = False
                                        self.Turn = self.swap_colour(self.Turn)

                                if self.selected_to_x_y(self.chosen)[0] == self.selected_to_x_y(self.chosen_index)[
                                    0] + 1 or \
                                        self.selected_to_x_y(self.chosen)[0] == \
                                        self.selected_to_x_y(self.chosen_index)[0] - 1:
                                    if self.selected_to_x_y(self.chosen)[1] == \
                                            self.selected_to_x_y(self.chosen_index)[1] + 2:
                                        print("taking " + str(self.board[self.chosen]))
                                        self.board[self.chosen] = self.chosen_piece
                                        self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                         self.selected_to_x_y(self.chosen_index)[0],
                                                                         self.selected_to_x_y(self.chosen_index)[1],
                                                                         "dead"]
                                        self.moving = False
                                        self.Turn = self.swap_colour(self.Turn)

                                    elif self.selected_to_x_y(self.chosen)[1] == \
                                            self.selected_to_x_y(self.chosen_index)[1] - 2:
                                        print("taking " + str(self.board[self.chosen]))
                                        self.board[self.chosen] = self.chosen_piece
                                        self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                         self.selected_to_x_y(self.chosen_index)[0],
                                                                         self.selected_to_x_y(self.chosen_index)[1],
                                                                         "dead"]
                                        self.moving = False
                                        self.Turn = self.swap_colour()

                        if self.chosen_piece[1] == "Pawn":

                            if self.board[self.chosen][0] == self.Turn:  # Cant take my own piece
                                pass  # don't wanna take my own piece
                            elif self.event.type == pygame.MOUSEBUTTONDOWN:  # #### taking the initial click as me wanting to move piece to its own location
                                if self.board[
                                    self.chosen] == self.chosen_piece:  # so it doesnt swap to its own location
                                    pass
                                if self.board[self.chosen_index][0] == "Black":
                                    if self.board[self.chosen][
                                        0] == "Null":  # ## If pawn just wants to traverse, and not capture
                                        if self.selected_to_x_y(self.chosen)[0] == \
                                                self.selected_to_x_y(self.chosen_index)[
                                                    0]:  # x position will never change so need to check this
                                            if self.selected_to_x_y(self.chosen_index)[1] == 1:  # if on 2nd rank
                                                if self.selected_to_x_y(self.chosen)[1] == 3:  # to double jump
                                                    print("taking " + str(self.board[self.chosen]))
                                                    self.board[self.chosen] = self.chosen_piece
                                                    self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                        self.selected_to_x_y(self.chosen)[0], \
                                                            self.selected_to_x_y(self.chosen)[1]
                                                    self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                                     self.selected_to_x_y(
                                                                                         self.chosen_index)[0],
                                                                                     self.selected_to_x_y(
                                                                                         self.chosen_index)[1],
                                                                                     "dead"]
                                                    self.moving = False
                                                    self.Turn = self.swap_colour()

                                                    # #### Creating ghost pawn to allow en passant
                                                    self.board[self.chosen_index + 8] = ["Black", "Pawn",
                                                                                         "noPicture",
                                                                                         self.selected_to_x_y(
                                                                                             self.chosen_index)[
                                                                                             0],
                                                                                         self.selected_to_x_y(
                                                                                             self.chosen_index)[
                                                                                             1] + 1, "ghost"]
                                                    check_ghost = True

                                            if self.selected_to_x_y(self.chosen)[1] == \
                                                    self.selected_to_x_y(self.chosen_index)[
                                                        1] + 1:
                                                print("taking " + str(self.board[self.chosen]))
                                                self.board[self.chosen] = self.chosen_piece
                                                self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                    self.selected_to_x_y(self.chosen)[0], \
                                                        self.selected_to_x_y(self.chosen)[1]
                                                self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                                 self.selected_to_x_y(
                                                                                     self.chosen_index)[0],
                                                                                 self.selected_to_x_y(
                                                                                     self.chosen_index)[1],
                                                                                 "dead"]
                                                self.moving = False
                                                self.Turn = self.swap_colour()

                                    if self.board[self.chosen][5] == "ghost":
                                        if self.chosen == self.x_y_to_selected(
                                                self.selected_to_x_y(self.chosen_index)[0] - 1,
                                                self.selected_to_x_y(self.chosen_index)[
                                                    1] + 1):  # bottom left
                                            print("taking " + str(self.board[self.chosen]))
                                            self.board[self.chosen] = self.chosen_piece
                                            self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                self.selected_to_x_y(self.chosen)[
                                                    0], \
                                                    self.selected_to_x_y(self.chosen)[
                                                        1]
                                            self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[0],
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[1], "dead"]
                                            self.board[self.chosen - 8] = ["Null", "Null", "noPicture",
                                                                           self.selected_to_x_y(self.chosen_index)[
                                                                               0],
                                                                           self.selected_to_x_y(self.chosen_index)[
                                                                               1], "dead"]
                                            print("ghost taken as ", self.Turn)
                                            self.moving = False
                                            self.Turn = self.swap_colour()

                                        if self.chosen == self.x_y_to_selected(
                                                self.selected_to_x_y(self.chosen_index)[0] + 1,
                                                self.selected_to_x_y(self.chosen_index)[
                                                    1] + 1):  # bottom right

                                            print("taking " + str(self.board[self.chosen]))
                                            self.board[self.chosen] = self.chosen_piece
                                            self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                self.selected_to_x_y(self.chosen)[
                                                    0], \
                                                    self.selected_to_x_y(self.chosen)[
                                                        1]
                                            self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[0],
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[1], "dead"]
                                            self.board[self.chosen - 8] = ["Null", "Null", "noPicture",
                                                                           self.selected_to_x_y(self.chosen_index)[
                                                                               0],
                                                                           self.selected_to_x_y(self.chosen_index)[
                                                                               1], "dead"]
                                            print("ghost taken as ", self.Turn)
                                            self.moving = False
                                            self.Turn = self.swap_colour(self.Turn)
                                            print("board is now", str(self.board[self.chosen]))

                                    elif self.board[self.chosen][0] != self.Turn and self.board[self.chosen][
                                        0] != "Null":  # if pawn wants to capture
                                        if self.chosen == self.x_y_to_selected(
                                                self.selected_to_x_y(self.chosen_index)[0] - 1,
                                                self.selected_to_x_y(self.chosen_index)[
                                                    1] + 1):  # bottom left
                                            print("taking " + str(self.board[self.chosen]))
                                            self.board[self.chosen] = self.chosen_piece
                                            self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                self.selected_to_x_y(self.chosen)[
                                                    0], \
                                                    self.selected_to_x_y(self.chosen)[
                                                        1]
                                            self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[0],
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[1], "dead"]
                                            moving = False
                                            self.Turn = self.swap_colour(self.Turn)

                                        if self.chosen == self.x_y_to_selected(
                                                self.selected_to_x_y(self.chosen_index)[0] + 1,
                                                self.selected_to_x_y(self.chosen_index)[
                                                    1] + 1):  # bottom right
                                            print("taking " + str(self.board[self.chosen]))
                                            self.board[self.chosen] = self.chosen_piece
                                            self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                self.selected_to_x_y(self.chosen)[
                                                    0], \
                                                    self.selected_to_x_y(self.chosen)[
                                                        1]
                                            self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[0],
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[1], "dead"]
                                            self.moving = False
                                            self.Turn = self.swap_colour()

                                # #######

                                elif self.board[self.chosen_index][0] == "White":
                                    if self.board[self.chosen][
                                        0] == "Null":  # ## If pawn just wants to traverse, and not capture
                                        if self.selected_to_x_y(self.chosen)[0] == \
                                                self.selected_to_x_y(self.chosen_index)[
                                                    0]:  # x position will never change so need to check this
                                            if self.selected_to_x_y(self.chosen_index)[1] == 6:  # if on 7th rank
                                                if self.selected_to_x_y(self.chosen)[1] == 4:  # to double jump
                                                    print("taking " + str(self.board[self.chosen]))
                                                    self.board[self.chosen] = self.chosen_piece
                                                    self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                        self.selected_to_x_y(self.chosen)[0], \
                                                            self.selected_to_x_y(self.chosen)[1]
                                                    self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                                     self.selected_to_x_y(
                                                                                         self.chosen_index)[0],
                                                                                     self.selected_to_x_y(
                                                                                         self.chosen_index)[1],
                                                                                     "dead"]
                                                    self.moving = False
                                                    self.Turn = self.swap_colour()

                                                    # #### Creating ghost pawn to allow en passant
                                                    self.board[self.chosen_index - 8] = ["White", "Pawn",
                                                                                         "noPicture",
                                                                                         self.selected_to_x_y(
                                                                                             self.chosen_index)[
                                                                                             0],
                                                                                         self.selected_to_x_y(
                                                                                             self.chosen_index)[
                                                                                             1] + 1, "ghost"]
                                                    self.check_ghost = True

                                            if self.selected_to_x_y(self.chosen)[1] == \
                                                    self.selected_to_x_y(self.chosen_index)[
                                                        1] - 1:
                                                print("taking " + str(self.board[self.chosen]))
                                                self.board[self.chosen] = self.chosen_piece
                                                self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                    self.selected_to_x_y(self.chosen)[0], \
                                                        self.selected_to_x_y(self.chosen)[1]
                                                self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                                 self.selected_to_x_y(
                                                                                     self.chosen_index)[0],
                                                                                 self.selected_to_x_y(
                                                                                     self.chosen_index)[1],
                                                                                 "dead"]
                                                self.moving = False
                                                self.Turn = self.swap_colour()

                                    if self.board[self.chosen][5] == "ghost":  # ### if can en passant
                                        if self.chosen == self.x_y_to_selected(
                                                self.selected_to_x_y(self.chosen_index)[0] - 1,
                                                self.selected_to_x_y(self.chosen_index)[
                                                    1] - 1):  # top left
                                            print("taking " + str(self.board[self.chosen]))
                                            self.board[self.chosen] = self.chosen_piece
                                            self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                self.selected_to_x_y(self.chosen)[
                                                    0], \
                                                    self.selected_to_x_y(self.chosen)[
                                                        1]
                                            self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[0],
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[1], "dead"]
                                            self.board[self.chosen + 8] = ["Null", "Null", "noPicture",
                                                                           self.selected_to_x_y(self.chosen_index)[
                                                                               0],
                                                                           self.selected_to_x_y(self.chosen_index)[
                                                                               1], "dead"]
                                            print("ghost taken as ", self.Turn)
                                            self.moving = False
                                            self.Turn = self.swap_colour()

                                        if self.chosen == self.x_y_to_selected(
                                                self.selected_to_x_y(self.chosen_index)[0] + 1,
                                                self.selected_to_x_y(self.chosen_index)[
                                                    1] - 1):  # top right
                                            print("taking " + str(self.board[self.chosen]))
                                            self.board[self.chosen] = self.chosen_piece
                                            self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                self.selected_to_x_y(self.chosen)[
                                                    0], \
                                                    self.selected_to_x_y(self.chosen)[
                                                        1]
                                            self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[0],
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[1], "dead"]
                                            self.board[self.chosen + 8] = ["Null", "Null", "noPicture",
                                                                           self.selected_to_x_y(self.chosen_index)[
                                                                               0],
                                                                           self.selected_to_x_y(self.chosen_index)[
                                                                               1], "dead"]
                                            print("ghost taken as ", self.Turn)
                                            self.moving = False
                                            self.Turn = self.swap_colour()

                                    elif self.board[self.chosen][0] != self.Turn and self.board[self.chosen][
                                        0] != "Null":  # if pawn wants to capture diagonally normally
                                        if self.chosen == self.x_y_to_selected(
                                                self.selected_to_x_y(self.chosen_index)[0] - 1,
                                                self.selected_to_x_y(self.chosen_index)[
                                                    1] - 1):  # top left
                                            print("taking " + str(self.board[self.chosen]))
                                            self.board[self.chosen] = self.chosen_piece
                                            self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                self.selected_to_x_y(self.chosen)[
                                                    0], \
                                                    self.selected_to_x_y(self.chosen)[
                                                        1]
                                            self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[0],
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[1], "dead"]
                                            self.moving = False
                                            self.Turn = self.swap_colour()

                                        if self.chosen == self.x_y_to_selected(
                                                self.selected_to_x_y(self.chosen_index)[0] + 1,
                                                self.selected_to_x_y(self.chosen_index)[
                                                    1] - 1):  # top right
                                            print("taking " + str(self.board[self.chosen]))
                                            self.board[self.chosen] = self.chosen_piece
                                            self.board[self.chosen][3], self.board[self.chosen][4] = \
                                                self.selected_to_x_y(self.chosen)[
                                                    0], \
                                                    self.selected_to_x_y(self.chosen)[
                                                        1]
                                            self.board[self.chosen_index] = ["Null", "Null", "noPicture",
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[0],
                                                                             self.selected_to_x_y(
                                                                                 self.chosen_index)[1], "dead"]
                                            self.moving = False
                                            self.Turn = self.swap_colour()




    def run(self):
        board_display = threading.Thread(target = self.solo_mode_display)
        board_display.start()
        self.solo_mode_logic()

        board_display.join()




if __name__ == "__main__":
    display = Chess()
    display.run()
