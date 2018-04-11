# coding=utf-8

import random

class CircleObstacle(object):
    '''静态圆形障碍物，圆心坐标(x,y), 半径radius， 当前环境env指map类实例'''
    def __init__(self, uid, x, y, radius, env):
        self.uid = uid
        self.x, self.y = x, y
        self.radius = radius
        self.env = env

    #障碍物圆的左右边界
    def obsXminXmax(self):
        return self.x - self.radius, self.x + self.radius

    #障碍物圆的上下边界
    def obsYminYmax(self):
        return self.y - self.radius, self.y + self.radius

    def obsGetUid(self):
        return self.uid


    #障碍物下一时刻的位置是否合法,return True合法，False不合法
    #（1.越出边界---圆心是否在比原地图缩小圆半径长度的新地图中
    #2.走到目的地---目的地坐标是否在圆障碍物的半径内
    #3.走到USV---USV的圆心坐标与障碍物圆的圆心坐标差值是否在（两圆半径之和范围）
    #4.走到其他障碍物区域--两障碍物圆心距离是否在（两圆半径之和范围））
    def obsCheckLegal(self, coordinateX, coordinateY):
        #越出边界
        if( (coordinateX < self.radius) or (coordinateY < self.radius) or coordinateX > (self.env.width - 1 - self.radius) or coordinateY > (self.env.height - 1 - self.radius)):
            #print('越出边界')
            return False

        #走到终点目的地
        if ( (coordinateX - self.env.target_x)*(coordinateX - self.env.target_x) + (coordinateY - self.env.target_y)*(coordinateY - self.env.target_y) ) <= ((self.radius + self.env.target_radius)*(self.radius + self.env.target_radius)):
            #print('走到终点目的地')
            return False

        #走到USV
        for ship in self.env.friendly_ships:
            if( (coordinateX - ship.x)*(coordinateX - ship.x) + (coordinateY - ship.y)*(coordinateY - ship.y) ) <= ((ship.radius + self.radius)*(ship.radius + self.radius)):
                #print('走到USV')
                return False


        countCollision = -1
        #走到其他障碍物区域(注意：当前位置和其本身的障碍物肯定是相撞的)
        for obs in self.env.obs:
            if ( (coordinateX - obs.x)*(coordinateX - obs.x) + (coordinateY- obs.y)*(coordinateY- obs.y) ) <= ( (obs.radius + self.radius)*(obs.radius + self.radius) ):
                countCollision += 1
        if countCollision > 0:
            #print('走到其他障碍物区域',countCollision)
            return False

        #以上情况都合法，则返回True
        return True


    def obsRandomMove(self):
        rand1, rand2 = random.uniform(-1, 1), random.uniform(-1, 1)
        afterRandX, afterRandY = self.x + rand1, self.y + rand2
        #print('圆形障碍物--初始位置：',self.x, self.y)
        if (self.obsCheckLegal(afterRandX, afterRandY)):
            self.x, self.y = afterRandX, afterRandY
            #print('圆形障碍物--随机移动后的位置：', self.x, self.y)



