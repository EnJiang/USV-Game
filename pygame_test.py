#coding:utf-8

from game import BasicGUIGame
from map_ import BasicMap
from usv import OneStepUSV

class MyUSV(OneStepUSV):
  '''一个策略简单的USV,派生自OneStepUSV'''
  def __init__(self, uid, x, y, env):
    super(MyUSV, self).__init__(uid, x, y, env)

  def decision_algorithm(self):
    if(self.is_enemy):
      return self.attack_decision_algorithm()
    else:
      return self.protection_decision_algorithm()

  def euclidean_distance(self, x1, y1, x2, y2):
      '''计算两点的欧式距离'''
      return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

  def attack_decision_algorithm(self):
    '''进攻方策略:在上下左右四个格子中,选择离目标最近的那个格子,如果出现相等就随机选一个;
    如果发现目标格子被其它舰艇占用,选择次近的格子;如果全部被占用,保持不动
    (这不见得是什么高明的策略,即是是防守方保持静止,也很有可能使进攻方进入死循环)'''
    target_x, target_y = self.env.target_coordinate()
    distance_up = self.euclidean_distance(target_x, target_y, self.x, (self.y + 1))
    distance_down = self.euclidean_distance(target_x, target_y, self.x, (self.y - 1))
    distance_left = self.euclidean_distance(target_x, target_y, (self.x - 1), self.y)
    distance_right = self.euclidean_distance(target_x, target_y, (self.x + 1), self.y)
    distances = [distance_up, distance_down, distance_left, distance_right]
    distances.sort()

    final_decision = {"stay":True, "clockwise": True, "angular_speed": 0.0}

    for distance in distances:
      if distance==distance_up:
        decision_x, decision_y = self.x, self.y + 1
        angular_to_be = 90.0
      elif distance==distance_down:
        decision_x, decision_y = self.x, self.y - 1
        angular_to_be = 270.0
      elif distance==distance_left:
        decision_x, decision_y = self.x - 1, self.y
        angular_to_be = 0.0
      elif distance==distance_right:
        decision_x, decision_y = self.x + 1, self.y
        angular_to_be = 180.0

      if(self.is_decision_legal(decision_x, decision_y)):
          final_decision["stay"] = False
          final_decision["clockwise"] = angular_to_be - self.direction > 0
          final_decision["angular_speed"] = abs(angular_to_be - self.direction)
          break

    return self.action_class(final_decision["stay"], final_decision["clockwise"], final_decision["angular_speed"])

  def protection_decision_algorithm(self):
    '''试图出现在进攻方想要出现的那一个格子上,更具体的说,以进攻方的目标格子为"目标",实行进攻方的策略.
    这个测试游戏里面敌舰只有一艘,所以敌人想要去的位置是确定的,如果敌人选择不动,以敌人的位置为目标位置'''

    '''得到敌人的目标位置'''
    enemy = self.env.enemy_ships[0]
    enemy_action = enemy.attack_decision_algorithm()
    if(enemy_action.stay):
      target_x, target_y = enemy.coordinate()
    else:
      if(enemy_action.clockwise):
        enemyDirection = enemy.direction + enemy_action.angular_speed
        if(enemyDirection >= 360):
          enemyDirection -= 360
      else:
        enemyDirection = enemy.direction - enemy_action.angular_speed
        if(enemyDirection < 0):
          enemyDirection += 360

      enemy_x, enemy_y = enemy.coordinate()
      if(enemyDirection==0.0):
        target_x, target_y = enemy_x - 1, enemy_y
      if(enemyDirection==90.0):
        target_x, target_y = enemy_x, enemy_y + 1
      if(enemyDirection==180.0):
        target_x, target_y = enemy_x + 1, enemy_y
      if(enemyDirection==270):
        target_x, target_y = enemy_x, enemy_y - 1

    '''下面套用attack_decision_algorithm'''
    distance_up = self.euclidean_distance(target_x, target_y, self.x, (self.y + 1))
    distance_down = self.euclidean_distance(target_x, target_y, self.x, (self.y - 1))
    distance_left = self.euclidean_distance(target_x, target_y, (self.x - 1), self.y)
    distance_right = self.euclidean_distance(target_x, target_y, (self.x + 1), self.y)
    distances = [distance_up, distance_down, distance_left, distance_right]
    distances.sort()

    final_decision = {"stay":True, "clockwise": True, "angular_speed": 0.0}

    for distance in distances:
      if distance==distance_up:
        decision_x, decision_y = self.x, self.y + 1
        angular_to_be = 90.0
      elif distance==distance_down:
        decision_x, decision_y = self.x, self.y - 1
        angular_to_be = 270.0
      elif distance==distance_left:
        decision_x, decision_y = self.x - 1, self.y
        angular_to_be = 0.0
      elif distance==distance_right:
        decision_x, decision_y = self.x + 1, self.y
        angular_to_be = 180.0

      if(self.is_decision_legal(decision_x, decision_y)):
          final_decision["stay"] = False
          final_decision["clockwise"] = angular_to_be - self.direction > 0
          final_decision["angular_speed"] = abs(angular_to_be - self.direction)
          break

    return self.action_class(final_decision["stay"], final_decision["clockwise"], final_decision["angular_speed"])


if __name__ == '__main__':
    '''开始游戏'''
    test_map = BasicMap(20,15)
    test_map.set_target(4,4)
    # print test_map

    test_friendly_ship = MyUSV(uid=0,x=5,y=5,env=test_map)
    test_friendly_ship.set_as_friendly()
    test_map.add_ship(test_friendly_ship)
    test_friendly_ship1 = MyUSV(uid=1,x=4,y=5,env=test_map)
    test_friendly_ship1.set_as_friendly()
    test_map.add_ship(test_friendly_ship1)
    test_friendly_ship2 = MyUSV(uid=2,x=5,y=4,env=test_map)
    test_friendly_ship2.set_as_friendly()
    test_map.add_ship(test_friendly_ship2)
    test_friendly_ship3 = MyUSV(uid=3,x=6,y=4,env=test_map)
    test_friendly_ship3.set_as_friendly()
    test_map.add_ship(test_friendly_ship3)
    test_friendly_ship4 = MyUSV(uid=4,x=5,y=6,env=test_map)
    test_friendly_ship4.set_as_friendly()
    test_map.add_ship(test_friendly_ship4)
    test_friendly_ship5 = MyUSV(uid=5,x=7,y=4,env=test_map)
    test_friendly_ship5.set_as_friendly()
    test_map.add_ship(test_friendly_ship5)
    test_friendly_ship6 = MyUSV(uid=6,x=7,y=5,env=test_map)
    test_friendly_ship6.set_as_friendly()
    test_map.add_ship(test_friendly_ship6)
    test_friendly_ship7 = MyUSV(uid=7,x=7,y=6,env=test_map)
    test_friendly_ship7.set_as_friendly()
    test_map.add_ship(test_friendly_ship7)

    test_enemy_ship = MyUSV(uid=8,x=10,y=10,env=test_map)
    test_enemy_ship.set_as_enemy()
    test_map.add_ship(test_enemy_ship)
    # print test_map

    game = BasicGUIGame()
    game.set_map(test_map)
    game.start()
