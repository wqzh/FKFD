

from numpy import pi, cos, sin, atan2, sqrt



Ma = 340  # 1Ma = 340m/s
Kilo = 1000 # 1Km
Px = 500    # 1px = 500m
InfDistance = 1000 # 1000Km

FPS = 30
INTERVAL = 1/FPS


MISSILES = { # 'typename' : info
    'Red-A' : {'name': 'A型导弹-中远程', 'maxtravel': 200*Kilo, 'maxspeed':2.7*Ma,},
    'Red-B' : {'name': 'B型导弹-中程', 'maxtravel': 70*Kilo, 'maxspeed':4*Ma,},
    'Blue-NearSea' : {'name':'掠海飞行', 'height': 200, 'maxspeed':0.9*Ma, 
                      'maxtravel': InfDistance*Kilo},
    'Blue-HighFly' : {'name':'高空飞行', 'height': 20000, 'maxspeed':3*Ma, 
                      'maxtravel': InfDistance*Kilo}
}

PROBABILITY = {
    'Red-A' : {'Blue-NearSea':0.7, 'Blue-HighFly':0.4}, 
    'Red-B' : {'Blue-NearSea':0.9, 'Blue-HighFly':0.9}, 
}


class Missile():
    def __init__(self, speed, angle, typename, tarname, tartype,
                 x, y, tarx, tary):
        self.initx, self.inity = x, y
        self.x, self.y = x, y
        self.quadx, self.quady = self.x - tarx, tary - self.y
        self.tarx, tary = tarx, tary # 目标位置
        self.tarname = tarname       # 目标名称
        self.tartype = tartype       # 目标类型
        
        self.typename = typename     # 本导弹类型
        self.maxtravel = -1   # 最大射程
        self.travelled = -1   # 已飞行距离
        self.interprob = -1  # 拦截成功概率
        self.speed = speed
        
        self.lock = False   # 操作锁
        self.delete = True  # 删除标志
        
    def move():
        pass

