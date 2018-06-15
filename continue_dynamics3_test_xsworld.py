#coding:utf-8


from game import BasicPyGame, MyContinueGame, PyGameXSWorld, MyContinueGameModify
from map_ import MyContinueObsMap
from usv import MyContinueUSV, MyContinueDynamicsUSV3XSWorld
from CircleObstacle import CircleObstacle

import time



if __name__ == '__main__':

    starttimetest = time.time()


    #开关控制switch
    dynamicsSwitch = True    #True表示加入动力学方程，False表示不加动力学方程（决策Action内容不同）
    envDisturbSwitch = False  #False表示无环境干扰，True表示有环境干扰(干扰产生的数值很小很小的，影响不大)
    obsMoveSwitch = False     #False表示障碍物不随机移动; True表示障碍物随机移动


    FTListValue = []   #[]为空默认表示：使用路径导引算法计算F，T然后更新， 不为空表示给定F，T列表，可视化观察


    '''开始游戏'''
    test_map = MyContinueObsMap(3.0, 3.0)
    test_map.set_target(0.50,2.50)
    test_map.set_target_radius(0.1)


    # USV友艇起始点,(注：初始点的设定要合法--即在map缩小ship.radius的范围)
    if dynamicsSwitch == True:
        test_friendly_ship = MyContinueDynamicsUSV3XSWorld(uid=0, x=2.50, y=0.50, env=test_map, envDisturb=envDisturbSwitch, FTListValue = FTListValue)
        #envDisturb:False表示无环境干扰，True表示有环境干扰(干扰产生的数值很小很小0.1左右吧)

        test_friendly_ship.set_usv_radius(0.1)
        test_friendly_ship.set_init_usv_pos(2.50, 0.50)

    else:
        test_friendly_ship = MyContinueUSV(uid=0, x=2.50, y=0.50, env=test_map)

    test_friendly_ship.set_as_friendly()
    test_map.add_ship(test_friendly_ship)


    # 静态矩形障碍物区域（注：初始位置的设定要合法，即在map缩小obs.radius的范围）
    obs1 = CircleObstacle(uid=0, x=0.85, y=1.00, radius=0.1, env=test_map);test_map.addobs(obs1)
    obs2 = CircleObstacle(uid=1, x=1.50, y=0.50, radius=0.1, env=test_map);test_map.addobs(obs2)
    obs3 = CircleObstacle(uid=2, x=1.60, y=1.40, radius=0.2, env=test_map);test_map.addobs(obs3)
    obs4 = CircleObstacle(uid=3, x=1.10, y=1.80, radius=0.1, env=test_map);test_map.addobs(obs4)
    obs5 = CircleObstacle(uid=3, x=0.30, y=1.60, radius=0.2, env=test_map);test_map.addobs(obs5)

    obs6 = CircleObstacle(uid=4, x=2.00, y=1.00, radius=0.1, env=test_map);test_map.addobs(obs6)
    obs7 = CircleObstacle(uid=5, x=2.30, y=1.80, radius=0.2, env=test_map);test_map.addobs(obs7)
    obs8 = CircleObstacle(uid=6, x=1.80, y=2.40, radius=0.2, env=test_map);test_map.addobs(obs8)
    obs9 = CircleObstacle(uid=6, x=1.20, y=2.60, radius=0.1, env=test_map);test_map.addobs(obs9)


    if len(FTListValue) == 0 :
        game = MyContinueGameModify(obsMoveSwitch)     #obsMoveSwitch: False表示障碍物不随机移动; True表示障碍物随机移动
        # game = PyGameXSWorld(obsMoveSwitch)  # obsMoveSwitch: False表示障碍物不随机移动; True表示障碍物随机移动
    else:
        game = BasicPyGame(obsMoveSwitch)
    game.set_map(test_map)

    game.start()

    print(time.time() - starttimetest)





#MyContinueDynamicsUSV3SmallWorld是在10*10地图上的
# 可视化：PyGameXSWorld  不可视化：MyContinueGameModify

#测试加入附加质量、附加科氏力、非线形阻尼（柯老师提供的参数）