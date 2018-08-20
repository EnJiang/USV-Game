# -*- coding:UTF-8 -*-

from map_ import MyContinueObsMap
from usv import MyContinueUSV_SmallMap
from CircleObstacle import CircleObstacle

from game import *

if __name__ == '__main__':
    '''开始游戏：
    map.py:                   class MyContinueObsMap(BasicMap):
    usv.py:                   class MyContinueUSV(BasicPlaneUSV):
    Game.py:                  class MyContinueGame(BasicGame):(增加障碍物是否随机移动开关:False-静态障碍物 True-随机移动障碍物)
    CircleObstacle.py:        圆形障碍物
    continue_obsmap_test.py:  主函数
    '''
    test_map = MyContinueObsMap(3.0, 3.0)
    test_map.set_target(0.50, 2.50)  #目标终点,(注：初始点的设定要合法--即在map缩小ship.radius的范围)
    test_map.set_target_radius(0.1)


    test_friendly_ship = MyContinueUSV_SmallMap(uid=0, x=2.50, y=0.50, env=test_map)    #USV友艇起始点,(注：初始点的设定要合法--即在map缩小ship.radius的范围)
    test_friendly_ship.set_as_friendly()
    test_map.add_ship(test_friendly_ship)
    test_friendly_ship.set_usv_radius(0.1)
    test_friendly_ship.set_usv_speed(0.1)


    # 静态矩形障碍物区域（注：初始位置的设定要合法，即在map缩小obs.radius的范围）
    obs1 = CircleObstacle(uid=0, x=0.85, y=1.00, radius=0.1, env=test_map);test_map.addobs(obs1)
    obs2 = CircleObstacle(uid=1, x=2.30, y=2.60, radius=0.1, env=test_map);test_map.addobs(obs2)



    game = CoutinuePyGame(False)    #False表示障碍物不随机移动; True表示障碍物随机移动
    # game = CoutinueNoPyGame(False)


    game.set_map(test_map)

    game.start()



