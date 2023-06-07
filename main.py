import winsound
from itertools import chain
from random import randint
import time
from typing import List


# Exceptions block


class SBException(Exception):
    def __init__(self):
        pass


class ShipNotFitted(SBException):
    def __init__(self, errmsg=''):
        pew()
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

class Dot_n:
    def __init__(self, x, y, xy_data=None):
        self.x = x
        self.y = y
        if xy_data != None:
            self.xy_data = xy_data

    def set_xy_data(self, value):
        if isinstance(value, int):
            self.xy_data = value
        else:
            raise ValueError("Должно быть целое число!")

    def get_xy_data(self):
            return self.xy_data

arr_dot_n =[
    [Dot_n(0, 0, 1), Dot_n(1, 0, 2),Dot_n(2, 0, 3)],
    [Dot_n(0, 1, 4), Dot_n(1, 1, 5),Dot_n(2, 1, 6)],
    [Dot_n(0, 2, 7), Dot_n(1, 2, 8),Dot_n(2, 2, 9)]
           ]
def show_me():
    for y in range(3):
        for x in range(3):
            xyd = Dot_n.get_xy_data(arr_dot_n[y][x])
            print(xyd, end=' ')
        print()

show_me()
x=2
y=1
Dot_n.set_xy_data(arr_dot_n[y][x], 555)
print(Dot_n.get_xy_data(arr_dot_n[y][x]))

show_me()

quit(0)

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_xy(self):
        return [self.x, self.y]
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def read(self, bat):
        return bat[self.y][self.x]
    
    def wright(self, bat, val=0):
        bat[self.y][self.x] = val
        return


class Ship:
    def __init__(self, shp_x, shp_y, size, dir_vec, rest_of_cells):
        self.shp_x = shp_x  # координата носа корабля X
        self.shp_y = shp_y  # координата носа корабля Y
        self.size = size  # размер корабля
        self.dir_vec = dir_vec  # ориентация корабля 0- горизонтально слева на право 1- вертикально сверху вниз
        self.rest_of_cells = rest_of_cells  # остаток жизни корабля
         
    def dots(self):
        sd_l = direction(self.dir_vec)
        dx = sd_l[0]
        dy = sd_l[1]
        sd_l.clear()
        for i in range(self.size):
            sd_l.append(Dot(self.shp_x + i * dx, self.shp_y + i * dy))
        return sd_l


