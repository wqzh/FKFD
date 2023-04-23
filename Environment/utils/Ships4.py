# from . import BaseShip
from . import BaseShip4
from . import FirePowerUnit as FPU

__all__ = ['Aircraft', 'Destroyer', 'Frigate']

r"""
在 Ship 的基础上添加 多个火力单元
"""

class Aircraft(BaseShip4.Ship):
    def __init__(self, missles=0, x=200., y=200., type='Aircraft', **kwargs):
        super(Aircraft, self).__init__(missles=missles, type=type)
        #self.__dict__.update(kwargs)
        self.x, self.y = x, y
        self.__dict__.update(kwargs)
        #print(self.__dict__)
    


class Destroyer(BaseShip4.Ship):
    def __init__(self, missles=0, x=100., y=100., type='Destroyer', **kwargs):
        super(Destroyer, self).__init__(missles=missles, type=type)
        self.x, self.y = x, y
        
        #self.fpu_F = FPU.FirePowerUnit()
        #print('create FirePowerUnit')
        
        self.__dict__.update(kwargs)
        
        for fpu in self.fpu:
            if 'far' == fpu:
                self.fpu_3 = FPU.FirePowerUnit(name=self.name+'_3', type='far')
            elif 'mid' == fpu:
                self.fpu_2 = FPU.FirePowerUnit(name=self.name+'_2', type='mid')
            else:
                self.fpu_1 = FPU.FirePowerUnit(name=self.name+'_1', type='near') 


class Frigate(BaseShip4.Ship):
    def __init__(self, missles=0, x=100., y=100., type='Frigate', **kwargs):
        super(Frigate, self).__init__(missles=missles, type=type)
        self.x, self.y = x, y
        self.__dict__.update(kwargs)
        
        for fpu in self.fpu:
            if 'far' == fpu:
                self.fpu_3 = FPU.FirePowerUnit(name=self.name+'_3', type='far')
            elif 'mid' == fpu:
                self.fpu_2 = FPU.FirePowerUnit(name=self.name+'_2', type='mid')
            else:
                self.fpu_1 = FPU.FirePowerUnit(name=self.name+'_1', type='near') 
        
    
if __name__ == "__main__":
    air = Aircraft(**{ 'y' : 250, 'speed' : 10, 'missles' : 20, 'name' : 'a1'})
    des = Destroyer(**{'x' : 200, 'y' : 300, 'speed' : 5, 'missles' : 10, 'name' : 'd1'})
    fri = Frigate(**{'x' : 230, 'y' : 250, 'speed' : 5, 'missles' : 10, 'name' : 'f1'})
    #des = Destroyer(missles=4, x=100, y=100)
    #fri = Frigate(missles=3, x=200, y=200)
    
    