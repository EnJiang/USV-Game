# coding:utf-8

import copy


class BasicMap(object):
    '''Map类描绘了当前整个海面上的状况
    在这个简单的字符界面中"~"代表空白海面,E代表敌方舰船,F代表友方舰船'''

    def __init__(self, width, height):
        super(BasicMap, self).__init__()
        self.width, self.height = width, height
        self.target_x = 0.0
        self.target_y = 0.0
        self.friendly_ships = []
        self.enemy_ships = []
        self.ships = []

    def set_target(self, x, y):
        self.target_x, self.target_y = x, y

    def target_coordinate(self):
        return self.target_x, self.target_y

    def add_ship(self, ship):
        if(ship.is_enemy):
            self.enemy_ships.append(ship)
        else:
            self.friendly_ships.append(ship)
        self.ships.append(ship)

    def __str__(self):
        _str_ = ""

        matrix = [['~' for i in range(self.width)] for j in range(self.height)]
        matrix[self.target_y][self.target_x] = 'T'
        for ship in self.ships:
            ship_x, ship_y = ship.coordinate()
            if(ship.is_enemy):
                matrix[ship_y][ship_x] = 'E'
            else:
                matrix[ship_y][ship_x] = 'F'

        for line in matrix:
            for one in line:
                _str_ += one + ' '
            _str_ += '\n'

        return _str_


class LargeMap(BasicMap):
    """一个较大的地图,用大型矩阵来描绘一个伪二维连续平面
    每次USV移动之后,LargeMap会对USV的位置进行校正,将其浮点区域去掉并
    定位到最近的那一个矩阵点"""

    def __init__(self, width, height):
        super(LargeMap, self).__init__(width, height)
