
class Ship(object):
    def __init__(self, missles:int, type:str, name=None, x:float=10, y:float=10,):
        self.x, self.y = x, y
        self.missles = missles
        self.type = type
        self.name = name
        
    def move(self, ):
        pass
    
    def fire(self,):
        pass
    
    def __repr__(self,):
        return f'{self.__dict__}'