#coding:utf-8


from game import BasicGame
from map_ import BasicMap
from usv import OneStepUSV
from implementation import *


# class MyUSV(BasicPlaneUSV):
#   '''一个策略简单的USV,派生自OneStepUSV'''
#   def __init__(self, uid, x, y, env):
#     super(MyUSV, self).__init__(uid, x, y, env)
#
#   def decision_algorithm(self):
#     Action = self.action_class
#     return Action(False, False, 2.0, 1)
#
# if __name__ == '__main__':
#     '''开始游戏'''
#     test_map = BasicMap(100, 100)
#     test_map.set_target(50, 50)
#     # print test_map
#
#     test_friendly_ship = MyUSV(uid=0,x=50, y=80, env=test_map)
#     test_friendly_ship.set_as_friendly()
#     test_map.add_ship(test_friendly_ship)
#
#
#     game = BasicGUIGame()
#     game.set_map(test_map)
#     game.start()


class MyUSV(OneStepUSV):
    '''一个策略简单的USV,派生自OneStepUSV'''

    def __init__(self, uid, x, y, env):
        super(MyUSV, self).__init__(uid, x, y, env)


    def finda(self):
        findamap = self.env.str2()  #A*方法的输入地图

        #A*方法的过程求解及结果
        #print('self.env.str2()',self.env.str2())
        #print(self.env.width)；print(self.env.height)

        #findamap 与 diagram的图是镜像对称的，x与y是相反的
        diagram = GridWithWeights(len(findamap[0]),len(findamap))
        obstacles = []
        for kk in range(len(findamap)):
            for hh in range(len(findamap[kk])):
                if findamap[kk][hh] == 'S':
                    startpoint = (hh,kk)
                if findamap[kk][hh] == 'E':
                    endpoint = (hh,kk)
                if findamap[kk][hh] == '#':
                    obstacles.append((hh,kk))

        diagram.walls = obstacles
        #print('draw_grid')
        #draw_grid(diagram, weights=2,start=startpoint, goal=endpoint)
        came_from, cost_so_far = a_star_search(diagram, start = startpoint, goal = endpoint)
        #draw_grid(diagram, width=1, path=reconstruct_path(came_from, start=startpoint, goal=endpoint))
        pathtm = reconstruct_path(came_from, start=startpoint, goal=endpoint)
        '''print(pathtm)'''
        #print(pathtm[0]);print(pathtm[1]);print(pathtm[1][1])
        firstnode = (pathtm[0][1],pathtm[0][0])
        secondnode = (pathtm[1][1],pathtm[1][0])
        #print(firstnode,secondnode)



        # 这里的地图形式是：左上角是（0，0），右下角是（n,n）,,所以下面上下左右如下描述：：
        if secondnode[1] - firstnode[1] == 0 and secondnode[0] - firstnode[0] == -1:
            string = 'up'
        elif secondnode[1] - firstnode[1] == -1 and secondnode[0] - firstnode[0] == 0:
            string = 'left'
        elif secondnode[1] - firstnode[1] == 0 and secondnode[0] - firstnode[0] == 1:
            string = 'down'
        else:
            string = 'right'

        '''print('action是上下左右中的',string)'''
        #print('USV当前位置：',self.x,self.y)


        if (string =='left'):
            direct = 270.0
        elif(string =='down'):
            direct = 180.0
        elif(string =='right'):
            direct = 90.0
        else:
            direct = 0.0


        Action = self.action_class

        # 这里要根据A*算法进行修改，只获取走一步，
        next_action = Action(False, True, direct)
        # print('使用A*算法的下一步：',next_action)

        return next_action


    def decision_algorithm(self):
        act = self.finda()
        return act


    def update_direction(self, action):
        #self.angular_speed = action.angular_speed
        #self.turn(action.clockwise)
        self.direction = action.angular_speed


    def recordenv(self):
        curenv = self.env.env_matrix()
        return curenv

    def recordaction(self):
        curaction = self.decision_algorithm()
        return curaction

