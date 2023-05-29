# Exceptions block
class SBExceptions(Exception):
    def __init__(self):
        pass


class ShipNotFitted(SBExceptions):
    def __init__(self, errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg
        
        
class BoardOutException(SBExceptions):
    def __init__(self,errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg


class DotIsBusy(SBExceptions):
    def __init__(self,errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg


class DotAllReadyPoked(SBExceptions):
    def __init__(self,errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg


class DotTooClose(SBExceptions):
    def __init__(self,errmsg=''):
        self.errmsg = "Sea Battle exception:" + errmsg


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    

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
    def __init__(self, battle_field, ships, visible, w_ship_rest):
        self.battle_field = battle_field  # двумерный массив состояния игрового поля
        self.ships = ships  # список кораблей на доске
        self.visible = visible  # признак видимости кораблей при выводе
        self.w_ship_rest = w_ship_rest  # число оставшихся в живых кораблей
        if self.battle_field is None or \
                self.ships is None or \
                self.visible is None or \
                self.w_ship_rest is None:
            Board.board_reset(self)
            
    def board_reset(self):  # сброс игрового поля
        self.battle_field = [0] * 6
        for i in range(6):
            self.battle_field[i] = [0] * 6
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
            if self.battle_field[sp_x + i * dx][sp_y + i * dy] == 0:
                sdl.append(Dot(sp_x + i * dx, sp_y + i * dy))
                self.battle_field[sp_x + i * dx][sp_y + i * dy] = 1
        if len(sdl) == s_size:
            return sdl
        if len(sdl) > 0:
            for i in range(len(sdl)):
                self.battle_field[sdl[i].x][sdl[i].y] = 0
        raise ShipNotFitted('Установить корабль не удалось!')
    
    def out_bf(self):
        for b in range(6):
            print(bf.battle_field[b])
        print('-----------------------')
        return
    
    
    def contour(self, ship_cells):
        
        return
    
    
    def dot_is_free(self, xf, yf):
        
        return
        

# Internal logic

 
# Frontend logics



sh = Ship(1,1,3,0,3)
print(sh.dots())
for i in sh.dots():
    print(i.x, i.y)
    
bf = Board(battle_field=None, ships=None, visible=None, w_ship_rest=None)

try:
    bf.add_ship(2, 1, 1, 3)
except ShipNotFitted(''):
    print('Кораблик не влез.')
else:
    bf.out_bf()
pass

try:
    bf.add_ship(2, 1, 0, 3)
except ShipNotFitted(''):
    print('Кораблик не влез.')
else:
    bf.out_bf()

