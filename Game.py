#coding:utf-8

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
      if(shipX==targetX and shipY==targetY):
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