# coding:utf-8

import pygame
from pygame.locals import *
import copy
from collections import namedtuple
from time import sleep
import numpy as np


# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# plt.ion()
# fig = plt.figure()
# ax = fig.add_subplot(111)



class BasicGame(object):
    """基本游戏逻辑"""

    def __init__(self):
        super(BasicGame, self).__init__()
        self.is_target_safe = True

    def set_map(self, gameMap):
        self.map = gameMap

    def update(self):
        for ship in self.map.ships:
            ship.move()
        self.check_target()
        #print (self.map.str2())

    def check_target(self):
        target_x, target_y = self.map.target_coordinate()
        for ship in self.map.enemy_ships:
            ship_x, ship_y = ship.coordinate()
            if(ship_x == target_x and ship_y == target_y):
                self.is_target_safe = False

    def is_game_over(self):
        return not self.is_target_safe

    def start(self):
        while not self.is_game_over():
            self.update()
            print ('----------------------------------------------------------------------------------------')
            print ("press any key to continue")
            #raw_input()
            input()
        print ("you lost!")


class MyGame(BasicGame):
    def __init__(self):
        super(MyGame, self).__init__()
        self.recordlist = []
        self.arriveTarget = 0
        self.arriveObstacle = 0


    def update(self):
        # print('update_之前：输出ma.str2()函数的地图形式：：')
        # print(self.map.str2())

        try:
            for ship in self.map.friendly_ships:
                #if ship.uid == 0: recenv = ship.recordenv()
                if not ship.is_enemy: recenv = ship.recordenv()
                # if ship.uid == 0: recaction = ship.recordaction()
                if not ship.is_enemy: recaction = ship.recordaction()
                ship.move()
                self.recordlist.append((recenv, recaction))
                self.check_target()
                self.check_obstacle()

            #这里添加enemy_ships的随机变动：上下左右或是原地（在USV.py中添加moverandom()方法）
            for ship in self.map.enemy_ships:
                ship.moverandom()


        except IndexError as e:
                self.is_target_safe = False
                self.arriveObstacle = True

        # print('update_之后：输出ma.str2()函数的地图形式：：')
        # print(self.map.str2())


    def check_target(self):
        target_x, target_y = self.map.target_coordinate()
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()
            if(ship_x == target_x and ship_y == target_y):
                self.is_target_safe = True
                self.arriveTarget = True


    def check_obstacle(self):
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()
            for obstacle in self.map.enemy_ships:
                obstacle_x, obstacle_y = obstacle.coordinate()
                if(ship_x == obstacle_x and ship_y == obstacle_y):
                    self.is_target_safe = False
                    self.arriveObstacle = True


    def is_game_over(self):
        return not self.is_target_safe


    def start(self):
        while not self.is_game_over():
            #print('game-start-update前的地图形式：');print(self.map.str2())
            self.update()
            # print('\n决策链（当前环境env + 采取动作action）',self.recordlist)
            print(self.map.env_matrix())
            print ('----------------------------------------------------------------------------------------')
            #print ("press any key to continue");input()
        print ("game over!")
        print('是否到达终点：(0表示没，1表示到达)',self.arriveTarget)
        print('是否碰到障碍物：(0表示没，1表示碰到)', self.arriveObstacle)


class BasicGUIGame(BasicGame):
    """基本的GUI引擎, 使用pygame"""

    def __init__(self):
        super(BasicGUIGame, self).__init__()
        self.gui = pygame
        self.gui_init()

    def gui_init(self):
        self.gui_screen = self.gui.display.set_mode((800, 600), 0, 32)
        self.gui.display.set_caption("USV")
        self.gui_background = self.gui.image.load(
            'src/img/bg/seaSurface.png').convert()
        self.gui_friendly_ship = self.gui.image.load(
            'src/img/usv/friendly.png').convert_alpha()
        self.gui_enemy_ship = self.gui.image.load(
            'src/img/usv/enemy.png').convert_alpha()
        self.gui_target = self.gui.image.load(
            'src/img/target/blueTarget.png').convert_alpha()

    def update(self):
        '''地图里面为了符合人的习惯,定整个矩阵的左下角为(0,0), x轴负方向为0°, y轴正方形为90°
        和计算机矩阵左上角为(0,0)的习惯稍微不同. 而且pygame已经做过校正了, x就是水平方向,
        所以有(x1, y1)=(x, height-y)
        pygame定义,负角度顺时针转动,所以我们角度加个负'''

        x_unit = 800.0 / self.map.width
        y_unit = 600.0 / self.map.height

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        self.gui_screen.blit(self.gui_background, (0, 0))

        for ship in self.map.ships:
            ship.move()
            ship_x, ship_y = ship.coordinate()
            ship_w, ship_h = x_unit, y_unit
            if(ship.is_enemy):
                gui_enemy_ship = self.gui.transform.rotozoom(
                    self.gui_enemy_ship, -ship.direction, x_unit / 16)
                self.gui_screen.blit(
                    gui_enemy_ship, (ship_x * x_unit - ship_w / 2, (self.map.height - ship_y) * y_unit - ship_h / 2))
            else:
                gui_friendly_ship = self.gui.transform.rotozoom(
                    self.gui_friendly_ship, -ship.direction, x_unit / 16)
                self.gui_screen.blit(
                    gui_friendly_ship, (ship_x * x_unit - ship_w / 2, (self.map.height - ship_y) * y_unit - ship_h / 2))

        self.check_target()

        target_x, target_y = self.map.target_coordinate()
        target_w, target_h = x_unit, y_unit
        self.gui_screen.blit(
            self.gui.transform.rotozoom(self.gui_target, 0, x_unit / 16),
            (target_x * x_unit - target_w / 2, (self.map.height - target_y) * y_unit - target_h / 2))

        self.gui.display.update()

    def start(self):
        while not self.is_game_over():
            self.update()
            sleep(0.01)

        self.gui.display.set_caption("Game Over!")
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            self.gui.display.update()


