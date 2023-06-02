# Exceptions block
from typing import List


class SBException(Exception):
    def __init__(self):
        pass


class ShipNotFitted(SBException):
    def __init__(self, errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg
        
        
class BoardOutException(SBException):
    def __init__(self,errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg


class DotIsBusy(SBException):
    def __init__(self,errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg


class DotAllReadyPoked(SBException):
    def __init__(self,errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg


class DotTooClose(SBException):
    def __init__(self,errmsg=''):
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
        
    def dots(self):
        sdl = []
        if self.dir_vec == 0:
            dx = 1
            dy = 0
        else:
            dx = 0
            dy = 1
        for i in range(self.size):
            sdl.append(Dot(self.shp_x + i * dx, self.shp_y + i * dy))
        return sdl


class Board:
    def __init__(self, battle_field, ships, visible, w_ship_rest, battle_field_size=6):
        self.battle_field = battle_field  # двумерный массив состояния игрового поля
        self.ships = ships  # список кораблей на доске
        self.visible = visible  # признак видимости кораблей при выводе
        self.w_ship_rest = w_ship_rest  # число оставшихся в живых кораблей
        self.battle_field_size = battle_field_size  # размерность игрового поля
       
    def board_reset(self):  # сброс игрового поля
        self.battle_field = [0] * self.battle_field_size
        for i in range(self.battle_field_size):
            self.battle_field[i] = [0] * self.battle_field_size
        self.ships = 0
        self.visible = True
        self.w_ship_rest = 0
        return
        
    def add_ship(self, sp_x, sp_y, s_dir, s_size):
        sdl = []
        if s_dir == 0:
            dx = 1
            dy = 0
        else:
            dx = 0
            dy = 1
        for i in range(s_size):
            if self.battle_field[sp_y + i * dy][sp_x + i * dx] == 0:  # точка на поле свободна
                sdl.append(Dot(sp_x + i * dx, sp_y + i * dy))  # в список точек корабля ее
                self.battle_field[sp_y + i * dy][sp_x + i * dx] = 1  # метим точку кораблем
            else:
                break
        if len(sdl) == s_size:  # если корабль встал на поле, создадим контур корабля
            return sdl
        if len(sdl) > 0:
            for i in range(len(sdl)):
                self.battle_field[sdl[i].y][sdl[i].x] = 0
        raise ShipNotFitted(f'В точку [{sp_x},{sp_y}] установить корабль не удалось!')

    def contour(self, ship_cells):
        csdl = []
        for sc in ship_cells:
            pass
        #     print(Dot.dot_read(sc, self.battle_field), end=', ')
        # print()
        # print(ship_cells, '\n', csdl)

        if len(csdl) > 0:
            pass
        return csdl
    
    
    
    
    
    
    def out_bf(self):
        for b in range(6):
            print(self.battle_field[b])
        print('-----------------------')
        return
  
    def dot_is_free(self, xf, yf):
        return self.battle_field[xf][yf] == 0
        

# Internal logic

 
# Frontend logics


# sh = Ship(1,1,3,0,3)
#
# for i in sh.dots():
#     print(i.x, i.y, end=', ')
# print()


bf = Board(battle_field=None, ships=None, visible=None, w_ship_rest=None)
bf.board_reset()

try:
    sh = bf.add_ship(1,1, 1, 2)
except ShipNotFitted as er:
    print(er)
else:
    bf.out_bf()
    cont_sh = bf.contour(sh)

print("Координаты точек корабля = ", end='')
for sc in sh:
    print(Dot.get_dot_xy(sc), end=' ')

size = len(sh)
print('Size = ', size, end='\n')
shp_dir = 0
if size > 1:
    xyl = []
    for sc in sh:
        xyl.append(Dot.get_dot_xy(sc))
    shp_dir = xyl[0][0] == xyl[1][0]
    print(xyl[0][0], xyl[1][0], shp_dir)
    
for sc in sh:
    x = Dot.get_dot_x(sc)
    y = Dot.get_dot_y(sc)
    if shp_dir == 0:
        c_l = [[x - 1, y], [x + size, y]]  # для горизонтали
        for dx in range(-1, size + 1):
            c_l.append([x + dx, y + 1])
            c_l.append([x + dx, y - 1])
    else:
        c_l = [[y, x - 1], [y, x + size]]  # для вертикали
        for dx in range(-1, size + 1):
            c_l.append([y + 1, x + dx])
            c_l.append([y - 1, x + dx])
            
    print(c_l)
    clgood = []
    for dx in c_l:
        # print(f'Check>({dx[0]}, {dx[1]}) = ', end='')
        if (0 <= dx[0] < bf.battle_field_size) and\
           (0 <= dx[1] < bf.battle_field_size):
            # print('   good=', dx)
            clgood.append(dx)
    print(clgood)
    break




# try:
#     bf.add_ship(2, 1, 0, 3)
# except ShipNotFitted as er:
#     print(er)
# else:
#     bf.out_bf()
#



"""
    for x in range(6):
        for y in range(6):
            sdl.append(Dot(x, y))  # в список точек
    
    for sc in sdl:
        print(Dot.dot_read(sc, bf.battle_field), ' = ', end='')
        print(Dot.get_dot_xy(sc), Dot.get_dot_x(sc), Dot.get_dot_y(sc))
"""
