
import sys
import time
from time import strftime, gmtime
from typing import Optional, Union
import numpy as np
from numpy import random
import numpy.random as npr
import math
from math import sin, cos, sqrt, pi


import pygame
from pygame.draw import line, circle
from pygame.gfxdraw import line as lline
from pygame.gfxdraw import aacircle, filled_polygon
import gym
from gym import logger, spaces
from gym.utils.renderer import Renderer

from Environment.const import *
import Environment.config as config
from Environment.utils.Ships import Aircraft, Destroyer, Frigate
from Environment.utils.BaseMissile import Missile
from Environment.ware.util import hit_point

from random import randint
#np.random.seed(117)


class AirBattleEnv(gym.Env[np.ndarray, Union[int, np.ndarray]]):
    metadata = {
        "render_modes": ["human", "rgb_array", "single_rgb_array"],
        "render_fps": 50,
    }

    def __init__(self, render_mode: Optional[str] = None):
        global EPISODE, SUCCESS, FAIL
        global EPISODE_STR, SUCCESS_STR, FAIL_STR, FRAME_STR
        global DECISION_TIME, COMMAND_TIME, ACTION_TIME
        
        EPISODE += 1
        EPISODE_STR = EPISODE_STR_ + str(EPISODE)
        SUCCESS_STR  = SUCCESS_STR_ + str(SUCCESS)
        FAIL_STR  = FAIL_STR_ + str(FAIL)
        FRAME_STR = FRAME_STR_
        
        DECISION_TIME = DECISION_STR_
        COMMAND_TIME = COMMAND_STR_
        ACTION_TIME = ACTION_STR_
        
        self._pygame_init()
        self._load_from_config()
        self.missiles_counter = 0
        self.terminate = False
        self.destroyed = False
        self.n_intercept_success = 0
        self.launched_all = 0
        #self.success_all = 0
        self.radar = 0
        self.frame_id = 1
        
        self.render_mode = render_mode
        self.renderer = Renderer(self.render_mode, self._render)
        self.steps = 0

    def _pygame_init(self, ):
        pygame.init()
        pygame.display.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # (width, height)
        fonts = pygame.font.get_fonts()
        # self.font = pygame.font.SysFont('./assets/pala.ttf', 15)
        self.font = pygame.font.SysFont(['SimHei','fangsong', 
                                          'simsun', 'consoles', 'microsieverts'], 20)
        

    def _load_from_config(self, ):
        self.red_aircraft_dict = {}
        self.red_destroyer_dict = {}
        self.red_frigate_dict = {}
        self.red_missile_dict = {}
        self.blue_missile_dict = {}
        
        for aircft in config.red_aircraft:
            self.red_aircraft_dict[aircft['name']] = Aircraft(**aircft)
        for destroyer in config.red_destroyer:
            self.red_destroyer_dict[destroyer['name']] = Destroyer(**destroyer)
        for frigate in config.red_frigate:
            self.red_frigate_dict[frigate['name']] = Frigate(**frigate)
        
        ## 记录驱逐舰的位置
        self.dest_cord = [(round(d.quadx,3), round(d.quady,3)) \
                          for k,d in self.red_destroyer_dict.items()]
        
        for missile in config.red_missile:
            self.red_missile_dict[missile['name']] = Missile(**missile)
        for missile in config.blue_missile:
            self.blue_missile_dict[missile['name']] = Missile(**missile)
        
    def step(self, action=[], ids=[]):
        
        if REAL_TIME: #真实时间, 1S 只仿真5帧
            time.sleep(1/FPS)
        
        terminate = False
        if self.missiles_counter == 100 or self.destroyed: #每轮最多50枚敌方导弹
            terminate  = True
            global SUCCESS, FAIL
            if self.destroyed: FAIL += 1
            else: SUCCESS += 1
            
        if terminate:
            return [], 0, True ,{}
        
        # if self.frame_id > 10:
        #     print(f"第 {self.frame_id} 帧")
        #     um = self.blue_missile_dict[str(2)]
        #     print('2', um.lock, um.x, um.y, um.hitx, um.hity)
        
        reward1, reward2 = 0, 0
        launch, intercept = [], []
        if any(action) and any(ids):
            print(f'========> 第 {self.frame_id} 帧 <========')
            print('动作：', action)  # 动作   red-id 
            print('观测：', ids)      #导弹id  blue-id
        
        for shipid,(a,i) in enumerate(zip(action, ids), 1): 
            if i == 0:
                if a ==0: 
                    reward1 -=0; reward2 += 0 # 没观测到导弹，没发射
                else:
                    # a is typeid 
                    launch.append(a)
                    reward1 -=10; reward2 += 0 # 没有观测到导弹，却发射
            else:
                if a==0: 
                    reward1 -=10; reward2 += 0 # 观测到导弹，没发射
                else:
                    self.launched_all += 1
                    
                    destroyer = self.red_destroyer_dict['d'+str(shipid)]
                    msl = self.blue_missile_dict[str(i)]
                    
                    destroyer.cooldown = 3 * FPS # 3s 内不能再次发射
                    destroyer.color = UNAVAILABLE_COLOR
                    
                    success_prob = PROBABILITY_[a][msl.typeid] #根据导弹类型确定拦截概率
                    # success_prob = 0.8   #固定拦截概率
                    print(f'==> 拦截概率: {a}(r{self.launched_all}) -> {msl.typeid}({i}), prob: {success_prob}') 
                    
                    ## 计算预计拦截点
                    blue = (msl.x, msl.y, msl.quadx, msl.quady, msl.speed, msl.cos, msl.sin)
                    red = (destroyer.quadx, destroyer.quady, MISSILES_RED[a]['maxspeed'])
                    # print('blue:', blue, '\nred:', red)
                    hitx, hity = hit_point(blue, red)
                    assert hitx+hity>0, '无解 T_T'
                    
                    ## 我方导弹设置
                    speed, name = MISSILES_RED[a]['maxspeed'], 'r'+ str(self.launched_all)
                    color = CLR_RED_MISSILE_A if a==1 else CLR_RED_MISSILE_B
                    red_launch = Missile(speed=speed, x=destroyer.x, y=destroyer.y, 
                                         tarx=hitx, tary=hity,name=name, color=color)
                    red_launch.hitx, red_launch.hity = hitx, hity
                    red_launch.will_delete = True
                    self.red_missile_dict[name] = red_launch
                    
                    launch.append(a)
                    reward1 -=2    # 发射1枚导弹, -2
                    reward2 += 5   # 动作正确，给与奖励， 不管是否拦截成功
                    
                    
                    ## 敌方导弹设置
                    msl.hitx, msl.hity = hitx, hity
                    assert msl.hitx+msl.hity>0, 'Bad hitx, hity!'
                    if random.rand() < success_prob: #概率拦截
                        #print(str(i))
                        assert not msl.lock, f"missile {i} is locked. Can't operate!"
                        
                        ## 敌方导弹设置
                        intercept.append(i)
                        msl.will_delete = True
                        self.blue_missile_dict[str(i)] = msl
                        
                        ##reward2 += 3 # 不合适
                    
                    ## enemy missile lock
                    self.blue_missile_dict[str(i)].lock = True
                    
                    # assert self.blue_missile_dict[str(i)].lock, 'lock should be True'
                    
        # if any(action) and any(ids):
        #     print(f'发射{len(launch)}枚导弹: {launch}， 拦截成功{len(intercept)}枚导弹: {intercept}')
        
        # generate enemy's new missiles
        self._generate_missile(self.steps)
        
        reward = reward1 + reward2
        
        # see = [k for k, m in self.blue_missile_dict.items() \
        #        if m.distance<=400 and not m.delete]
        # # get observation
        # print(f'发现{len(see)}枚导弹：', see)
        
        observation = {}
        if not terminate:
            obs_msl = [[int(k), round(m.quadx,3), round(m.quady,3), \
                       [round(sqrt((m.quadx-x)**2 + (m.quady-y)**2),3) for x,y in self.dest_cord], \
                       m.typeid, m.speed] \
                for k, m in self.blue_missile_dict.items()  if (m.distance<=400 and  m.lock==False)]
            obs_ship = [[d.idx, d.cooldown==0, ] \
                        for k,d in self.red_destroyer_dict.items() ] 
            if len(obs_msl) == 0: obs_msl = [[]]
        
        self.radar += RADAR_ROTATION
        self.steps += 1
        info = None
        
        #观测：导弹+舰艇状态
        observation['missiles'] = obs_msl
        observation['ships'] = obs_ship
        
        return observation, reward, terminate, info

    def reset(self, *, seed: Optional[int] = None,
              return_info: bool = False,
              options: Optional[dict] = None, ):
        print(f'====> ALL CLEAR {self.launched_all} <====')
        super().reset()
        self.__init__()
        self.renderer.reset()

    def render(self, mode="human"):
        if self.render_mode is not None:
            return self.renderer.get_renders()
        else:
            return self._render(mode)

    def _display_legend(self, x = 40):
        #LOCS = [(x, 5), (x, 26), (x, 45), (x, 75), (x, 100), (x,145), (x,165)]
        circle(self.screen, CLR_RED_AIRCRAFT, (15, 15), 5)
        circle(self.screen, CLR_RED_DESTROYER, (15, 40), 3)
        circle(self.screen, CLR_RED_FRIGATE, (15, 60), 3)
        
        circle(self.screen, CLR_RED_MISSILE_A, (15, 90), 3)
        circle(self.screen, CLR_RED_MISSILE_B, (15, 110), 3)
        circle(self.screen, CLR_BLUE_NEARSEA, (15, 155), 3)
        circle(self.screen, CLR_BLUE_HIGHFLY, (15, 175), 3)
        
        for lgd, loc,clr in zip(LEGENDS, LOCS, CLRS):
            text_surface = self.font.render(lgd, True, clr)
            self.screen.blit(text_surface, loc)
        
        ## 决策用时 print()

    def _generate_missile(self, step, tarx=AIRCRAFT_X, tary=AIRCRAFT_Y, ):
        # generate missile every 2 steps
        if step % 2 != 1:  return
        if len(self.blue_missile_dict) == 5: return
        if random.rand() < 0.5: # generate probability
            return
        
        ### generate missile cordinate(random)
        # x, y = random.randint(10, 690), random.randint(10, 690) # screen-size [700, 700]
        # while (x - tarx) ** 2 + (y - tary) ** 2 < 50000:
        #     x, y = random.randint(10, 690), random.randint(10, 690)
        
        ### generate missile cordinate(Possion distribution)
        theta = npr.uniform(0, 2*pi)
        radius = npr.uniform(370, 450)
        x = radius * cos(theta) + AIRCRAFT_X
        y = radius * sin(theta) + AIRCRAFT_Y
        
        self.missiles_counter += 1
        name = str(self.missiles_counter)
        typeid = 1 if npr.rand()<0.05 else 2 # 5% NearSea, 95% HighFly
        msl_info = MISSILES_EMEMY[typeid]
        color, speed, maxtravel = msl_info['color'], msl_info['maxspeed'], msl_info['maxtravel']
        
        self.blue_missile_dict[name] = Missile(speed=speed, x=x, y=y, 
            tarx=tarx, tary=tary,name=name, typeid=typeid, typename=MISSILES_EMEMY[typeid],
            color=color, maxtravel=maxtravel)

    def _render(self, mode="human"):
        # print('in _render human')
        self.screen.fill(CLR_BACKGROUND)
        self.screen.blit(self.font.render(EPISODE_STR, True, (0, 0, 0)), (350, 35))
        self.screen.blit(self.font.render(SUCCESS_STR, True, (10, 180, 12)), (450, 20))
        self.screen.blit(self.font.render(FAIL_STR, True, (255, 0, 0)), (450, 45))
        self.screen.blit(self.font.render(FRAME_STR+str(self.frame_id), True, (255, 0, 255)), (350, 60))
        
        ## 绘制基本的图像：探测范围圈、示意图
        for name, aircft in self.red_aircraft_dict.items():
            circle(self.screen, CLR_RED_AIRCRAFT, (aircft.x, aircft.y), 5)
            # circle(self.screen, CLR_25KM_CIRCLE, (aircft.x, aircft.y), 25, 1)   # 25km circle
            # circle(self.screen, CLR_50KM_CIRCLE, (aircft.x, aircft.y), 50, 1)   # 50km circle
            # circle(self.screen, CLR_200KM_CIRCLE, (aircft.x, aircft.y), 200, 1)  # 200km circle
            # circle(self.screen, CLR_400KM_CIRCLE, (aircft.x, aircft.y), 400, 1)  # 400km circle
            aacircle(self.screen, aircft.x, aircft.y, 25, CLR_25KM_CIRCLE)
            aacircle(self.screen, aircft.x, aircft.y, 50, CLR_50KM_CIRCLE)
            aacircle(self.screen, aircft.x, aircft.y, 200, CLR_200KM_CIRCLE)
            aacircle(self.screen, aircft.x, aircft.y, 400, CLR_400KM_CIRCLE)
            
            #line(self.screen, CLR_GREEN, (500,500), (900,500), 1) 
            # line(self.screen, CLR_GREEN, (AIRCRAFT_X,AIRCRAFT_Y), 
            #     (AIRCRAFT_X+400*cos(self.radar),AIRCRAFT_Y-400*sin(self.radar)), 2)
            # 雷达扫描显示
            if RADAR_DSIPLAY:
                cos_, sin_ = cos(self.radar), sin(self.radar)
                r1_cos_, r1_sin_ = 400*cos_, 400*sin_
                r2_cos_, r2_sin_ = 10*cos_, 10*sin_
                
                p1 = (AIRCRAFT_X,AIRCRAFT_Y)
                p2 = (AIRCRAFT_X+r1_cos_,AIRCRAFT_Y-r1_sin_)
                q1 = (AIRCRAFT_X+r2_sin_,AIRCRAFT_Y-r2_cos_)
                q2 = (AIRCRAFT_X+r1_cos_+r2_sin_, AIRCRAFT_Y-r1_sin_-r2_cos_)
                filled_polygon(self.screen, (p1, p2, q2, q1), CLR_RADAR)
            
            #self.screen.blit(self.font.render('25KM', True, (0, 51, 255)), (AIRCRAFT_X+25, AIRCRAFT_Y))
            self.screen.blit(self.font.render('50KM', True, CLR_KM_TITLE), (AIRCRAFT_X+50, AIRCRAFT_Y))
            self.screen.blit(self.font.render('200KM', True, CLR_KM_TITLE), (AIRCRAFT_X+200, AIRCRAFT_Y))
            self.screen.blit(self.font.render('400KM', True, CLR_KM_TITLE), (AIRCRAFT_X+400, AIRCRAFT_Y))
            
        for name, destroyer in self.red_destroyer_dict.items():
            # destroyer.radar += destroyer.incr
            # cos_, sin_ = cos(destroyer.radar), sin(destroyer.radar)
            # r1_cos_, r1_sin_ = 400*cos_, 400*sin_
            # r2_cos_, r2_sin_ = 10*cos_, 10*sin_
            # X_, Y_ = destroyer.x, destroyer.y
            # p1 = (X_,Y_)
            # p2 = (X_+r1_cos_,Y_-r1_sin_)
            # q1 = (X_+r2_sin_,Y_-r2_cos_)
            # q2 = (X_+r1_cos_+r2_sin_, Y_-r1_sin_-r2_cos_)
            
            # filled_polygon(self.screen, (p1, p2, q2, q1), (102, 255, 196))
            
            circle(self.screen, destroyer.color, (destroyer.x, destroyer.y), 3)
            self.screen.blit(self.font.render(str(destroyer.idx), 
                            True, CLR_RED_DESTROYER), (destroyer.x, destroyer.y))
            #if destroyer.cooldown>0 : destroyer.cooldown -= 1
            if destroyer.cooldown>1: 
                destroyer.cooldown -= 1
            elif destroyer.cooldown==1:
                destroyer.cooldown = 0
                destroyer.color = AVAILABLE_COLOR
        
        for name, frigate in self.red_frigate_dict.items():
            circle(self.screen, CLR_RED_FRIGATE, (frigate.x, frigate.y), 3)
            # if frigate.cooldown>0 : frigate.cooldown -= 1
        
        ## 导弹全部轮询更新, 保证获取的是同一时刻(帧)的状态
        for name, missile in self.red_missile_dict.items():
            missile.move(FRAME_INTERVAL)
        for name, missile in self.blue_missile_dict.items():
            missile.move(FRAME_INTERVAL)
        
        ## 红方导弹(拦截导弹) 轮询
        rm_red, rm_blue = [], []
        for name, missile in self.red_missile_dict.items():
            ###missile.move()
            if missile.delete:
                circle(self.screen, (100, 100, 102), (missile.x, missile.y), 4)
            else:
                #circle(self.screen, missile.color, (missile.x, missile.y), 2)
                line(self.screen, missile.color, (missile.initx, missile.inity),  (missile.x, missile.y), 1)
                self.screen.blit(self.font.render(missile.name, True, missile.color), (missile.x, missile.y))
            #if missile.countdown <= 0 : rm_red.append(name)
            if missile.delete: rm_red.append(name)
        
        ## 蓝方导弹(巡航导弹) 轮询
        self.n_intercept_success = 0
        for name, missile in self.blue_missile_dict.items():
            ###missile.move()
            #if missile.countdown <= 0 : rm_blue.append(name)
            if missile.delete : rm_blue.append(name)

            if missile.delete:
                if missile.will_delete:
                    self.n_intercept_success += 1
                else: # missile hit the target(Aircraft):
                    self.destroyed = True
                circle(self.screen, (100, 100, 102), (missile.x, missile.y), 4)
            else:
                line(self.screen, missile.color, (missile.initx, missile.inity),  (missile.x, missile.y), 1)
                # lline(self.screen, int(missile.initx), int(missile.inity), int(missile.x), int(missile.y), missile.color)
                # circle(self.screen, missile.color, (missile.x, missile.y), 2)
                if missile.distance <400:
                    self.screen.blit(self.font.render(name, True, missile.color), (missile.x, missile.y))
        
        for m in rm_red : self.red_missile_dict.pop(m)
        for m in rm_blue : self.blue_missile_dict.pop(m)
        self._display_legend()
        self.frame_id += 1
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                sys.exit()

    def close(self):
        pygame.display.quit()
        pygame.quit()


if __name__ == "__main__":
    env = AirBattleEnv()
    env.reset()
    env.render()

    for t in range(1, 10000):
        env.render()
        observation, reward, terminate, info = env.step(action=[2, -1, 3, 5]) # 替换 action=[2, -1, 3, 5]
        #env.radar += 0.23
        if terminate:
            print('--> terminate=True, reset the env!')
            env.reset()
        #env.render()
        #time.sleep(0.01)
        # time.sleep(FRAME_INTERVAL)
    
        #print(f'==> step: {t} \n',  observation, reward, terminate, info, '\n')
    
    env.close()