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
        print self.map

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
            print '----------------------------------------------------------------------------------------'
            print "press any key to continue"
            raw_input()
        print "you lost!"


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
