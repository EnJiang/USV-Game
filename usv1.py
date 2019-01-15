# coding=utf-8

from collections import namedtuple
from math import sin, cos, pi, atan, sqrt
from implementation import *
import random


global DEBUGPrint
DEBUGPrint = False


class StaticUSV(object):
    """一个静态的USV类,move方法将会留空,这表示此类USV不可行动"""

    def __init__(self, uid, x, y, env):
        '''每艘USV的独立id,可以用来区分各舰'''
        self.id = uid
        '''env是指当前USV所在的环境,它指向当前游戏中这艘USV所在的Map类实例'''
        self.env = env
        self.x, self.y = x, y
        self.speed = 0.0
        self.angular_speed = 0.0
        self.direction = 0.0
        self.is_enemy = False

    def decision_algorithm(self):
        '''decision_algroithm是指导USV运动的方法,返回一个自定义的action字典'''
        pass

    def move(self):
        '''USV运动的主方法,根据action来调用其它辅助函数完成下一时刻USV位置的计算'''
        pass

    def is_decision_legal(self, decisionX, decisionY):
        '''判断USV决定要去的位置是否合法;在这个基本的函数里,所有舰艇不得走出地图范围,不得走到
        其它舰艇已经占用的位置;友军舰艇不得走到被保护的目标点.'''
        width, height = self.env.width, self.env.height
        if(decisionX < 0 or decisionY < 0 or decisionX > width - 1 or decisionY > height - 1):
            return False

        occupied = False
        for ship in self.env.ships:
            if(ship.id == self.id):
                continue
            shipX, shipY = ship.coordinate()
            if(shipX == decisionX and shipY == decisionY):
                occupied = True

        if(not self.is_enemy):
            tX, tY = self.env.target_coordinate()
            if(tX == decisionX and tY == decisionY):
                occupied = True

        if(occupied):
            return False

        return True

    def turn(self, clockwise):
        '''这一函数描绘本艘USV在一单位时间内如何改变自身方向,因此其作用是在顺时针或逆时针方向上
        增加当前USV角速度的绝对值(角度变化=角速度*1时间单位=角速度的绝对值)'''
        if(clockwise):
            self.direction += self.angular_speed
            if(self.direction >= 360):
                self.direction -= 360
        else:
            self.direction -= self.angular_speed
            if(self.direction < 0):
                self.direction += 360

    def coordinate(self):
        '''返回本USV的位置'''
        return self.x, self.y

    def set_as_enemy(self):
        '''将本USV定义为敌方(进攻方)'''
        self.is_enemy = True

    def set_as_friendly(self):
        '''将本USV定义为友军(防守方)'''
        self.is_enemy = False

    def set_as_target(self):
        self.is_target=True

class BasicPlaneUSV(StaticUSV):
    """基本平面USV, 这个USV可以在瞬间改变自己的角速度和速度, 转动后在对应方向上走动一帧时间*速度的距离"""

    def __init__(self, uid, x, y, env):
        super(BasicPlaneUSV, self).__init__(uid, x, y, env)
        self.action_class = Action = namedtuple("action", ['stay', 'clockwise', 'angular_speed', 'speed'])

    def decision_algorithm(self):
        '''这种USV的action对象有四个属性:1.stay,如果设为True,代表USV决定不行动,后面的参数被忽略;
        2.clockwise,转动方向是否是顺时针;3.angular_speed角速度;4.speed速度.
        如果stay参数为False,USV将会根据clockwise的指示转动angular_speed*t(一帧时间)度,然后前进当前的速度*t的距离'''
        Action = self.action_class
        example_action = Action(False, False, 20.0, 10.0)
        example_action1 = Action(False, False, 0.0, 0.0)
        raise Exception("请覆盖decision_algorithm方法!")

    def move(self):
        action = self.decision_algorithm()
        if(not action.stay):
            self.update_direction(action)
            self.update_speed(action)
            self.update_coordinate()

    def update_direction(self, action):
        self.angular_speed = action.angular_speed
        self.turn(action.clockwise)

    def update_speed(self, action):
        self.speed = action.speed

    def update_coordinate(self):    #x轴负方向是0度，y正方向是90度，所以如下计算
        self.x -= cos(pi * self.direction / 180) * self.speed
        self.y += sin(pi * self.direction / 180) * self.speed

