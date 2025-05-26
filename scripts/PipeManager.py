import random
import config.constants as constants
from scripts.Pipe import Pipe

class PipeManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PipeManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        
        self.GAP = constants.GAP
        self.SNAP_POINTS = [-48,-32, -16, 0]
        
        y = self.get_new_snap_point()
        self.pipes = [Pipe(y), Pipe(y + self.GAP)]

    def get_new_snap_point(self):
        return random.choice(self.SNAP_POINTS)
    
    def get_pipes(self):
        return self.pipes
    
    def reset(self):
        y = self.get_new_snap_point()
        self.pipes[0].reset(y)
        self.pipes[1].reset(y + self.GAP)

        
    def update(self):
        if self.pipes:
            for pipe in self.pipes:
                pipe.update()
            
            if self.pipes[0].check_off_screen():
                self.pipes[0].reset_x()
                self.pipes[1].reset_x()
                
                new_y = self.get_new_snap_point()
                
                self.pipes[0].set_y(new_y)
                self.pipes[1].set_y(new_y + self.GAP)
                
    
    def draw(self, screen):
        if self.pipes:
            for pipe in self.pipes:
                pipe.draw(screen)