class MyGame(BasicGame):
    def __init__(self):
        super(MyGame, self).__init__()
        self.recordlist = []
        self.arriveTarget = 0
        self.arriveObstacle = 0


    # def update(self):
    #     print('update_之前：输出ma.str2()函数的地图形式：：')
    #     print(self.map.str2())
    #     for ship in self.map.friendly_ships:
    #         ship.move()
    #         #print('船体位置：',ship.coordinate())
    #     self.check_target()
    #     #print (self.map)
    #     print('update_之后：输出ma.str2()函数的地图形式：：')
    #     print(self.map.str2())

    def update(self):
        # print('update_之前：输出ma.str2()函数的地图形式：：')
        # print(self.map.str2())
        try:
            for ship in self.map.friendly_ships:
                #if ship.uid == 0: recenv = ship.recordenv()
                if not ship.is_enemy: recenv = ship.recordenv()
                # if ship.uid == 0: recaction = ship.recordaction()
                if not ship.is_enemy: recaction = ship.recordaction()
                ship.move()
                self.recordlist.append((recenv, recaction))
                self.check_target()
                self.check_obstacle()
        except IndexError as e:
                self.is_target_safe = False
                self.arriveObstacle = True

        # print('update_之后：输出ma.str2()函数的地图形式：：')
        # print(self.map.str2())


    def check_target(self):
        target_x, target_y = self.map.target_coordinate()
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()
            if(ship_x == target_x and ship_y == target_y):
                self.is_target_safe = True
                self.arriveTarget = True


    def check_obstacle(self):
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()
            for obstacle in self.map.enemy_ships:
                obstacle_x, obstacle_y = obstacle.coordinate()
                if(ship_x == obstacle_x and ship_y == obstacle_y):
                    self.is_target_safe = False
                    self.arriveObstacle = True


    def is_game_over(self):
        return not self.is_target_safe


    def start(self):
        while not self.is_game_over():
            #print('game-start-update前的地图形式：')
            #print(self.map.str2())
            self.update()
            # print('\n决策链（当前环境env + 采取动作action）',self.recordlist)
            print(self.map.env_matrix())
            print ('----------------------------------------------------------------------------------------')
            print ("press any key to continue")
            #raw_input()
            input()
        print ("game over!")
        print('是否到达终点：(0表示没，1表示到达)',self.arriveTarget)
        print('是否碰到障碍物：(0表示没，1表示碰到)', self.arriveObstacle)




if __name__ == '__main__':
    '''开始游戏'''
    test_map = BasicMap(10, 10)
    test_map.set_target(9, 9)
    #print (test_map.str2())


    test_friendly_ship = MyUSV(uid=0, x=0, y=0, env=test_map)    #USV友艇起始点
    test_friendly_ship.set_as_friendly()
    test_map.add_ship(test_friendly_ship)

    # 静态敌船--障碍物区域
    test_enemy_ship1 = MyUSV(uid=1, x=2, y=2, env=test_map);test_enemy_ship1.set_as_enemy();test_map.add_ship(test_enemy_ship1)
    test_enemy_ship2 = MyUSV(uid=2, x=3, y=2, env=test_map);test_enemy_ship2.set_as_enemy();test_map.add_ship(test_enemy_ship2)
    test_enemy_ship3 = MyUSV(uid=3, x=4, y=2, env=test_map);test_enemy_ship3.set_as_enemy();test_map.add_ship(test_enemy_ship3)
    test_enemy_ship4 = MyUSV(uid=4, x=2, y=5, env=test_map);test_enemy_ship4.set_as_enemy();test_map.add_ship(test_enemy_ship4)
    test_enemy_ship5 = MyUSV(uid=5, x=2, y=6, env=test_map);test_enemy_ship5.set_as_enemy();test_map.add_ship(test_enemy_ship5)

    test_enemy_ship6 = MyUSV(uid=6, x=2, y=7, env=test_map);test_enemy_ship6.set_as_enemy();test_map.add_ship(test_enemy_ship6)
    test_enemy_ship7 = MyUSV(uid=7, x=3, y=5, env=test_map);test_enemy_ship7.set_as_enemy();test_map.add_ship(test_enemy_ship7)
    test_enemy_ship8 = MyUSV(uid=8, x=3, y=6, env=test_map);test_enemy_ship8.set_as_enemy();test_map.add_ship(test_enemy_ship8)
    test_enemy_ship9 = MyUSV(uid=9, x=4, y=3, env=test_map);test_enemy_ship9.set_as_enemy();test_map.add_ship(test_enemy_ship9)
    test_enemy_ship10 = MyUSV(uid=10, x=5, y=6, env=test_map);test_enemy_ship10.set_as_enemy();test_map.add_ship(test_enemy_ship10)

    test_enemy_ship11 = MyUSV(uid=11, x=6, y=5, env=test_map);test_enemy_ship11.set_as_enemy();test_map.add_ship(test_enemy_ship11)
    test_enemy_ship12 = MyUSV(uid=12, x=7, y=5, env=test_map);test_enemy_ship12.set_as_enemy();test_map.add_ship(test_enemy_ship12)
    test_enemy_ship13 = MyUSV(uid=13, x=7, y=6, env=test_map);test_enemy_ship13.set_as_enemy();test_map.add_ship(test_enemy_ship13)
    test_enemy_ship14 = MyUSV(uid=14, x=7, y=7, env=test_map);test_enemy_ship14.set_as_enemy();test_map.add_ship(test_enemy_ship14)
    test_enemy_ship15 = MyUSV(uid=15, x=8, y=5, env=test_map);test_enemy_ship15.set_as_enemy();test_map.add_ship(test_enemy_ship15)

    print('game-start:初始地图：',test_map.str2());print('\n')
    game = MyGame()
    game.set_map(test_map)

    game.start()
