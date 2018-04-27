#coding:utf-8


from game import MyContinueGame
from map_ import MyContinueObsMap
from usv import MyContinueUSV, MyContinueDynamicsUSV
from CircleObstacle import CircleObstacle

import time


if __name__ == '__main__':

    #starttimetest = time.time()


    #开关控制switch
    dynamicsSwitch = True    #True表示加入动力学方程，False表示不加动力学方程（决策Action内容不同）
    envDisturbSwitch = False  #False表示无环境干扰，True表示有环境干扰(干扰产生的数值很小很小的，影响不大)
    obsMoveSwitch = False     #False表示障碍物不随机移动; True表示障碍物随机移动


    '''开始游戏'''
    test_map = MyContinueObsMap(100, 100)
    test_map.set_target(30.0, 30.0) #目标终点,(注：初始点的设定要合法--即在map缩小ship.radius的范围)
    #左上角(30.0, 30.0) 右上角(31.0, 59.0)  左下角(80.0, 30.0)   右下角(80.0, 60.0)
    #print (test_map.env_matrix())


    # USV友艇起始点,(注：初始点的设定要合法--即在map缩小ship.radius的范围)
    if dynamicsSwitch == True:
        test_friendly_ship = MyContinueDynamicsUSV(uid=0, x=52.0, y=50.0, env=test_map, envDisturb=envDisturbSwitch)    #envDisturb:False表示无环境干扰，True表示有环境干扰(干扰产生的数值很小很小0.1左右吧)
    else:
        test_friendly_ship = MyContinueUSV(uid=0, x=12.0, y=50.0, env=test_map)
    test_friendly_ship.set_as_friendly()
    test_map.add_ship(test_friendly_ship)


    # 静态矩形障碍物区域（注：初始位置的设定要合法，即在map缩小obs.radius的范围）
    obs1 = CircleObstacle(uid=0, x=10.0, y=10.0, radius=1, env=test_map);test_map.addobs(obs1)
    #obs2 = CircleObstacle(uid=1, x=40.0, y=40.0, radius=1, env=test_map);test_map.addobs(obs2)
    obs3 = CircleObstacle(uid=2, x=63.0, y=65.0, radius=1, env=test_map);test_map.addobs(obs3)


    print('game-start:初始地图：\n',test_map.env_matrix());print('\n')
    game = MyContinueGame(obsMoveSwitch)     #obsMoveSwitch: False表示障碍物不随机移动; True表示障碍物随机移动
    game.set_map(test_map)

    game.start()

    #print(time.time() - starttimetest)

