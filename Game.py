# coding:utf-8

import pygame
from pygame.locals import *

from time import sleep


class BasicGame(object):
    """基本游戏逻辑"""

    def __init__(self):
        super(BasicGame, self).__init__()
        self.isTargetSafe = True

    def setMap(self, gameMap):
        self.map = gameMap

    def update(self):
        for ship in self.map.ships:
            ship.move()
        self.checkTarget()

    def checkTarget(self):
        targetX, targetY = self.map.targetCoordinate()
        for ship in self.map.enemyShips:
            shipX, shipY = ship.coordinate()
            if(shipX == targetX and shipY == targetY):
                self.isTargetSafe = False

    def isGameOver(self):
        return not self.isTargetSafe

    def start(self):
        while not self.isGameOver():
            self.update()
            print self.map
            print '----------------------------------------------------------------------------------------'
            print "press any key to continue"
            raw_input()
        print "you lost!"


class GUIGame(BasicGame):
    """docstring for GUIGame"""

    def __init__(self):
        super(GUIGame, self).__init__()
        self.gui = pygame
        self.guiInit()

    def guiInit(self):
        self.guiScreen = self.gui.display.set_mode((800, 600), 0, 32)
        self.gui.display.set_caption("USV")
        self.guiBackground = self.gui.image.load(
            'src/img/bg/seaSurface.png').convert()
        self.guiFriendlyShip = self.gui.image.load(
            'src/img/usv/friendly.png').convert_alpha()
        self.guiEnemyShip = self.gui.image.load(
            'src/img/usv/enemy.png').convert_alpha()
        self.guiTarget = self.gui.image.load(
            'src/img/target/blueTarget.png').convert_alpha()

    def update(self):
        xUnit = 800.0 / self.map.width
        yUnit = 600.0 / self.map.height

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        self.guiScreen.blit(self.guiBackground, (0, 0))

        for ship in self.map.ships:
            ship.move()
            shipX, shipY = ship.coordinate()
            shipW, shipH = 32, 32
            if(ship.isEnemy):
                guiEnemyShip = self.gui.transform.rotate(
                    self.guiEnemyShip, -ship.direction)
                self.guiScreen.blit(
                    guiEnemyShip, (shipX * xUnit - shipW / 2, shipY * yUnit - shipH / 2))
            else:
                guiFriendlyShip = self.gui.transform.rotate(
                    self.guiFriendlyShip, -ship.direction)
                self.guiScreen.blit(
                    guiFriendlyShip, (shipX * xUnit - shipW / 2, shipY * yUnit - shipH / 2))

        self.checkTarget()

        targetX, targetY = self.map.targetCoordinate()
        targetW, targetH = 32, 32
        self.guiScreen.blit(
            self.guiTarget, (targetX * xUnit - targetW / 2, targetY * yUnit - targetH / 2))

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
