#coding:utf-8


from game import MyContinueGame
from map_ import MyContinueObsMap
from usv import MyContinueUSV
from CircleObstacle import CircleObstacle



if __name__ == '__main__':
    '''开始游戏：
    map.py:                   class MyContinueObsMap(BasicMap):
    usv.py:                   class MyContinueUSV(BasicPlaneUSV):
    Game.py:                  class MyContinueGame(BasicGame):(增加障碍物是否随机移动开关:False-静态障碍物 True-随机移动障碍物)
    CircleObstacle.py:        圆形障碍物
    continue_obsmap_test.py:  主函数
    '''
    test_map = MyContinueObsMap(100, 100)
    test_map.set_target(30.0, 55.0)  #目标终点,(注：初始点的设定要合法--即在map缩小ship.radius的范围)

    test_friendly_ship = MyContinueUSV(uid=0, x=12.0, y=50.0, env=test_map)    #USV友艇起始点,(注：初始点的设定要合法--即在map缩小ship.radius的范围)
    test_friendly_ship.set_as_friendly()
    test_map.add_ship(test_friendly_ship)

    # 静态矩形障碍物区域（注：初始位置的设定要合法，即在map缩小obs.radius的范围）
    obs1 = CircleObstacle(uid=0, x=10.0, y=10.0, radius=1, env=test_map);test_map.addobs(obs1)
    obs2 = CircleObstacle(uid=1, x=40.0, y=40.0, radius=1, env=test_map);test_map.addobs(obs2)
    obs3 = CircleObstacle(uid=2, x=70.0, y=60.0, radius=1, env=test_map);test_map.addobs(obs3)

    print('game-start:初始地图：\n',test_map.env_matrix());print('\n')
    game = MyContinueGame(False)   #False表示障碍物不随机移动; True表示障碍物随机移动
    game.set_map(test_map)

    game.start()


