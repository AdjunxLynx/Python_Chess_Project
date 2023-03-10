# https://emea01.safelinks.protection.outlook.com/?url=https%3A%2F%2Flevelup.gitconnected.com%2Fchess-python-ca4532c7f5a4&data=04%7C01%7C%7Cd0c85321db5a44db830f08d8ea56fcda%7C84df9e7fe9f640afb435aaaaaaaaaaaa%7C1%7C0%7C637517006617853837%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C1000&sdata=6H8JdLa%2BzY7AHFZ5rAaIyb0Ppivo39PmPTA%2FGhkyaQw%3D&reserved=0
# pygame module
import pygame


class Chess():
    import pygame

    def __init__(self, dimensions=960, fps=999999):
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
        try:
            from Logins import Logins
            self.Logins = Logins
            print(self.Logins)
        except:
            self.Logins = {"kamil": "1234"}

        self.clock = pygame.time.Clock()

        # Typing Variables

        self.pygame.event.set_blocked(771)
        self.selected_colour_username = self.get_selected_colour_username()

        # ## Scene Variables

        self.Credits = False
        self.soloMode = False  # will display the normal chess game when True
        self.Login = True  # the first page is the Login page
        self.mainPage = False  # will display the mainpage of the application when True
        # the mainpage will consist of Start(soloMode), Options, and load(load game)

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

        # colour binary codes:

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

    def display_fps(self):  # Displays current FPS
        fps_counter = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps_counter, True, pygame.Color("coral"))
        self.game_display.blit(fps_text, (910, 0))

    def loadPictures(self):  # loads, resizes and blits active chess pieces
        for i in range(64):
            if self.board[i][2] == "noPicture":
                pass
            elif self.board[i][5] == "life":
                self.piece_image = pygame.image.load("Pictures/" + self.board[i][2])
                self.piece_image = pygame.transform.scale(self.piece_image, (self.boxL, self.boxL))
                self.game_display.blit(self.piece_image, ((self.selected_to_x_y(i)[0] * self.boxL) + 20, (
                        self.selected_to_x_y(i)[
                            1] * self.boxL) + 20))  # self.board[i][2&3] to get x&y co-ordinates respectively

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

    def login(self):
        self.DrawButton(self.black, 330, 300, 800, 100, "Login")

        if self.clickableButton(330, 300, 800, 100):
            try:
                if self.Logins[self.true_username] == self.true_password:
                    print("Logged In")
                    print(
                        "\'{0}\' Successfully logged in with the password:\'{1}\'".format(self.true_username,
                                                                                          self.true_password))
                    return True
                else:
                    print("Incorrect Password ")
                    return False
            except KeyError:
                print("KeyError, No Username or Password to check for")
            except Exception as x:
                print(x)

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

            mouse_x, mouse_y = pygame.mouse.get_pos()
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

    def highlighted(self, selected, Turn):
        if selected is None:
            piece_name = "Null"
            piece_colour = "Null"
            life = "dead"
        else:
            # Finds the values for colour, name and life situation
            piece_colour = self.board[selected][0]
            piece_name = self.board[selected][1]
            life = self.board[selected][5]

        if selected is None:
            pass

        elif life == "life":
            if piece_colour == self.Turn:
                if piece_name == "Rook":
                    for i in range(1, 8):  # ###### highlights rook downwards. Working

                        scan_vertical = (8 * i)
                        skip = False
                        if selected + scan_vertical > 63:
                            skip = True
                        if not skip:
                            if self.board[selected + scan_vertical][0] == "Null":  # to make sure next space is empty
                                # creates vertical rook highlight going down from rook
                                pygame.draw.circle(self.game_display, self.cyan, (
                                    (self.selected_to_x_y(selected)[0] * self.boxL) + 20 + self.boxL / 2,
                                    (i * self.boxL + 20 + self.selected_to_x_y(selected)[
                                        1] * self.boxL + self.boxL / 2)),
                                                   self.circle_radius)
                            elif self.board[selected + scan_vertical][
                                0] != self.Turn:  # if can take opposite colour, will show self.red highlight
                                pygame.draw.circle(self.game_display, self.red, (
                                    (self.selected_to_x_y(selected)[0] * self.boxL) + 20 + self.boxL / 2,
                                    (i * self.boxL + 20 + self.selected_to_x_y(selected)[
                                        1] * self.boxL + self.boxL / 2)),
                                                   self.circle_radius)
                                break
                            elif self.board[selected + scan_vertical][0] == self.Turn:
                                break

                    for i in range(1, 8):  # ###### highlights rook upwards

                        scan_vertical = (8 * i)
                        skip = False
                        if selected - scan_vertical < 0:
                            skip = True
                        if not skip:
                            if self.board[selected - scan_vertical][0] == "Null":
                                # to make sure next space is empty
                                # creates vertical rook highlight going down from rook
                                pygame.draw.circle(self.game_display, self.cyan, (
                                    self.selected_to_x_y(selected)[0] * self.boxL + 20 + self.boxL / 2,
                                    self.selected_to_x_y(selected)[1] * self.boxL - self.boxL * i + self.boxL / 2 + 20),
                                                   self.circle_radius)
                            elif self.board[selected - scan_vertical][
                                0] != self.Turn:  # if can take opposite colour, will show self.red highlight
                                pygame.draw.circle(self.game_display, self.red, (
                                    self.selected_to_x_y(selected)[0] * self.boxL + 20 + self.boxL / 2,
                                    self.selected_to_x_y(selected)[1] * self.boxL - self.boxL * i + self.boxL / 2 + 20),
                                                   self.circle_radius)
                                break
                            elif self.board[selected - scan_vertical][0] == self.Turn:
                                break

                    for i in range(1, 8):  # ### highlights rook to the left
                        skip = False
                        if self.selected_to_x_y(selected - i)[0] < 0:
                            skip = True
                        if not skip:
                            if self.board[selected - i][0] == "Null":
                                # to make sure next space is empty
                                # creates vertical rook highlight going down from rook
                                pygame.draw.circle(self.game_display, self.cyan, (
                                    self.selected_to_x_y(selected)[0] * self.boxL - self.boxL * i + 20 + self.boxL / 2,
                                    self.selected_to_x_y(selected)[1] * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                            elif self.board[selected - i][
                                0] != self.Turn:  # if can take opposite colour, will show self.red highlight
                                pygame.draw.circle(self.game_display, self.red, (
                                    self.selected_to_x_y(selected)[0] * self.boxL - self.boxL * i + 20 + self.boxL / 2,
                                    self.selected_to_x_y(selected)[1] * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break
                            elif self.board[selected - i][0] == self.Turn:
                                break

                    for i in range(1, 8):  # ##### highlights rook to the right
                        skip = False
                        if self.selected_to_x_y(selected + i)[0] == 0 or self.selected_to_x_y(selected + i)[0] > 7:
                            skip = True

                        if self.selected_to_x_y(selected + i)[0] < self.selected_to_x_y(selected)[0]:
                            skip = True

                        if not skip:
                            if self.board[selected + i][0] == "Null":
                                # to make sure next space is empty
                                # creates vertical rook highlight going down from rook
                                pygame.draw.circle(self.game_display, self.cyan, (
                                    self.selected_to_x_y(selected)[0] * self.boxL + self.boxL * i + 20 + self.boxL / 2,
                                    self.selected_to_x_y(selected)[1] * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                            elif self.board[selected + i][
                                0] != self.Turn:  # if can take opposite colour, will show self.red highlight
                                pygame.draw.circle(self.game_display, self.red, (
                                    self.selected_to_x_y(selected)[0] * self.boxL + self.boxL * i + 20 + self.boxL / 2,
                                    self.selected_to_x_y(selected)[1] * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break
                            elif self.board[selected + i][0] == self.Turn:
                                break

                if piece_name == "Pawn":  # ################################################### done i believe
                    # print("Pawn Highlighted")
                    if piece_colour == "White":
                        try:
                            if selected // 8 == 6:
                                if self.board[selected - 8][1] == "Null" and self.board[selected - 16][1] == "Null":
                                    # print("double move possible")
                                    pygame.draw.circle(self.game_display, self.cyan,
                                                       (selected % 8 * self.boxL + 20 + self.boxL / 2,
                                                        self.selected_to_x_y(selected)[1] *
                                                        115 + 20 - self.boxL + self.boxL / 2), self.circle_radius)
                                    pygame.draw.circle(self.game_display, self.cyan,
                                                       (selected % 8 * self.boxL + 20 + self.boxL / 2,
                                                        ((self.selected_to_x_y(selected)[1]) - 1) *
                                                        self.boxL + 20 - self.boxL + self.boxL / 2), self.circle_radius)
                                    self.x_y_to_selected(self.selected_to_x_y(selected)[0],
                                                              self.selected_to_x_y(selected)[1] + 1)

                            if self.board[selected - 8][1] == "Null":

                                # print ("Space in front available ")
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   (selected % 8 * self.boxL + 20 + self.boxL / 2,
                                                    self.selected_to_x_y(selected)[1] *
                                                    self.boxL + 20 - self.boxL + self.boxL / 2), self.circle_radius)
                            else:

                                pass
                            if self.board[selected - 9][0] != self.Turn and self.board[selected - 9][0] != "Null":
                                pygame.draw.circle(self.game_display, self.red, (
                                    (self.selected_to_x_y(selected)[0]) * self.boxL + 20 - self.boxL + self.boxL / 2,
                                    (self.selected_to_x_y(selected)[1]) * self.boxL - self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)

                            # -7 to find top right capture
                            if self.board[selected - 7][0] != self.Turn and self.board[selected - 7][0] != "Null":
                                pygame.draw.circle(self.game_display, self.red, (
                                    (self.selected_to_x_y(selected)[0]) * self.boxL + 20 + self.boxL + self.boxL / 2,
                                    (self.selected_to_x_y(selected)[1]) * self.boxL - self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                        except:
                            pass

                    if piece_colour == "Black":
                        try:
                            if selected // 8 == 1:
                                if self.board[selected + 8][1] == "Null" and self.board[selected + 16][1] == "Null":
                                    # print("double move possible")
                                    pygame.draw.circle(self.game_display, self.cyan,
                                                       (selected % 8 * self.boxL + 20 + self.boxL / 2,
                                                        ((self.selected_to_x_y(selected)[1]) + 3) *
                                                        115 + 20 - self.boxL + self.boxL / 2), self.circle_radius)
                                    pygame.draw.circle(self.game_display, self.cyan,
                                                       (selected % 8 * self.boxL + 20 + self.boxL / 2,
                                                        ((self.selected_to_x_y(selected)[1]) + 2) *
                                                        self.boxL + 20 - self.boxL + self.boxL / 2), self.circle_radius)
                                    self.x_y_to_selected(self.selected_to_x_y(selected)[0],
                                                         self.selected_to_x_y(selected)[1] + 1)

                            if self.board[selected + 8][1] == "Null":

                                # print ("Space in front available ")
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   (selected % 8 * self.boxL + 20 + self.boxL / 2,
                                                    ((self.selected_to_x_y(selected)[1]) + 2) *
                                                    self.boxL + 20 - self.boxL + self.boxL / 2), self.circle_radius)
                            else:
                                # print("space in front not available ")
                                pass
                            if self.board[selected + 9][0] != self.Turn and self.board[selected + 9][0] != "Null":
                                pygame.draw.circle(self.game_display, self.red, (
                                    (self.selected_to_x_y(selected)[
                                         0] + 2) * self.boxL + 20 - self.boxL + self.boxL / 2,
                                    (self.selected_to_x_y(selected)[
                                         1] + 2) * self.boxL - self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)

                            # -7 to find bottom right capture
                            if self.board[selected + 7][0] != self.Turn and self.board[selected + 7][0] != "Null":
                                pygame.draw.circle(self.game_display, self.red, (
                                    (self.selected_to_x_y(selected)[
                                         0] - 2) * self.boxL + 20 + self.boxL + self.boxL / 2,
                                    (self.selected_to_x_y(selected)[
                                         1] + 2) * self.boxL - self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                        except:
                            pass

                    # ########### capture highlighting

                    # -9 to find bottom left capture

                    # ####################

                if piece_name == "Bishop":
                    try:
                        for i in range(1, 8):  # ####up left
                            if self.selected_to_x_y(selected - (9 * i))[0] == -1 or \
                                    self.selected_to_x_y(selected - (9 * i))[1] == -1:
                                break
                            elif self.board[selected - (9 * i)][0] == "Null":
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] - i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] - i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                            elif self.board[selected - (9 * i)][0] != self.Turn:
                                pygame.draw.circle(self.game_display, self.red,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] - i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] - i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break
                            elif self.board[selected - (9 * i)][0] == self.Turn:
                                break

                        for i in range(1, 8):  # #### up right
                            if self.selected_to_x_y(selected - 7 * i)[0] == 8 or self.selected_to_x_y(selected - 7 * i)[
                                1] == 0:
                                break
                            elif self.board[selected - (7 * i)][0] == "Null":
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] + i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] - i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                            elif self.board[selected - (7 * i)][0] != self.Turn:
                                pygame.draw.circle(self.game_display, self.red,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] + i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] - i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break
                            elif self.board[selected - (7 * i)][0] == self.Turn:
                                break

                        for i in range(1, 8):  # ###### down left
                            if self.board[selected + (7 * i)][0] == "Null":
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] - i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] + i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                            elif self.board[selected + (7 * i)][0] != self.Turn:

                                pygame.draw.circle(self.game_display, self.red,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] - i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] + i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break
                            elif self.board[selected + (7 * i)][0] == self.Turn:
                                break
                        for i in range(1, 8):  # ###### down right
                            if self.board[selected + (9 * i)][0] == "Null":
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] + i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] + i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)

                            elif self.board[selected + (9 * i)][0] != self.Turn:
                                pygame.draw.circle(self.game_display, self.red,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] + i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] + i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break

                            elif self.board[selected + (9 * i)][0] == self.Turn:
                                break
                    except:
                        pass

                if piece_name == "Queen":
                    try:
                        for i in range(1, 8):  # ####up left
                            if self.selected_to_x_y(selected - (9 * i))[0] == -1 or \
                                    self.selected_to_x_y(selected - (9 * i))[1] == -1:
                                break
                            elif self.board[selected - (9 * i)][0] == "Null":
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] - i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] - i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                            elif self.board[selected - (9 * i)][0] != self.Turn:
                                pygame.draw.circle(self.game_display, self.red,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] - i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] - i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break
                            elif self.board[selected - (9 * i)][0] == self.Turn:
                                break

                        for i in range(1, 8):  # #### up right
                            if self.selected_to_x_y(selected - 7 * i)[0] == 8 or self.selected_to_x_y(selected - 7 * i)[
                                1] == 0:
                                break
                            elif self.board[selected - (7 * i)][0] == "Null":
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] + i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] - i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                            elif self.board[selected - (7 * i)][0] != self.Turn:
                                pygame.draw.circle(self.game_display, self.red,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] + i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] - i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break
                            elif self.board[selected - (7 * i)][0] == self.Turn:
                                break

                        for i in range(1, 8):  # ###### down left
                            if self.board[selected + (7 * i)][0] == "Null":
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] - i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] + i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                            elif self.board[selected + (7 * i)][0] != self.Turn:

                                pygame.draw.circle(self.game_display, self.red,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] - i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] + i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break
                            elif self.board[selected + (7 * i)][0] == self.Turn:
                                break
                        for i in range(1, 8):  # ###### down right
                            if self.board[selected + (9 * i)][0] == "Null":
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] + i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] + i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)

                            elif self.board[selected + (9 * i)][0] != self.Turn:
                                pygame.draw.circle(self.game_display, self.red,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] + i) * self.boxL + 20 + self.boxL / 2, (
                                                            self.selected_to_x_y(selected)[
                                                                1] + i) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break

                            elif self.board[selected + (9 * i)][0] == self.Turn:
                                break
                    except:
                        pass

                    for i in range(1, 8):  # ###### highlights rook downwards. Working

                        scan_vertical = (8 * i)
                        skip = False
                        if selected + scan_vertical > 63:
                            skip = True
                        if not skip:
                            if self.board[selected + scan_vertical][0] == "Null":  # to make sure next space is empty
                                # creates vertical rook highlight going down from rook
                                pygame.draw.circle(self.game_display, self.cyan, (
                                    (self.selected_to_x_y(selected)[0] * self.boxL) + 20 + self.boxL / 2,
                                    (i * self.boxL + 20 + self.selected_to_x_y(selected)[
                                        1] * self.boxL + self.boxL / 2)),
                                                   self.circle_radius)
                            elif self.board[selected + scan_vertical][
                                0] != self.Turn:  # if can take opposite colour, will show self.red highlight
                                pygame.draw.circle(self.game_display, self.red, (
                                    (self.selected_to_x_y(selected)[0] * self.boxL) + 20 + self.boxL / 2,
                                    (i * self.boxL + 20 + self.selected_to_x_y(selected)[
                                        1] * self.boxL + self.boxL / 2)),
                                                   self.circle_radius)
                                break
                            elif self.board[selected + scan_vertical][0] == self.Turn:
                                break

                    for i in range(1, 8):  # ###### highlights rook upwards

                        scan_vertical = (8 * i)
                        skip = False
                        if selected - scan_vertical < 0:
                            skip = True
                        if not skip:
                            if self.board[selected - scan_vertical][0] == "Null":
                                # to make sure next space is empty
                                # creates vertical rook highlight going down from rook
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   (self.selected_to_x_y(selected)[0] * self.boxL + 20 + self.boxL / 2,
                                                    self.selected_to_x_y(selected)[
                                                        1] * self.boxL - self.boxL * i + 20 + self.boxL / 2),
                                                   self.circle_radius)
                            elif self.board[selected - scan_vertical][
                                0] != self.Turn:  # if can take opposite colour, will show self.red highlight
                                pygame.draw.circle(self.game_display, self.red,
                                                   (self.selected_to_x_y(selected)[0] * self.boxL + 20 + self.boxL / 2,
                                                    self.selected_to_x_y(selected)[
                                                        1] * self.boxL - self.boxL * i + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break
                            elif self.board[selected - scan_vertical][0] == self.Turn:
                                break

                    for i in range(1, 8):  # ### highlights rook to the left
                        skip = False
                        if self.selected_to_x_y(selected - i)[0] == 0:
                            skip = True
                        if not skip:
                            if self.board[selected - i][0] == "Null":
                                # to make sure next space is empty
                                # creates vertical rook highlight going down from rook
                                pygame.draw.circle(self.game_display, self.cyan, (
                                    self.selected_to_x_y(selected)[0] * self.boxL - self.boxL * i + 20 + self.boxL / 2,
                                    self.selected_to_x_y(selected)[1] * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                            elif self.board[selected - i][
                                0] != self.Turn:  # if can take opposite colour, will show self.red highlight
                                pygame.draw.circle(self.game_display, self.red, (
                                    self.selected_to_x_y(selected)[0] * self.boxL - self.boxL * i + 20 + self.boxL / 2,
                                    self.selected_to_x_y(selected)[1] * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break
                            elif self.board[selected - i][0] == self.Turn:
                                break

                    for i in range(1, 8):  # ##### highlights rook to the right
                        skip = False
                        if self.selected_to_x_y(selected + i)[0] == 0:
                            skip = True
                        if not skip:
                            if self.board[selected + i][0] == "Null":
                                # to make sure next space is empty
                                # creates vertical rook highlight going down from rook
                                pygame.draw.circle(self.game_display, self.cyan, (
                                    self.selected_to_x_y(selected)[0] * self.boxL + self.boxL * i + 20 + self.boxL / 2,
                                    self.selected_to_x_y(selected)[1] * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                            elif self.board[selected + i][
                                0] != self.Turn:  # if can take opposite colour, will show self.red highlight
                                pygame.draw.circle(self.game_display, self.red, (
                                    self.selected_to_x_y(selected)[0] * self.boxL + self.boxL * i + 20 + self.boxL / 2,
                                    self.selected_to_x_y(selected)[1] * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)
                                break
                            elif self.board[selected + i][0] == self.Turn:
                                break
                    # will include only code from both rook and bishop
                    # print("Queen Highlighted")

                if piece_name == "King":
                    try:
                        # #### 8 different directions the king can move in
                        if self.board[selected - 9][0] == "Null":  # ### top left
                            pygame.draw.circle(self.game_display, self.cyan,
                                               (
                                                   (self.selected_to_x_y(selected)[
                                                        0] - 1) * self.boxL + 20 + self.boxL / 2,
                                                   (self.selected_to_x_y(selected)[
                                                        1] - 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                        elif self.board[selected - 9][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red,
                                               (
                                                   (self.selected_to_x_y(selected)[
                                                        0] - 1) * self.boxL + 20 + self.boxL / 2,
                                                   (self.selected_to_x_y(selected)[
                                                        1] - 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)

                        if self.board[selected - 8][0] == "Null":  # ### top middle
                            pygame.draw.circle(self.game_display, self.cyan,
                                               (self.selected_to_x_y(selected)[0] * self.boxL + 20 + self.boxL / 2, (
                                                       self.selected_to_x_y(selected)[
                                                           1] - 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                        elif self.board[selected - 8][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red,
                                               (self.selected_to_x_y(selected)[0] * self.boxL + 20 + self.boxL / 2, (
                                                       self.selected_to_x_y(selected)[
                                                           1] - 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)

                        if self.board[selected - 7][0] == "Null":  # ### top right
                            pygame.draw.circle(self.game_display, self.cyan,
                                               (
                                                   (self.selected_to_x_y(selected)[
                                                        0] + 1) * self.boxL + 20 + self.boxL / 2,
                                                   (self.selected_to_x_y(selected)[
                                                        1] - 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)

                        elif self.board[selected - 7][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red,
                                               (
                                                   (self.selected_to_x_y(selected)[
                                                        0] + 1) * self.boxL + 20 + self.boxL / 2,
                                                   (self.selected_to_x_y(selected)[
                                                        1] - 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)

                        if self.board[selected - 1][0] == "Null":  # #### left
                            pygame.draw.circle(self.game_display, self.cyan,
                                               (
                                                   (self.selected_to_x_y(selected)[
                                                        0] - 1) * self.boxL + 20 + self.boxL / 2,
                                                   (
                                                       self.selected_to_x_y(selected)[
                                                           1]) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                            if self.board[selected - 2][0] == "Null" and self.board[selected - 3][0] == "Null" and \
                                    self.board[selected - 4] and self.board[selected]:
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] - 2) * self.boxL + 20 + self.boxL / 2, (
                                                        self.selected_to_x_y(selected)[
                                                            1]) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)

                        elif self.board[selected - 1][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red,
                                               (
                                                   (self.selected_to_x_y(selected)[
                                                        0] - 1) * self.boxL + 20 + self.boxL / 2,
                                                   (
                                                       self.selected_to_x_y(selected)[
                                                           1]) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)

                        if self.board[selected + 1][0] == "Null":  # #### right
                            pygame.draw.circle(self.game_display, self.cyan,
                                               (
                                                   (self.selected_to_x_y(selected)[
                                                        0] + 1) * self.boxL + 20 + self.boxL / 2,
                                                   (
                                                       self.selected_to_x_y(selected)[
                                                           1]) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                            if self.board[selected + 2][0] == "Null" and self.board[selected + 3][6] and self.board[
                                selected]:  # # to castle right, space to right needs to be empty and usual castling rules apply
                                pygame.draw.circle(self.game_display, self.cyan,
                                                   ((self.selected_to_x_y(selected)[
                                                         0] + 2) * self.boxL + 20 + self.boxL / 2, (
                                                        self.selected_to_x_y(selected)[
                                                            1]) * self.boxL + 20 + self.boxL / 2),
                                                   self.circle_radius)

                        elif self.board[selected + 1][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red,
                                               (
                                                   (self.selected_to_x_y(selected)[
                                                        0] + 1) * self.boxL + 20 + self.boxL / 2,
                                                   (
                                                       self.selected_to_x_y(selected)[
                                                           1]) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                        if self.board[selected + 7][0] == "Null":  # #### bottom left
                            pygame.draw.circle(self.game_display, self.cyan,
                                               (
                                                   (self.selected_to_x_y(selected - 1)[
                                                       0]) * self.boxL + 20 + self.boxL / 2,
                                                   (self.selected_to_x_y(selected)[
                                                        1] + 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)

                        elif self.board[selected + 7][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red,
                                               (
                                                   (self.selected_to_x_y(selected - 1)[
                                                       0]) * self.boxL + 20 + self.boxL / 2,
                                                   (self.selected_to_x_y(selected)[
                                                        1] + 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)

                        if self.board[selected + 8][0] == "Null":  # #### bottom
                            pygame.draw.circle(self.game_display, self.cyan,
                                               ((self.selected_to_x_y(selected)[0]) * self.boxL + 20 + self.boxL / 2, (
                                                       self.selected_to_x_y(selected)[
                                                           1] + 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)

                        elif self.board[selected + 8][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red,
                                               ((self.selected_to_x_y(selected)[0]) * self.boxL + 20 + self.boxL / 2, (
                                                       self.selected_to_x_y(selected)[
                                                           1] + 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)

                        if self.board[selected + 9][0] == "Null":  # ##### bottom right
                            pygame.draw.circle(self.game_display, self.cyan,
                                               (
                                                   (self.selected_to_x_y(selected)[
                                                        0] + 1) * self.boxL + 20 + self.boxL / 2,
                                                   (self.selected_to_x_y(selected)[
                                                        1] + 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)

                        elif self.board[selected + 9][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.cyan,
                                               (
                                                   (self.selected_to_x_y(selected)[
                                                        0] + 1) * self.boxL + 20 + self.boxL / 2,
                                                   (self.selected_to_x_y(selected)[
                                                        1] + 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                    except:
                        pass

                if piece_name == "Knight":
                    # print("Knight selected")
                    try:  # while a knight is at the centre of the self.board, it can move normally
                        # ## afaik, this is working perfectly fine.
                        if self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] - 2,
                                                           self.selected_to_x_y(selected)[1] - 1)][
                            0] == "Null":  # 2 left one up
                            pygame.draw.circle(self.game_display, self.cyan, (
                                (self.selected_to_x_y(selected)[0] - 2) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] - 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                        elif self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] - 2,
                                                             self.selected_to_x_y(selected)[1] - 1)][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red, (
                                (self.selected_to_x_y(selected)[0] - 2) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] - 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                    except:
                        pass
                    try:
                        if self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] - 2,
                                                           self.selected_to_x_y(selected)[1] + 1)][
                            0] == "Null":  # 2 left one down
                            pygame.draw.circle(self.game_display, self.cyan, (
                                (self.selected_to_x_y(selected)[0] - 2) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] + 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                        elif self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] - 2,
                                                             self.selected_to_x_y(selected)[1] + 1)][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red, (
                                (self.selected_to_x_y(selected)[0] - 2) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] + 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                    except:
                        pass
                    try:
                        if self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] + 2,
                                                           self.selected_to_x_y(selected)[1] + 1)][
                            0] == "Null":  # 2 right one down
                            pygame.draw.circle(self.game_display, self.cyan, (
                                (self.selected_to_x_y(selected)[0] + 2) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] + 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                        elif self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] + 2,
                                                             self.selected_to_x_y(selected)[1] + 1)][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red, (
                                (self.selected_to_x_y(selected)[0] + 2) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] + 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                    except:
                        pass
                    try:
                        if self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] + 2,
                                                           self.selected_to_x_y(selected)[1] - 1)][
                            0] == "Null":  # 2 right one up
                            pygame.draw.circle(self.game_display, self.cyan, (
                                (self.selected_to_x_y(selected)[0] + 2) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] - 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                        elif self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] + 2,
                                                             self.selected_to_x_y(selected)[1] - 1)][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red, (
                                (self.selected_to_x_y(selected)[0] + 2) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] - 1) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                    except:
                        pass
                    try:
                        if self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] + 1,
                                                           self.selected_to_x_y(selected)[1] + 2)][
                            0] == "Null":  # 1 right 2 down
                            pygame.draw.circle(self.game_display, self.cyan, (
                                (self.selected_to_x_y(selected)[0] + 1) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] + 2) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                        elif self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] + 1,
                                                             self.selected_to_x_y(selected)[1] + 2)][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red, (
                                (self.selected_to_x_y(selected)[0] + 1) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] + 2) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                    except:
                        pass
                    try:
                        if self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] + 1,
                                                           self.selected_to_x_y(selected)[1] - 2)][
                            0] == "Null":  # 1 right 2 up
                            pygame.draw.circle(self.game_display, self.cyan, (
                                (self.selected_to_x_y(selected)[0] + 1) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] - 2) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                        elif self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] + 1,
                                                             self.selected_to_x_y(selected)[1] - 2)][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red, (
                                (self.selected_to_x_y(selected)[0] + 1) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] - 2) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                    except:
                        pass
                    try:
                        if self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] - 1,
                                                           self.selected_to_x_y(selected)[1] + 2)][
                            0] == "Null":  # 1 left 2 down
                            pygame.draw.circle(self.game_display, self.cyan, (
                                (self.selected_to_x_y(selected)[0] - 1) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] + 2) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                        elif self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] - 1,
                                                             self.selected_to_x_y(selected)[1] + 2)][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red, (
                                (self.selected_to_x_y(selected)[0] - 1) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] + 2) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                    except:
                        pass
                    try:

                        if self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] - 1,
                                                           self.selected_to_x_y(selected)[1] - 2)][
                            0] == "Null":  # 1 left 2 up
                            pygame.draw.circle(self.game_display, self.cyan, (
                                (self.selected_to_x_y(selected)[0] - 1) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] - 2) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                        elif self.board[self.x_y_to_selected(self.selected_to_x_y(selected)[0] - 1,
                                                             self.selected_to_x_y(selected)[1] - 2)][0] != self.Turn:
                            pygame.draw.circle(self.game_display, self.red, (
                                (self.selected_to_x_y(selected)[0] - 1) * self.boxL + 20 + self.boxL / 2,
                                (self.selected_to_x_y(selected)[1] - 2) * self.boxL + 20 + self.boxL / 2),
                                               self.circle_radius)
                    except:
                        pass

    def x_y_to_selected(self, x, y):
        if x >= 8 or x < 0 or y >= 8 or y < 0:
            return 10000
        return ((y * 8) + x)

    def swap_colour(self):
        if self.Turn == "White":
            return "Black"
        elif self.Turn == "Black":
            return "White"

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

    def set_blocked_typing(self):
        pygame.event.set_blocked(1025)  # blocks mouse clicks from being detected
        pygame.event.set_blocked(1026)
        pygame.event.set_blocked(1024)  # blocks mouse movement to be detected
        pygame.event.set_blocked(769)

    def run(self):
        while self.gameRunning:

            # ### getters for main

            self.event_list = pygame.event.get()

            # print(event_list)
            self.display_fps()
            pygame.display.flip()
            self.clock.tick(self.FPS)
            self.game_display.fill(self.white)
            mouse_x, mouse_y = self.get_mouse()

            for self.event in self.event_list:
                if self.event.type == pygame.QUIT:
                    self.gameRunning = False

            if not self.typing_username:
                selected_colour_username = (0, 0, 0)
            if self.typing_username:
                selected_colour_username = (100, 100, 255)

            if not self.typing_password:
                selected_colour_password = (0, 0, 0)
            if self.typing_password:
                selected_colour_password = (100, 255, 100)

            if self.Login:
                font = pygame.font.SysFont("calibri", 30)
                pygame.draw.rect(self.game_display, self.grey, (330, 400, 300, 100), 5)
                # creates username text box
                pygame.draw.rect(self.game_display, self.grey, (330, 600, 300, 100), 5)
                # creates username password box

                self.game_display.blit(font.render(self.true_username, True, selected_colour_username), (350, 435))
                # noinspection PyUnboundLocalVariable
                self.game_display.blit(font.render(self.hidden_password, True, selected_colour_password), (350, 635))
                # game_display.blit(font.render(true_password, True, selected_colour_password), (350, 700))

                if self.username == "" and not self.typing_username:
                    self.game_display.blit(font.render("username", True, selected_colour_username), (350, 435))
                    # if empty and not ready to type, will display username
                if self.password == "" and not self.typing_password:
                    self.game_display.blit(font.render("hidden password", True, selected_colour_password), (350, 635))
                    # if empty and not ready to type, will display password

                self.hidden_password = "*" * len(self.true_password)
                # creates a password that looks "encrypted"

                if self.login():
                    self.mainPage = True
                    self.Login = False

                if self.exclusiveButton(330, 300, 400, 100):
                    self.typing_username = False

                if self.exclusiveButton(330, 300, 600, 100):
                    self.typing_password = False

                if self.clickableButton(330, 300, 400, 100):
                    self.typing_username = True
                    self.typing_password = False

                if self.clickableButton(330, 300, 600, 100):
                    self.typing_username = False
                    self.typing_password = True

                if self.typing_username:
                    #self.Login = False  # ## comment out for password
                    #self.mainPage = True  # ## comment out for password
                    # ## foo
                    pygame.event.set_blocked(1025)  # blocks mouse clicks from being detected
                    pygame.event.set_blocked(1026)
                    pygame.event.set_blocked(1024)  # blocks mouse movement to be detected
                    pygame.event.set_blocked(769)  # blocks key up inputs KeyUp

                    if self.input_text(self.event_list, self.username) is None:
                        pass
                    elif self.input_text(self.event_list, self.username) == "backspace":
                        self.true_username = self.true_username[0:len(self.true_username) - 1]
                    else:
                        self.username = str(self.input_text(self.event_list, self.username))
                        self.true_username += self.username
                        pygame.event.set_allowed(769)  # allows key up inputs to be detected
                        pygame.event.set_allowed(1024)  # allows mouse movement to be detected

                if self.typing_password:
                    pygame.event.set_blocked(769)  # blocks key up inputs KeyUp
                    pygame.event.set_blocked(1024)  # blocks mouse movements to be detected
                    pygame.event.set_blocked(1025)  # blocks mouse clicks to be detected
                    pygame.event.set_blocked(1026)
                    if self.input_text(self.event_list, self.password) is None:
                        pass
                    elif self.input_text(self.event_list, self.password) == "backspace":
                        self.true_password = self.true_password[0:len(self.true_password) - 1]
                    else:
                        self.password = str(self.input_text(self.event_list, self.password))
                        self.true_password += self.password
                        pygame.event.set_allowed(1024)  # allows mouse movement to be detected
                        pygame.event.set_allowed(769)  # allows key up inputs to be detected
                pygame.event.set_allowed(1025)  # allows mouse clicks to be detected
                pygame.event.set_allowed(1026)
            if self.mainPage:

                font = pygame.font.SysFont("calibri", 30)
                self.DrawButton(self.grey, 380, 200, 600, 80, "Solo Mode")
                if self.clickableButton(380, 200, 600, 80):
                    self.mainPage = False
                    self.soloMode = True

                # draws button for chess game

                pygame.draw.rect(self.game_display, self.brown, (10, 10, 100, 35))
                self.game_display.blit(font.render("Credits", True, self.black), (10, 10))
                # draws button for credits screen

                if self.clickableButton(10, 100, 10, 35):
                    self.mainPage = False
                    self.Credits = True

                # creates button for credits screen
            if self.Credits:

                pygame.draw.rect(self.game_display, self.lBrown, (380, 200, 200, 80))
                self.game_display.blit(font.render("Credits:", True, self.black), (410, 225))

                self.game_display.blit(
                    font.render("https://levelup.gitconnected.com/chess-python-ca4532c7f5a4", True, self.black),
                    (60, 275))
                self.game_display.blit(font.render("https://www.stackoverflow.com/adjunxlynx", True, self.black),
                                       (60, 305))
                self.game_display.blit(font.render("https://www.google.com", True, self.black), (60, 335))
                # my sources

                self.game_display.blit(font.render("Made by Kamil Leocadie-Olsen", True, self.black), (250, 800))
                # creator
                self.DrawButton(self.black, 890, 60, 10, 50, "back")

                # draws a back button to go to to main screen
                if self.clickableButton(890, 70, 10, 50):
                    self.mainPage = True
                    self.Credits = False

            if self.soloMode:

                self.chosen = self.selected()
                # print(self.chosen)
                x, y = self.selected_to_x_y(self.chosen)
                self.DrawBoard()
                self.loadPictures()
                if self.moving:
                    self.highlighted(self.chosen_index, self.Turn)
                else:
                    self.highlighted(self.chosen, self.Turn)

                self.DrawButton(self.cyan, 0, 30, 0, 15, "back")
                font = pygame.font.SysFont("calibri", 12)
                pygame.draw.rect(self.game_display, self.cyan, (0, 0, 30, 15))
                self.game_display.blit(font.render("back", True, self.black),
                                       (0, 0))  # draws a back button to go back to Mainscreen

                if self.ischeckmate(self.board) == "white":
                    print("white won")
                elif self.ischeckmate(self.board) == "black":
                    print("black won")

                if self.clickableButton(0, 30, 0, 15):
                    self.soloMode = False
                    self.mainPage = True
                    # creates a back button to go back to Mainscreen
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


if __name__ == "__main__":
    display = Chess()
    display.run()
