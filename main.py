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


class Dot:
    def __init__(self, _x, _y, status=None):
        self.x = _x
        self.y = _y
        if status is not None:
            self.status = status
    
    def get_xy(self):
        return [self.x, self.y]
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def get_status(self):
        return self.status
    
    def set_status(self, value):
        if isinstance(value, int):
            self.status = value
        else:
            raise ValueError("Должно быть целое число!")


class Ship:
    def __init__(self, shp_x, shp_y, size, dir_vec, rest_of_cells):
        self.shp_x = shp_x  # координата носа корабля X
        self.shp_y = shp_y  # координата носа корабля Y
        self.size = size  # размер корабля
        self.dir_vec = dir_vec  # ориентация корабля 0- горизонтально слева на право 1- вертикально сверху вниз
        self.rest_of_cells = rest_of_cells  # остаток жизни корабля
         
    def dots(self):
        dx = direction(self.dir_vec)[0]
        dy = direction(self.dir_vec)[1]
        sd_l = []
        for i in range(self.size):
            sd_l.append(Dot(self.shp_x + i * dx, self.shp_y + i * dy))
        return sd_l


class Board:
    def __init__(self, battle_field, out_buf, ships, visible, w_ship_rest, battle_title='', battle_field_size=6):
        self.battle_field = battle_field  # одномерный массив состояния игрового поля
        self.out_buf = out_buf  # массив строк для вывода поля в консоль
        self.ships = ships  # список кораблей на доске
        self.visible = visible  # признак видимости кораблей при выводе содержимого поля
        self.w_ship_rest = w_ship_rest  # число оставшихся клеток живых кораблей
        self.battle_title = battle_title # заголовок окна "Поле "______
        self.battle_field_size = battle_field_size  # размерность игрового поля
       
    def board_reset(self):  # сброс игрового поля
        _out_buf = [
            #00000000001111111111222
            #01234567890123456789012
            '      Поле             ',
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
        self.battle_field: List[Dot] = []
        for y in range(self.battle_field_size):
            for x in range(self.battle_field_size):
                self.battle_field.append(Dot(x, y, 0))
        self.out_buf = _out_buf
        self.ships = []
        self.visible = True
        self.w_ship_rest = 0
        s = self.battle_title
        if len(s) > 0:
            if len(s) > 6:
                s = s[:6]
            ls = len(_out_buf[0])
            _out_buf[0] = _out_buf[0][:11] + s
            while len(_out_buf[0]) < ls:
                _out_buf[0] = _out_buf[0] + ' '
        return
        
    def add_ship(self, sp_x, sp_y, s_dir, s_size):
        print('Поле', self.battle_title, end=' ')
        print(f'Запрос на корабль: X={sp_x+1:2d} Y={sp_y+1:2d}', S_DIR_STR[s_dir], "размер=",s_size)
        dx = direction(s_dir)[0]
        dy = direction(s_dir)[1]
        sdl = []
        for i in range(s_size):
            d_dot = self.battle_field[sp_x + i * dx + (sp_y + i * dy) * self.battle_field_size]
            if d_dot.status == 0:  # точка на поле свободна
                sdl.append(d_dot)  # в список точек корабля
            else:
                break
        if len(sdl) != s_size:  # если корабль НЕ встал на поле
            raise ShipNotFitted(f'Из точки [{sp_x + 1},{sp_y + 1}] корабль расположить не получается!')
        sdc = Board.contour(self, sdl)  # создадим контур корабля
        for d_dot in sdc:  # проверим на близкие корабли по контуру
            if Dot.get_status(d_dot) & 1:  # точка на контуре - другой корабль
                raise ShipNotFitted(f'В точку [{sp_x + 1},{sp_y + 1}] установить корабль не удалось!')
        if self.visible:
            for sc in sdc:  # прорисуем контур корабля
                sc.status = sc.status | 0b10
        for sc in sdl:  # прорисуем корабль
            sc.status = 1
        self.ships.append(sdl)  # внесем корабль в группу кораблей поля боя
        return sdl  # вернем список точек корабля при успехе
    
    def out(self, x, y):
        if Dot(x, y) not in self.battle_field:
            raise BoardOutException('Координаты за пределами поля!')
        return
    
    def contour(self, ship_cells):
        def dot_in_board(xc, yc):
            nonlocal d_c_l
            try:
                self.out(xc, yc)
            except BoardOutException:
                pass
            else:
                dt = self.battle_field[xc + yc * self.battle_field_size]
                d_c_l.append(dt)
            return
        
        size = len(ship_cells)
        
        print("Координаты точек корабля = ", end='')  # для настойки алгоритма
        for sc in ship_cells:
            print(Dot.get_xy(sc), '=', Dot.get_status(sc), sc in self.battle_field, end=' ')
        print('Size = ', size, end='\n')
        
        shp_dir = 0  # False - горизонтально по умолчанию для одноклеточных кораблей
        if size > 1:
            sc = iter(ship_cells)  # установление по факту ориентации корабля для 2-х и более клеточных моделей
            shp_dir = get_dir(next(sc), next(sc))  # False - горизонтально True - вертикально
        d_c_l = []
        for sc in ship_cells:  # формирование списка точек контура вокруг корабля в рамках игрового поля
            x = sc.x
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
    
    def out_raw(self):  # вывод поля в нативном формате для настройки алгоритма
        print('Поле', self.battle_title)
        print(chr(0x00A6) + '=' * self.battle_field_size * 2 + chr(0x21d2) + ' X')
        for b in range(self.battle_field_size):
            print(chr(0x00A6), end=' ')
            for a in range(self.battle_field_size):
                #ds = a + b * self.battle_field_size
                d = self.battle_field[a + b * self.battle_field_size]
                print(d.status, end=' ')
            print()
        print(chr(0x21d3) + '-' * (self.battle_field_size * 2 - 0))
        print('Y')
        return
    
    def shot(self, x, y):  # выстрел в игровое поле, при попадании в корабль возвращает True
        self.out(x, y)  # координаты в пределах игрового поля?
        dt = self.battle_field[x + y * self.battle_field_size]  # считываем из поля боя клетку
        if self.dot_with_flags(x, y, FIRE+SHIP):
            raise DotAllReadyPoked('По кораблю уже стреляли!')
        if self.dot_with_flags(x, y, FIRE):
            raise DotAllReadyPoked('Сюда уже стреляли!')
        if self.dot_with_flags(x, y, SHIP):  # попали в корабль
            dt.status = dt.status | SHIP  # отмечаем, что в клетке корабль
        dt.status = dt.status | FIRE  # отмечаем, что в клетку произведен выстрел
        return
    
    def dot_with_flags(self, xf, yf, flag):  # возвращает True если флаги по маске установлены
        dt = self.battle_field[xf + yf * self.battle_field_size]  # считываем из поля боя клетку
        return dt.status & flag == flag
    
class Player:
    def __init__(self, my_board, enemy_board):
        self.my_board = my_board
        self.enemy_board = enemy_board
        
    def ask(self):
        raise NotImplementedError()
    
    # def move(self):
    #     while True:
    #         try:
    #             xy_coord = self.ask()
            
    
    
    

        
    
    
FREE_CELL_SGN = '◦'  # свободная клетка
SHIP_SGN = '█'  # в клетке корабль (или его часть)
CON_SHIP_SGN = '░'  # контур вокруг корабля
DEAD_SHIP_SGN = '▚'  # в клетке подбитый корабль (или его часть)
MISS_FIRE_SGN = 'X'  # в клетку стреляли, но промахнулись
S_DIR_STR = ['горизонтально', 'вертикально']  # строка индикации направления корабля
SHIP = 0b0001  # флаг корабля в клетке
CONT = 0b0010  # флаг корабельного контура
FIRE = 0b0100  # флаг выстрела в клетку
CNDS = 0b1000  # флаг контура подбитого корабля

def bat_fld_analyzer(bt_in):
    for y in range(bt_in.battle_field_size):
        for x in range(bt_in.battle_field_size):
            sig = FREE_CELL_SGN  # по умолчанию - свободное поле
            cell = bt_in.battle_field[x + y * bt_in.battle_field_size]
            if cell.status & 1 == 1:  # клетка с кораблем
                if cell.status & 4 == 4:  # корабль подбит
                    sig = DEAD_SHIP_SGN  # показываем подбитый
                elif bt_in.visible:
                    sig = SHIP_SGN  # показываем целый
            else:
                if cell.status & 4 == 4:  # в клетку был выстрел
                    sig = MISS_FIRE_SGN  # показываем выстрел
                elif cell.status & 8 == 8:  # клетка - контур подбитого корабля
                    sig = CON_SHIP_SGN  # показываем контур
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
        for i in range(uf.battle_field_size + 2):
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
        Board.out_raw(bf)
        Board.out_raw(uf)
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


def pause(t):
    ps = 0
    while ps < t:
        print('*', end='')
        time.sleep(1)
        ps += 1
    print()
    return


bf = Board(battle_field=None, out_buf=None,
           ships=None, visible=None, w_ship_rest=None, battle_title='AI bot', battle_field_size=10)
bf.board_reset()
bf.visible = True

uf = Board(battle_field=None, out_buf=None,
           ships=None, visible=None, w_ship_rest=None, battle_title='User', battle_field_size=10)
uf.board_reset()
uf.visible = True

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

bat_fld_analyzer(bf)
bf.out_raw()

screen_update('L')
screen_update('R')

screen_update('LR')

drx = 1
dry = 1
dd = bf.battle_field[drx + dry * bf.battle_field_size]
dr = dd.status
dr = dr | 0b100
dd.status = dr
pause(3)
bat_fld_analyzer(bf)
bf.out_raw()
screen_update('LR')

drx = 1
dry = 2
dr = bf.battle_field[drx + dry * bf.battle_field_size].status
dr = dr | 0b100
bf.battle_field[drx + dry * bf.battle_field_size].status = dr
pause(3)
bat_fld_analyzer(bf)
bf.out_raw()
screen_update('LR')

drx = 2
dry = 2
dr = bf.battle_field[drx + dry * bf.battle_field_size].status
dr = dr | 0b100
bf.battle_field[drx + dry * bf.battle_field_size].status = dr
pause(3)
bat_fld_analyzer(bf)
bf.out_raw()
screen_update('LR')
screen_update('ub')

