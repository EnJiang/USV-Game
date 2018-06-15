# coding:utf-8

import pygame
from pygame.locals import *
import copy
from collections import namedtuple
from time import sleep
import numpy as np
from math import sin, cos, pi


# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# plt.ion()
# fig = plt.figure()
# ax = fig.add_subplot(111)



class BasicGame(object):
    """基本游戏逻辑"""

    def __init__(self):
        super(BasicGame, self).__init__()
        self.is_target_safe = True

    def set_map(self, gameMap):
        self.map = gameMap

    def update(self):
        for ship in self.map.ships:
            ship.move()
        self.check_target()
        #print (self.map.str2())

    def check_target(self):
        target_x, target_y = self.map.target_coordinate()
        for ship in self.map.enemy_ships:
            ship_x, ship_y = ship.coordinate()
            if(ship_x == target_x and ship_y == target_y):
                self.is_target_safe = False

    def is_game_over(self):
        return not self.is_target_safe

    def start(self):
        while not self.is_game_over():
            self.update()
            print ('----------------------------------------------------------------------------------------')
            print ("press any key to continue")
            #raw_input()
            input()
        print ("you lost!")


class MyGame(BasicGame):
    def __init__(self):
        super(MyGame, self).__init__()
        self.recordlist = []
        self.arriveTarget = 0
        self.arriveObstacle = 0


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

            #这里添加enemy_ships的随机变动：上下左右或是原地（在USV.py中添加moverandom()方法）
            for ship in self.map.enemy_ships:
                ship.moverandom()


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
            #print('game-start-update前的地图形式：');print(self.map.str2())
            self.update()
            # print('\n决策链（当前环境env + 采取动作action）',self.recordlist)
            print(self.map.env_matrix())
            print ('----------------------------------------------------------------------------------------')
            #print ("press any key to continue");input()
        print ("game over!")
        print('是否到达终点：(0表示没，1表示到达)',self.arriveTarget)
        print('是否碰到障碍物：(0表示没，1表示碰到)', self.arriveObstacle)




class BasicGUIGame(BasicGame):
    """基本的GUI引擎, 使用pygame"""

    def __init__(self):
        super(BasicGUIGame, self).__init__()
        self.gui = pygame
        self.gui_init()

    def gui_init(self):
        self.gui_screen = self.gui.display.set_mode((800, 600), 0, 32)
        self.gui.display.set_caption("USV")
        self.gui_background = self.gui.image.load(
            'src/img/bg/seaSurface.png').convert()
        self.gui_friendly_ship = self.gui.image.load(
            'src/img/usv/friendly.png').convert_alpha()
        self.gui_enemy_ship = self.gui.image.load(
            'src/img/usv/enemy.png').convert_alpha()
        self.gui_target = self.gui.image.load(
            'src/img/target/blueTarget.png').convert_alpha()

    def update(self):
        '''地图里面为了符合人的习惯,定整个矩阵的左下角为(0,0), x轴负方向为0°, y轴正方形为90°
        和计算机矩阵左上角为(0,0)的习惯稍微不同. 而且pygame已经做过校正了, x就是水平方向,
        所以有(x1, y1)=(x, height-y)
        pygame定义,负角度顺时针转动,所以我们角度加个负'''

        x_unit = 800.0 / self.map.width
        y_unit = 600.0 / self.map.height

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        self.gui_screen.blit(self.gui_background, (0, 0))

        for ship in self.map.ships:
            ship.move()
            ship_x, ship_y = ship.coordinate()
            ship_w, ship_h = x_unit, y_unit
            if(ship.is_enemy):
                gui_enemy_ship = self.gui.transform.rotozoom(
                    self.gui_enemy_ship, -ship.direction, x_unit / 16)
                self.gui_screen.blit(
                    gui_enemy_ship, (ship_x * x_unit - ship_w / 2, (self.map.height - ship_y) * y_unit - ship_h / 2))
            else:
                gui_friendly_ship = self.gui.transform.rotozoom(
                    self.gui_friendly_ship, -ship.direction, x_unit / 16)
                self.gui_screen.blit(
                    gui_friendly_ship, (ship_x * x_unit - ship_w / 2, (self.map.height - ship_y) * y_unit - ship_h / 2))

        self.check_target()

        target_x, target_y = self.map.target_coordinate()
        target_w, target_h = x_unit, y_unit
        self.gui_screen.blit(
            self.gui.transform.rotozoom(self.gui_target, 0, x_unit / 16),
            (target_x * x_unit - target_w / 2, (self.map.height - target_y) * y_unit - target_h / 2))

        self.gui.display.update()

    def start(self):
        while not self.is_game_over():
            self.update()
            sleep(0.01)

        self.gui.display.set_caption("Game Over!")
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            self.gui.display.update()






