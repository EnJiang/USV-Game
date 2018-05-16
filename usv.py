# coding=utf-8

from collections import namedtuple
from math import sin, cos, pi, atan, sqrt
from implementation import *
import random
import time


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
        example_action1 = Action(True, False, 0.0, 0.0)
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

    def decision_algorithm(self):
        '''这种USV的action字典有三个参数:1.stay,如果设为True,代表USV决定不行动,后面的参数被忽略;
        2.clockwise,转动方向是否是顺时针;3.angular_speed角速度.
        如果stay参数为False,USV将会根据clockwise的指示转动angular_speed度,然后前进一步.注意由于
        此模型下angular_speed只能为90的倍数'''
        Action = self.action_class
        example_action = Action(False, False, 20.0)
        example_action1 = Action(True, False, 0.0)
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


    def finda(self):
        findamap = self.env.str2()  #A*方法的输入地图

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





class MyContinueUSV(BasicPlaneUSV):
    '''一个策略简单的USV,派生自BasicObsUSV,用于连续环境下USV，
        认为USV可瞬间达到下一次角速度且按照speed走一帧时间的距离
    '''

    def __init__(self, uid, x, y, env):
        super(MyContinueUSV, self).__init__(uid, x, y, env)
        self.action_class = Action = namedtuple("action", ['stay', 'clockwise', 'angular_speed', 'speed'])
        self.speed = 1
        self.radius = 1


    def getuid(self):
        return self.id



    def update_coordinate(self):    #x轴负方向是0度，y正方向是90度，(按照左上角是0，0更新坐标),所以如下计算
        self.y -= cos(pi * self.direction / 180) * self.speed
        self.x -= sin(pi * self.direction / 180) * self.speed



    def decision_algorithm(self):
        '''这种USV的action对象有四个属性:
        1.stay,如果设为True,代表USV决定不行动,后面的参数被忽略;
        2.clockwise,转动方向是否是顺时针;
        3.angular_speed角速度;
        4.speed速度.
        如果stay参数为False,USV将会根据clockwise的指示转动angular_speed*t(一帧时间)度,然后前进当前的速度*t的距离'''
        #Action = self.action_class
        #act = Action(False, False, 2.0, 1.0)

        #act = self.pathGuide()
        act = self.pathGuide2()
        return act





    #起点朝向终点进行导引-方法1
    def pathGuide(self):
        #difference_angular = self.next_angular_guide2() - self.direction
        difference_angular = self.next_angular_guide3((self.x, self.y), self.env.target_coordinate()) - self.direction
        #print('当前direction,当前difference_angular：',self.direction,difference_angular)
        Action = self.action_class
        act = Action(False, True, difference_angular, self.speed)
        return act


    def next_angular_guide(self):
        target_x, target_y = self.env.target_coordinate()
        #print('USV&终点', self.x, self.y, target_x, target_y)

        # USV与终点在同一垂直线上：(USV最左侧值与终点最左侧值的差值是否在USV的2倍半径范围内)
        if abs(round(self.y, 0) - round(target_y, 0)) <= self.radius * 2:
            if self.x < target_x:
                angle = 270
                #print('斜率对应的角度angle-整数1:',angle)
                return angle
            else:
                angle = 90
                #print('斜率对应的角度angle-整数2:', angle)
                return angle

        # USV与终点在同一垂直线上：
        if abs(round(self.x, 0) - round(target_x, 0)) <= self.radius * 2:
            if self.y < target_y:
                angle = 180
                #print('斜率对应的角度angle-整数3:', angle)
                return angle
            else:
                angle = 0
                #print('斜率对应的角度angle-整数4:', angle)
                return angle

        # 斜率可计算(这里要适应左上角是(0,0)的状况，和传统左下角是(0,0)有差异)
        slope = (self.x - target_x) / (target_y - self.y)
        # 斜率转换为弧度
        arc = atan(slope) / pi * 180

        # 终点在起点的左区域
        if target_y < self.y:
            # 左上角区域
            if target_x < self.x:
                angle = - round(arc, 0)
                #print('斜率对应的角度angle-小数1:', angle)
                return angle
            # 左下角区域
            else:
                angle = 360 - round(arc, 0)
                #print('斜率对应的角度angle-小数2:', angle)
                return angle

        # 终点在起点的右区域
        else:
            angle = 180 - round(arc, 0)
            #print('斜率对应的角度angle-小数3:', angle)
            return angle



    def next_angular_guide2(self):
        target_x, target_y = self.env.target_coordinate()
        #print('USV&终点',self.x,self.y,target_x, target_y)

        #USV与终点在同一垂直线上：
        if round(self.y, 0) - round(target_y, 0) == 0:
            if self.x < target_x:
                angle = 270
                #print('斜率对应的角度angle-整数1:',angle)
                return angle
            else:
                angle = 90
                #print('斜率对应的角度angle-整数2:', angle)
                return angle

        # USV与终点在同一垂直线上：
        if round(self.x, 0) - round(target_x, 0) == 0:
            if self.y < target_y:
                angle = 180
                #print('斜率对应的角度angle-整数3:', angle)
                return angle
            else:
                angle = 0
                #print('斜率对应的角度angle-整数4:', angle)
                return angle

        # 假设斜率都存在（因为USV和终点都是浮点数，不可能完全相等，存在误差）
        # 斜率可计算(这里要适应左上角是(0,0)的状况，和传统左下角是(0,0)有差异)
        slope = (self.x - target_x) / (target_y - self.y)
        # 斜率转换为弧度
        arc = atan(slope) / pi * 180
        #print('arc:', arc)

        # 终点在起点的左区域
        if target_y < self.y:
            # 左上角区域
            if target_x < self.x:
                angle = - round(arc, 0)
                #print('斜率对应的角度angle1-小数:', angle)
                return angle
            # 左下角区域
            else:
                angle = 360 - round(arc, 0)
                #print('斜率对应的角度angle2-小数:', angle)
                return angle

        # 终点在起点的右区域
        else:
            angle = 180 - round(arc, 0)
            #print('斜率对应的角度angle3-小数:', angle)
            return angle



    #含有输入参数startPoint[0]\ startPoint[1]表示：startPoint.x,startPoint.y(按照next_angular_guide2修改)
    def next_angular_guide3(self, startPoint, endPoint):
        #target_x, target_y = self.env.target_coordinate()
        # print('USV&终点',self.x,self.y,target_x, target_y)

        # USV与终点在同一垂直线上：
        if round(startPoint[1], 0) - round(endPoint[1], 0) == 0:
            if startPoint[0] < endPoint[0]:
                angle = 270
                # print('斜率对应的角度angle-整数1:',angle)
                return angle
            else:
                angle = 90
                # print('斜率对应的角度angle-整数2:', angle)
                return angle

        # USV与终点在同一垂直线上：
        if round(startPoint[0], 0) - round(endPoint[0], 0) == 0:
            if startPoint[1] < endPoint[1]:
                angle = 180
                # print('斜率对应的角度angle-整数3:', angle)
                return angle
            else:
                angle = 0
                # print('斜率对应的角度angle-整数4:', angle)
                return angle

        # 假设斜率都存在（因为USV和终点都是浮点数，不可能完全相等，存在误差）
        # 斜率可计算(这里要适应左上角是(0,0)的状况，和传统左下角是(0,0)有差异)
        slope = (startPoint[0] - endPoint[0]) / (endPoint[1] - startPoint[1])
        # 斜率转换为弧度
        arc = atan(slope) / pi * 180
        # print('arc:', arc)

        # 终点在起点的左区域
        if endPoint[1] < startPoint[1]:
            # 左上角区域
            if endPoint[0] < startPoint[0]:
                angle = - round(arc, 0)
                # print('斜率对应的角度angle1-小数:', angle)
                return angle
            # 左下角区域
            else:
                angle = 360 - round(arc, 0)
                # print('斜率对应的角度angle2-小数:', angle)
                return angle

        # 终点在起点的右区域
        else:
            angle = 180 - round(arc, 0)
            # print('斜率对应的角度angle3-小数:', angle)
            return angle





    #起点与终点间添加一系列不与障碍物相交的中间点-方法2
    def pathGuide2(self):
        res = self.pathGuide_explore()
        difference_angular = self.next_angular_guide3(res[0], res[1]) - self.direction
        #print('当前direction,当前difference_angular：',self.direction,difference_angular)
        Action = self.action_class
        act = Action(False, True, difference_angular, self.speed)
        return act


    #迭代初始赋值
    def pathGuide_explore(self):
        target_x, target_y = self.env.target_coordinate()
        toUseList = [(target_x, target_y),(self.x, self.y)]
        pathList =[]
        pathListRes = self.iter_explore(toUseList, pathList)
        pathListRes.append((target_x, target_y))
        return pathListRes


    #迭代
    def iter_explore(self, toUseList, pathList):
        while len(toUseList)>=2:
            #判断toUseList最后两点是否与障碍物相交
            if ( self.pointToLine_Length(toUseList) ):
                #不相交，pop和insert
                pathList.append(toUseList.pop())

            else:
                #相交，找随机点
                randx = round(random.uniform(0 + self.radius, self.env.width),4)
                randy = round(random.uniform(0 + self.radius, self.env.height),4)
                toUseList.insert(len(toUseList)-1, (randx, randy))
                pathList = self.iter_explore(toUseList, pathList)

        return pathList



    #直线(a,b) point(x3);;a,b,x3是三点：构建Ax+By+c=0   但是没有考虑到障碍物与线段的垂线交点在线段延长线上
    def pointToLine_Length2(self, toUseList):
        a = toUseList[-1]
        b = toUseList[-2]

        # A = b.y - a.y
        # B = a.x - b.x
        # C = b.x * a.y - a.x * b.y
        A = b[1] - a[1]
        B = a[0] - b[0]
        C = b[0] * a[1] - a[0] * b[1]

        for obs in self.env.obs:
            d = abs((A * obs.x + B * obs.y + C) / sqrt(A * A + B * B))
            if ( d - obs.radius <= 0.05):
                return False
                #与障碍物相交
        #与障碍物不相交
        return True


    #充分考虑了：障碍物与线段的距离（而不是障碍物与直线的距离，两者区别很大）
    #https://www.cnblogs.com/lyggqm/p/4651979.html
    def pointToLine_Length(self, toUseList):
        A = toUseList[-1]
        B = toUseList[-2]

        AB = (B[0] - A[0], B[1] - A[1])
        ABdic = sqrt(AB[0] * AB[0] + AB[1] * AB[1])

        for obs in self.env.obs:
            P = (obs.x, obs.y)
            AP = (P[0] - A[0], P[1] - A[1])

            dot = (AP[0] * AB[0] + AP[1] * AB[1]) / (ABdic * ABdic)

            AC = (AB[0] * dot, AB[1] * dot)
            C = (AC[0] + A[0], AC[1] + A[1])

            if (dot > 1):
                BP = (P[0] - B[0], P[1] - B[1])
                leng = sqrt(BP[0] * BP[0] + BP[1] * BP[1])
            elif dot < 0:
                AP = (P[0] - A[0], P[1] - A[1])
                leng = sqrt(AP[0] * AP[0] + AP[1] * AP[1])
            else:
                PC = (C[0] - P[0], C[1] - P[1])
                leng = sqrt(PC[0] * PC[0] + PC[1] * PC[1])

            if (leng - obs.radius <= 0.05):
                return False
                # 与障碍物相交
        # 与障碍物不相交
        return True













