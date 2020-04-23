import pygame
import random
import os

pygame.init()
size = width, height = 910, 1010
screen = pygame.display.set_mode(size)
LEVEL = 3
COLOR_GRID = (145, 145, 145)
COLOR_BACKGROUND = (111, 111, 111)


class Board:
    def __init__(self, width, height, mine):
        self.width = width
        self.height = height
        self.mine = mine
        self.board = [[-1] * height for _ in range(height)]
        self.n_mine = self.coord_mine48()
        self.left = 5
        self.top = 105
        self.cell_size = 30
        self.first_step = True
        self.cell_list = []
        self.flag = True

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

# процедура, усложняющая расстановку мин(ввиде прямоугольника)
    def coord_mine12(self):
        k = 0
        x = random.randint(8, 23)
        y = random.randint(8, 23)
        for i in range(5):
            if self.board[x][y + i] != 10:
                self.board[x][y + i] = 10
                k += 1
        for i in range(1, 3):
            if self.board[x + i][y + 4] != 10:
                self.board[x + i][y + 4] = 10
                k += 1
        for i in range(1, 3):
            if self.board[x + i][y] != 10:
                self.board[x + i][y] = 10
                k += 1
        for i in range(1, 4):
            if self.board[x + 2][y + i] != 10:
                self.board[x + 2][y + i] = 10
                k += 1
        if k < 12:
            for i in range(12 - k):
                    x = random.randint(0, self.height - 1)
                    y = random.randint(0, self.height - 1)
                    if self.board[x][y] == -1:
                        self.board[x][y] = 10
                    else:
                        while self.board[x][y] != -1:
                            x = random.randint(0, self.height - 1)
                            y = random.randint(0, self.height - 1)
                        self.board[x][y] = 10

# цикл, создающий мины
    def coord_mine48(self):
        for i in range(self.mine - 12):
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.height - 1)
            if self.board[x][y] == -1:
                self.board[x][y] = 10
            else:
                while self.board[x][y] != -1:
                    x = random.randint(0, self.height - 1)
                    y = random.randint(0, self.height - 1)
                self.board[x][y] = 10
# уровень сложности
        for i in range(LEVEL):
            self.coord_mine12()
# цикл проверки кол-ва мин
        n = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 10:
                    n += 1
        return n

# функция, которая открывает все мины, если вы проиграли
# также если флажок стоит не на мине, то функция подставит вместо флажка картинку
    def all_mine(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 10:
                    self.board[i][j] = 11
                elif self.board[i][j] == 12:
                    self.board[i][j] = 14
        self.flag = False

# подгружает картинки из папки и задает им нужные размеры
    def load_image(self, name, x=28, y=28):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname).convert()
        image1 = pygame.transform.scale(image, (x, y))
        return image1

    def render(self):
        white = pygame.Color('white')
        red = pygame.Color('red')
        blue = pygame.Color('blue')
        orange = pygame.Color('orange')
        purple = pygame.Color('purple')
        bomb = self.load_image('mine2.png')
        flag = self.load_image('flag2.png')
        brake_bomb = self.load_image('wrong_flag.png')
        title_flag = self.load_image('flag.png', 46, 63)
        screen.blit(title_flag, (20, 20))
        font = pygame.font.Font(None, 32)
        text = font.render(str(self.n_mine), 1, white)
        screen.blit(text, (90, 38))
        if self.flag is False and self.n_mine > 0:
            text = font.render('Вы проиграли!', 1, white)
            screen.blit(text, (150, 38))
        elif self.flag is False and self.n_mine == 0:
            text = font.render('Вы победили!', 1, white)
            screen.blit(text, (150, 38))
        font = pygame.font.Font(None, 18)
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                w = self.cell_size
# -1 означает неоткрытую клетку, 10 - закрытая бомба(данные значения не прорисовываются)
                if self.board[i][j] == -1 or self.board[i][j] == 10:
                    pygame.draw.rect(screen, COLOR_GRID, (x, y, w, w), 1)
