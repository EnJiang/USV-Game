#coding:utf-8

import copy

class BasicMap(object):
  '''Map类描绘了当前整个海面上的状况
  在这个简单的字符界面中"~"代表空白海面,E代表敌方舰船,F代表友方舰船'''
  def __init__(self, width, height):
    super(BasicMap, self).__init__()
    self.width, self.height = width, height
    self.targetX = 0.0
    self.targetY = 0.0
    self.friendlyShips = []
    self.enemyShips = []
    self.ships = []

  def setTarget(self, x, y):
    self.targetX, self.targetY = x, y

  def targetCoordinate(self):
    return self.targetX, self.targetY

  def addShip(self, ship):
    if(ship.isEnemy):
      self.enemyShips.append(ship)
    else:
      self.friendlyShips.append(ship)
    self.ships.append(ship)

  def __str__(self):
    _str_ = ""

    matrix = [['~' for i in range(self.width)] for j in range(self.height)]
    matrix[self.targetY][self.targetX] = 'T'
    for ship in self.ships:
      shipX, shipY = ship.coordinate()
      if(ship.isEnemy):
        matrix[shipY][shipX] = 'E'
      else:
        matrix[shipY][shipX] = 'F'

    for line in matrix:
      for one in line:
        _str_ += one + ' '
      _str_ += '\n'

    return _str_