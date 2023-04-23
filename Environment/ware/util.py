import numpy.random as npr
from numpy import pi, cos, sin, sqrt

from Environment.const import PROBABILITY, AIRCRAFT_X, AIRCRAFT_Y

import sys

def Possion_coordinate():
    theta = npr.uniform(0, 2*pi)
    radius = npr.uniform(210, 350)
    
    x = radius * cos(theta) + 300
    y = radius * sin(theta) + 300
    print(x,y)


def intercept_prob(red_msl_type, blue_msl_type):
    return PROBABILITY[red_msl_type][blue_msl_type]



def line_intersect_circle(circle_param, start_pt, end_pt):
    # 计算圆 与 直接相交的点, 并进行筛选
    # modified by zwq. 2022.12.02
    # https://blog.csdn.net/wyll19980812/article/details/124769513
    
    # `circle_param` is the circle parameter, `start_pt` and `end_pt` is the two end of the line
    #
    x0, y0, r0 = circle_param
    x1, y1 = start_pt
    x2, y2 = end_pt
    # if r0 == 0: return [[x1, y1]]
    if x1 == x2:
        if abs(r0) >= abs(x1 - x0):
            p1 = x1, round(y0 - sqrt(r0 ** 2 - (x1 - x0) ** 2), 5)
            p2 = x1, round(y0 + sqrt(r0 ** 2 - (x1 - x0) ** 2), 5)
            inp = [p1, p2]
            # select the points lie on the line segment
            inp = [p for p in inp if p[0] >= min(x1, x2) and p[0] <= max(x1, x2)]
        else:
            inp = []
    else:
        k = (y1 - y2) / (x1 - x2)
        b0 = y1 - k * x1
        a = k ** 2 + 1
        b = 2 * k * (b0 - y0) - 2 * x0
        c = (b0 - y0) ** 2 + x0 ** 2 - r0 ** 2
        delta = b ** 2 - 4 * a * c
        if delta >= 0:
            p1x = round((-b - sqrt(delta)) / (2 * a), 5)
            p2x = round((-b + sqrt(delta)) / (2 * a), 5)
            p1y = round(k * p1x + b0, 5)
            p2y = round(k * p2x + b0, 5)
            inp = [(p1x, p1y), (p2x, p2y)]
            # select the points lie on the line segment
            inp = [p for p in inp if p[0] >= min(x1, x2) and p[0] <= max(x1, x2)]
        else:
            inp = []
    xyd = [(x,y, round(sqrt((x-x1)**2 + (y-y1)**2), 5)) for x,y in inp]
    
    if len(xyd) < 2 : return xyd
    #print('==> x,y,distance', xyd)
    return [xyd[1]] if xyd[0][2]>xyd[1][2]  else [xyd[0]] 
    # return inp

# print(line_intersect_circle((20, 20, 200), (300, 340), (0, 0)))
# print(line_intersect_circle((0, 0, 200), (200, 200), (-200, 200))) #haha
# print(line_intersect_circle((0, 0, 200), (200, 200), (-200, -200)))
# print(line_intersect_circle((0, 0, 3), (200, 200), (200, 500)))
# print(line_intersect_circle((0, 0, 400), (200, 200), (200, 300)))

isclose_100m = lambda x,y=0,e=1 : y-e<x<y+e # 0.1Px = 100m

def hit_point(blue, red):
    bx, by, bqx, bqy,bv, cosb, sinb = blue
    rqx, rqy, rv = red
    d = sqrt(bqx**2 + bqy**2)
    cntdown = d / bv
    #AIRCRAFT_X, AIRCRAFT_Y
    # dis_t_, dis_br_ = [], []
    t, dt = 0.01, 0.1
    while t < cntdown:
        d1 = bv * t
        dx, dy = d1 * cosb, d1 * sinb
        tx, ty = bx + dx, by + dy
        btqx, btqy = tx - AIRCRAFT_X, AIRCRAFT_Y - ty
        #dis_t  = sqrt((btqx-bqx)**2 + (btqy-bqy)**2) # blue move distance in t
        dis_br = sqrt((btqx-rqx)**2 + (btqy-rqy)**2)  # blue-red distance
        dis_vt = rv * t
        # dis_t_.append(dis_t)
        # dis_br_.append(dis_br)
        # print('blue', btqx, btqy, 't', t, 'dis', dis_t, dis_br)
        if isclose_100m(dis_vt, dis_br, 0.4): 
            # print('------------> 有解 <------------', round(tx,3), round(ty,3), round(btqx,3), round( btqy,3))
            return tx, ty#, dis_t_, dis_br_
        t += dt
    # print('~~~~~~~~~~~~~> 无解！ <~~~~~~~~~~~~~')
    # sys.exit(0)
    return 0,0#, dis_t_, dis_br_

# blue = (127.53396423211476, 531.1982532139858, -372.4660357678853, -31.198253213985822, 1.02, 0.9965103708259718, -0.08346904118464639)
# red = (-20, 20, 0.9180000000000001)

def hit_point2(blue, red):
    bx, by, bqx, bqy,bv, cosb, sinb = blue
    rqx, rqy, rv = red
    d = sqrt(bqx**2 + bqy**2)
    cntdown = d / bv
    #AIRCRAFT_X, AIRCRAFT_Y
    dis_t_, dis_br_ = [], []
    t, dt = 0.01, 0.1
    while t < cntdown:
        d1 = bv * t
        dx, dy = d1 * cosb, d1 * sinb
        tx, ty = bx + dx, by + dy
        btqx, btqy = tx - AIRCRAFT_X, AIRCRAFT_Y - ty
        dis_t  = rv * t 
        dis_br = sqrt((btqx-rqx)**2 + (btqy-rqy)**2) 
        dis_t_.append(dis_t)
        dis_br_.append(dis_br)
        # print('blue', btqx, btqy, 't', t, 'dis', dis_t, dis_br)
        if isclose_100m(dis_t, dis_br, 0.1): 
            print('------------> 有解 <------------', round(tx,3), round(ty,3), round(btqx,3), round( btqy,3))
            return tx, ty, dis_t_, dis_br_
        t += dt
    print('~~~~~~~~~~~~~> 无解！ <~~~~~~~~~~~~~')
    # sys.exit(0)
    return 0,0, dis_t_, dis_br_

if __name__ == "__main__":
    blue =(853.5085816650629, 686.6597166481754, 353.50858166506293, -186.6597166481754, 1.02, -0.8842961988721, -0.4669263674931578) 
    red = (20, -20, 0.9180000000000001)
    # hit_point(blue, red)
    
    _,_, d1, d2 = hit_point2(blue, red)
    import matplotlib.pyplot as plt
    plt.plot(range(len(d1)), d1)
    plt.plot(range(len(d2)), d2)


"""
(127.53396423211476, 531.1982532139858, -372.4660357678853, -31.198253213985822, 1.02, 0.9965103708259718, -0.08346904118464639)
 (-20, 20, 0.9180000000000001)
 
 blue -17.616465497638046 -1.4755787066535504 t 349.1100000000109 356.0922000000112 356.16508461960666
------------> 有解 <------------ 482.38353450236195 501.47557870665355

(853.5085816650629, 686.6597166481754, 353.50858166506293, -186.6597166481754, 1.02, -0.8842961988721, -0.4669263674931578) 
 (20, -20, 0.9180000000000001)
 

"""
if __name__ == "_main__":
    print(intercept_prob('Red-A-MidFar', 'Blue-HighFly'))
    print(intercept_prob('Red-B-Mid', 'Blue-NearSea'))
