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

    def check_target(self):
        target_x, target_y = self.map.target_coordinate()
        for ship in self.map.enemy_ships:
            ship_x, ship_y = ship.coordinate()
            if(ship_x == target_x and ship_y == target_y):
                self.is_target_safe = False

    def isGameOver(self):
        return not self.is_target_safe

    def start(self):
        while not self.isGameOver():
            self.update()
            print self.map
            print '----------------------------------------------------------------------------------------'
            print "press any key to continue"
            raw_input()
        print "you lost!"


class BasicGUIGame(BasicGame):
    """基本的GUI引擎, 使用pygame"""

    def __init__(self):
        super(GUIGame, self).__init__()
        self.gui = pygame
        self.guiInit()

    def guiInit(self):
        self.gui_screen = self.gui.display.set_mode((800, 600), 0, 32)
        self.gui.display.set_caption("USV")
        self.guiBackground = self.gui.image.load(
            'src/img/bg/seaSurface.png').convert()
        self.gui_friendly_ship = self.gui.image.load(
            'src/img/usv/friendly.png').convert_alpha()
        self.gui_enemy_ship = self.gui.image.load(
            'src/img/usv/enemy.png').convert_alpha()
        self.gui_target = self.gui.image.load(
            'src/img/target/blueTarget.png').convert_alpha()

    def update(self):
        xUnit = 800.0 / self.map.width
        yUnit = 600.0 / self.map.height

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        self.gui_screen.blit(self.guiBackground, (0, 0))

        for ship in self.map.ships:
            ship.move()
            ship_x, ship_y = ship.coordinate()
            ship_w, ship_h = 32, 32
            if(ship.is_enemy):
                gui_enemy_ship = self.gui.transform.rotate(
                    self.gui_enemy_ship, -ship.direction)
                self.gui_screen.blit(
                    gui_enemy_ship, (ship_x * xUnit - ship_w / 2, ship_y * yUnit - ship_h / 2))
            else:
                gui_friendly_ship = self.gui.transform.rotate(
                    self.gui_friendly_ship, -ship.direction)
                self.gui_screen.blit(
                    gui_friendly_ship, (ship_x * xUnit - ship_w / 2, ship_y * yUnit - ship_h / 2))

        self.check_target()

        target_x, target_y = self.map.target_coordinate()
        target_w, target_h = 32, 32
        self.gui_screen.blit(
            self.gui_target, (target_x * xUnit - target_w / 2, target_y * yUnit - target_h / 2))

        self.gui.display.update()

    def start(self):
        while not self.isGameOver():
            self.update()
            sleep(0.5)

        self.gui.display.set_caption("Game Over!")
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            self.gui.display.update()