class Board:
    def __init__(self, dot_battle_field, battle_field, out_buf, ships, visible, w_ship_rest, battle_field_size=6 ):
        self.dot_battle_field = dot_battle_field
        self.battle_field = battle_field  # двумерный массив состояния игрового поля
        self.out_buf = out_buf  # массив строк для вывода поля в консоль
        self.ships = ships  # список кораблей на доске
        self.visible = visible  # признак видимости кораблей при выводе содержимого поля
        self.w_ship_rest = w_ship_rest  # число оставшихся клеток живых кораблей
        self.battle_field_size = battle_field_size  # размерность игрового поля
       
    def board_reset(self):  # сброс игрового поля
        _out_buf = [
            '    Игра с AI          ',
            '   1 2 3 4 5 6 7 8 9 10',
            ' 1 ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ',
            ' 2 ◦ ░ ░ ░ ░ ░ ░ ◦ ◦ ▚ ',
            ' 3 ◦ ░ ▚ ▚ ░ █ ░ ◦ X ◦ ',
            ' 4 ◦ ░ ░ ░ ░ █ ░ ◦ ◦ ◦ ',
            ' 5 ◦ ◦ ◦ ◦ ░ ▚ ░ ◦ ◦ ◦ ',
            ' 6 ◦ ◦ ◦ ◦ ░ ░ ░ ◦ ◦ █ ',
            ' 7 ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ █ ',
            ' 8 █ █ ◦ █ ▚ █ ◦ ◦ ◦ ◦ ',
            ' 9 ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ',
            '10 ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ '
        ]
        self.dot_battle_field: List[Dot] = []
        for x in range(self.battle_field_size):
            for y in range(self.battle_field_size):
                self.dot_battle_field.append(Dot(x, y))
        self.battle_field = [[0] * self.battle_field_size for _ in range(self.battle_field_size)]
        self.out_buf = _out_buf
        self.ships = []
        self.visible = True
        self.w_ship_rest = 0
        return
        
    def add_ship(self, sp_x, sp_y, s_dir, s_size):
        
        print('Запрос на корабль:', sp_x+1, sp_y+1, s_dir, s_size)
        
        sdl = direction(s_dir)
        dx = sdl[0]
        dy = sdl[1]
        sdl.clear()
        for i in range(s_size):
            if self.battle_field[sp_y + i * dy][sp_x + i * dx] == 0:  # точка на поле свободна
                sdl.append(Dot(sp_x + i * dx, sp_y + i * dy))  # в список точек корабля
            else:
                break
        if len(sdl) != s_size:  # если корабль НЕ встал на поле
            raise ShipNotFitted(f'Из точки [{sp_x + 1},{sp_y + 1}] корабль расположить не получается!')
        sdc = Board.contour(self, sdl)  # создадим контур корабля
        for sc in sdc:  # проверим на близкие корабли по контуру
            if self.battle_field[Dot.get_y(sc)][Dot.get_x(sc)] & 1:  # точка на контуре - другой корабль
                raise ShipNotFitted(f'В точку [{sp_x + 1},{sp_y + 1}] установить корабль не удалось!')
        if self.visible:
            for sc in sdc:  # прорисуем контур корабля
                sc_data = self.battle_field[Dot.get_y(sc)][Dot.get_x(sc)]
                self.battle_field[Dot.get_y(sc)][Dot.get_x(sc)] = sc_data | 0b10
        for sc in sdl:  # прорисуем корабль
            self.battle_field[Dot.get_y(sc)][Dot.get_x(sc)] = 1
        self.ships.append(sdl)
        return sdl
    
    def contour(self, ship_cells):
        def dot_in_board(xc, yc):
            nonlocal d_c_l
            dt = Dot(xc, yc)
            if dt in self.dot_battle_field:
                d_c_l.append(dt)
            return
        
        size = len(ship_cells)
        
        print("Координаты точек корабля = ", end='')
        for sc in ship_cells:
            print(Dot.get_xy(sc), '=', Dot.read(sc, self.battle_field), sc in self.dot_battle_field, end=' ')
        print('Size = ', size, end='\n')
        
        shp_dir = 0  # False - горизонтально по умолчанию для одноклеточных кораблей
        if size > 1:
            sc = iter(ship_cells)  # установление по факту ориентации корабля для 2-х и более клеточных моделей
            shp_dir = get_dir(next(sc), next(sc))  # False - горизонтально True - вертикально
        d_c_l: Dot = []
        for sc in ship_cells:  # формирование списка точек контура вокруг корабля в рамках игрового поля
            x = Dot.get_x(sc)
            y = Dot.get_y(sc)
            if shp_dir == 0:  # для горизонтали
                dot_in_board(x - 1, y)
                dot_in_board(x + size, y)
                for dx in range(-1, size + 1):
                    dot_in_board(x + dx, y + 1)
                    dot_in_board(x + dx, y - 1)
            else:  # для вертикали
                dot_in_board(y, x - 1)
                dot_in_board(y, x + size)
                for dx in range(-1, size + 1):
                    dot_in_board(y + 1, x + dx)
                    dot_in_board(y - 1, x + dx)
            break  # достаточно одного прохода
        return d_c_l
    
    def out_raw(self):
        print(chr(0x00A6) + '=' * self.battle_field_size * 3 + chr(0x21d2) + ' X')
        for b in range(self.battle_field_size):
            print(chr(0x00A6) + str(self.battle_field[b]))
        print(chr(0x21d3) + '-' * (self.battle_field_size * 3 -1))
        print('Y')
        return
    
    def dot_is_free(self, xf, yf):
        return self.battle_field[yf][xf] == 0
    
    
free_cell_sgn = '◦'  # свободная клетка
ship_sgn = '█'  # в клетке корабль (или его часть)
con_ship_sgn = '░'  # контур вокруг корабля
dead_ship_sgn = '▚'  # в клетке подбитый корабль (или его часть)
miss_fire_sgn = 'X'  # в клетку стреляли, но промахнулись


