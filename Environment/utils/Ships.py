from . import BaseShip
from Environment.const import AIRCRAFT_X, AIRCRAFT_Y, UNAVAILABLE_COLOR, AVAILABLE_COLOR 

__all__ = ['Aircraft', 'Destroyer', 'Frigate']


class Aircraft(BaseShip.Ship):
    def __init__(self, missles=0, x=200., y=200., type='Aircraft', **kwargs):
        super(Aircraft, self).__init__(missles=missles, type=type)
        #self.__dict__.update(kwargs)
        self.x, self.y = x, y
        self.__dict__.update(kwargs)
        #print(self.__dict__)
    


class Destroyer(BaseShip.Ship):
    def __init__(self, missles=0, x=100., y=100., type='Destroyer', **kwargs):
        super(Destroyer, self).__init__(missles=missles, type=type)
        self.x, self.y = x, y
        self.quadx, self.quady = x - AIRCRAFT_X, AIRCRAFT_Y - y
        
        # self.available_color = AVAILABLE_COLOR
        # self.unavailable_color = UNAVAILABLE_COLOR
        self.color = AVAILABLE_COLOR
        
        self.__dict__.update(kwargs)


class Frigate(BaseShip.Ship):
    def __init__(self, missles=0, x=100., y=100., type='Frigate', **kwargs):
        super(Frigate, self).__init__(missles=missles, type=type)
        self.x, self.y = x, y
        self.__dict__.update(kwargs)
    
if __name__ == "__main__":
    air = Aircraft(**{ 'y' : 250, 'speed' : 10, 'missles' : 20, 'name' : 'a1'})
    des = Destroyer(**{'x' : 200, 'y' : 300, 'speed' : 5, 'missles' : 10, 'name' : 'd1'})
    fri = Frigate(**{'x' : 230, 'y' : 250, 'speed' : 5, 'missles' : 10, 'name' : 'f1'})
    #des = Destroyer(missles=4, x=100, y=100)
    #fri = Frigate(missles=3, x=200, y=200)
    
    