class MyContinueGame(BasicGame):
    def __init__(self,obsmove):
        super(MyContinueGame, self).__init__()
        self.arriveTarget = 0
        self.arriveObstacle = 0
        self.arriveUnlegal = 0
        self.obsMoveBool = obsmove #默认false，障碍物不随机移动


    #获取船体当前的状态信息 u,v,r(速度信息)
    def get_uvr_u(self):
        for ship in self.map.friendly_ships:
            if ship.getuid() == 0:
                return ship.u

    def get_uvr_v(self):
        for ship in self.map.friendly_ships:
            if ship.getuid() == 0:
                return ship.v

    def get_uvr_r(self):
        for ship in self.map.friendly_ships:
            if ship.getuid() == 0:
                return ship.r

    #获取船体当前的航向
    def get_xyh_heading(self):
        for ship in self.map.friendly_ships:
            if ship.getuid() == 0:
                return ship.heading


    def update(self):
        #print('update_之前：输出map.env_matrix()函数的地图形式：：')

        #np.set_printoptions(threshold=np.nan)
        #print(self.map.env_matrix())



        # ax.set_xlim(0,100)
        # ax.set_ylim(100,0)
        #
        # import time
        # start = time.time()
        # temptestoutput = self.map.env_matrix()
        # # print('输出值为1的位置：',np.argwhere(temptestoutput == 1))
        # # print('输出值为-1的位置：', np.argwhere(temptestoutput == -1))
        # # print('输出值为2的位置：', np.argwhere(temptestoutput == 2))
        # lines = []
        # for i in range(len(np.argwhere(temptestoutput == 1))):
        #     lines.append(ax.scatter(np.argwhere(temptestoutput == 1)[i][1], np.argwhere(temptestoutput == 1)[i][0], s=6, c='g', marker='.'))   #绿色
        #
        # for i in range(len(np.argwhere(temptestoutput == -1))):
        #     lines.append(ax.scatter(np.argwhere(temptestoutput == -1)[i][1], np.argwhere(temptestoutput == -1)[i][0], s=60, c='r',marker='*'))  #红色终点
        # for i in range(len(np.argwhere(temptestoutput == 2))):
        #     lines.append(ax.scatter(np.argwhere(temptestoutput == 2)[i][1], np.argwhere(temptestoutput == 2)[i][0], s=60, c='b',marker='o'))    #蓝色USV
        # plt.pause(0.01)
        # for each in lines:
        #     each.remove()
        # plt.show()
        # print(time.time() - start)



        for ship in self.map.friendly_ships:
            if ship.getuid() == 0:
                ship.move()
            self.check_target()
            self.check_obstacle()
            self.check_legal()

        if self.obsMoveBool == False:
            pass
        else:
            #添加圆形障碍物的移动（需在其移动方法中添加对所随机移动的下一位置的合法性判断，若下一位置不合法则保持原位置）
            for obstacle in self.map.obs:
               obstacle.obsRandomMove()

        #print('update_之后：输出ma.env_matrix()函数的地图形式：：')
        #print(self.map.env_matrix())

    #USV是否到达终点
    def check_target(self):
        target_x, target_y = self.map.target_coordinate()
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()
            if ((ship_x - target_x)*(ship_x - target_x) + (ship_y - target_y)*(ship_y - target_y)) <= ((ship.radius + self.map.target_radius)*(ship.radius + self.map.target_radius)):
                self.is_target_safe = False
                self.arriveTarget = 1
                break

    #USV是否碰到障碍物
    def check_obstacle(self):
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()

            for obstacle in self.map.obs:
                if ((ship_x - obstacle.x)*(ship_x - obstacle.x) + (ship_y - obstacle.y)*(ship_y - obstacle.y)) <= ((ship.radius + obstacle.radius)*(ship.radius + obstacle.radius)):
                    self.is_target_safe = False
                    self.arriveObstacle = 1
                    break

    #USV是否越界
    def check_legal(self):
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()

            width, height = self.map.width,self.map.height
            if ( ship_x < ship.radius  or ship_y < ship.radius or ship_x > (width - 1 - ship.radius) or ship_y > (height - 1 - ship.radius)):
                self.is_target_safe = False
                self.arriveUnlegal = 1

    def is_game_over(self):
        return not self.is_target_safe

    def start(self):
        i = 0
        while not self.is_game_over():
            #print('game-start-update前的地图形式：');#print(self.map.str2())
            self.update()
            i += 1
            # print ('----------------------------------------------------------------------------------------')
            #print ("press any key to continue");input()
        print ("game over!")
        print('是否到达终点：(0表示没，1表示到达)',self.arriveTarget)
        print('是否碰到障碍物：(0表示没，1表示碰到)', self.arriveObstacle)
        print('是否走出区域：(0表示没，1表示走出去)', self.arriveUnlegal)
        print('game-update次数',i)










