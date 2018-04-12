# coding:utf-8

import copy
import numpy as np


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

    def str2(self):

        matrix = [['.' for i in range(self.width)] for j in range(self.height)]
        matrix[self.target_x][self.target_y] = 'E'   #A*中的终点目标end
        for ship in self.ships:
            ship_x, ship_y = ship.coordinate()
            if(ship.is_enemy):
                matrix[ship_x][ship_y] = '#'    #A*中的障碍物区域#
            else:
                matrix[ship_x][ship_y] = 'S'    #A*中的起始点start


        strlist = []
        for i in range(self.width):
            temprow = ''
            for j in range(self.height):
                temprow = temprow + matrix[i][j]
            strlist.append(temprow)

        return strlist


    def env_matrix(self):
        env_np = np.zeros((self.width,self.height))
        for ship in self.friendly_ships:
            ship_x, ship_y = ship.coordinate()
            env_np[ship_x][ship_y] = 1

        for ship in self.enemy_ships:
            ship_x, ship_y = ship.coordinate()
            env_np[ship_x][ship_y] = -1
            
        env_np[self.target_x][self.target_y] = 2
        # return np.reshape(env_np, (1, ) + env_np.shape)
        return env_np



class MatrixMap(BasicMap):
    """一个较大的地图,用大型矩阵来描绘一个伪二维连续平面
    成员属性中的USV的位置仍为浮点数, 但是提供一个api接口用于输出位置矩阵
    此时USV的位置将被定位到最近的那个点位上"""

    def __init__(self, width, height):
        super(MatrixMap, self).__init__(width, height)

    def env_matrix(self):
        pass




class MyContinueObsMap(BasicMap):
    """一个较大的地图,用大型矩阵来描绘一个伪二维连续平面
    成员属性中的USV的位置仍为浮点数, 但是提供一个api接口用于输出位置矩阵
    此时USV的位置将被定位到最近的那个点位上"""

    def __init__(self, width, height):
        super(MyContinueObsMap, self).__init__(width, height)
        self.obs = []
        self.target_radius = 1

    def addobs(self, obstacle):
        self.obs.append(obstacle)

    # 输出全局地图
    def env_matrix(self):
        env_np = np.zeros((self.width, self.height))
        for ship in self.ships:
            ship_x, ship_y = ship.coordinate()
            ship_x = (int)(round(ship_x, 0));
            ship_y = (int)(round(ship_y, 0))
            env_np[ship_x][ship_y] = 1  # 1表示USV：USV的圆心

            for i in range(ship_x - ship.radius, ship_x + ship.radius + 1):
                for j in range(ship_y - ship.radius, ship_y + ship.radius + 1):
                    if ((i - ship_x) * (i - ship_x) + (j - ship_y) * (j - ship_y)) <= (ship.radius * ship.radius):
                        env_np[i][j] = 1  # 表示USV： USV的半径区域

        for obs in self.obs:
            # 方式1：这样做会出现障碍物在移动过程中，占据（二、三、四、5⃣五）个栅格单元的情况
            # xmin,xmax = obs.obsXminXmax()
            # xmin = (int)(round(xmin,0));xmax = (int)(round(xmax,0))
            #
            # ymin, ymax = obs.obsYminYmax()
            # ymin = (int)(round(ymin,0));ymax = (int)(round(ymax,0))
            #
            # for ix in range(xmin, xmax+1):
            #     for iy in range(ymin, ymax+1):
            #         if ((ix - obs.x)*(ix - obs.x) + (iy - obs.y)*(iy - obs.y))<= (obs.radius *obs.radius):
            #             env_np[ix][iy] = -1   #-1表示障碍物

            # 方式2：类似USV，这样保证就算障碍物移动，也一直是（中间、上下左右）五个栅格单元
            obs_x = (int)(round(obs.x, 0))
            obs_y = (int)(round(obs.y, 0))
            env_np[obs_x][obs_y] = -1  # -1表示圆形障碍物：障碍物的圆心
            for ix in range(obs_x - obs.radius, obs_x + obs.radius + 1):
                for iy in range(obs_y - obs.radius, obs_y + obs.radius + 1):
                    if ((ix - obs_x) * (ix - obs_x) + (iy - obs_y) * (iy - obs_y)) <= (obs.radius * obs.radius):
                        env_np[ix][iy] = -1  # -1表示障碍物

        after_targetx, after_targety = (int)(round(self.target_x, 0)), (int)(round(self.target_y, 0))
        env_np[after_targetx][after_targety] = 2  # 2表示终点:终点圆心
        for itar in range(after_targetx - self.target_radius, after_targetx + self.target_radius + 1):
            for jtar in range(after_targety - self.target_radius, after_targety + self.target_radius + 1):
                if ((itar - after_targetx) * (itar - after_targetx) + (jtar - after_targety) * (
                    jtar - after_targety)) <= (self.target_radius * self.target_radius):
                    env_np[itar][jtar] = 2  # 2表示终点:终点圆心

        return env_np


