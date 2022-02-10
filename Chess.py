import tkinter
import os


master = tkinter.Tk()
master.title('Chess')
canvas = tkinter.Canvas(master, height=660, width=750)
master.resizable(width=False, height=False)
path = F"images\\"
field = tkinter.PhotoImage(file=path + 'Field.png')
field_numbers = tkinter.PhotoImage(file=path + 'Field_numbers.png')
outline_pic = tkinter.PhotoImage(file=path + 'Outline.png')
right_text = tkinter.PhotoImage(file=path + 'Right_text.png')
White_win = tkinter.PhotoImage(file=path + 'White_win.png')
Black_win = tkinter.PhotoImage(file=path + 'Black_win.png')
Black_Rook_pic = tkinter.PhotoImage(file=path + 'Black_Rook.png')
Black_Knight_pic = tkinter.PhotoImage(file=path + 'Black_Knight.png')
Black_Bishop_pic = tkinter.PhotoImage(file=path + 'Black_Bishop.png')
Black_Queen_pic = tkinter.PhotoImage(file=path + 'Black_Queen.png')
Black_King_pic = tkinter.PhotoImage(file=path + 'Black_King.png')
Black_Pawn_pic = tkinter.PhotoImage(file=path + 'Black_Pawn.png')
White_Rook_pic = tkinter.PhotoImage(file=path + 'White_Rook.png')
White_Knight_pic = tkinter.PhotoImage(file=path + 'White_Knight.png')
White_Bishop_pic = tkinter.PhotoImage(file=path + 'White_Bishop.png')
White_Queen_pic = tkinter.PhotoImage(file=path + 'White_Queen.png')
White_King_pic = tkinter.PhotoImage(file=path + 'White_King.png')
White_Pawn_pic = tkinter.PhotoImage(file=path + 'White_Pawn.png')

start_row, start_col = None, None
end_row, end_col = None, None
outline_placed = False
step_to_king = False
game_over = False
WHITE = 1
BLACK = 2


def change_pawn():
    global game_over, step_to_king
    if not game_over:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        chars = ['Q', 'N', 'R', 'B']
        row, col, row1, col1, char = row_text.get(), col_text.get(),\
                                     row1_text.get(), col1_text.get(), char_text.get()
        if all([col.upper() in letters, row.isdigit(),
                col1.upper() in letters, row1.isdigit(), char.upper() in chars]):
            if correct_coords(int(row) - 1, int(row1) - 1):
                col, col1, row, row1 = letters.index(col.upper()),\
                                       letters.index(col1.upper()), int(row) - 1, int(row1) - 1
                if board.field[row1][col1]:
                    if board.field[row1][col1].char() == 'K':
                        step_to_king = True
                if board.move_and_promote_pawn(abs(row - 7), col, abs(row1 - 7), col1, char):
                    row, row1 = abs(row - 7), abs(row1 - 7)
                    if board.field[row1][col1].get_color() == BLACK:
                        if char.upper() == 'Q':
                            new_figure = canvas.create_image((col1 * 80 + 40, abs(row1 - 7) * 80 + 40), image=Black_Queen_pic)
                        elif char.upper() == 'N':
                            new_figure = canvas.create_image((col1 * 80 + 40, abs(row1 - 7) * 80 + 40), image=Black_Knight_pic)
                        elif char.upper() == 'R':
                            new_figure = canvas.create_image((col1 * 80 + 40, abs(row1 - 7) * 80 + 40), image=Black_Rook_pic)
                        elif char.upper() == 'B':
                            new_figure = canvas.create_image((col1 * 80 + 40, abs(row1 - 7) * 80 + 40), image=Black_Bishop_pic)
                    else:
                        if char.upper() == 'Q':
                            new_figure = canvas.create_image((col1 * 80 + 40, abs(row1 - 7) * 80 + 40), image=White_Queen_pic)
                        elif char.upper() == 'N':
                            new_figure = canvas.create_image((col1 * 80 + 40, abs(row1 - 7) * 80 + 40), image=White_Knight_pic)
                        elif char.upper() == 'R':
                            new_figure = canvas.create_image((col1 * 80 + 40, abs(row1 - 7) * 80 + 40), image=White_Rook_pic)
                        elif char.upper() == 'B':
                            new_figure = canvas.create_image((col1 * 80 + 40, abs(row1 - 7) * 80 + 40), image=White_Bishop_pic)
                    if step_to_king:
                        game_over = True
                        if board.color == 1:
                            canvas.create_image((320, 320), image=Black_win)
                        else:
                            canvas.create_image((320, 320), image=White_win)
                    canvas.delete(field_pic[row][col], field_pic[row1][col1])
                    field_pic[row][col], field_pic[row1][col1] = None, new_figure
                    change_color()
                step_to_king = False



