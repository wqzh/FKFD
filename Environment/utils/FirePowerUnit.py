
from Environment.utils.BaseMissile import Missile

class FirePowerUnit():
    def __init__(self, name='', speed=3, type='far', n_missiles=10):
        self.name = name
        self.speed = speed
        self.type = type # [Far, Mid, Near]
        self.n_missiles = n_missiles
        self.missiles = []
        print(f'creat FPU: name : {name}, type : {type}')
        
    
    def fire(self, tarx, tary):
        self.n_missiles -= 1
        m = Missile(speed=self.speed, tarx=tarx, tary=tary)
        #self.missiles.append(m)
        return m