def bat_fld_analizer(bt_in):
    for y in range(bt_in.battle_field_size):
        for x in range(bt_in.battle_field_size):
            sig = free_cell_sgn
            #cell_data = bt_in.battle_field[y][x]
            cell_data = Dot.read(Dot(x, y), bt_in.battle_field)
            if x == 1 and y == 2:
                print(f'BFA({x:2d},{y:2d})=', bin(cell_data))
            if cell_data & 1 == 1:  # клетка с кораблем
                if bt_in.visible:
                    sig = ship_sgn
                else:
                    sig = free_cell_sgn
                    if cell_data & 4 == 4:  # корабль подбит, показываем
                        sig = dead_ship_sgn
            else:
                if cell_data & 2 == 2:  # клетка контур
                    sig = con_ship_sgn
                    if cell_data & 4 == 4:  # в клетку был выстрел
                        sig = miss_fire_sgn
            s1 = str(bt_in.out_buf[y + 2])
            s2 = s1
            x_ind = 3 + x * 2
            s1 = s1[:x_ind]
            s2 = s2[x_ind + 1:]
            s0 = s1 + sig + s2
            bt_in.out_buf[y + 2] = s0
    return

def screen_update(position='L'):
    def l_r_out():  # вывод левого и правого игровых полей
        max_battle_field_size = bf.battle_field_size
        if uf.battle_field_size > max_battle_field_size:
            max_battle_field_size = uf.battle_field_size
        for i in range(max_battle_field_size + 2):
            s_l = str(bf.out_buf[i])
            s_r = str(uf.out_buf[i])
            s_lr = s_l[:(3 + 2 * bf.battle_field_size)] + '          ' + s_r[:(3 + 2 * uf.battle_field_size)]
            print(s_lr)
        print()
        return
    
    def l_out():  # вывод левого игрового поля
        for i in range(bf.battle_field_size + 2):
            s_l = str(bf.out_buf[i])
            s_lr = s_l[:(3 + 2 * bf.battle_field_size)]
            print(s_lr)
        print()
        return
    
    def r_out():  # вывод правого игрового поля
        for i in range(bf.battle_field_size + 2):
            s_r = str(uf.out_buf[i])
            s_lr = s_r[:(3 + 2 * uf.battle_field_size)]
            print(s_lr)
        print()
        return
    
    if position == 'L':
        l_out()
    elif position == 'R':
        r_out()
    elif position == 'LR':
        l_r_out()
    else:
        bf.out_raw()
    return
    
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
    return Dot.get_x(d1) == Dot.get_x(d2)


# Internal logic

 
# Frontend logics

def pew(snd='pew.wav'):
    winsound.PlaySound(snd, winsound.SND_FILENAME)
    return

bf = Board(dot_battle_field=None, battle_field=None, out_buf=None,\
           ships=None, visible=None, w_ship_rest=None, battle_field_size=10)
bf.board_reset()
bf.visible = True

uf = Board(dot_battle_field=None, battle_field=None, out_buf=None,\
           ships=None, visible=None, w_ship_rest=None, battle_field_size=10)
uf.board_reset()

bf.out_raw()

try:
    sh = bf.add_ship(1, 1, 1, 2)
except ShipNotFitted as er:
    print(er)
else:
    pass
bf.out_raw()

try:
    sh = bf.add_ship(3, 0, 0, 3)
except ShipNotFitted as er:
    print(er)
else:
    pass
bf.out_raw()

try:
    sh = bf.add_ship(2, 3, 0, 3)
except ShipNotFitted as er:
    print(er)
else:
    pass

# Dot.wright(Dot(4,4), bf.battle_field, 4)
# Dot.wright(Dot(4,4), bf.battle_field, 6)
# Dot.wright(Dot(5,5), bf.battle_field, 4)
# Dot.wright(Dot(6,6), bf.battle_field, 2)
# Dot.wright(Dot(7,7), bf.battle_field, 1)
# Dot.wright(Dot(8,8), bf.battle_field, 8)
# Dot.wright(Dot(9,9), bf.battle_field, 9)

bat_fld_analizer(bf)
bf.out_raw()
screen_update('LR')

drx = 1
dry = 1
dr = Dot.read(Dot(drx, dry), bf.battle_field)
print(bin(dr))
dr = dr | 0b100
print(bin(dr))
Dot.wright(Dot(drx, dry), bf.battle_field, dr)

ps = 0
while ps < 3:
    print('*', end='')
    time.sleep(1)
    ps += 1
print()


bat_fld_analizer(bf)
bf.out_raw()
screen_update('LR')

drx = 1
dry = 2
dr = Dot.read(Dot(drx, dry), bf.battle_field)
print(bin(dr))
dr = dr | 0b100
print(bin(dr))
Dot.wright(Dot(drx, dry), bf.battle_field, dr)
ps = 0
while ps < 3:
    print('*', end='')
    time.sleep(1)
    ps += 1
print()
bat_fld_analizer(bf)
bf.out_raw()
screen_update('LR')