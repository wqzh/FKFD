
############################# 语言设置 #############################
LANGUAGE = 'CN'
#LANGUAGE = 'EN'

if LANGUAGE == 'CN':
    DECISION_STR_ = "步骤决策用时:"
    COMMAND_STR_  = "指挥单元用时:"
    ACTION_STR_   = "动作单元用时:"
    LEGENDS = ['航母', '驱逐舰', '护卫舰', '拦截导弹-A(中远程)', '拦截导弹-B(中程)', 
                 '掠海飞行导弹(敌)', '高空飞行导弹(敌)']
    SUCCESS_STR_  = "成功 :"
    FAIL_STR_  =    "失败 :"
    EPISODE_STR_ = "轮数:"
    FRAME_STR_ = "帧:"
    SIMULATE_STR_ = "仿真时间:"
    H_ = '时'
    M_ = '分'
    S_ = '秒'
    
elif LANGUAGE == 'EN':
    DECISION_STR_ = "Decision time     :"
    COMMAND_STR_  = "Command Uint time :"
    ACTION_STR_   = "Action Uint time  :"
    LEGENDS = ['Aircraft', 'Destroyer', 'Frigate', 'Interceptor-A', 'Interceptor-B', 
              'Enemy-NearSea', 'Enemy-HighFly']
    SUCCESS_STR_  = "success: "
    FAIL_STR_  = "  fail : "
    EPISODE_STR_ = "episode:"
    FRAME_STR_ = "frame:"
    SIMULATE_STR_ = "simulation time:"
    H_ = 'H'
    M_ = 'M'
    S_ = 'S'


############################# 运行配置 #############################

RADAR_DSIPLAY = True  # 开启雷达显示 True False

## 每秒帧数
FPS = 5
FRAME_INTERVAL = 1/FPS
# FRAME_INTERVAL = 0.01

ACCERATE_SIMULATE = True
REAL_TIME = not ACCERATE_SIMULATE

RADAR_ROTATION = 0.005  # sleep None
# RADAR_ROTATION = 0.04  # FPS


############################### 全局常量#############################

SUCCESS, FAIL = 0, 0
EPISODE = SUCCESS + FAIL - 1

SUCCESS_STR, FAIL_STR  = '', ''
EPISODE_STR = ''

############################### 基本常数 #############################
# (全部换算成以'米'为单位)
Ma = 340  # 1Ma = 340m/s
KM = 1000 # 1Km
Px = 1000    # 1px = 1000m
InfDistance = 1000 # 1000Km




## 坐标常量 px
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000

AIRCRAFT_X, AIRCRAFT_Y = 500, 500
DESTROYER_DIST = 20


############################# 颜色常量 #############################

colors = {
   'bg'    : (222, 222, 222),
'aircft' : (255, 0, 0),
'destroyer': (240, 128, 128),
 'frigate' : (204, 0, 102),
'our-missile' : (0, 100, 102),
'ene-missile' : (0, 51, 255)
}

CLR_BACKGROUND = (222, 222, 222)
CLR_RED_AIRCRAFT = (255, 0, 0)
CLR_RED_DESTROYER = (240, 128, 128)
CLR_RED_FRIGATE = (204, 0, 102)

"""
CLR_RED_MISSILE_A = (120, 100, 102)
CLR_RED_MISSILE_B =  (51, 102, 153)
CLR_BLUE_NEARSEA = (100, 51, 255)
CLR_BLUE_HIGHFLY = (192, 96, 0)
"""

CLR_RED_MISSILE_A = (255, 32, 0)
CLR_RED_MISSILE_B =  (255, 64, 0)
CLR_BLUE_NEARSEA = (0, 64, 255)
CLR_BLUE_HIGHFLY = (0, 32, 255)


CLR_BALCK = (0,0,0)

CLR_RED = (255,0,0)
CLR_GREEN = (0, 255, 0)
CLR_BLUE = (0, 0, 255)

CLR_25KM_CIRCLE = (240, 20, 20)
CLR_50KM_CIRCLE = (200, 20, 20)
CLR_200KM_CIRCLE = (150, 20, 20)
CLR_400KM_CIRCLE = (70, 20, 20)