class OneStepUSV(BasicPlaneUSV):
    """一个简单的USV类,在网格上它一次只能走动一步.每一时间单位,这种USV能够瞬时的改变自己的角速度,然后转动,最后向
    转动后的方向上移动一格."""

    def __init__(self, uid, x, y, env):
        super(OneStepUSV, self).__init__(uid, x, y, env)
        self.action_class = namedtuple("action", ['stay', 'clockwise', 'angular_speed'])
        self.speed = 1
        self.radius = 1

    def decision_algorithm(self):
        '''这种USV的action字典有三个参数:1.stay,如果设为True,代表USV决定不行动,后面的参数被忽略;
        2.clockwise,转动方向是否是顺时针;3.angular_speed角速度.
        如果stay参数为False,USV将会根据clockwise的指示转动angular_speed度,然后前进一步.注意由于
        此模型下angular_speed只能为90的倍数'''
        Action = self.action_class
        example_action = Action(False, False, 20.0)
        example_action1 = Action(False, False, 0.0)
        raise Exception("请覆盖decision_algorithm方法!")

    def move(self):
        action = self.decision_algorithm()
        '''print('USV中的action',action)'''
        if(not action.stay):
            self.update_direction(action)
            self.update_coordinate()


    def moverandom(self):
        Action = self.action_class
        action = Action(False, False, 90.0 * random.randint(0, 3))
        self.update_direction(action)
        self.update_coordinate_enemyship()


    def update_coordinate_enemyship(self):
        originalx, originaly = self.x, self.y
        beforetemp = self.env.env_matrix()

        if (self.direction == 0.0):  # 向上移动一格，将direct置为0度
            self.x -= self.speed
        elif (self.direction == 90.0):  # 向右移动一格，将direct置为90度
            self.y += self.speed
        elif (self.direction == 180.0):  # 向下移动一格，将direct置为180度
            self.x += self.speed
        elif (self.direction == 270.0):  # 向左移动一格，将direct置为270度
            self.y -= self.speed

        #越界处理
        if self.x <0 or self.x >self.env.width-1 or self.y <0 or self.y >self.env.height-1:
            if self.x <0: self.x = 0
            if self.x >self.env.width-1: self.x = self.env.width-1
            if self.y <0 : self.y = 0
            if self.y >self.env.height-1: self.y = self.env.height-1

        # 判断更新后的位置是否合法(是否越界或是该位置有值)
        if beforetemp[self.x][self.y] != 0:
            self.x, self.y = originalx, originaly


    def update_coordinate(self):     #左上角是（0，0）

        #print('USV中位置更新之前：',self.x,self.y)
        #print(self.direction)
        if(self.direction == 0.0):       #向上移动一格，将direct置为0度
            self.x -= self.speed
        elif(self.direction == 90.0):    #向右移动一格，将direct置为90度
            self.y += self.speed
        elif(self.direction == 180.0):   #向下移动一格，将direct置为180度
            self.x += self.speed
        elif(self.direction == 270.0):   #向左移动一格，将direct置为270度
            self.y -= self.speed
        else:
            raise Exception(
                "OneStepUSV的direction属性应该是正交角度,然而,得到了 %f 度" % self.direction)

class MyUSV(OneStepUSV):
    '''一个策略简单的USV,派生自OneStepUSV'''

    def __init__(self, uid, x, y, env):
        super(MyUSV, self).__init__(uid, x, y, env)


    def getlocation(self,a):
        #获取a的下标值
        #index=self.id.index
        if self.id==a:
            xx=self.x
            yy=self.y
        #xx=self.x[a]
        #yy=self.y[a]
        location=(xx,yy)
        
        return location



    def finda(self,policys):
        findamap = self.env.str2()  #A*方法的输入地图

        #findamap 与 diagram的图是镜像对称的，x与y是相反的
        diagram = GridWithWeights(len(findamap[0]),len(findamap))
        obstacles = []
        friends=[]
        for kk in range(len(findamap)):
            for hh in range(len(findamap[kk])):
                if findamap[kk][hh] == 'S':
                    obstacles.append((hh, kk))
                if findamap[kk][hh] == 'E':
                    endpoint = (hh, kk)
                if findamap[kk][hh] == '#':
                    startpoint = (hh, kk)

        diagram.walls = obstacles

        #按照uid寻找友军集合
        #id=self.id
        '''
        for i in self.id:
            row=self.x[i]
            col=self.y[i]
            if findamap[row][col] == 'S':
                friends.append(i)
        '''

        friends=[0,1,2,3]




        #按照policy策略 寻找路径
        for i in policys:
            a=policys[i]
            ss=self.getlocation(self,a[0])

            if a[1] in friends:
                came_from,cost_so_far=a_star_arround(diagram,start=ss, midpoint=self.getlocation(self,a[1]),goal=endpoint)
            #elif a[1] not in friends:
            else:
                came_from,cost_so_far=a_star_search(diagram,start=ss,goal=endpoint)


        #print('draw_grid')
        #draw_grid(diagram, weights=2,start=startpoint, goal=endpoint)
        #came_from, cost_so_far = a_star_search(diagram, start = startpoint, goal = endpoint)
        #draw_grid(diagram, width=1, path=reconstruct_path(came_from, start=startpoint, goal=endpoint))
        pathtm = reconstruct_path(came_from, start=startpoint, goal=endpoint)
        '''print(pathtm)'''
        firstnode = (pathtm[0][1],pathtm[0][0])
        secondnode = (pathtm[1][1],pathtm[1][0])



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

#  find target



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