# 11 - открытая бомба(открывается при попадании), подгружается картинка мины
                elif self.board[i][j] == 11:
                    pygame.draw.rect(screen, COLOR_GRID, (x, y, w, w), 1)
                    screen.blit(bomb, (x + 1, y + 1))
# 12 или 13 - ставится флаг при нажатии на правую клавишу
                elif self.board[i][j] == 12 or self.board[i][j] == 13:
                    pygame.draw.rect(screen, COLOR_GRID, (x, y, w, w), 1)
                    screen.blit(flag, (x + 1, y + 1))
# 14 - открытая неправильная позиция флажка
                elif self.board[i][j] == 14:
                    pygame.draw.rect(screen, COLOR_GRID, (x, y, w, w), 1)
                    screen.blit(brake_bomb, (x + 1, y + 1))
# при открывании клетки, выводится значение(каждая цифра имеет свой цвет)
                else:
                    if self.board[i][j] == 0:
                        text = font.render(str(self.board[i][j]), 1, white)
                        screen.blit(text, (x + 10, y + 10))
                        pygame.draw.rect(screen, COLOR_GRID, (x, y, w, w), 1)
                    if self.board[i][j] == 1:
                        text = font.render(str(self.board[i][j]), 1, blue)
                        screen.blit(text, (x + 10, y + 10))
                        pygame.draw.rect(screen, COLOR_GRID, (x, y, w, w), 1)
                    if self.board[i][j] == 2:
                        text = font.render(str(self.board[i][j]), 1, orange)
                        screen.blit(text, (x + 10, y + 10))
                        pygame.draw.rect(screen, COLOR_GRID, (x, y, w, w), 1)
                    if self.board[i][j] == 3:
                        text = font.render(str(self.board[i][j]), 1, red)
                        screen.blit(text, (x + 10, y + 10))
                        pygame.draw.rect(screen, COLOR_GRID, (x, y, w, w), 1)
                    if self.board[i][j] > 3:
                        text = font.render(str(self.board[i][j]), 1, purple)
                        screen.blit(text, (x + 10, y + 10))
                        pygame.draw.rect(screen, COLOR_GRID, (x, y, w, w), 1)

    def get_click(self, mouse_pos, mouse_buttom):
        cell = self.get_cell(mouse_pos)
# отработка действий левой клавиши
        if mouse_buttom == 1:
            i, j = cell
# если при первом нажатии вы попадаете на мину, то она переносится в другое место
            if self.first_step and self.board[j][i] == 10:
                x = random.randint(0, self.height - 1)
                y = random.randint(0, self.height - 1)
                if self.board[x][y] == -1:
                    self.board[x][y] = 10
                else:
                    while self.board[x][y] != -1:
                        x = random.randint(0, self.height - 1)
                        y = random.randint(0, self.height - 1)
                    self.board[x][y] = 10
                self.board[j][i] = -1

            if self.board[j][i] == -1 or self.board[j][i] == 10:
                self.on_click(cell)
# отработка действий правой клавиши(установка флага)
        else:
            i, j = cell
# флаг стоит неправильно
            if self.board[j][i] == -1:
                self.board[j][i] = 12
                self.n_mine -= 1
# флаг стоит на мине
            elif self.board[j][i] == 10:
                self.board[j][i] = 13
                self.n_mine -= 1
# отмена флага и возврат первоначального положения(клетка становится закрытой)
            elif self.board[j][i] == 12:
                self.board[j][i] = -1
                self.n_mine += 1
            elif self.board[j][i] == 13:
                self.board[j][i] = 10
                self.n_mine += 1
            if self.n_mine == 0:
                self.flag = False

# преобразует координаты из пикселей в координаты списка board
    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x1 = (x - self.left) // self.cell_size
        y1 = (y - self.top) // self.cell_size
        if x1 > len(self.board[0]) - 1 or y1 > len(self.board) - 1:
            return None
        else:
            return x1, y1

    def on_click(self, cell):
        x, y = cell