CLR_KM_TITLE = (130, 151, 205)
CLR_RADAR = (102, 255, 196)

UNAVAILABLE_COLOR = CLR_RED
AVAILABLE_COLOR = CLR_GREEN #CLR_RED_DESTROYER

CLRS = (CLR_RED_AIRCRAFT, CLR_RED_DESTROYER, CLR_RED_FRIGATE, 
        CLR_RED_MISSILE_A, CLR_RED_MISSILE_B, CLR_BLUE_NEARSEA, CLR_BLUE_HIGHFLY)



############################# 坐标设置  #############################
x = 40
LOCS = [(x, 5), (x, 26), (x, 45), (x, 75), (x, 100), (x,145), (x,165)]

LOC_MISSILE_STR = (750, 20)
LOC_DECISION_STR = (750, 40)
LOC_COMMAND_STR = (750, 65)
LOC_ACTION_STR = (750, 90)

LOC_SUCCESS_STR = (550, 20)
LOC_FAIL_STR = (550, 45)

LOC_EPISODE_STR = (350, 25)
LOC_FRAME_STR = (350, 55)
LOC_SIMULATE_STR = (300, 80)

#####################################################################



############################# 导弹参数#############################
# 所有的距离单位都为 米(meter), 1像素表示500m或者1000m 

MISSILES_EMEMY = {
    1 : {'color': CLR_BLUE_NEARSEA, 'maxspeed': 0.9*Ma/Px, 'maxtravel': InfDistance*KM/Px},
    2 : {'color': CLR_BLUE_HIGHFLY, 'maxspeed': 3*Ma/Px, 'maxtravel': InfDistance*KM/Px}
}
MISSILES_RED = {
    1 : {'color': CLR_RED_MISSILE_A, 'maxspeed': 2.7*Ma/Px, 'maxtravel': 200*KM/Px},
    2 : {'color': CLR_RED_MISSILE_B, 'maxspeed': 4*Ma/Px, 'maxtravel': 70*KM/Px}
}



MISSILES_EMEMY_ID = {
    1: '掠海飞行',
    2 :'高空飞行'
}
MISSILES_RED_ID = {
    1 : 'A型导弹-中远程', 
    2 : 'B型导弹-中程'
}

MISSILES = { # 'typename' : info
    'Red-A-MidFar' : {'name': 'A型导弹-中远程', 'id':1, 'maxtravel': 200*KM/Px, 'maxspeed':2.7*Ma/Px,},
    'Red-B-Mid' :    {'name': 'B型导弹-中程',  'id':2, 'maxtravel': 70*KM/Px, 'maxspeed':4*Ma/Px,},
    'Blue-NearSea' : {'name':'掠海飞行', 'id':1, 'height': 200, 'maxspeed':0.9*Ma/Px, 
                      'maxtravel': InfDistance*KM/Px},
    'Blue-HighFly' : {'name':'高空飞行', 'id':2, 'height': 20000, 'maxspeed':3*Ma/Px, 
                      'maxtravel': InfDistance*KM/Px}
}
#            500m      1000m
# 2.7Ma =  1.836 Px   0.918 Px
# 4Ma   =  2.72 Px    1.36 Px

# 0.9Ma =  0.612 Px   0.306 Px
# 3Ma  =   2.04 Px    1.02 Px


## 拦截概率
PROBABILITY = {
    'Red-A-MidFar' : {'Blue-NearSea':0.7, 'Blue-HighFly':0.4}, 
    'Red-B-Mid'    : {'Blue-NearSea':0.9, 'Blue-HighFly':0.9}, 
}

PROBABILITY_ = {
    1 : {1: 0.7, 2 : 0.4},
    2 : {1: 0.9, 2 : 0.9}
}



# speed : 1 Mach = 1225km/h
'''
        200km   50km  <50km
Ours:    2.7     3.6    -
Enemy:    4       3      2

考虑到 pygame 中的坐标(px, 像素) 与 实际距离(km) 的转换，
'''



