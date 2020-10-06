
import pygame
import time
import copy


# setup constant values
VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]
INDEXES = [0, 1, 2, 3, 4, 5, 6, 7, 8]
WIDTH1, WIDTH2 = 900, 630
WIDTH = WIDTH2
DIFF = int(WIDTH / 9)
HEIGHT = WIDTH + DIFF
FPS = 120
HOLD = 2
FONT = 'Calibri'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
LIGHTGREY = (192, 192, 192)
DARKGREY = (64, 64, 64)
GREEN = (0, 255, 0)
PINK = (255, 0, 127)
BLUE = (0, 128, 255)
RED = (255, 0, 0)
LIGHTPURPLE = (229, 204, 255)
LIGHTORANGE = (255, 178, 102)


FONTSIZELARGE = 80 - int((WIDTH1 - WIDTH) / 10)
FONTSIZESMALL = 30 - int((WIDTH1 - WIDTH) / 25)
FONTSIZEWORD = 40 - int((WIDTH1 - WIDTH) / 20)
FONTSIZEBIGWORD = 120 - int((WIDTH1 - WIDTH) / 10)

LINEWIDTHREGULAR = 1
LINEWIDTHBOLD = 4

NUMOFBOARD = 5

BOARD1 = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]]

BOARD2 = [[1, 2, 0, 6, 0, 0, 4, 0, 9],
        [0, 0, 0, 0, 0, 4, 1, 0, 2],
        [0, 0, 6, 0, 1, 0, 5, 0, 0],
        [6, 0, 8, 1, 0, 0, 0, 0, 0],
        [0, 5, 0, 3, 4, 2, 0, 0, 0],
        [4, 0, 2, 0, 0, 8, 0, 0, 0],
        [8, 0, 7, 0, 0, 0, 3, 0, 5],
        [3, 0, 4, 0, 0, 0, 0, 2, 6],
        [0, 0, 0, 4, 0, 0, 0, 0, 0]]

BOARD3 = [[1, 5, 8, 0, 6, 0, 0, 0, 0],
        [9, 0, 0, 0, 0, 4, 0, 7, 0],
        [3, 0, 0, 8, 0, 0, 0, 0, 1],
        [5, 1, 0, 2, 7, 0, 9, 0, 0],
        [0, 0, 4, 0, 3, 0, 0, 5, 7],
        [0, 7, 0, 0, 0, 0, 0, 1, 0],
        [4, 0, 0, 0, 0, 1, 8, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 1, 9, 0]]

BOARD4 = [[6, 8, 0, 0, 0, 0, 3, 4, 0],
        [0, 5, 0, 0, 0, 0, 0, 9, 0],
        [0, 0, 0, 4, 2, 0, 0, 0, 8],
        [0, 7, 9, 0, 0, 0, 0, 8, 0],
        [0, 3, 0, 0, 0, 0, 2, 0, 0],
        [0, 6, 2, 5, 9, 8, 0, 0, 0],
        [0, 9, 1, 2, 0, 6, 4, 0, 0],
        [0, 4, 5, 8, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 9, 0, 5, 0]]

BOARD5 = [[4, 0, 5, 0, 6, 2, 7, 3, 0],
        [7, 6, 3, 1, 0, 0, 0, 4, 0],
        [9, 0, 8, 0, 0, 0, 0, 5, 0],
        [0, 3, 0, 0, 4, 0, 0, 0, 0],
        [0, 7, 0, 5, 0, 1, 0, 0, 4],
        [0, 4, 0, 8, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 6, 3, 0, 2],
        [3, 9, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 5, 0, 0, 1, 0]]


