#coding:utf-8

from game import BasicGUIGame
from map_ import BasicMap
from usv import BasicPlaneUSV

class MyUSV(BasicPlaneUSV):
  '''一个策略简单的USV,派生自OneStepUSV'''
  def __init__(self, uid, x, y, env):
    super(MyUSV, self).__init__(uid, x, y, env)

  def decision_algorithm(self):
    Action = self.action_class
    return Action(False, False, 2.0, 1)

if __name__ == '__main__':
    '''开始游戏'''
    test_map = BasicMap(100, 100)
    test_map.set_target(50, 50)
    # print test_map

    test_friendly_ship = MyUSV(uid=0,x=50, y=80, env=test_map)
    test_friendly_ship.set_as_friendly()
    test_map.add_ship(test_friendly_ship)

    game = BasicGUIGame()
    game.set_map(test_map)
    game.start()