# открытие мины
        if self.board[y][x] == 10:
            self.board[y][x] = 11
            self.all_mine()

        else:
            n = self.open_cell(y, x)
            if n == 0:
                cell = y, x
                self.cell_list.append(cell)
                self.board[y][x] = n
                self.open_null_cell()
            else:
                self.board[y][x] = n

# функция, считающая мины у клетки
    def open_cell(self, i, j):
        true_list = [10, 13]
        n = 0
        if j > 0 and self.board[i][j - 1] in true_list:
            n += 1
        if j < self.height - 1 and self.board[i][j + 1] in true_list:
            n += 1

        if i > 0 and self.board[i - 1][j] in true_list:
            n += 1
        if i > 0 and j > 0 and self.board[i - 1][j - 1] in true_list:
            n += 1
        if i > 0 and j < self.height - 1 and self.board[i - 1][j + 1] in true_list:
            n += 1

        if i < self.height - 1 and self.board[i + 1][j] in true_list:
            n += 1
        if i < self.height - 1 and j > 0 and self.board[i + 1][j - 1] in true_list:
            n += 1
        if i < self.height - 1 and j < self.height - 1 and self.board[i + 1][j + 1] in true_list:
            n += 1
        return n

# функция, проверяющая является ли клетка пустой(значение клетки равно 0)
    def open_null_cell(self):
        while len(self.cell_list) > 0:
            i, j = self.cell_list[0]

            if j > 0:
                if self.board[i][j - 1] == -1:
                    n = self.open_cell(i, j - 1)
                    self.board[i][j - 1] = n
                    if n == 0:
                        cell = i, j - 1
                        self.cell_list.append(cell)

            if j < self.height - 1:
                if self.board[i][j + 1] == -1:
                    n = self.open_cell(i, j + 1)
                    self.board[i][j + 1] = n
                    if n == 0:
                        cell = i, j + 1
                        self.cell_list.append(cell)

            if i > 0:
                if self.board[i - 1][j] == -1:
                    n = self.open_cell(i - 1, j)
                    self.board[i - 1][j] = n
                    if n == 0:
                        cell = i - 1, j
                        self.cell_list.append(cell)

            if i > 0 and j > 0:
                if self.board[i - 1][j - 1] == -1:
                    n = self.open_cell(i - 1, j - 1)
                    self.board[i - 1][j - 1] = n
                    if n == 0:
                        cell = i - 1, j - 1
                        self.cell_list.append(cell)

            if i > 0 and j < self.height - 1:
                if self.board[i - 1][j + 1] == -1:
                    n = self.open_cell(i - 1, j + 1)
                    self.board[i - 1][j + 1] = n
                    if n == 0:
                        cell = i - 1, j + 1
                        self.cell_list.append(cell)

            if i < self.height - 1:
                if self.board[i + 1][j] == -1:
                    n = self.open_cell(i + 1, j)
                    self.board[i + 1][j] = n
                    if n == 0:
                        cell = i + 1, j
                        self.cell_list.append(cell)

            if i < self.height - 1 and j > 0:
                if self.board[i + 1][j - 1] == -1:
                    n = self.open_cell(i + 1, j - 1)
                    self.board[i + 1][j - 1] = n
                    if n == 0:
                        cell = i + 1, j - 1
                        self.cell_list.append(cell)

            if i < self.height - 1 and j < self.height - 1:
                if self.board[i + 1][j + 1] == -1:
                    n = self.open_cell(i + 1, j + 1)
                    self.board[i + 1][j + 1] = n
                    if n == 0:
                        cell = i + 1, j + 1
                        self.cell_list.append(cell)

            del self.cell_list[0]


board = Board(30, 30, 60)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if board.flag:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos, 1)
                    if board.first_step:
                        board.first_step = False
                if event.button == 3:
                    board.get_click(event.pos, 3)
    screen.fill(COLOR_BACKGROUND)
    board.render()
    pygame.display.flip()


pygame.quit()