# create Board class representing the board and manage cubes
class Board:
    _values = []

    def __init__(self, width, height, top_left):
        self._width = width
        self._height = height
        self._cubes = \
            [[Cube(i, j, self._values[j][i], top_left[0], top_left[1], self._values[j][i] in VALUES, int(width / 9), (-1, -1, -1))
             for j in range(9)] for i in range(9)]
        self._current_cube_position = (None, None)
        self._top_left = top_left
        self._indexes = []

    # determine and set current cube position when clicked
    def click(self, position):
        l, t = self._top_left
        w, h = position
        i, j = (w - l) // (self._width / 9), (h - t) // (self._height / 9)

        # deactivate previous selected cube
        if self._current_cube_position[0] is not None:
            self.get_cube(self._current_cube_position).set_selected(False)
            self.dye_cube(self._current_cube_position, (-1, -1, -1), (-1, -1, -1))

        # set current selected cube
        if i not in INDEXES or j not in INDEXES:
            self._current_cube_position = (None, None)
        else:
            self._current_cube_position = (int(i), int(j))
            self._cubes[int(i)][int(j)].set_selected(True)
            self.dye_cube(self._current_cube_position, LIGHTORANGE, LIGHTPURPLE)

        return self._current_cube_position

    # draw board
    def draw(self, win):

        l, t = self._top_left

        # draw cubes
        for i in range(9):
            for j in range(9):
                self._cubes[i][j].draw(win)

        # draw base lines
        for i in range(10):
            w = LINEWIDTHBOLD if i in [0, 3, 6, 9] else LINEWIDTHREGULAR
            pygame.draw.line(win, BLACK, (l, int(i * self._height / 9 + 1) + t),
                             (l + self._width, int(i * self._height / 9 + 1) + t), w)
            pygame.draw.line(win, BLACK, (int(i * self._width / 9) + l - 1, t),
                             (int(i * self._width / 9) + l - 1, t + self._height), w)

        # draw current selection rectangle
        pos = self._current_cube_position
        if pos[0] is not None:
            pygame.draw.rect(win, RED, (self.get_cube(pos).get_top_left()[0], self.get_cube(pos).get_top_left()[1],
                                        int(self._width / 9), int(self._width / 9)), 3)

    # dye the horizontal and vertical cubes of given position
    def dye_cube(self, position, color_horizontal, color_vertical):
        h, v = position
        for i in range(9):
            if i != h:
                self._cubes[i][v].set_color(color_horizontal)
            if i != v:
                self._cubes[h][i].set_color(color_vertical)

    # find the next empty spot in board
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self._values[i][j] not in VALUES:
                    return i, j
        return None, None

    # check if the given coordinate and value fit in the board
    def check_if_valid(self, tpl):

        i, j, value = tpl

        if value not in VALUES:
            return False

        # check for row and column
        for ind in range(9):
            if ind != j and self._values[i][ind] == value:
                return False
            if ind != i and self._values[ind][j] == value:
                return False

        # check for box
        for p in range(i // 3 * 3, i // 3 * 3 + 3):
            for q in range(j // 3 * 3, j // 3 * 3 + 3):
                if p != i and q != j and self._values[p][q] == value:
                    return False

        return True

    # clear the board and all the cube within
    def clear(self):
        for i in range(9):
            for j in range(9):
                self.get_cube((i, j)).clear()

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    # get cube using given position
    def get_cube(self, indexes):
        row, column = indexes
        if row is None or column is None:
            return None
        return self._cubes[row][column]

    def get_current_cube_position(self):
        return self._current_cube_position

    def get_top_left(self):
        return self._top_left

    def get_indexes(self):
        return self._indexes

    def set_current_cube_position(self, pos):
        self._current_cube_position = pos

    @classmethod
    def get_values(cls):
        return cls._values

    @classmethod
    def set_values(cls, val):
        cls._values = val


# create Cube class representing each square on board and manage the values within
class Cube:
    def __init__(self, row, column, value, left, top, permanent, side_length, color, selected=False):
        self._row = row
        self._column = column
        self._value = value
        self._permanent = permanent
        self._side_length = int(side_length)
        self._top_left = (int(self._row * side_length + left), int(self._column * side_length + top))
        self._color = color
        self._selected = selected
        self._temp = [False] * 9

    # draw cube
    def draw(self, win):

        w, h = self._top_left

        # draw cube color over the board
        if self._color[0] != -1:
            pygame.draw.rect(win, self._color, (w, h, self._side_length, self._side_length))

        # display current value
        if self._value != 0:
            font = pygame.font.SysFont(FONT, FONTSIZELARGE)
            text = font.render(str(self._value), 1, BLACK if self._permanent else BLUE)
            win.blit(text, (int(w + self._side_length / 2 - text.get_width() / 2),
                            int(h + self._side_length / 2 - text.get_height() / 2)))

        # display sketched value when current value is 0
        elif not self._permanent:
            for i in range(9):
                if self._temp[i]:
                    font = pygame.font.SysFont(FONT, FONTSIZESMALL)
                    text = font.render(str(i + 1), 1, GREY)
                    l, t = self._top_left
                    horizontal_gap = (self._side_length - text.get_width() * 3) / 4
                    vertical_gap = (self._side_length - text.get_height() * 3) / 4
                    win.blit(text, (int(l + ((i % 3) + 1) * horizontal_gap + (i % 3) * text.get_width()),
                                    int(t + ((i // 3) + 1) * vertical_gap + (
                                                i // 3) * text.get_height() + LINEWIDTHBOLD)))

    def clear(self):
        self.set_value(0)
        self.reset_temp()

    def get_row(self):
        return self._row

    def get_column(self):
        return self._column

    def get_value(self):
        return self._value

    def get_selected(self):
        return self._selected

    def get_temp(self):
        return self._temp

    def get_color(self):
        return self._color

    def get_top_left(self):
        return self._top_left

    def set_value(self, value):
        if not self._permanent:
            self._value = value

    def set_selected(self, selected):
        self._selected = selected

    def set_temp(self, index, bool_value):
        self._temp[index] = bool_value

    def set_color(self, color):
        self._color = color

    # reset list temp to initial value
    def reset_temp(self):
        self._temp = [False] * 9


def button(win, board, message, left, right, top, bottom, width,
           button_color, button_color_selected, font_color, font_size, action=None):
    # check if position is within the button
    if action is implement_back:
        pygame.event.wait()
    mouse = pygame.mouse.get_pos()
    valid = left <= mouse[0] <= right and top <= mouse[1] <= bottom

    # trigger effect when clicked
    click = pygame.mouse.get_pressed()
    if action:
        result = action(win, board, click[0] == 1, valid)
    else:
        result = False

    # draw button frame
    # pygame.draw.line(win, font_color, (left, top), (left, bottom), width * 2)
    # pygame.draw.line(win, font_color, (right, top), (right, bottom), width * 2)
    # pygame.draw.line(win, font_color, (left, top), (right + width, top), width * 2)
    # pygame.draw.line(win, font_color, (left, bottom), (right + width, bottom), width * 2)
    pygame.draw.rect(win, font_color, (left, top, right - left + width, bottom - top + width), width * 2)

    # draw button interior with hover effect
    if valid:
        pygame.draw.rect(win, button_color_selected, (left + width, top + width, right - left, bottom - top))
    else:
        pygame.draw.rect(win, button_color, (left + width, top + width, right - left, bottom - top))

    # draw button text
    font = pygame.font.SysFont(FONT, font_size)
    text = font.render(message, 1, font_color)
    text_rect = text.get_rect()
    text_rect.center = (int((left + right) / 2), int((top + bottom) / 2))
    win.blit(text, text_rect)

    return result


def implement_help(win, board, clicked, valid):
    if clicked and valid:
        return True
    else:
        return False


def implement_back(win, board, clicked, valid):
    win.fill(WHITE)
    for ind, msg in enumerate(['LEFT_MOUSE:', 'Select cell or button', '1 - 9:', 'Input value to cell',
                               'BACKSPACE:', 'Remove value or sketches from cell',
                               'SPACE:', 'Switch between input and sketch mode',
                               'ENTER:', 'Check if the board is correct', 'PAGE_UP:', 'Get a new puzzle',
                               'TAB:', 'Solve the board using back-tracking', '', 'algorithm with visualization',
                               '', '(definitely check it out!)']):
        font = pygame.font.SysFont(FONT, FONTSIZESMALL)
        text = font.render(msg, 1, BLACK)
        win.blit(text, (325 - int((WIDTH1 - WIDTH) / 7 * 2) if ind % 2 else 125 - int((WIDTH1 - WIDTH) / 7),
                        int(225 - int((WIDTH1 - WIDTH) / 15) + ind // 2 * (75 - int((WIDTH1 - WIDTH) / 10)))))

    if clicked and valid:
        return False
    else:
        return True


def update_window(win, board, time_passed):
    # draw or dye on display
    win.fill(WHITE)

    # draw time display
    font = pygame.font.SysFont(FONT, FONTSIZEWORD)
    text = font.render(f'Time Elapsed  {int(time_passed // 60):02} : {int(time_passed % 60):02}', 1, BLACK)
    win.blit(text, (int(WIDTH - text.get_width() - DIFF / 2 + (WIDTH1 - WIDTH) / 20),
                    int(HEIGHT - DIFF / 2 - text.get_height() / 2)))

    # draw board
    board.draw(win)


def main():
    # setup display
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    Board.set_values(copy.deepcopy(BOARD1))
    board = Board(WIDTH, WIDTH, (0, 0))

    # setup clock
    clock = pygame.time.Clock()

    # load sounds and music into pygame
    crash_sound = pygame.mixer.Sound("Sounds\\Crash.wav")
    cheer_sound = pygame.mixer.Sound("Sounds\\Cheer.wav")
    pygame.mixer.music.load("Sounds\\Between Worlds.wav")

    # setup icon
    icon = pygame.image.load('Images\\icon.jpg')
    pygame.display.set_icon(icon)

    # record game start time
    start_time = time.time()

    # setup game variables
    sketch = False
    run = True
    val = None
    solve_request = False
    clear_board = False
    back_track = False
    update_board = False
    ignore = False
    help_page = False
    current_board = 0
    count = 0

    # play music
    pygame.mixer.music.play(-1)

    # update display
    pygame.display.flip()

    # setup game loop
    while run:

        # record time elapsed
        time_passed = time.time() - start_time

        # check if during a solve or on help page
        if not (solve_request or help_page):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.KEYDOWN:

                    # record number key pressed and deal with them later
                    if event.key == pygame.K_1:
                        val = 1
                    elif event.key == pygame.K_2:
                        val = 2
                    elif event.key == pygame.K_3:
                        val = 3
                    elif event.key == pygame.K_4:
                        val = 4
                    elif event.key == pygame.K_5:
                        val = 5
                    elif event.key == pygame.K_6:
                        val = 6
                    elif event.key == pygame.K_7:
                        val = 7
                    elif event.key == pygame.K_8:
                        val = 8
                    elif event.key == pygame.K_9:
                        val = 9

                    # clear selected cube when delete or backspace is pressed
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        pos = board.get_current_cube_position()
                        if pos[0] is not None:
                            board.get_cube(pos).set_value(0)
                            board.get_cube(pos).reset_temp()
                        val = None

                    # switch between sketch and regular mode when space or shift is pressed
                    elif event.key == pygame.KMOD_SHIFT or event.key == pygame.K_SPACE:
                        sketch = not sketch
                        val = None

                    # check answer when return is pressed
                    elif event.key == pygame.K_RETURN:
                        correct = True

                        for i in range(9):
                            for j in range(9):
                                correct = board.check_if_valid((i, j, board.get_cube((j, i)).get_value()))
                                if not correct:
                                    break
                            if not correct:
                                break

                        if correct:
                            pygame.mixer.Sound.play(cheer_sound)
                            font = pygame.font.SysFont(FONT, FONTSIZEBIGWORD)
                            text = font.render('Congratulations!', 1, GREEN)
                            win.blit(text, (int(board.get_width() / 2 - text.get_width() / 2),
                                            int(board.get_height() / 2 - text.get_height() / 2)))

                            # hold display for two seconds and ignore window update
                            ignore = True
                            val = None

                        else:
                            pygame.mixer.Sound.play(crash_sound)
                            font = pygame.font.SysFont(FONT, FONTSIZEBIGWORD)
                            text = font.render('Try again!', 1, PINK)
                            win.blit(text, (int(board.get_width() / 2 - text.get_width() / 2),
                                            int(board.get_height() / 2 - text.get_height() / 2)))

                            ignore = True
                            val = None

                    # visually generate the answer using back-tracking algorithm
                    elif event.key == pygame.K_TAB:
                        solve_request = True
                        clear_board = True
                        val = None

                    # change to a new board
                    elif event.key == pygame.K_PAGEUP:
                        update_board = True
                        current_board = (current_board + 1) % NUMOFBOARD
                        val = None

                    elif event.key == pygame.K_PAGEDOWN:
                        update_board = True
                        current_board = (current_board + NUMOFBOARD - 1) % NUMOFBOARD
                        val = None

                    # change selected cube
                    elif event.key == pygame.K_UP:
                        pos = board.get_current_cube_position()
                        if pos[0] is not None and pos[1] is not None and pos[1] != 0:
                            board.get_cube(pos).set_selected(False)
                            board.set_current_cube_position((pos[0], pos[1] - 1))
                            board.get_cube((pos[0], pos[1] - 1)).set_selected(True)
                        val = None

                    elif event.key == pygame.K_DOWN:
                        pos = board.get_current_cube_position()
                        if pos[0] is not None and pos[1] is not None and pos[1] != 8:
                            board.get_cube(pos).set_selected(False)
                            board.set_current_cube_position((pos[0], pos[1] + 1))
                            board.get_cube((pos[0], pos[1] + 1)).set_selected(True)
                        val = None

                    elif event.key == pygame.K_LEFT:
                        pos = board.get_current_cube_position()
                        if pos[0] is not None and pos[1] is not None and pos[0] != 0:
                            board.get_cube(pos).set_selected(False)
                            board.set_current_cube_position((pos[0] - 1, pos[1]))
                            board.get_cube((pos[0] - 1, pos[1])).set_selected(True)
                        val = None

                    elif event.key == pygame.K_RIGHT:
                        pos = board.get_current_cube_position()
                        if pos[0] is not None and pos[1] is not None and pos[0] != 8:
                            board.get_cube(pos).set_selected(False)
                            board.set_current_cube_position((pos[0] + 1, pos[1]))
                            board.get_cube((pos[0] + 1, pos[1])).set_selected(True)
                        val = None

                # update board when mouse is clicked
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # the origin of pygame is at the top left corner, with x increases right and y increases down
                    position = pygame.mouse.get_pos()
                    board.click(position)
                    val = None

                # deal with instances where a number key is pressed
                current_position = board.get_current_cube_position()
                if val is not None and current_position[0] in INDEXES:

                    # draw sketch values
                    if sketch:
                        Board.get_values()[current_position[1]][current_position[0]] = 0
                        board.get_cube(current_position).set_value(0)
                        board.get_cube(current_position).set_temp(val - 1, True)

                    # draw regular values
                    else:
                        Board.get_values()[current_position[1]][current_position[0]] = val
                        board.get_cube(current_position).set_value(val)
                        board.get_cube(current_position).reset_temp()

                    val = None

        # a solve request has been made, should prioritize solve
        elif solve_request:

            # check if the first time in solve, if so clear board
            if clear_board:
                board.clear()
                if current_board == 0:
                    Board.set_values(copy.deepcopy(BOARD1))
                    board = Board(WIDTH, WIDTH, (0, 0))
                elif current_board == 1:
                    Board.set_values(copy.deepcopy(BOARD2))
                    board = Board(WIDTH, WIDTH, (0, 0))
                elif current_board == 2:
                    Board.set_values(copy.deepcopy(BOARD3))
                    board = Board(WIDTH, WIDTH, (0, 0))
                elif current_board == 3:
                    Board.set_values(copy.deepcopy(BOARD4))
                    board = Board(WIDTH, WIDTH, (0, 0))
                else:
                    Board.set_values(copy.deepcopy(BOARD5))
                    board = Board(WIDTH, WIDTH, (0, 0))
                clear_board = False

            else:

                # check if back tracking is needed
                if not back_track:
                    pos = board.find_empty()

                    # determine whether the board is solved and should exit the solve process
                    if pos[0] is None and pos[1] is None:
                        solve_request = False

                    else:

                        # check for valid values in the new position
                        inputted = False
                        for value in VALUES:
                            if board.check_if_valid((pos[0], pos[1], value)):
                                Board.get_values()[pos[0]][pos[1]] = value
                                board.get_cube((pos[1], pos[0])).set_value(value)
                                board.get_indexes().append((pos[0], pos[1], value))
                                inputted = True
                                break

                        # no valid value could fit, require back tracking
                        if not inputted:
                            back_track = True

                else:

                    # in case board could not be solved, quit solve process
                    if not board.get_indexes():
                        solve_request = False

                    else:
                        temp_index = board.get_indexes().pop(-1)

                        # check if further back tracking is needed
                        if temp_index[2] == 9:
                            Board.get_values()[temp_index[0]][temp_index[1]] = 0
                            board.get_cube((temp_index[1], temp_index[0])).set_value(0)
                            back_track = True

                        # find the next valid value for current position
                        else:
                            Board.get_values()[temp_index[0]][temp_index[1]] = 0
                            board.get_cube((temp_index[1], temp_index[0])).set_value(0)
                            inputted = False
                            for value in range(temp_index[2] + 1, 10):
                                if board.check_if_valid((temp_index[0], temp_index[1], value)):
                                    Board.get_values()[temp_index[0]][temp_index[1]] = value
                                    board.get_cube((temp_index[1], temp_index[0])).set_value(value)
                                    board.get_indexes().append((temp_index[0], temp_index[1], value))
                                    inputted = True
                                    break

                            back_track = not inputted

        # update board when requested
        if update_board:
            if current_board == 0:
                Board.set_values(copy.deepcopy(BOARD1))
                board = Board(WIDTH, WIDTH, (0, 0))
            elif current_board == 1:
                Board.set_values(copy.deepcopy(BOARD2))
                board = Board(WIDTH, WIDTH, (0, 0))
            elif current_board == 2:
                Board.set_values(copy.deepcopy(BOARD3))
                board = Board(WIDTH, WIDTH, (0, 0))
            elif current_board == 3:
                Board.set_values(copy.deepcopy(BOARD4))
                board = Board(WIDTH, WIDTH, (0, 0))
            else:
                Board.set_values(copy.deepcopy(BOARD5))
                board = Board(WIDTH, WIDTH, (0, 0))
            update_board = False

        # update surface if not ignored
        if not (help_page or ignore):
            update_window(win, board, time_passed)
        elif ignore:
            count += 1
            if count > HOLD * FPS:
                count = 0
                ignore = False

        # show sketch mode notification
        if sketch:
            font = pygame.font.SysFont(FONT, FONTSIZEWORD)
            text = font.render('Sketch Mode', 1, GREY)
            win.blit(text, (int(WIDTH / 2 - text.get_width() + 25), int(HEIGHT - DIFF / 2 - text.get_height() / 2)))

        # draw buttons with hover effect
        if help_page:
            help_page = button(win, board, 'back', 100, 200 - int((WIDTH1 - WIDTH) / 9),
                               100 + int((WIDTH1 - WIDTH) / 36), 150 - int((WIDTH1 - WIDTH) / 36), LINEWIDTHREGULAR,
                               WHITE, LIGHTGREY, DARKGREY, FONTSIZEWORD, implement_back)
        else:
            help_page = button(win, board, 'help', 100, 200 - int((WIDTH1 - WIDTH) / 9),
                               int(HEIGHT - DIFF / 2 - 25) + int((WIDTH1 - WIDTH) / 36),
                               int(HEIGHT - DIFF / 2 + 25) - int((WIDTH1 - WIDTH) / 36),
                               LINEWIDTHREGULAR, WHITE, LIGHTGREY, DARKGREY, FONTSIZEWORD, implement_help)

        # update display
        pygame.display.flip()

        # keep FPS
        clock.tick(FPS)


main()
pygame.quit()