#无附加质量和科氏力，线形阻尼
#修改了update_xyzuvr中坐标更新，  （路径导引：左0 下90 右180 上270）
class MyContinueDynamicsUSV(BasicPlaneUSV):
    '''一个策略简单的USV,派生自BasicObsUSV,用于连续环境下USV，
        认为USV可瞬间达到下一次角速度且按照speed走一帧时间的距离
    '''

    def __init__(self, uid, x, y, env, envDisturb):
        super(MyContinueDynamicsUSV, self).__init__(uid, x, y, env)
        self.action_class = Action = namedtuple("action", ['F', 'T'])
        self.radius = 1


        self.x, self.y = x, y
        self.heading = 0.0
        self.u = -50.0
        self.v = 0.0
        self.r = 0

        self.m11 = 120000.0#3980.0
        self.m22 = 217900.0#3980.0
        self.m33 = 63600000#19703.0

        self.d11 = 21500.0#50.0
        self.d22 = 117000.0#200.0
        self.d33 = 8020000.0#3224.0

        self.F_max = 1000000 * 2
        self.T_max = 60000 * 45000 * 2

        self.xyhList = [(self.x, self.y, self.heading)]
        self.uvrList = [(self.u, self.v, self.r)]

        self.expectStepLen = 1

        self.envDisturb = envDisturb  # 默认True,包含环境（风浪涌流干扰）

        self.tmp = 0

    def set_init_xyh(self,x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading

    def set_init_uvr(self,u, v, r):
        self.u = u
        self.v = v
        self.r = r

    def getuid(self):
        return self.id


    def decision_algorithm(self):
        '''这种USV的action对象有两个属性:
        1.F：表示前进驱动力
        2.T：表示转向'''
        Action = self.action_class

        #F= -13000;T= 2500
        F, T = self.pathGuide33()

        act = Action(F, T)#Action(30.0, 15.0)
        return act

    def update_xyduvr(self, F, T, t):
        '''输入变量：驱动力F,转向T,更新时间t;;;根据动力学方程计算uvr的加速度'''

        #这里可加一步判断F，T的范围**()

        # step1:根据F,T计算uvr的加速度
        if self.envDisturb == False: #无环境干扰（无风浪涌流）
            au = (self.m22 / self.m11) * self.v * self.r - (self.d11 / self.m11) * self.u + (F / self.m11)
            av = -(self.m11 / self.m22) * self.u * self.r - (self.d22 / self.m22) * self.v
            ar = ((self.m11 - self.m22) / self.m33) * self.u * self.v - (self.d33 / self.m33) * self.r + (T / self.m33)
        else:   #环境干扰（风浪涌流）
            timeexample = time.time()
            disturbU = 0.08 * (sin(0.2 * timeexample)) + cos(0.2 * timeexample + pi / 4) + sin(0.2 * timeexample + pi / 6)
            disturbV = disturbU
            disturbR = 0.1 * (sin(0.2 * timeexample)) + cos(0.2 * timeexample + pi / 4) + sin(0.2 * timeexample + pi / 6)
            if disturbU < -0.1:disturbU = -0.1
            if disturbU > 0.1: disturbU = 0.1
            if disturbV < -0.1:disturbV = -0.1
            if disturbV > 0.1: disturbV = 0.1
            if disturbR < -0.1:disturbR = -0.1
            if disturbR > 0.1: disturbR = 0.1


            au = (self.m22 / self.m11) * self.v * self.r - (self.d11 / self.m11) * self.u + (1 / self.m11) * (F + disturbU)
            av = -(self.m11 / self.m22) * self.u * self.r - (self.d22 / self.m22) * self.v + (1/self.m22) * (disturbV)
            ar = ((self.m11 - self.m22) / self.m33) * self.u * self.v - (self.d33 / self.m33) * self.r + (1 / self.m33) * (T + disturbR)

        # step2:根据时间t,计算更新后的uvr
        self.u += au * t
        self.v += av * t
        self.r += ar * t

        self.uvrList.append((self.u, self.v, self.r))

        # step3:uvr转换为x y heading   #这里注意：self.heading*pi/180
        ax = self.u * cos(self.heading*pi/180) - self.v * sin(self.heading*pi/180)
        ay = self.u * sin(self.heading*pi/180) + self.v * cos(self.heading*pi/180)
        aheading = self.r


        # step4:根据时间t,计算更新后的x y heading
        # 这里相当于把左上角(0,0)的坐标  转为左下角(0,0)的坐标，动力学更新方式， 转换到左上角(0,0)地图中的坐标
        # tempx = self.y
        # tempy = self.env.width - 1 - self.x
        # tempx = tempx + float("%.4f" % (ax * t))
        # tempy = tempy + float("%.4f" % (ay * t))
        # self.x = self.env.width - 1 - tempy
        # self.y = tempx
        #
        #
        self.x += float(ax * t)
        self.y += float(ay * t)


        self.heading += aheading * t
        self.heading = float('%.4f'% (self.heading % 360))  #380%360=20 (-50)%360=310
        self.xyhList.append((self.x, self.y, self.heading))

        #print('ax,ay,aheading:', list(map(float,[ax,ay,aheading])))

    def move(self):
        action = self.decision_algorithm()
        F, T = action.F, action.T
        # print("moving now...", F, T)
        F *= self.F_max
        T *= self.T_max
        target_x,target_y = self.env.target_coordinate()
        #当前位置距离终点的距离
        dis = sqrt( (self.x - target_x)*(self.x - target_x) + (self.y - target_y)*(self.y - target_y))
        #print('update_before:',int(self.x), int(self.y), int(self.heading))

        #如果当前位置距离终点在10范围内，大步伐更新；否则小步伐更新
        # print("before", self.coordinate(), self)
        if dis > 20:
            self.update_xyduvr(F, T, 1/120)
        else:
            self.update_xyduvr(F, T, 1/120)
        # print("after:", self.coordinate(), self)
        #print('update_after:', int(self.x), int(self.y), int(self.heading))


    #引导算法：：
    def pathGuide33(self):
        res = self.pathGuide_explore()
        # print('计算出的路径',res)

        #下一时刻期望的位置(x_res, y_res, heading_res)
        heading_res = self.next_angular_guide4(res[0], res[1])
        #注意角度的计算：之前没写*pi/180部分，哎
        # x_res = self.x - self.expectStepLen * cos(heading_res*pi/180)
        # y_res = self.y + self.expectStepLen * sin(heading_res*pi/180)

        #这里可能要修改吧？ 路径导引设定 0左 下90 右180 上270， 因此期望坐标应该是：
        x_res = self.x + self.expectStepLen * sin(heading_res * pi / 180)
        y_res = self.y - self.expectStepLen * cos(heading_res * pi / 180)

        #print('路径导引下一坐标',float('%.4f' %x_res),float('%.4f'%y_res))
        #print('期望角度', heading_res)
        #print('当前的角度',self.heading)

        #位置限定不出界
        if x_res < self.radius:
            x_res = self.radius
        if x_res > self.env.width -1 - self.radius:
            x_res = self.env.width -1 -self.radius
        if y_res < self.radius:
            y_res = self.radius
        if y_res > self.env.height -1 -self.radius:
            y_res = self.env.height -1 -self.radius


        F = -1000000
        #T = 60000*16000  #60000##-60000
        T = 60000*45000

        delta_heading = self.heading - heading_res
        if delta_heading < -180:
            delta_heading += 360
        if delta_heading >180:
            delta_heading -= 360
        T = -delta_heading * T / 180

        #print('计算出的下一控制策略',float('%.4f' %F), float('%.4f' %T))
        F /= self.F_max
        T /= self.T_max
        return F, T

    # 迭代初始赋值
    def pathGuide_explore(self):
        # print("in pathGuide_explore", self.coordinate(), self)
        target_x, target_y = self.env.target_coordinate()
        toUseList = [(target_x, target_y), (self.x, self.y)]
        pathList = []
        pathListRes = self.iter_explore(toUseList, pathList)
        pathListRes.append((target_x, target_y))
        return pathListRes

    # 迭代
    def iter_explore(self, toUseList, pathList):
        while len(toUseList) >= 2:
            # 判断toUseList最后两点是否与障碍物相交
            if (self.pointToLine_Length(toUseList)):
                # 不相交，pop和insert
                pathList.append(toUseList.pop())

            else:
                # 相交，找随机点
                randx = round(random.uniform(0 + self.radius, self.env.width), 4)
                randy = round(random.uniform(0 + self.radius, self.env.height), 4)
                toUseList.insert(len(toUseList) - 1, (randx, randy))
                pathList = self.iter_explore(toUseList, pathList)

        return pathList

    # 充分考虑了：障碍物与线段的距离（而不是障碍物与直线的距离，两者区别很大）
    def pointToLine_Length(self, toUseList):
        A = toUseList[-1]
        B = toUseList[-2]

        AB = (B[0] - A[0], B[1] - A[1])
        ABdic = sqrt(AB[0] * AB[0] + AB[1] * AB[1])

        for obs in self.env.obs:
            P = (obs.x, obs.y)
            AP = (P[0] - A[0], P[1] - A[1])

            dot = (AP[0] * AB[0] + AP[1] * AB[1]) / (ABdic * ABdic)

            AC = (AB[0] * dot, AB[1] * dot)
            C = (AC[0] + A[0], AC[1] + A[1])

            if (dot > 1):
                BP = (P[0] - B[0], P[1] - B[1])
                leng = sqrt(BP[0] * BP[0] + BP[1] * BP[1])
            elif dot < 0:
                AP = (P[0] - A[0], P[1] - A[1])
                leng = sqrt(AP[0] * AP[0] + AP[1] * AP[1])
            else:
                PC = (C[0] - P[0], C[1] - P[1])
                leng = sqrt(PC[0] * PC[0] + PC[1] * PC[1])

            if (leng - obs.radius <= 0.05):
                return False
                # 与障碍物相交
        # 与障碍物不相交
        return True

    #含有输入参数startPoint[0]\ startPoint[1]表示：startPoint.x,startPoint.y(按照next_angular_guide3修改)
    # #对应垂直方向y轴正方向是0度，顺时针转   （用于连续平面--action[F,T]）
    #https://www.cnblogs.com/lyggqm/p/4651979.html
    def next_angular_guide4(self, startPoint, endPoint):
        #target_x, target_y = self.env.target_coordinate()
        # print('USV&终点',self.x,self.y,target_x, target_y)

        # USV与终点在同一垂直线上：
        #if round(startPoint[1], 0) - round(endPoint[1], 0) == 0:
        if int(startPoint[1]) - int(endPoint[1]) == 0:
            if startPoint[0] < endPoint[0]:
                angle = 90#180
                #print('斜率对应的角度angle-整数1:',angle)
                return angle
            else:
                angle = 270#0
                #print('斜率对应的角度angle-整数2:', angle)
                return angle

        # USV与终点在同一水平线上：
        #if round(startPoint[0], 0) - round(endPoint[0], 0) == 0:
        if int(startPoint[0]) - int(endPoint[0]) == 0:
            if startPoint[1] < endPoint[1]:
                angle = 180#90
                #print('斜率对应的角度angle-整数3:', angle)
                return angle
            else:
                angle = 0#270
                #print('斜率对应的角度angle-整数4:', angle)
                return angle

        # 假设斜率都存在（因为USV和终点都是浮点数，不可能完全相等，存在误差）
        # 斜率可计算(这里要适应左上角是(0,0)的状况，和传统左下角是(0,0)有差异)
        slope = (startPoint[0] - endPoint[0]) / (endPoint[1] - startPoint[1])
        # 斜率转换为弧度
        arc = atan(slope) / pi * 180
        #print('arc:', arc)

        # 终点在起点的右区域
        if endPoint[1] > startPoint[1]:
            angle = 180 + (int)(arc)#90 - (int)(arc)
            #print('斜率对应的角度angle1-小数:', angle)
            return angle

        # 终点在起点的左区域
        else:
            # 左上角区域
            if endPoint[0] < startPoint[0]:
                angle = 360 + (int)(arc)
                #print('斜率对应的角度angle1-小数:', angle)
                return angle
            # 左下角区域
            else:
                angle = (int)(arc)
                #print('斜率对应的角度angle2-小数:', angle)
                return angle















#第三次尝试：加入非线性阻尼部分，USV动力学文档上的参数
class MyContinueDynamicsUSV3(BasicPlaneUSV):
    '''一个策略简单的USV,派生自BasicObsUSV,用于连续环境下USV，
        认为USV可瞬间达到下一次角速度且按照speed走一帧时间的距离
    '''


    def __init__(self, uid, x, y, env, envDisturb, FTListValue):
        super(MyContinueDynamicsUSV3, self).__init__(uid, x, y, env)
        self.action_class = Action = namedtuple("action", ['F', 'T'])
        self.radius = 1


        self.x, self.y = x, y
        self.heading = 0.0
        self.u = 0.0#-10.0
        self.v = 0.0
        self.r = 0.0

        #相关参数：m = 3980; X_u = -50; X_uu = -135; Y_v = -200; Y_vv = -2000; N_r = -3224; I = 19703; N_rrr = -3224


        # 地球惯性系中x,y方向上的加速度（正负含方向值),根据动力学更新x和y可知：其适应左上角(0,0)的地图
        # 所以：x向下是正方向，y向右是正方向
        self.ax = 0.0
        self.ay = 0.0

        self.xyhList = [(self.x, self.y, self.heading)]
        self.uvrList = [(self.u, self.v, self.r)]

        self.expectStepLen = 2
        self.F_max = 13100
        self.T_max = 258000
        self.FTList = []
        self.FTLen = 0

        self.envDisturb = envDisturb  # 默认True,包含环境（风浪涌流干扰）


        # 前段传入的参数，用于可视化观察
        self.FTListValue = FTListValue


        # 规划路径（该随机导引路径只产生一次）,否则会造成过程中路径不断变化，影响角度的无效变化
        # （路径的随机，造成角度一会大，一会小，造成多次迭代的失效）所以这里对随机导引路径只产生一次
        self.pathguideList = []

        # self.tUpdateCount记录按照更新位置的次数， self.RecordList记录：self.tUpdateCount%20==0 时的决策
        self.tUpdateCount = 0
        self.RecordList = []




    def set_init_xyh(self,x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading


    def set_init_uvr(self,u, v, r):
        self.u = u
        self.v = v
        self.r = r


    def getuid(self):
        return self.id


    #查看目前进行了多少次决策
    def getFTCurrentLen(self):
        return self.FTLen

    # 计算当前船与目标点的距离
    def getDistanceUSVTarget(self):
        target_x, target_y = self.env.target_coordinate()
        Dis = sqrt((self.x - target_x) * (self.x - target_x) + (self.y - target_y) * (self.y - target_y))
        Dis = float("%.4f" % Dis)
        return Dis


    def decision_algorithm(self):
        '''这种USV的action对象有两个属性:
        1.F：表示前进驱动力
        2.T：表示转向'''
        Action = self.action_class

        #F= -13000;T= 2500
        F, T = self.pathGuide33()

        #F驱动力，T转向的范围限定
        # if F < -6550: F = -6550
        # if F > 13100: F = 13100
        # if T < -2580: T = -2580
        # if T > 2580: T = 2580
        act = Action(F, T)#Action(30.0, 15.0)
        return act


    def update_xyduvr(self, F, T, t):
        '''输入变量：驱动力F,转向T,更新时间t;;;根据动力学方程计算uvr的加速度'''

        #这里可加一步判断F，T的范围**()

        # step1:根据F,T计算uvr的加速度
        if self.envDisturb == False: #无环境干扰（无风浪涌流）

            au = self.v * self.r + (-50 / 3980) * self.u + (-135 / 3980) * self.u * abs(self.u) + (1/3980) * F
            av = - self.u * self.r + (-200/3980) * self.v + (-2000/3980) * self.v * abs(self.v)
            ar = (-3224/19703) * self.r + (-3224/19703) * self.r * self.r * self.r + (1/19703) * T

        else:   #环境干扰（风浪涌流）
            timeexample = time.time()
            disturbU = 0.08 * (sin(0.2 * timeexample)) + cos(0.2 * timeexample + pi / 4) + sin(0.2 * timeexample + pi / 6)
            disturbV = disturbU
            disturbR = 0.1 * (sin(0.2 * timeexample)) + cos(0.2 * timeexample + pi / 4) + sin(0.2 * timeexample + pi / 6)
            if disturbU < -0.1:disturbU = -0.1
            if disturbU > 0.1: disturbU = 0.1
            if disturbV < -0.1:disturbV = -0.1
            if disturbV > 0.1: disturbV = 0.1
            if disturbR < -0.1:disturbR = -0.1
            if disturbR > 0.1: disturbR = 0.1


            au = self.v * self.r + (-50 / 3980) * self.u + (-135 / 3980) * self.u * abs(self.u) + (1/3980) * (F + disturbU)
            av = - self.u * self.r + (-200/3980) * self.v + (-2000/3980) * self.v * abs(self.v) + (1/3980) * (disturbV)
            ar = (-3224/19703) * self.r + (-3224/19703) * self.r * self.r * self.r + (1/19703) * (T + disturbR)

        # step2:根据时间t,计算更新后的uvr
        self.u += au * t
        self.v += av * t
        self.r += ar * t
        self.uvrList.append((self.u, self.v, self.r))

        # step3:uvr转换为x y heading   #这里注意：self.heading*pi/180
        ax = self.u * cos(self.heading*pi/180) - self.v * sin(self.heading*pi/180)
        ay = self.u * sin(self.heading*pi/180) + self.v * cos(self.heading*pi/180)
        self.ax = float("%.4f" % ax)
        self.ay = float("%.4f" % ay)

        aheading = self.r

        tempx = self.y
        tempy = self.env.width - 1 - self.x
        tempx = tempx + float("%.4f" % (ax * t))
        tempy = tempy + float("%.4f" % (ay * t))
        self.x = self.env.width - 1 - tempy
        self.y = tempx

        # step4:根据时间t,计算更新后的x y heading
        # self.x += float(ax * t)
        # self.y += float(ay * t)

        self.heading += aheading * t

        self.heading = self.heading % 360 #380%360=20 (-50)%360=310
        self.xyhList.append((self.x, self.y, self.heading))

        #print('ax,ay,aheading:', list(map(float,[ax,ay,aheading])))



    def move(self):
        # 每1/20 * 5次 帧决策一次
        # if len(self.FTListValue)==0:
        #     if self.tUpdateCount == 0 or self.tUpdateCount % 5 == 0:
        #         action = self.decision_algorithm()
        #         F, T = action.F, action.T
        #         self.RecordList.append((F, T))
        #     else:
        #         F = self.RecordList[-1][0]
        #         T = self.RecordList[-1][1]

        # 每1/20帧决策一次
        if len(self.FTListValue) == 0:
            action = self.decision_algorithm()
            F, T = action.F, action.T


        else:
            F, T = self.FTListValue[self.FTLen][0], self.FTListValue[self.FTLen][1]
            if (self.tUpdateCount + 1) % 5 == 0:
                self.FTLen = self.FTLen + 1

        F *= self.F_max
        T *= self.T_max


        target_x,target_y = self.env.target_coordinate()
        #当前位置距离终点的距离
        dis = sqrt( (self.x - target_x)*(self.x - target_x) + (self.y - target_y)*(self.y - target_y))


        if DEBUGPrint == True:
            print('update_before:',int(self.x), int(self.y), int(self.heading))

        #如果当前位置距离终点在10范围内，大步伐更新；否则小步伐更新
        if dis > 20:
            self.update_xyduvr(F, T, 1/20)
            self.tUpdateCount = self.tUpdateCount + 1
        else:
            self.update_xyduvr(F, T, 1/20)
            self.tUpdateCount = self.tUpdateCount + 1

        if DEBUGPrint == True:
            print('update_after:', int(self.x), int(self.y), int(self.heading))





    #修改引导算法：：
    def pathGuide33(self):
        #直接使用终点计算的方式
        # res = self.pathGuide_explore()
        #
        # #下一时刻期望的位置(x_res, y_res, heading_res)
        # heading_res = self.next_angular_guide4(res[0], res[1])
        #
        # #注意角度的计算：之前没写*pi/180部分，哎
        # x_res = res[1][0]
        # y_res = res[1][1]


        if len(self.pathguideList) == 0:
            self.pathguideList = self.pathGuide_explore()
            del self.pathguideList[0]

        if DEBUGPrint == True:
            print('计算出的路径', self.pathguideList)

        if len(self.pathguideList) > 1:
            disCharge = sqrt ((self.x - self.pathguideList[0][0])*(self.x - self.pathguideList[0][0]) + (self.y - self.pathguideList[0][1])*(self.y - self.pathguideList[0][1]))
            if disCharge <= 10:
                del self.pathguideList[0]

        # 下一时刻期望的位置(x_res, y_res, heading_res)
        heading_res = self.next_angular_guide4((self.x, self.y), self.pathguideList[0])

        #注意角度的计算：之前没写*pi/180部分，哎
        # x_res = self.x - self.expectStepLen * cos(heading_res*pi/180)
        # y_res = self.y + self.expectStepLen * sin(heading_res*pi/180)
        x_res = self.pathguideList[0][0]
        y_res = self.pathguideList[0][1]


        if DEBUGPrint == True:
            print('路径导引下一坐标',float('%.4f' %x_res),float('%.4f'%y_res))
            print('期望角度', heading_res)
            print('当前的角度',self.heading)

        #位置限定不出界
        if x_res < self.radius:
            x_res = self.radius
        if x_res > self.env.width -1 - self.radius:
            x_res = self.env.width -1 -self.radius
        if y_res < self.radius:
            y_res = self.radius
        if y_res > self.env.height -1 -self.radius:
            y_res = self.env.height -1 -self.radius



        #第一种测试F，T方法
        # F = 13100
        # T = -2580*1000
        #
        # delta_heading = self.heading - heading_res
        # if delta_heading < -180:
        #     delta_heading += 360
        # if delta_heading >180:
        #     delta_heading -= 360
        # T = delta_heading * T / 180




        # 第三种测试F，T方法    u_res=x_dot*cos(heading) + y_dot*sin(heading)
        # 根据期望位置求解，先将左上角00的期望位置转化为左下角00的位置
        # x_trans_res = y_res
        # y_trans_res = self.env.width - 1 - x_res
        # u_res = (x_trans_res - self.x)/(1/20) * cos(heading_res * pi /180) + (y_trans_res - self.y)/(1/20) * sin(heading_res * pi /180)
        # u_res = float("%.4f" % u_res)




        # 第二种测试F，T方法
        #求期望位置与当前位置的斜率
        # 斜率可计算(这里要适应左上角是(0,0)的状况 和 传统左下角是(0,0)有差异)
        #slope = (startPoint[0] - endPoint[0]) / (endPoint[1] - startPoint[1])
        if (y_res - self.y) != 0 :
            u_res = (self.x - x_res) / (y_res - self.y)
        else:
            u_res = self.u



        # 附加限制3: 垂直时，斜率不存在，所以进行限制 (目前终点是(30，52)，但快接近目标时，转了很多才到终点)
        if u_res > (self.env.width):
            u_res = self.env.width - 1
        if u_res < -(self.env.width):
            u_res = - self.env.width + 1


        if DEBUGPrint == True:
            print('期望速度u_res, 当前速度self.u', u_res, self.u)

            print('当前self.v,self.r', self.v, self.r)


        # 附加限制1
        # if 88< heading_res < 90 or 90<= heading_res <92:
        if -0.2 < self.u < 0.2:
            self.u = self.u * 2
        # 终点在(60,98)时，斜率为0，所以期望速度为0，到后面速度为0，会不动了，所以这里改变了速度



        F = (-3980.0 * self.v * self.r + 50 * self.u + 135 * abs(self.u) * self.u + 10 * 3980.0 * (u_res - self.u))
        F = F


        if heading_res == 0:
            if self.heading > 270: heading_res = 360
            if self.heading < 90: heading_res = 0

        delta_heading = self.heading - heading_res
        if delta_heading < -180:
            delta_heading += 360
        if delta_heading >180:
            delta_heading -= 360

        if DEBUGPrint == True:
            print('角度差delta_heading', delta_heading)


        T = (98515 * (-delta_heading - self.r))


        # 附加限制2：必须加在目标点在其上方这种情况，加在目标点在水平右侧时会出错
        if heading_res > 350 or heading_res < 10:
            if abs(delta_heading) <= 6:  # 3
                F = -abs(F)
            if heading_res >= 358 or heading_res <= 2:
                F = -abs(F)

        if 170 <= heading_res <= 190:
            if abs(delta_heading) <= 5:
                F = -abs(F)
            if 178 <= heading_res <= 182:
                F = -abs(F)

        if 80 <= heading_res <= 100:
            if abs(delta_heading) <= 3:
                F = -abs(F)
            if 88 <= heading_res <= 92:
                F = -abs(F)

        if 260 <= heading_res <= 280:
            if abs(delta_heading) <= 3:
                F = -abs(F)
            if 268 <= heading_res <= 272:
                F = -abs(F)


        if F < -6550:
            F = -6550
        if F > 13100:
            F = 13100
        if T < -2580*100:
            T = -2580*100
        if T > 2580*100:
            T = 2580*100




        F /= self.F_max
        T /= self.T_max


        self.FTList.append((F,T))
        self.FTLen = self.FTLen + 1

        if DEBUGPrint == True:
            print('计算出的下一控制策略',float('%.4f' %F), float('%.4f' %T))

        return F, T






    # 迭代初始赋值
    def pathGuide_explore(self):
        target_x, target_y = self.env.target_coordinate()
        toUseList = [(target_x, target_y), (float('%.6f' %self.x), float('%.6f' % self.y))]
        pathList = []
        pathListRes = self.iter_explore(toUseList, pathList)
        pathListRes.append((target_x, target_y))
        return pathListRes


    # 迭代
    def iter_explore(self, toUseList, pathList):
        while len(toUseList) >= 2:
            # 判断toUseList最后两点是否与障碍物相交
            if (self.pointToLine_Length(toUseList)):
                # 不相交，pop和insert
                pathList.append(toUseList.pop())

            else:
                # 相交，找随机点
                randx = round(random.uniform(0 + self.radius, self.env.width - 1 - self.radius*2), 4)
                #print(randx)
                randy = round(random.uniform(0 + self.radius, self.env.height - 1 - self.radius*2), 4)
                toUseList.insert(len(toUseList) - 1, (randx, randy))
                pathList = self.iter_explore(toUseList, pathList)

        return pathList



    # 充分考虑了：障碍物与线段的距离（而不是障碍物与直线的距离，两者区别很大）
    def pointToLine_Length(self, toUseList):
        A = toUseList[-1]
        B = toUseList[-2]

        AB = (B[0] - A[0], B[1] - A[1])
        ABdic = sqrt(AB[0] * AB[0] + AB[1] * AB[1])

        for obs in self.env.obs:
            P = (obs.x, obs.y)
            AP = (P[0] - A[0], P[1] - A[1])

            dot = (AP[0] * AB[0] + AP[1] * AB[1]) / (ABdic * ABdic)

            AC = (AB[0] * dot, AB[1] * dot)
            C = (AC[0] + A[0], AC[1] + A[1])

            if (dot > 1):
                BP = (P[0] - B[0], P[1] - B[1])
                leng = sqrt(BP[0] * BP[0] + BP[1] * BP[1])
            elif dot < 0:
                AP = (P[0] - A[0], P[1] - A[1])
                leng = sqrt(AP[0] * AP[0] + AP[1] * AP[1])
            else:
                PC = (C[0] - P[0], C[1] - P[1])
                leng = sqrt(PC[0] * PC[0] + PC[1] * PC[1])

            if (leng - obs.radius <= 0.05):
                return False
                # 与障碍物相交
        # 与障碍物不相交
        return True



    #含有输入参数startPoint[0]\ startPoint[1]表示：startPoint.x,startPoint.y(按照next_angular_guide3修改)
    # #对应垂直方向y轴正方向是0度，逆时针转（设置F常熟，T= 0，初始heading分别为0，90，180，270看USV走哪个方向）   （用于连续平面--action[F,T]）
    #https://www.cnblogs.com/lyggqm/p/4651979.html
    def next_angular_guide4(self, startPoint, endPoint):
        #target_x, target_y = self.env.target_coordinate()
        # print('USV&终点',self.x,self.y,target_x, target_y)

        # USV与终点在同一垂直线上：
        #if round(startPoint[1], 0) - round(endPoint[1], 0) == 0:
        if int(startPoint[1]) - int(endPoint[1]) == 0:
            if startPoint[0] < endPoint[0]:
                angle = 180

                if DEBUGPrint == True:
                    print('斜率对应的角度angle-整数1:',angle)

                return angle
            else:
                angle = 0

                if DEBUGPrint == True:
                    print('斜率对应的角度angle-整数2:', angle)

                return angle

        # USV与终点在同一水平线上：
        #if round(startPoint[0], 0) - round(endPoint[0], 0) == 0:
        if int(startPoint[0]) - int(endPoint[0]) == 0:
            if startPoint[1] < endPoint[1]:
                angle = 90#270

                if DEBUGPrint == True:
                    print('斜率对应的角度angle-整数3:', angle)

                return angle
            else:
                angle = 270#90

                if DEBUGPrint == True:
                    print('斜率对应的角度angle-整数4:', angle)

                return angle

        # 假设斜率都存在（因为USV和终点都是浮点数，不可能完全相等，存在误差）
        # 斜率可计算(这里要适应左上角是(0,0)的状况，和传统左下角是(0,0)有差异)
        slope = (startPoint[0] - endPoint[0]) / (endPoint[1] - startPoint[1])
        # 斜率转换为弧度
        arc = atan(slope) / pi * 180
        #print('arc:', arc)

        # # 终点在起点的右区域
        if endPoint[1] > startPoint[1]:
            angle = 90 - (int)(arc)#270 + (int)(arc)

            if DEBUGPrint == True:
                print('斜率对应的角度angle1-小数:', angle)

            return angle

        # 终点在起点的左区域
        else:
            angle = 270 - (int)(arc)#90 + (int)(arc)

            if DEBUGPrint == True:
                print('斜率对应的角度angle1-小数:', angle)

            return angle



    # 获取当前速度方向：即self.ax 与 self.ay的向量合成，是当前速度方向,输出的结果是：与当前USV连线的点--->用到pygame里面
    def get_curSpeedDirection(self):
        # print('测1：', self.ax, self.ay)

        # 设定速度方向画多长的线
        PointSpeedDirectionLen = 3
        tempTotal = sqrt(self.ax * self.ax + self.ay * self.ay)

        if self.ax == 0.0:
            after_ay = self.ay / abs(self.ay) * PointSpeedDirectionLen
            return 0, after_ay

        if self.ay == 0.0:
            after_ax = self.ax / abs(self.ax) * PointSpeedDirectionLen
            return after_ax, 0

        x_symbol = self.ax / abs(self.ax)
        y_symbol = self.ay / abs(self.ay)

        after_ax = float("%.4f" % (x_symbol * PointSpeedDirectionLen * abs(self.ax) / tempTotal))
        after_ay = float("%.4f" % (y_symbol * PointSpeedDirectionLen * abs(self.ay) / tempTotal))
        # print('测试速度方向的值2：', after_ax, after_ay)

        return after_ax, after_ay


    def transferAngle(self, point, point0, angle):
        angle = 360 - angle

        trans_x = (point[0] - point0[0]) * cos(angle*pi/180) + (point[1] - point0[1])*sin(angle*pi/180) + point0[0]
        trans_y = (point[0] - point0[0]) * sin(angle*pi/180) + (point[1] - point0[1])*cos(angle*pi/180) + point0[1]
        trans_x = float("%.4f" % trans_x)
        trans_y = float("%.4f" % trans_y)

        return trans_x, trans_y



