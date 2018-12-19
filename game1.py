# coding:utf-8

import pygame
from pygame.locals import *

from time import sleep


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
        print (self.map)

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
            print('----------------------------------------------------------------------------------------')
            print ("press any key to continue")
            input()
        print ("you lost!")


class MyGame(BasicGame):

    def __init__(self):
        super(MyGame, self).__init__()
        self.recordlist = []
        self.arriveTarget = 0
        self.arriveObstacle = 0
        self.arriveUnlegal = 0
        # self.obsMoveBool = False  # 默认false，障碍物不随机移动

    def update(self):

            global recenv
            global recaction
            for ship in self.map.enemy_ships:
                #if ship.uid == 0: recenv = ship.recordenv()
                if  ship.is_enemy: recenv = ship.recordenv()
                # if ship.uid == 0: recaction = ship.recordaction()
                if  ship.is_enemy: recaction = ship.recordaction()
                ship.move()
                self.recordlist.append((recenv, recaction))
                self.check_target()
                self.check_obstacle()
                self.check_legal()



    #USV是否到达终点
    def check_target(self):
        target_x, target_y = self.map.target_coordinate()
        for ship in self.map.enemy_ships:
            ship_x, ship_y = ship.coordinate()
            # if ((ship_x - target_x)*(ship_x - target_x) + (ship_y - target_y)*(ship_y - target_y)) <= ((ship.radius + self.map.target_radius)*(ship.radius + self.map.target_radius)):
            if (ship_x == target_x and ship_y == target_y):
                self.is_target_safe = False
                self.arriveTarget = 1
                break

    #USV是否碰到障碍物
    def check_obstacle(self):
        for ship in self.map.enemy_ships:
            ship_x, ship_y = ship.coordinate()

            # for obstacle in self.map.obs:
                # if ((ship_x - obstacle.x) * (ship_x - obstacle.x) + (ship_y - obstacle.y) * (ship_y - obstacle.y)) <= (
                #         (ship.radius + obstacle.radius) * (ship.radius + obstacle.radius)):
            for obstacle in self.map.friendly_ships:
                obstacle_x, obstacle_y = obstacle.coordinate()
                if (ship_x == obstacle_x and ship_y == obstacle_y):
                    self.is_target_safe = False
                    self.arriveObstacle = 1
                    break




    #USV是否越界
    def check_legal(self):
        for ship in self.map.enemy_ships:
            ship_x, ship_y = ship.coordinate()

            width, height = self.map.width,self.map.height
            # if ( ship_x < ship.radius  or ship_y < ship.radius or ship_x > (width - 1 - ship.radius) or ship_y > (height - 1 - ship.radius)):
            if (ship_x > (width - 1 ) or ship_y > ( height - 1 )):
                self.is_target_safe = False
                self.arriveUnlegal = 1

    def is_game_over(self):
        return not self.is_target_safe

    def start(self):
        i = 0
        print(self.map.env_matrix())
        print('----------------------------------------------------------------------------------------')
        while not self.is_game_over():
            #print('game-start-update前的地图形式：');#print(self.map.str2())
            self.update()
            i += 1
            print(self.map.env_matrix())
            print('----------------------------------------------------------------------------------------')
            print("press any key to continue")
            # raw_input()
            input()
            # print ('----------------------------------------------------------------------------------------')
            #print ("press any key to continue");input()
        print ("game over!")
        print('是否到达终点：(0表示没，1表示到达)',self.arriveTarget)
        print('是否碰到障碍物：(0表示没，1表示碰到)', self.arriveObstacle)
        print('是否走出区域：(0表示没，1表示走出去)', self.arriveUnlegal)
        print('game-update次数',i)
