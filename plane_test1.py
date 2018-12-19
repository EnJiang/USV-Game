#coding:utf-8


from game1 import BasicGame
from map_1 import BasicMap
from usv1 import OneStepUSV
from implementation import *

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
        global startpoint
        global endpoint
        diagram = GridWithWeights(len(findamap[0]),len(findamap))
        obstacles = []
        for kk in range(len(findamap)):
            for hh in range(len(findamap[kk])):
                if findamap[kk][hh] == 'S':
                    obstacles.append((hh, kk))

                if findamap[kk][hh] == 'E':
                    endpoint = (hh,kk)
                if findamap[kk][hh] == '#':
                    startpoint = (hh, kk)

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
        self.arriveUnlegal = 0
        # self.obsMoveBool = False  # 默认false，障碍物不随机移动

    def update(self):

            global recenv
            global recaction
            for ship in self.map.enemy_ships:
                #if ship.uid == 0: recenv = ship.recordenv()
                if  ship.is_enemy: recenv = ship.recordenv()
                # if ship.uid == 0: recaction = ship.recordaction()
                if  ship.is_enemy: recaction = ship.recordaction()
                ship.move()
                self.recordlist.append((recenv, recaction))
                self.check_target()
                self.check_obstacle()
                self.check_legal()



    #USV是否到达终点
    def check_target(self):
        target_x, target_y = self.map.target_coordinate()
        for ship in self.map.enemy_ships:
            ship_x, ship_y = ship.coordinate()
            # if ((ship_x - target_x)*(ship_x - target_x) + (ship_y - target_y)*(ship_y - target_y)) <= ((ship.radius + self.map.target_radius)*(ship.radius + self.map.target_radius)):
            if (ship_x == target_x and ship_y == target_y):
                self.is_target_safe = False
                self.arriveTarget = 1
                break

    #USV是否碰到障碍物
    def check_obstacle(self):
        for ship in self.map.enemy_ships:
            ship_x, ship_y = ship.coordinate()

            # for obstacle in self.map.obs:
                # if ((ship_x - obstacle.x) * (ship_x - obstacle.x) + (ship_y - obstacle.y) * (ship_y - obstacle.y)) <= (
                #         (ship.radius + obstacle.radius) * (ship.radius + obstacle.radius)):
            for obstacle in self.map.friendly_ships:
                obstacle_x, obstacle_y = obstacle.coordinate()
                if (ship_x == obstacle_x and ship_y == obstacle_y):
                    self.is_target_safe = False
                    self.arriveObstacle = 1
                    break

    #USV是否越界
    def check_legal(self):
        for ship in self.map.enemy_ships:
            ship_x, ship_y = ship.coordinate()

            width, height = self.map.width,self.map.height
            # if ( ship_x < ship.radius  or ship_y < ship.radius or ship_x > (width - 1 - ship.radius) or ship_y > (height - 1 - ship.radius)):
            if (ship_x > (width - 1 ) or ship_y > ( height - 1 )):
                self.is_target_safe = False
                self.arriveUnlegal = 1

    def is_game_over(self):
        return not self.is_target_safe

    def start(self):
        i = 0
        print(self.map.env_matrix())
        print('----------------------------------------------------------------------------------------')
        while not self.is_game_over():
            #print('game-start-update前的地图形式：');#print(self.map.str2())
            self.update()
            i += 1
            print(self.map.env_matrix())
            print('----------------------------------------------------------------------------------------')
            print("press any key to continue")
            # raw_input()
            input()
            # print ('----------------------------------------------------------------------------------------')
            #print ("press any key to continue");input()
        print ("game over!")
        print('是否到达终点：(0表示没，1表示到达)',self.arriveTarget)
        print('是否碰到障碍物：(0表示没，1表示碰到)', self.arriveObstacle)
        print('是否走出区域：(0表示没，1表示走出去)', self.arriveUnlegal)
        print('game-update次数',i)



if __name__ == '__main__':
    '''开始游戏'''

    test_map = BasicMap(10, 10)
    test_map.set_target(5, 5)

    # 防御艇
    test_friendly_ship1 = MyUSV(uid=0,x=3,y=5, env=test_map);test_friendly_ship1.set_as_friendly();test_map.add_ship(test_friendly_ship1)
    test_friendly_ship2 = MyUSV(uid=1, x=5, y=3, env=test_map);test_friendly_ship2.set_as_friendly();test_map.add_ship(test_friendly_ship2)
    test_friendly_ship3 = MyUSV(uid=2, x=5, y=7, env=test_map);test_friendly_ship3.set_as_friendly();test_map.add_ship(test_friendly_ship3)
    test_friendly_ship4 = MyUSV(uid=3, x=7, y=5, env=test_map);test_friendly_ship4.set_as_friendly();test_map.add_ship(test_friendly_ship4)

    # 攻击艇
    test_enemy_ship1 = MyUSV(uid=4, x=1, y=1, env=test_map);test_enemy_ship1.set_as_enemy();test_map.add_ship(test_enemy_ship1)
    test_enemy_ship2 = MyUSV(uid=5, x=1, y=4, env=test_map);test_enemy_ship2.set_as_enemy();test_map.add_ship(test_enemy_ship2)
    test_enemy_ship3 = MyUSV(uid=6, x=5, y=0, env=test_map);test_enemy_ship3.set_as_enemy();test_map.add_ship(test_enemy_ship3)
    test_enemy_ship4 = MyUSV(uid=7, x=9, y=1, env=test_map);test_enemy_ship4.set_as_enemy();test_map.add_ship(test_enemy_ship4)
    test_enemy_ship5 = MyUSV(uid=8, x=8, y=9, env=test_map);test_enemy_ship5.set_as_enemy();test_map.add_ship(test_enemy_ship5)
    test_enemy_ship6 = MyUSV(uid=9, x=5, y=9, env=test_map);test_enemy_ship6.set_as_enemy();test_map.add_ship(test_enemy_ship6)
    test_enemy_ship7 = MyUSV(uid=10,x=2, y=8, env=test_map);test_enemy_ship7.set_as_enemy();test_map.add_ship(test_enemy_ship7)


    print('game-start:初始地图：',test_map.str2());print('\n')

    game = MyGame()
    game.set_map(test_map)

    game.start()
