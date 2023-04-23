import math
from math import sqrt,atan2, sin, cos, pi

from Environment.const import MISSILES_EMEMY, MISSILES_RED


isclose = lambda x,y,e=2 : y-e<x<y+e
isclose2 = lambda x,y,e=1e-2 : y-e<x<y+e

isclose_100m = lambda x,y=0,e=0.1 : y-e<x<y+e # 0.1Px = 100m
isclose_1000m = lambda x,y=0,e=1 : y-e<x<y+e # 0.1Px = 100m

def check_distance(x1, y1, x2, y2, d, EPSILON = 5):
    dis = sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return d-EPSILON < dis < d+EPSILON

xy_op = [(1, -1), (-1, -1), (-1, 1), (1, 1),]

class Missile(object):
    def __init__(self, speed=-1, angle=0., type='', x=100., y=100., 
                 height=0, tarx=-1.,tary=-1., typename='', **kwargs):
        self.initx, self.inity = x,y
        self.height = height
        self.x, self.y = x, y
        #self.quadx, self.quady = 0., 0.  # quadrant coordinate
        self.quadx, self.quady = self.x - tarx, tary - self.y
        self.type = type
        self.speed = speed
        self.distance = 0
        self.typename = typename
        self.typeid = -1
        self.color = (0,0,0)
        self.hitx, self.hity = 0, 0
        
        #self.tarspeed = tarspeed
        self.maxtravel = 0
        self.travelled = 0
        
        self.lock = False
        self.delete = False     # intercept or hit
        self.will_delete = False
        self.intercept = False  # intercept
        self.hit = False        # hit target

        if tarx > 0: # target exists
            #print(x, tarx, y, tary)
            #self.angle = atan((tary-y)/(tarx-x))
            self.tarx, self.tary = tarx, tary
            self.angle = atan2(tary-y, tarx-x)
            distance = sqrt((tary-y)**2 + (tarx-x)**2)
            self.distance = distance
            self.countdown = distance / speed
        else:
            self.angle = angle
            self.countdown = 0.
        #print(self.angle/pi * 180)
        degree = self.angle/pi * 180
        if -180 <= degree < -90:
            opx, opy = xy_op[3]
        elif -90 <= degree < 0:
            opx, opy = xy_op[0]
        elif 0 <= degree < 90:
            opx, opy = xy_op[1]
        elif 90 <= degree <= 180:
            opx, opy = xy_op[2]
        #self.cos, self.sin = opx * cos(self.angle),opy * sin(self.angle)
        self.cos, self.sin =  cos(self.angle), sin(self.angle)
        
        self.__dict__.update(kwargs)
        #print(self.__dict__)

    def move(self, time=1.0):
        time = min(time, self.countdown)
        x, y = self.x, self.y
        d = self.speed * time
        #dx, dy = d * cos(self.angle), d * sin(self.angle)
        dx, dy = d*self.cos, d*self.sin

        #self.hit = True
        # self.countdown -= time

        #print('cntdown', self.countdown)
        self.x, self.y = x + dx, y + dy  # pygame coordinate
        self.quadx, self.quady = self.x-self.tarx, self.tary-self.y
        self.distance = sqrt((self.tary-self.y)**2 + (self.tarx-self.x)**2)
        # if isclose_100m(self.distance, .0):
        #     self.hit = True
        #     self.delete = True
        #     self.countdown = 0.0
        #     print(f'~~ hit : {self.name} hit the target!')
        
        # if isclose2(self.countdown,0.0) and self.intercept:
        #     if self.will_delete:
        #         self.delete = True
        #     else:
        #         self.intercept = False
        
        if self.lock:
            distance = sqrt((self.hity-self.y)**2 + (self.hitx-self.x)**2)
            if isclose_100m(distance, .0, 0.5):
                if self.will_delete:
                    self.delete = True
                    return
                else:
                    print(f'~~~~~~~~~~> missile {self.name} unlock! <~~~~~~~~~~')
                    self.lock = False
        
        #self.delete = self.hit or self.intercept
        self.countdown -= time
        if isclose2(self.countdown, 0, 0.1):
            self.delete = True
    
    def move_auto(self, tarqx, tarqy, tarh, time=1.0):
        # assert self.height <= tarh
        time = min(time, self.countdown)
        #self.countdown -= time
        d = self.speed*time
        
        x,y,h = tarqx-self.quadx, tarqy-self.quady, tarh-self.height
        norm = sqrt(x*x + y*y + h*h)
        dx,dy,dh = x/norm*d, y/norm*d, h/norm*d
        self.x += dx
        self.y += dy
        self.height += dh
        self.quadx, self.quady = self.x-self.tarx, self.tary-self.y
        self.travelled += d
        
        ## 超出最大射程
        if self.travelled > self.maxtravel:
            print(f'==>{self.name} maxtravel: {self.maxtravel} used out. <==')
            self.delete = True
        
        if isclose_100m(self.distance, .0):
            self.hit = True
            self.delete = True
            self.countdown = 0.0
            print(f'~~ hit : {self.name} hit the target! ~~')
        
        self.countdown -= time
        
    
    def hit_point(self, x1, y1, v1, x2, y2, v2):
        """
        x1, y1 : 当前敌方导弹的坐标 (pygame coordinate)
        x2, y2 : 当前我方舰艇的坐标 (quadrant coordinate)
        v1 : 敌方导弹 速度
        v2 : 拦截导弹 速度
        """
        good_distance = False
        tx, ty, x, y = .0, .0, .0, .0
        t, dt, tall = .0, .1, self.countdown
        
        while t < tall:
            t += dt
            d1 = v1 * t
            dx, dy = d1 * self.cos, d1 * self.sin
            x, y = x1 + dx, y1 + dy
            tx, ty = x - self.tarx, self.tary - y
            d2 = v2 * t
            good_distance = check_distance(tx, ty, x2, y2, d2)
            
            if good_distance: break
        
        """ 碰撞点x, 碰撞点y, 碰撞时间 """
        if good_distance:
            #print('==> inter1', x, y, tx, ty, t)
            #print('==> inter2', x, y, tx+500, 500-ty, t)
            #print(x, y, tx, ty, t)
            return x, y, tx, ty, t
        
        print('can not found hit point')
        return -1., -1., -1., -1., -1.

    def __del__(self,):
        print(f'== del missile : {self.name} ==')
    
    def __repr__(self,):
        return f'{self.__dict__}'