class BasicPyGame(MyContinueGame):
    """基本的GUI引擎, 使用pygame"""

    def __init__(self, obsmove):
        super(BasicPyGame, self).__init__(obsmove)
        self.gui = pygame
        self.gui_init()

        self.obsMoveBool = obsmove  # 默认false，障碍物不随机移动


    def gui_init(self):
        self.gui_screen = self.gui.display.set_mode((800, 800), 0, 32)
        self.gui.display.set_caption("USV")


    #1.USV的五个定点（头1，左上2，左下3，右上4，右下5）根据中心点即USV位置点和其半径求解
    #注意顺序（头1，左上2，右上4，右下5，左下3），连接成一个闭合多边行
    #师弟参数格式
    # def allPointUSV(self, curPoint, USVradius):
    #     pointList = []
    #     halfR = USVradius/2
    #     pointList.append((curPoint[0], curPoint[1]-USVradius))
    #
    #     pointList.append((curPoint[0] - halfR, curPoint[1]))
    #
    #     pointList.append((curPoint[0] - halfR, curPoint[1] + USVradius))
    #     pointList.append((curPoint[0] + halfR, curPoint[1] + USVradius))
    #
    #     pointList.append((curPoint[0] + halfR, curPoint[1]))
    #
    #     return pointList


    #柯老师版参数
    def allPointUSV(self, curPoint, USVradius):
        pointList = []
        halfR = USVradius/2
        pointList.append((curPoint[0] - USVradius, curPoint[1]))
        pointList.append((curPoint[0], curPoint[1] + halfR))

        pointList.append((curPoint[0] + USVradius, curPoint[1] + halfR))
        pointList.append((curPoint[0] + USVradius, curPoint[1] - halfR))

        pointList.append((curPoint[0], curPoint[1] - halfR))
        return pointList

    def transferAngle(self, pointList, point, angle):
        angle = 360 - angle
        transList = []
        for i in range(len(pointList)):
            trans_x = (pointList[i][0] - point[0]) * cos(angle*pi/180) + (pointList[i][1] - point[1])*sin(angle*pi/180) + point[0]
            trans_y = (pointList[i][0] - point[0]) * sin(angle*pi/180) + (pointList[i][1] - point[1])*cos(angle*pi/180) + point[1]
            trans_x = float("%.4f" % trans_x)
            trans_y = float("%.4f" % trans_y)
            transList.append((trans_x, trans_y))
        return transList

    #2输入当前点(x,y)的List,所绕点(x0,y0),逆时针旋转的角度数Angle,输出是旋转后的五个点坐标
    #所绕点应该是移动后的USV位置，逆时针旋转的角度是USV.heading
    #https://www.cnblogs.com/MachineVision/p/5778677.html
    # def transferAngle(self, pointList, point, angle):
    #     transList = []
    #     for i in range(len(pointList)):
    #         trans_x = (pointList[i][0] - point[0]) * cos(angle*pi/180) + (pointList[i][1] - point[1])*sin(angle*pi/180) + point[0]
    #         trans_y = (pointList[i][0] - point[0]) * sin(angle*pi/180) + (pointList[i][1] - point[1])*cos(angle*pi/180) + point[1]
    #         trans_x = float("%.4f" % trans_x)
    #         trans_y = float("%.4f" % trans_y)
    #         transList.append((trans_x, trans_y))
    #     return transList


    #3.将transList中 每一点的坐标(x,y) 换成(y*y_unit,x*unit)
    def pyTrans(self, transList, xunit, yunit):
        pyTransList = []
        for i in range(len(transList)):
            px = transList[i][1] * yunit
            py = transList[i][0] * xunit
            pyTransList.append((px,py))
        #print('pygame画图上的坐标：', pyTransList)
        return pyTransList


    #4.获取当前速度方向：即self.ax 与 self.ay的向量合成，是当前速度方向



    def update(self):

        x_unit = 800.0 / self.map.width
        y_unit = 800.0 / self.map.height

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        self.gui_screen.fill((99,184,255))  # (255,255,255)白色填充

        for ship in self.map.friendly_ships:
            if ship.getuid() == 0:
                ship.move()
                #USV: ship_x * x_unit, ship_y * y_unit   此时USV的中心在画布的位置\\ship.heading
                USVPoint = self.allPointUSV((ship.x,ship.y), ship.radius)
                TransUSVPoint = self.transferAngle(USVPoint, (ship.x,ship.y), ship.heading)
                PyTransList = self.pyTrans(TransUSVPoint, x_unit, y_unit)
                self.gui.draw.polygon(self.gui_screen, (0, 255, 0), PyTransList)


                #获取船体当前加速度ship.get_curSpeedDirection()，是左下角是(0,0)的情况，
                #但这里计算的坐标是左上角是(0,0)的情况，所以变换关系是：ship.x - speedDirectPosy， ship.y + speedDirectPosx
                speedDirectPosx, speedDirectPosy = ship.get_curSpeedDirection()
                # af_speedDirectPosx = (ship.x - speedDirectPosy) * x_unit
                # af_speedDirectPosy = (ship.y + speedDirectPosx) * y_unit

                af_speedDirectPosx = (ship.x - speedDirectPosx) * x_unit
                af_speedDirectPosy = (ship.y + speedDirectPosy) * y_unit

                #加速度导引线
                self.gui.draw.line(self.gui_screen, (0, 255, 0), [ship.y * y_unit, ship.x * x_unit],[af_speedDirectPosy, af_speedDirectPosx], 1)

                # af_speedDirectPosx2 = (ship.x + speedDirectPosx) * x_unit
                # af_speedDirectPosy2 = (ship.y + speedDirectPosy) * y_unit
                # # 加速度导引线
                # self.gui.draw.line(self.gui_screen, (0, 255, 0), [ship.y * y_unit, ship.x * x_unit],[af_speedDirectPosy2, af_speedDirectPosx2], 1)


                #print('测试速度方向值：',speedDirectPosx, speedDirectPosy)

                # speedDirectPosx2, speedDirectPosy2 = ship.get_curSpeedDirection2()
                # af_speedDirectPosx2 = (speedDirectPosx2 + ship.x) * x_unit
                # af_speedDirectPosy2 = (speedDirectPosy2 + ship.y) * y_unit

                # speedDirectPosx3, speedDirectPosy3 = ship.get_curSpeedDirection3()
                # af_speedDirectPosx3 = (speedDirectPosx3 + ship.x) * x_unit
                # af_speedDirectPosy3 = (speedDirectPosy3 + ship.y) * y_unit

                #self.gui.draw.line(self.gui_screen, (0, 0, 0), [ship.y * y_unit, ship.x * x_unit],[af_speedDirectPosy2, af_speedDirectPosx2], 1)
                #self.gui.draw.line(self.gui_screen, (255, 0, 0), [ship.y * y_unit, ship.x * x_unit],[af_speedDirectPosy3, af_speedDirectPosx3], 1)


            self.check_target()
            self.check_obstacle()
            self.check_legal()

        if self.obsMoveBool == False:
            for obstacle in self.map.obs:
                # 画障碍物: 中心点 + radius
                self.gui.draw.circle(self.gui_screen, (0, 0, 0), [int(obstacle.y*y_unit), int(obstacle.x*x_unit)], int(obstacle.radius*x_unit))
            pass

        else:
            #添加圆形障碍物的移动（需在其移动方法中添加对所随机移动的下一位置的合法性判断，若下一位置不合法则保持原位置）
            for obstacle in self.map.obs:
               obstacle.obsRandomMove()
               # 画障碍物: 中心点 + radius
               self.gui.draw.circle(self.gui_screen, (0, 0, 0), [int(obstacle.y*y_unit), int(obstacle.x*x_unit)], int(obstacle.radius*x_unit))


        # 画终点：中心点 + radius
        target_x, target_y = self.map.target_coordinate()
        self.gui.draw.circle(self.gui_screen, (255, 0, 0), [int(target_y*y_unit), int(target_x*x_unit)], int(self.map.target_radius*x_unit))


        #更新
        self.gui.display.update()


        #print('update_之后：输出ma.env_matrix()函数的地图形式：：')
        #print(self.map.env_matrix())



    def start(self):
        i = 0
        while not self.is_game_over():
            self.update()
            i += 1
            #print('-----')
            #sleep(0.1)

        print("game over!")
        print('是否到达终点：(0表示没，1表示到达)', self.arriveTarget)
        print('是否碰到障碍物：(0表示没，1表示碰到)', self.arriveObstacle)
        print('是否走出区域：(0表示没，1表示走出去)', self.arriveUnlegal)

        # #print('FTList:',self.map.friendly_ships[0].FTList)
        # print('FTLen:',self.map.friendly_ships[0].FTLen)   #等于： print('FTList的长度:', len(self.map.friendly_ships[0].FTList))
        # print(self.map.friendly_ships[0].RecordList)

        print('game-update次数', i)

        self.gui.display.set_caption("Game Over!")
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            #self.gui.display.update()








