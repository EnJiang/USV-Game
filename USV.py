#coding=utf-8

class StaticUSV(object):
  """一个静态的USV类,move方法将会留空,这表示此类USV不可行动"""
  def __init__(self, uid, x, y, env):
    '''每艘USV的独立id,可以用来区分各舰'''
    self.id = uid
    '''env是指当前USV所在的环境,它指向当前游戏中这艘USV所在的Map类实例'''
    self.env = env
    self.x, self.y = x, y
    self.speed = 0.0
    self.angularSpeed = 0.0
    self.direction = 0.0
    self.isEnemy = False

  def decisionAlgorithm(self):
    '''decisionAlgrithm是指导USV运动的方法,返回一个自定义的action字典'''
    pass

  def move(self):
    '''USV运动的主方法,根据action来调用其它辅助函数完成下一时刻USV位置的计算'''
    pass

  def isDecisionLegal(self, decisionX, decisionY):
    '''判断USV决定要去的位置是否合法;在这个基本的函数里,所有舰艇不得走出地图范围,不得走到
    其它舰艇已经占用的位置;友军舰艇不得走到被保护的目标点.'''
    weight, height = self.env.weight, self.env.height
    if(decisionX < 0 or decisionY < 0 or decisionX > weight - 1 or decisionY > height - 1):
      return False

    occupied = False
    for ship in self.env.ships:
      if(ship.id == self.id):
        continue
      shipX, shipY = ship.coordinate()
      if(shipX == decisionX and shipY == decisionY):
        occupied = True

    if(not self.isEnemy):
      tX, tY = self.env.targetCoordinate()
      if(tX == decisionX and tY == decisionY):
        occupied = True

    if(occupied):
      return False

    return True

  def turn(self, clockwise):
    '''这一函数描绘本艘USV在一单位时间内如何改变自身方向,因此其作用是在顺时针或逆时针方向上
    增加当前USV角速度的绝对值(角度变化=角速度*1时间单位=角速度的绝对值)'''
    if(clockwise):
      self.direction += self.angularSpeed
      if(self.direction >= 360):
        self.direction -= 360
    else:
      self.direction -= self.angularSpeed
      if(self.direction < 0):
        self.direction += 360

  def coordinate(self):
    '''返回本USV的位置'''
    return self.x,self.y

  def setAsEnemy(self):
    '''将本USV定义为敌方(进攻方)'''
    self.isEnemy = True

  def setAsFriendly(self):
    '''将本USV定义为友军(防守方)'''
    self.isEnemy = False


class OneStepUSV(StaticUSV):
  """一个简单的USV类,在网格上它一次只能走动一步.每一时间单位,这种USV能够瞬时的改变自己的角速度,然后转动,最后向
  转动后的方向上移动一格."""
  def __init__(self, uid, x, y, env):
    super(OneStepUSV, self).__init__(uid, x, y, env)
    self.speed = 1

  def decisionAlgorithm(self):
    '''这种USV的action字典有三个参数:1.stay,如果设为True,代表USV决定不行动,后面的参数被忽略;
    2.clockwise,转动方向是否是顺时针;3.angularSpeed角速度.
    如果stay参数为False,USV将会根据clockwise的指示转动angularSpeed度,然后前进一步.注意由于
    此模型下angularSpeed只能为90的倍数'''
    exampleAction = {'stay':False,'clockwise':True,'angularSpeed':90.0}
    exampleAction1 = {'stay':True,'clockwise':True,'angularSpeed':0}
    exampleAction2 = {'stay':False,'clockwise':False,'angularSpeed':270.0}
    raise Exception("请覆盖decisionAlgorithm方法!")

  def move(self):
    action = self.decisionAlgorithm()
    if(not action["stay"]):
      self.updateDirection(action)
      self.updateCoordinate()

  def updateDirection(self, action):
    self.angularSpeed = action["angularSpeed"]
    self.turn(action["clockwise"])

  def updateCoordinate(self):
    if(self.direction == 0.0):
      self.x -= self.speed
    elif(self.direction == 90.0):
      self.y -= self.speed
    elif(self.direction == 180.0):
      self.x += self.speed
    elif(self.direction == 270.0):
      self.y += self.speed
    else:
      raise Exception("OneStepUSV的direction属性应该是正交角度,然而,得到了 %f 度" % self.direction)
    # print "我是%d号船,我现在走到了(%f,%f)"%(self.id,self.x,self.y)
