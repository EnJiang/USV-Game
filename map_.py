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
        '''地图里面为了符合人的习惯,定整个矩阵的左下角为(0,0), x轴负方向为0°, y轴正方形为90°
        和计算机矩阵左上角为(0,0)的习惯稍微不同,故x和y是反过来的,镜像对称'''

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


class MatrixMap(BasicMap):
    """一个较大的地图,用大型矩阵来描绘一个伪二维连续平面
    成员属性中的USV的位置仍为浮点数, 但是提供一个api接口用于输出位置矩阵
    此时USV的位置将被定位到最近的那个点位上"""

    def __init__(self, width, height):
        super(MatrixMap, self).__init__(width, height)

    def env_matrix(self):
        pass