#地图3*3
class PyGameXSWorld(MyContinueGame):
    """基本的GUI引擎, 使用pygame"""

    def __init__(self, obsmove):
        super(PyGameXSWorld, self).__init__(obsmove)
        self.gui = pygame
        self.gui_init()

        self.obsMoveBool = obsmove  # 默认false，障碍物不随机移动


    def gui_init(self):
        self.gui_screen = self.gui.display.set_mode((600, 600), 0, 32)
        self.gui.display.set_caption("USV")




    #柯老师版参数
    def allPointUSV(self, curPoint, USVradius):
        pointList = []
        halfR = USVradius/2
        pointList.append((curPoint[0] - USVradius, curPoint[1]))
        pointList.append((curPoint[0], curPoint[1] + halfR))

        pointList.append((curPoint[0] + USVradius, curPoint[1] + halfR))
        pointList.append((curPoint[0] + USVradius, curPoint[1] - halfR))

        pointList.append((curPoint[0], curPoint[1] - halfR))
        return pointList

    def transferAngle(self, pointList, point, angle):
        angle = 360 - angle
        transList = []
        for i in range(len(pointList)):
            trans_x = (pointList[i][0] - point[0]) * cos(angle*pi/180) + (pointList[i][1] - point[1])*sin(angle*pi/180) + point[0]
            trans_y = (pointList[i][0] - point[0]) * sin(angle*pi/180) + (pointList[i][1] - point[1])*cos(angle*pi/180) + point[1]
            trans_x = float("%.4f" % trans_x)
            trans_y = float("%.4f" % trans_y)
            transList.append((trans_x, trans_y))
        return transList



    #3.将transList中 每一点的坐标(x,y) 换成(y*y_unit,x*unit)
    def pyTrans(self, transList, xunit, yunit):
        pyTransList = []
        for i in range(len(transList)):
            px = transList[i][1] * yunit
            py = transList[i][0] * xunit
            pyTransList.append((px,py))
        #print('pygame画图上的坐标：', pyTransList)
        return pyTransList


    #4.获取当前速度方向：即self.ax 与 self.ay的向量合成，是当前速度方向



    def update(self):

        x_unit = 600.0 / self.map.width
        y_unit = 600.0 / self.map.height

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        self.gui_screen.fill((99,184,255))  # (255,255,255)白色填充

        for ship in self.map.friendly_ships:
            if ship.getuid() == 0:
                ship.move()
                #USV: ship_x * x_unit, ship_y * y_unit   此时USV的中心在画布的位置\\ship.heading
                USVPoint = self.allPointUSV((ship.x,ship.y), ship.radius)
                TransUSVPoint = self.transferAngle(USVPoint, (ship.x,ship.y), ship.heading)
                PyTransList = self.pyTrans(TransUSVPoint, x_unit, y_unit)
                self.gui.draw.polygon(self.gui_screen, (0, 255, 0), PyTransList)


                #获取船体当前加速度ship.get_curSpeedDirection()，是左下角是(0,0)的情况，
                #但这里计算的坐标是左上角是(0,0)的情况，所以变换关系是：ship.x - speedDirectPosy， ship.y + speedDirectPosx
                speedDirectPosx, speedDirectPosy = ship.get_curSpeedDirection()

                af_speedDirectPosx = (ship.x - speedDirectPosx) * x_unit
                af_speedDirectPosy = (ship.y + speedDirectPosy) * y_unit

                #加速度导引线
                self.gui.draw.line(self.gui_screen, (0, 255, 0), [ship.y * y_unit, ship.x * x_unit],[af_speedDirectPosy, af_speedDirectPosx], 1)

            self.check_target()
            self.check_obstacle()
            self.check_legal()

        if self.obsMoveBool == False:
            for obstacle in self.map.obs:
                # 画障碍物: 中心点 + radius
                self.gui.draw.circle(self.gui_screen, (0, 0, 0), [int(obstacle.y*y_unit), int(obstacle.x*x_unit)], int(obstacle.radius*x_unit))
            pass

        else:
            #添加圆形障碍物的移动（需在其移动方法中添加对所随机移动的下一位置的合法性判断，若下一位置不合法则保持原位置）
            for obstacle in self.map.obs:
               obstacle.obsRandomMove()
               # 画障碍物: 中心点 + radius
               self.gui.draw.circle(self.gui_screen, (0, 0, 0), [int(obstacle.y*y_unit), int(obstacle.x*x_unit)], int(obstacle.radius*x_unit))


        # 画终点：中心点 + radius
        target_x, target_y = self.map.target_coordinate()
        self.gui.draw.circle(self.gui_screen, (255, 0, 0), [int(target_y*y_unit), int(target_x*x_unit)], int(self.map.target_radius*x_unit))


        #更新
        self.gui.display.update()


    # USV是否越界
    def check_legal(self):
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()

            width, height = self.map.width, self.map.height

            if (ship_x < ship.radius or ship_y < ship.radius or ship_x > (width - ship.radius) or ship_y > (
                    height - ship.radius)):
                self.is_target_safe = False
                self.arriveUnlegal = 1




    def start(self):
        i = 0
        while not self.is_game_over():
            self.update()
            i += 1
            #print('-----')
            #sleep(0.1)

        print("game over!")
        print('是否到达终点：(0表示没，1表示到达)', self.arriveTarget)
        print('是否碰到障碍物：(0表示没，1表示碰到)', self.arriveObstacle)
        print('是否走出区域：(0表示没，1表示走出去)', self.arriveUnlegal)
        #
        # #print('FTList:',self.map.friendly_ships[0].FTList)
        print('FTLen:',self.map.friendly_ships[0].FTLen)   #等于： print('FTList的长度:', len(self.map.friendly_ships[0].FTList))
        print(self.map.friendly_ships[0].RecordList)
        print(i)

        self.gui.display.set_caption("Game Over!")
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            #self.gui.display.update()







class MyContinueGameModify(MyContinueGame):
    """基本的GUI引擎, 使用pygame"""

    #修正了是否越界函数：USV是否越界
    def check_legal(self):
        for ship in self.map.friendly_ships:
            ship_x, ship_y = ship.coordinate()

            width, height = self.map.width, self.map.height

            if (ship_x < ship.radius or ship_y < ship.radius or ship_x > (width - ship.radius) or ship_y > (
                    height - ship.radius)):
                self.is_target_safe = False
                self.arriveUnlegal = 1


