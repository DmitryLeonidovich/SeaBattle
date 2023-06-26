import sys
if sys.platform == 'win32':
    import winsound
from random import randint
import time
from typing import List


FREE_CELL_SGN = '◦'  # свободная клетка
SHIP_SGN = '█'  # в клетке корабль (или его часть)
CON_SHIP_SGN = '░'  # контур вокруг корабля
DEAD_SHIP_SGN = '▚'  # в клетке подбитый корабль (или его часть)
MISS_FIRE_SGN = 'X'  # в клетку стреляли, но промахнулись
S_DIR_STR = ['горизонтально', 'вертикально']  # строка индикации направления корабля
IN_BATTLE_FIELD = ['вне поля боя', 'в поле боя']  # строка индикации расположения точки
SHIP = 0b0001  # флаг корабля в клетке
CONT = 0b0010  # флаг корабельного контура
FIRE = 0b0100  # флаг выстрела в клетку
C_DS = 0b1000  # флаг контура подбитого корабля


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


def pew(snd='pew.wav'):
    try:
        winsound.PlaySound(snd, winsound.SND_FILENAME)
    except NameError:
        pass
    else:
        return


def pause(t):
    ps = 0
    while ps < t:
        print('>', end='')
        time.sleep(1)
        ps += 1
    print('', end='')
    return


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
        dx, dy = direction(self.dir_vec)
        # dy = direction(self.dir_vec)[1]
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
        self.battle_title = battle_title  # заголовок окна "Поле "______
        self.battle_field_size = battle_field_size  # размерность игрового поля
       
    def board_reset(self):  # сброс игрового поля
        _out_buf = [
            # 0000000001111111111222
            # 1234567890123456789012
            
            ' Поле                  ',
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
            _out_buf[0] = _out_buf[0][:6] + s
            while len(_out_buf[0]) < ls:
                _out_buf[0] = _out_buf[0] + ' '
        return
        
    def add_ship(self, sp_x, sp_y, s_dir, s_size):
        dx, dy = direction(s_dir)
        if sp_x + s_size * dx > self.battle_field_size or sp_y + s_size * dy > self.battle_field_size:
            raise ShipNotFitted(f'Из точки [{sp_x + 1},{sp_y + 1}] корабль расположить не получается!')
        # print('Поле', self.battle_title, end=' ')
        # print(f'Запрос на корабль: X={sp_x + 1:2d} Y={sp_y + 1:2d}', S_DIR_STR[s_dir], f'размер={s_size:1d}')
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
            if Dot.get_status(d_dot) & SHIP:  # точка на контуре - другой корабль
                raise ShipNotFitted(f'В точку [{sp_x + 1},{sp_y + 1}] установить корабль не удалось!')
        if self.visible:
            for sc in sdc:  # прорисуем контур корабля
                sc.status = sc.status | CONT
        for sc in sdl:  # прорисуем корабль
            sc.status = SHIP
        self.ships.append(sdl)  # внесем корабль в группу кораблей поля боя
        return sdl  # вернем список точек корабля при успехе
    
    def out(self, o_x, o_y):
        if Dot(o_x, o_y) not in self.battle_field:
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
                # print('Поле', self.battle_title,'DotXY=', Dot.get_xy(dt), 'DotStatus=', Dot.get_status(dt))
            return
        
        size = len(ship_cells)
        
        # print("Координаты точек корабля = ", end='')  # для настойки алгоритма
        # for sc in ship_cells:
        #     print(Dot.get_xy(sc), '=', Dot.get_status(sc), IN_BATTLE_FIELD[sc in self.battle_field], end=' ')
        shp_dir = 0  # False - горизонтально по умолчанию для одноклеточных кораблей
        if size > 1:
            sc = iter(ship_cells)  # установление по факту ориентации корабля для 2-х и более клеточных моделей
            shp_dir = get_dir(next(sc), next(sc))  # False - горизонтально True - вертикально
        # print(', расположен', S_DIR_STR[shp_dir], ', размер =', size, end='\n')
        d_c_l = []
        for sc in ship_cells:  # формирование списка точек контура вокруг корабля в рамках игрового поля
            x_c, y_c = Dot.get_xy(sc)
            dot_in_board(x_c - 1 + shp_dir, y_c - 1 * shp_dir)
            dot_in_board(x_c + size * (1 - shp_dir), y_c + size * shp_dir)
            for d_s in range(-1, size + 1):
                dot_in_board(x_c + shp_dir + d_s * (1 - shp_dir), y_c + 1 - shp_dir + d_s * shp_dir)
                dot_in_board(x_c - shp_dir + d_s * (1 - shp_dir), y_c - 1 + shp_dir + d_s * shp_dir)
            break  # достаточно одного прохода
        return d_c_l
    
    def out_raw(self):  # вывод поля в нативном формате для настройки алгоритма
        print('Поле', self.battle_title)
        print(chr(0x00A6) + '=' * self.battle_field_size * 2 + chr(0x21d2) + ' X')
        for b in range(self.battle_field_size):
            print(chr(0x00A6), end=' ')
            for a in range(self.battle_field_size):
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
            dt.status = dt.status | FIRE  # отмечаем, что в клетке подбит корабль
            return True
        dt.status = dt.status | FIRE  # отмечаем, что в клетку произведен выстрел
        return False
    
    def dot_with_flags(self, xf, yf, flag):  # возвращает True если флаги по маске установлены
        dt = self.battle_field[xf + yf * self.battle_field_size]  # считываем из поля боя клетку
        return dt.status & flag == flag
    
    def bat_fld_analyzer(self):
        for y in range(self.battle_field_size):
            for x in range(self.battle_field_size):
                sig = FREE_CELL_SGN  # по умолчанию - свободное поле
                bf_pos = x + y * self.battle_field_size
                cell = self.battle_field[bf_pos]
                if cell.status & 1 == 1:  # клетка с кораблем
                    if cell.status & 4 == 4:  # корабль подбит
                        sig = DEAD_SHIP_SGN  # показываем подбитый
                    elif self.visible:
                        sig = SHIP_SGN  # показываем целый
                else:
                    if cell.status & 4 == 4:  # в клетку был выстрел
                        sig = MISS_FIRE_SGN  # показываем выстрел
                    elif cell.status & 8 == 8:  # клетка - контур подбитого корабля
                        sig = CON_SHIP_SGN  # показываем контур
                s1 = str(self.out_buf[y + 2])
                s2 = s1
                x_ind = 3 + x * 2
                s1 = s1[:x_ind]
                s2 = s2[x_ind + 1:]
                s0 = s1 + sig + s2
                self.out_buf[y + 2] = s0
        return
    
    
class Player:
    def __init__(self, my_board, enemy_board):
        self.my_board = my_board
        self.enemy_board = enemy_board
        
    def ask(self):
        raise NotImplementedError()
    
    def move(self):
        while True:
            try:
                xy_coord = self.ask()
                # print('Выстрел в', xy_coord.x + 1, xy_coord.y + 1)
                hit_ok = Board.shot(self.enemy_board, xy_coord.x, xy_coord.y)
                return hit_ok
            except BoardOutException as e:
                print(e)
            except DotAllReadyPoked as e:
                print(e)
                
        
class AI(Player):
    def ask(self):
        dum = []
        for i in self.enemy_board.battle_field:  # создание списка точек для удара на поле оппонента
            if i.status & (FIRE + C_DS) == 0:
                dum.append(i)
        if len(dum) < 1:
            raise BoardOutException("Нет места для выстрела!!!")
        
        # выбор точки для выстрела в поле врага
        d_ind = randint(0, len(dum))
        d = self.enemy_board.battle_field[d_ind]
        print(f"Удар в точку: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            xy = input("Введите X и Y через пробел: ").split()
            if len(xy) != 2:
                print("Введите только 2 координаты!")
                continue
            x, y = xy
            if not (x.isdigit()) or not (y.isdigit()):
                print(" Вводите числа! ")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)




class Game:
    def __init__(self):
        self.bf = Board(battle_field=None, out_buf=None,
                        ships=None, visible=True, w_ship_rest=None, battle_title='AI bot', battle_field_size=6)
        self.uf = Board(battle_field=None, out_buf=None,
                        ships=None, visible=True, w_ship_rest=None, battle_title='User', battle_field_size=10)
        self.random_board(self.uf)
        self.random_board(self.bf)
        self.guru = AI(self.bf, self.uf)
        self.nemo = User(self.uf, self.bf)

    def random_board(self, bd):
        # print('\nРасстановка кораблей на поле', bd.battle_title)
        while True:
            bd.board_reset()
            ship_type = [
                        [3, 2, 2, 1, 1, 1, 1],              # 6 x 6
                        [3, 3, 2, 2, 1, 1, 1, 1],           # 7 x 7
                        [4, 3, 3, 2, 2, 1, 1, 1, 1],        # 8 x 8
                        [4, 3, 3, 2, 2, 2, 1, 1, 1, 1],     # 9 x 9
                        [4, 4, 3, 3, 2, 2, 1, 1, 1, 1, 1],  # 10 x 10
                        ]
            att1 = True
            while att1:
                steps = 0
                for st in ship_type[bd.battle_field_size - 6]:
                    while True:
                        steps += 1
                        bd_set_x = randint(0, bd.battle_field_size-1)
                        bd_set_y = randint(0, bd.battle_field_size-1)
                        bd_set_d = randint(0, 99)
                        if bd_set_d > 49:
                            bd_set_d = 1
                        else:
                            bd_set_d = 0
                        bd_set = [bd_set_x, bd_set_y, bd_set_d, st]
                        try:
                            bd.add_ship(bd_set_x, bd_set_y, bd_set_d, st)
                            # bd.out_raw()
                            # print('Good=', bd_set)
                            break  # корабль встал удачно, берем следующий, если есть
                        except ShipNotFitted:
                            # bd.out_raw()
                            # print(' Bad=', bd_set)
                            pass  # корабль не вписался в поле
                        if steps > 2000:  # смотрим, есть ли еще лимит попыток размещения
                            att1 = False  # лимит попыток исчерпан - сброс игрового поля как тупикового
                            pew()  # ============================================
                            pew()  # ============================================
                            break
                    if not att1:
                        break  # Выходим из цикла по размещению кораблей, т.к. нужно сбросить поле
                if att1:
                    # print('Поле сформировано за', steps, 'шагов.')
                    return  # если цикл по кораблям закончился традиционно - выходим, все они установлены
                pass  # нет, цикл еще с перспективой - берем следующий корабль на размещение
            pass  # сюда попадают при необходимости сбросить поле
        pass  # отсюда сброс поля и делают
        # сюда никогда не попадают
    
    def screen_update(self, bf, uf, position='L'):
        def l_r_out():  # вывод левого и правого игровых полей
            max_battle_field_size = bf.battle_field_size
            if uf.battle_field_size > max_battle_field_size:
                max_battle_field_size = uf.battle_field_size
            for i in range(max_battle_field_size + 2):
                if i > bf.battle_field_size + 1:
                    s_l = " " * (3 + 2 * bf.battle_field_size)
                else:
                    s_l = str(bf.out_buf[i])
                if i > uf.battle_field_size + 1:
                    s_r = " " * (3 + 2 * uf.battle_field_size)
                else:
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
        elif position == 'LR' or position == 'RL':
            l_r_out()
        else:
            Board.out_raw(bf)
            Board.out_raw(uf)
        return
    
    def greetings(self):
        print("Hello!!! This is Sea Battle.")
        
    def loop(self):
        curr_move = 0  # ноль - игрок, 1 - компьютер
        while True and curr_move < 100:
            self.bf.bat_fld_analyzer()
            self.uf.bat_fld_analyzer()
            self.screen_update(self.bf, self.uf, "LR")
            if curr_move % 2 == 0:
                print("Ваш выстрел.")
                repeat = self.nemo.move()
            else:
                print("Стреляет компьютер.", end='')
                pause(3)
                repeat = self.guru.move()
            if repeat:
                curr_move -= 1
            curr_move += 1
        return
    
    def start(self):
        self.greetings()
        pew()
        self.loop()
      
        
game = Game()
game.start()
quit(0)

game.bf.visible = False
game.screen_update(game.bf, game.uf, "RL")
game.bf.board_reset()
game.bf.bat_fld_analyzer()
game.screen_update(game.bf, game.uf, "RL")
quit(0)

print("=" * 80)
game.bf.add_ship(6, 4, 1, 4)
game.bf.bat_fld_analyzer()
game.screen_update(game.bf, game.uf, "L")
game.bf.add_ship(1, 6, 0, 4)
game.bf.bat_fld_analyzer()
game.screen_update(game.bf, game.uf, "L")

game.screen_update(game.bf, game.uf, "==")
print("Доброго вечера, мы со Skill Factory.")
quit(0)