def change_color():
    if opponent(board.color) == WHITE:
        canvas.itemconfig(player_color, fill='black', outline='black')
    else:
        canvas.itemconfig(player_color, fill='white', outline='white')


def move_castling_pic(row, col, col1, king_col, rook_x, rook_y, king_x):
    field_pic[row][col], field_pic[row][col1] = None, field_pic[row][col]
    canvas.coords(field_pic[row][col1], rook_x, rook_y)
    field_pic[row][4], field_pic[row][king_col] = None, field_pic[row][4]
    canvas.coords(field_pic[row][king_col], king_x, rook_y)
    change_color()
    master.focus_set()


def apply_castling():
    if not game_over:
        if castling_text.get() == '1':
            if board.castling0():
                if board.color == WHITE:
                    move_castling_pic(7, 0, 3, 2, 280, 40, 200)
                else:
                    move_castling_pic(0, 0, 3, 2, 280, 600, 200)
        elif castling_text.get() == '8':
            if board.castling7():
                if board.color == WHITE:
                    move_castling_pic(7, 7, 5, 6, 440, 40, 520)
                else:
                    move_castling_pic(0, 7, 5, 6, 440, 600, 520)


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        self.castling_possible = {(WHITE, 0): True, (WHITE, 7): True,
                                  (BLACK, 0): True, (BLACK, 7): True,
                                  (WHITE, 'K'): True, (BLACK, 'K'): True}
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        if isinstance(self.field[row][col], Rook) and (col == 0 or col == 7):
            self.castling_possible[(self.color, col)] = False
        if isinstance(self.field[row][col], King) and col == 4:
            self.castling_possible[(self.color, 'K')] = False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)
        return True

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        if isinstance(self.field[row][col], Pawn):
            if self.move_piece(row, col, row1, col1):
                if self.field[row1][col1].get_color() == WHITE and row1 == 7 or \
                        self.field[row1][col1].get_color() == BLACK and row1 == 0:
                    clr = opponent(self.color)
                    if char.upper() == 'Q':
                        self.field[row1][col1] = Queen(clr)
                    if char.upper() == 'R':
                        self.field[row1][col1] = Rook(clr)
                    if char.upper() == 'B':
                        self.field[row1][col1] = Bishop(clr)
                    if char.upper() == 'N':
                        self.field[row1][col1] = Knight(clr)
                    return True
        return False

    def castling0(self):
        row = 0 if self.color == WHITE else 7
        if self.castling_possible[(self.color, 'K')] and isinstance(self.field[row][4], King) and\
                self.field[row][4].get_color() != opponent(self.color):
            if self.castling_possible[(self.color, 0)] and isinstance(self.field[row][0], Rook) and\
                    self.field[row][0].get_color() != opponent(self.color):
                if self.move_piece(row, 0, row, 3):
                    self.field[row][2], self.field[row][4] = King(opponent(self.color)), None
                    return True
        return False

    def castling7(self):
        row = 0 if self.color == WHITE else 7
        if self.castling_possible[(self.color, 'K')] and isinstance(self.field[row][4], King) and\
                self.field[row][4].get_color() != opponent(self.color):
            if self.castling_possible[(self.color, 7)] and isinstance(self.field[row][7], Rook) and\
                    self.field[row][7].get_color() != opponent(self.color):
                if self.move_piece(row, 7, row, 5):
                    self.field[row][6], self.field[row][4] = King(opponent(self.color)), None
                    return True
        return False