class MyContinueGame(BasicGame):
    def __init__(self,obsmove):
        super(MyContinueGame, self).__init__()
        self.arriveTarget = 0
        self.arriveObstacle = 0
        self.arriveUnlegal = 0
        self.obsMoveBool = obsmove #默认false，障碍物不随机移动

    def update(self):
        #print('update_之前：输出map.env_matrix()函数的地图形式：：')

        #np.set_printoptions(threshold=np.nan)
        #print(self.map.env_matrix())



        # ax.set_xlim(0,100)
        # ax.set_ylim(100,0)
        
        # import time
        # start = time.time()
        # temptestoutput = self.map.env_matrix()
        # # print('输出值为1的位置：',np.argwhere(temptestoutput == 1))
        # # print('输出值为-1的位置：', np.argwhere(temptestoutput == -1))
        # # print('输出值为2的位置：', np.argwhere(temptestoutput == 2))
        # lines = []
        # for i in range(len(np.argwhere(temptestoutput == 1))):
        #     lines.append(ax.scatter(np.argwhere(temptestoutput == 1)[i][1], np.argwhere(temptestoutput == 1)[i][0], s=6, c='g', marker='.'))   #绿色
        
        # for i in range(len(np.argwhere(temptestoutput == -1))):
        #     lines.append(ax.scatter(np.argwhere(temptestoutput == -1)[i][1], np.argwhere(temptestoutput == -1)[i][0], s=60, c='r',marker='*'))  #红色终点
        # for i in range(len(np.argwhere(temptestoutput == 2))):
        #     lines.append(ax.scatter(np.argwhere(temptestoutput == 2)[i][1], np.argwhere(temptestoutput == 2)[i][0], s=60, c='b',marker='o'))    #蓝色USV
        # plt.pause(0.01)
        # for each in lines:
        #     each.remove()
        # plt.show()
        # print(time.time() - start)



        for ship in self.map.friendly_ships:
            if ship.getuid() == 0:
                ship.move()
            self.check_target()
            self.check_obstacle()
            self.check_legal()

        if self.obsMoveBool == False:
            pass
        else:
            #添加圆形障碍物的移动（需在其移动方法中添加对所随机移动的下一位置的合法性判断，若下一位置不合法则保持原位置）
            for obstacle in self.map.obs:
               obstacle.obsRandomMove()

        #print('update_之后：输出ma.env_matrix()函数的地图形式：：')
        #print(self.map.env_matrix())

    #USV是否到达终点
    def check_target(self):
        target_x, target_y = self.map.target_coordinate()
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()
            if ((ship_x - target_x)*(ship_x - target_x) + (ship_y - target_y)*(ship_y - target_y)) <= ((ship.radius + self.map.target_radius)*(ship.radius + self.map.target_radius)):
                self.is_target_safe = False
                self.arriveTarget = 1
                break

    #USV是否碰到障碍物
    def check_obstacle(self):
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()

            for obstacle in self.map.obs:
                if ((ship_x - obstacle.x)*(ship_x - obstacle.x) + (ship_y - obstacle.y)*(ship_y - obstacle.y)) <= ((ship.radius + obstacle.radius)*(ship.radius + obstacle.radius)):
                    self.is_target_safe = False
                    self.arriveObstacle = 1
                    break

    #USV是否越界
    def check_legal(self):
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()

            width, height = self.map.width,self.map.height
            if ( ship_x < ship.radius  or ship_y < ship.radius or ship_x > (width - 1 - ship.radius) or ship_y > (height - 1 - ship.radius)):
                self.is_target_safe = False
                self.arriveUnlegal = 1

    def is_game_over(self):
        return not self.is_target_safe

    def start(self):
        i = 0
        while not self.is_game_over():
            #print('game-start-update前的地图形式：');#print(self.map.str2())
            self.update()
            i += 1
            # print ('----------------------------------------------------------------------------------------')
            #print ("press any key to continue");input()
        # print ("game over!")
        # print('是否到达终点：(0表示没，1表示到达)',self.arriveTarget)
        # print('是否碰到障碍物：(0表示没，1表示碰到)', self.arriveObstacle)
        # print('是否走出区域：(0表示没，1表示走出去)', self.arriveUnlegal)
        print(i)