if __name__ == "__main__":
    pi = pi
    #m = Missile(speed=10, angle=pi/4)
    #m = Missile(**{'x' : 200, 'y' : 300, 'tarx' : 250, 'tary' : 250, 'speed' : 20, 'type' : 'Unknow', 'name' : 'm1'})
    #m = Missile(speed=10, x=300, y=300, tarx=500, tary=300, name='m1')
    m = Missile(speed=10, x=300, y=300, tarx=500, tary=500, name='m1')
    #m = Missile(speed=10, x=300, y=300, tarx=300, tary=500, name='m1')
    #m = Missile(speed=10, x=300, y=300, tarx=200, tary=500, name='m1')
    #m = Missile(speed=10, x=300, y=300, tarx=100, tary=300,name='m1')
    #m = Missile(speed=10, x=300, y=300, tarx=100, tary=100, name='m1')
    #m = Missile(speed=10, x=300, y=300, tarx=300, tary=200, name='m1')
    #m = Missile(speed=10, x=300, y=300, tarx=500, tary=200, name='m1')
    import time
    for t in range(2):
        m.move()
        # print(t, m.x, m.y)
        #print(t, m.quadx, m.quady)
        m.hit_point(m.quadx, m.quady, m.speed, 0, 50, 20)
        time.sleep(1.)