class Rook:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Knight:
    '''Класс коня. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        if (abs(row - row1) == 2 and abs(col - col1) == 1) or\
                (abs(row - row1) == 1 and abs(col - col1) == 2):
            if board.field[row1][col1]:
                if board.field[row1][col1].get_color() == self.color:
                    return False
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        if 0 <= row1 < 8 and 0 <= col < 8:
            if abs(row - row1) <= 1 and abs(col - col1) <= 1:
                if board.field[row1][col1]:
                    if board.field[row1][col1].get_color() == self.color:
                        return False
                return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        row_step, col_step, temp_row, temp_col = 1, 1, row, col
        if row == row1 and col == col1:
            return False
        if row1 in range(8) and col1 in range(8):
            if abs(row - row1) == abs(col - col1) or \
                    (row != row1 and col == col1) or \
                    (row == row1 and col != col1):
                if row > row1:
                    row_step = -1
                elif row == row1:
                    row_step = 0
                if col > col1:
                    col_step = -1
                elif col == col1:
                    col_step = 0
                for i in range(max(abs(row - row1), abs(col - col1))):
                    temp_row += row_step
                    temp_col += col_step
                    if board.field[temp_row][temp_col]:
                        if board.field[temp_row][temp_col].get_color() == self.color:
                            return False
                        if temp_row != row1 or temp_col != col1:
                            return False
                return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        row_step, col_step, temp_row, temp_col = 1, 1, row, col
        if row == row1 and col == col1:
            return False
        if row1 in range(8) and col1 in range(8):
            if abs(row - row1) == abs(col - col1):
                if row > row1:
                    row_step = -1
                elif row == row1:
                    row_step = 0
                if col > col1:
                    col_step = -1
                elif col == col1:
                    col_step = 0
                for i in range(max(abs(row - row1), abs(col - col1))):
                    temp_row += row_step
                    temp_col += col_step
                    if board.field[temp_row][temp_col]:
                        if board.field[temp_row][temp_col].get_color() == self.color:
                            return False
                        if temp_row != row1 or temp_col != col1:
                            return False
                return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


canvas.create_image((0, 0), image=field, anchor='nw')
canvas.create_image((0, 0), image=field_numbers, anchor='nw')
canvas.create_image((663, 10), image=right_text, anchor='nw')
player_color = canvas.create_rectangle(((682, 47), (731, 96)), fill='white', outline='white')
Black_Rook0 = canvas.create_image((40, 40), image=Black_Rook_pic)
Black_Rook7 = canvas.create_image((600, 40), image=Black_Rook_pic)
Black_Knight0 = canvas.create_image((120, 40), image=Black_Knight_pic)
Black_Knight7 = canvas.create_image((520, 40), image=Black_Knight_pic)
Black_Bishop0 = canvas.create_image((200, 40), image=Black_Bishop_pic)
Black_Bishop7 = canvas.create_image((440, 40), image=Black_Bishop_pic)
Black_Queen = canvas.create_image((280, 40), image=Black_Queen_pic)
Black_King = canvas.create_image((360, 40), image=Black_King_pic)
White_Rook0 = canvas.create_image((40, 600), image=White_Rook_pic)
White_Rook7 = canvas.create_image((600, 600), image=White_Rook_pic)
White_Knight0 = canvas.create_image((120, 600), image=White_Knight_pic)
White_Knight7 = canvas.create_image((520, 600), image=White_Knight_pic)
White_Bishop0 = canvas.create_image((200, 600), image=White_Bishop_pic)
White_Bishop7 = canvas.create_image((440, 600), image=White_Bishop_pic)
White_Queen = canvas.create_image((280, 600), image=White_Queen_pic)
White_King = canvas.create_image((360, 600), image=White_King_pic)
Black_Pawn0 = canvas.create_image((40, 120), image=Black_Pawn_pic)
Black_Pawn1 = canvas.create_image((120, 120), image=Black_Pawn_pic)
Black_Pawn2 = canvas.create_image((200, 120), image=Black_Pawn_pic)
Black_Pawn3 = canvas.create_image((280, 120), image=Black_Pawn_pic)
Black_Pawn4 = canvas.create_image((360, 120), image=Black_Pawn_pic)
Black_Pawn5 = canvas.create_image((440, 120), image=Black_Pawn_pic)
Black_Pawn6 = canvas.create_image((520, 120), image=Black_Pawn_pic)
Black_Pawn7 = canvas.create_image((600, 120), image=Black_Pawn_pic)
White_Pawn0 = canvas.create_image((40, 520), image=White_Pawn_pic)
White_Pawn1 = canvas.create_image((120, 520), image=White_Pawn_pic)
White_Pawn2 = canvas.create_image((200, 520), image=White_Pawn_pic)
White_Pawn3 = canvas.create_image((280, 520), image=White_Pawn_pic)
White_Pawn4 = canvas.create_image((360, 520), image=White_Pawn_pic)
White_Pawn5 = canvas.create_image((440, 520), image=White_Pawn_pic)
White_Pawn6 = canvas.create_image((520, 520), image=White_Pawn_pic)
White_Pawn7 = canvas.create_image((600, 520), image=White_Pawn_pic)
castling_text, row_text, col_text = tkinter.StringVar(), tkinter.StringVar(), tkinter.StringVar()
row1_text, col1_text, char_text = tkinter.StringVar(), tkinter.StringVar(), tkinter.StringVar()
col_entry = tkinter.Entry(width=5, borderwidth=5, textvariable=col_text)
col_entry.place(x=668, y=348, anchor='nw')
row_entry = tkinter.Entry(width=5, borderwidth=5, textvariable=row_text)
row_entry.place(x=709, y=348, anchor='nw')
col1_entry = tkinter.Entry(width=5, borderwidth=5, textvariable=col1_text)
col1_entry.place(x=668, y=390, anchor='nw')
row1_entry = tkinter.Entry(width=5, borderwidth=5, textvariable=row1_text)
row1_entry.place(x=709, y=390, anchor='nw')
char_entry = tkinter.Entry(width=5, borderwidth=5, textvariable=char_text)
char_entry.place(x=689, y=431, anchor='nw')
move_pawn = tkinter.Button(text="Применить", width=9, background="#D2D2D2", command=change_pawn)
move_pawn.place(x=674, y=472, anchor='nw')
castling_entry = tkinter.Entry(width=6, borderwidth=5, textvariable=castling_text)
castling_entry.place(x=668, y=542, anchor='nw')
castling_button = tkinter.Button(text="Apply", width=4, background="#D2D2D2", command=apply_castling)
castling_button.place(x=710, y=542, anchor='nw')
field_pic = [[None] * 8 for i in range(8)]
field_pic[0] = [White_Rook0, White_Knight0, White_Bishop0, White_Queen,
                White_King, White_Bishop7, White_Knight7, White_Rook7]
field_pic[1] = [White_Pawn0, White_Pawn1, White_Pawn2, White_Pawn3,
                White_Pawn4, White_Pawn5, White_Pawn6, White_Pawn7]
field_pic[6] = [Black_Pawn0, Black_Pawn1, Black_Pawn2, Black_Pawn3,
                Black_Pawn4, Black_Pawn5, Black_Pawn6, Black_Pawn7]
field_pic[7] = [Black_Rook0, Black_Knight0, Black_Bishop0, Black_Queen,
                Black_King, Black_Bishop7, Black_Knight7, Black_Rook7]
board = Board()


def press_lm(event):
    global end_row, end_col, outline_placed, outline, start_row,\
        start_col, player_color, game_over, step_to_king
    end_row, end_col = abs(event.y // 80 - 7), abs(event.x // 80)
    master.focus_set()
    if not game_over and not start_row is None:
        if correct_coords(end_row, end_col):
            if outline_placed:
                canvas.delete(outline)
                outline_placed = False
                if board.field[end_row][end_col]:
                    if board.field[end_row][end_col].char() == 'K':
                        step_to_king = True
                if board.move_piece(start_row, start_col, end_row, end_col):
                    canvas.delete(field_pic[end_row][end_col])
                    field_pic[start_row][start_col],\
                    field_pic[end_row][end_col] = None, field_pic[start_row][start_col]
                    canvas.coords(field_pic[end_row][end_col],
                                  abs(end_col) * 80 + 40, abs(end_row - 7) * 80 + 40)
                    if step_to_king:
                        game_over = True
                        if board.color == 1:
                            canvas.create_image((320, 320), image=Black_win)
                        else:
                            canvas.create_image((320, 320), image=White_win)
                step_to_king = False
                change_color()


def press_rm(event):
    global start_row, start_col, outline_placed, outline
    x, y = event.x // 80, event.y // 80
    master.focus_set()
    if not game_over:
        if correct_coords(y, x):
            if outline_placed:
                canvas.delete(outline)
            outline_placed = True
            outline = canvas.create_image(((x) * 80 - 2, (y) * 80 - 2),
                                          image=outline_pic, anchor='nw')
            start_row, start_col = abs(y - 7), abs(x)


def close_mainloop(event):
    master.destroy()


canvas.pack()
canvas.bind("<Button-1>", press_lm)
canvas.bind("<Button-3>", press_rm)
master.bind("<Escape>", close_mainloop)
master.mainloop()