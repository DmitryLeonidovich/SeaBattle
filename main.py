import winsound
from itertools import chain
from random import randint
from typing import List


# Exceptions block


class SBException(Exception):
    def __init__(self):
        pass


class ShipNotFitted(SBException):
    def __init__(self, errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg
        
        
class BoardOutException(SBException):
    def __init__(self, errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg


class DotIsBusy(SBException):
    def __init__(self, errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg


class DotAllReadyPoked(SBException):
    def __init__(self, errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg


class DotTooClose(SBException):
    def __init__(self, errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_dot_xy(self):
        return [self.x, self.y]
    
    def get_dot_x(self):
        return self.x
    
    def get_dot_y(self):
        return self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def dot_read(self, bat):
        return bat[self.x][self.y]
    
    def dot_wright(self, bat, val=0):
        bat[self.x][self.y] = val
        return


class Ship:
    def __init__(self, shp_x, shp_y, size, dir_vec, rest_of_cells):
        self.shp_x = shp_x  # координата носа корабля X
        self.shp_y = shp_y  # координата носа корабля Y
        self.size = size  # размер корабля
        self.dir_vec = dir_vec  # ориентация корабля 0- горизонтально слева на право 1- вертикально сверху вниз
        self.rest_of_cells = rest_of_cells  # остаток жизни корабля
    
    # @staticmethod
    
        
    def dots(self):
        sdl = direction(self.dir_vec)
        dx = sdl[0]
        dy = sdl[1]
        sdl.clear()
        for i in range(self.size):
            sdl.append(Dot(self.shp_x + i * dx, self.shp_y + i * dy))
        return sdl


class Board:
    def __init__(self, dot_battle_field, battle_field, ships, visible, w_ship_rest, battle_field_size=6 ):
        self.dot_battle_field = dot_battle_field
        self.battle_field = battle_field  # двумерный массив состояния игрового поля
        self.ships = ships  # список кораблей на доске
        self.visible = visible  # признак видимости кораблей при выводе содержимого поля
        self.w_ship_rest = w_ship_rest  # число оставшихся клеток живых кораблей
        self.battle_field_size = battle_field_size  # размерность игрового поля
        
       
    def board_reset(self):  # сброс игрового поля
        self.dot_battle_field: List[Dot] = []
        for x in range(self.battle_field_size):
            for y in range(self.battle_field_size):
                self.dot_battle_field.append(Dot(x, y))
        
        print('Список Dot на поле:', self.dot_battle_field)
        
        self.battle_field = [[0] * self.battle_field_size for _ in range(self.battle_field_size)]
        self.ships = 0
        self.visible = True
        self.w_ship_rest = 0
        return
        
    def add_ship(self, sp_x, sp_y, s_dir, s_size):
        sdl = direction(s_dir)
        dx = sdl[0]
        dy = sdl[1]
        sdl.clear()
        for i in range(s_size):
            if self.battle_field[sp_y + i * dy][sp_x + i * dx] == 0:  # точка на поле свободна
                sdl.append(Dot(sp_x + i * dx, sp_y + i * dy))  # в список точек корабля ее
                self.battle_field[sp_y + i * dy][sp_x + i * dx] = 1  # метим точку кораблем
            else:
                break
        if len(sdl) == s_size:  # если корабль встал на поле, создадим контур корабля
            sdc = Board.contour(self, sdl)
            print('Контур корабля = ', end='')
            for f in sdc:
                print(Dot.get_dot_xy(f), end=' ')
            print()
            if len(sdc) > 0:
                return sdl
        if len(sdl) > 0:  # стираем корабль, не встает в выбранное место
            for i in range(len(sdl)):
                self.battle_field[sdl[i].y][sdl[i].x] = 0
        raise ShipNotFitted(f'В точку [{sp_x + 1},{sp_y + 1}] установить корабль не удалось!')
    
    # @staticmethod
    
        
    def contour(self, ship_cells):
        def dot_in_board(xc, yc):
            nonlocal d_c_l
            dt = Dot(xc, yc)
            if dt in self.dot_battle_field:
                d_c_l.append(dt)
            return
        
        print("Координаты точек корабля = ", end='')
        for sc in ship_cells:
            print(Dot.get_dot_xy(sc), sc in self.dot_battle_field, end=' ')
        size = len(ship_cells)
        print('Size = ', size, end='\n')
        
        cl_good = []
        cl_dbl_good = []
        
        shp_dir = 0
        if size > 1:
            sc = iter(ship_cells)  # установление по факту ориентации корабля для 2-х и более клеточных моделей
            shp_dir = get_dir(next(sc), next(sc))  # False - горизонтально True - вертикально
        d_c_l: Dot = []
        for sc in ship_cells:  # формирование списка точек контура вокруг корабля в рамках игрового поля
            x = Dot.get_dot_x(sc)
            y = Dot.get_dot_y(sc)
            if shp_dir == 0:  # для горизонтали
                dot_in_board(x - 1, y)
                dot_in_board(x + size, y)
                for dx in range(-1, size + 1):
                    dot_in_board(x + dx, y + 1)
                    dot_in_board(x + dx, y - 1)
            else:
                dot_in_board(y, x - 1)
                dot_in_board(y, x + size)
                for dx in range(-1, size + 1):
                    dot_in_board(y + 1, x + dx)
                    dot_in_board(y - 1, x + dx)
            """
            print('         d_c_l = ', end='')
            for f in d_c_l:
                print(Dot.get_dot_xy(f), end=', ')
            print()
            """
            
            cont_dump = []
            for i in range(len(cl_good)):  # сохраняем контур на случай отката
                cont_dump.append(self.battle_field[cl_good[i][1]][cl_good[i][0]])
                # print(cont_dump, cl_good[i][1], cl_good[i][0])
            for i in range(len(cl_good)):  # метим контур
                ship_too_close = self.battle_field[cl_good[i][1]][cl_good[i][0]] == 1
                if ship_too_close:  # признак нахождения рядом с соседним кораблем
                    for j in range(len(cl_good)):  # восстанавливаем контур на поле боя
                        self.battle_field[cl_good[j][1]][cl_good[i][0]] = cont_dump[j]
                    cl_good.clear()  # стираем список точек контура
                    break
                else:
                    self.battle_field[cl_good[i][1]][cl_good[i][0]] = 2
            break
        return d_c_l
    
    def out_bf_raw(self):
        print('\u00A6' + '=' * self.battle_field_size * 3 + '\u21d2 X')
        for b in range(self.battle_field_size):
            print('\u00A6' + str(self.battle_field[b]))
        print('\u21d3' + '-' * (self.battle_field_size * 3 -1))
        print('Y')
        return
    
    def screen_update(self, position='L'):
        s = ' ' + ' 0 1 2'
        print(s)
        s = ' ' + chr(0x22f1) + '0 1 2 \u25a0'
        print(s)
        # for x in range(self.battle_field_size):
        #     for y in range(self.battle_field_size):
        #         pass
        i = 0
        # print("Character set")
        # start = 8500
        # for x in range(0xFF):
        #     for y in range(25):
        #         #s = '\' + 'u' + f'{i+9632:04X}'
        #         s = hex(i+start)
        #         s = s[2:]
        #         s = chr(92) + 'u' + s
        #         print(f'{i+start:04X}=' + chr(i + start), end=' ')
        #         i += 1
        #     print()
        # print('\u274c')
        # print('\u274e')
        # print('\u2b1b')
        # print('\u2b1c')
        # print('\u26d5')
        # print('\u2591')
        # print('\u2588')
        # print('\u229a')
        
        return
  
    def dot_is_free(self, xf, yf):
        return self.battle_field[xf][yf] == 0


# unclassified functions
def direction(s_dir=0):
    if s_dir == 0:
        dx = 1
        dy = 0
    else:
        dx = 0
        dy = 1
    return [dx, dy]
    
    
def get_dir(d1, d2):
    return Dot.get_dot_x(d1) == Dot.get_dot_x(d2)


# Internal logic

 
# Frontend logics

def pew(snd='pew.wav'):
    winsound.PlaySound(snd, winsound.SND_FILENAME)
    return

bf = Board(dot_battle_field=None, battle_field=None, ships=None, visible=None, w_ship_rest=None, battle_field_size=10)
bf.board_reset()

bf. out_bf_raw()

try:
    sh = bf.add_ship(1, 1, 1, 2)
except ShipNotFitted as er:
    print(er)
else:
    pass
bf. out_bf_raw()

try:
    sh = bf.add_ship(3, 0, 0, 2)
except ShipNotFitted as er:
    print(er)
else:
    pass
bf. out_bf_raw()

try:
    sh = bf.add_ship(2, 3, 0, 3)
except ShipNotFitted as er:
    print(er)
else:
    pass
bf. out_bf_raw()

bf.screen_update()

"""
    for x in range(6):
        for y in range(6):
            sdl.append(Dot(x, y))  # в список точек
    
    for sc in sdl:
        print(Dot.dot_read(sc, bf.battle_field), ' = ', end='')
        print(Dot.get_dot_xy(sc), Dot.get_dot_x(sc), Dot.get_dot_y(sc))
"""
