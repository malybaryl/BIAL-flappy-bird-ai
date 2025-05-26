import pygame
import config.config as config
from scripts.Assets import Assets

class Pipe:
    def __init__(self, y):
        self.assets = Assets()
        
        self.SPEED = 1
        self.COLLIDER_WIDTH = self.assets.assets['pipe'][0].get_width()
        self.COLLIDER_HEIGHT = self.assets.assets['pipe'][0].get_height()
        self.DRAW_COLLIDER = False
        
        self.y = y
        self.x = config.WIDTH
        self.collider = pygame.Rect(self.x, self.y, self.COLLIDER_WIDTH, self.COLLIDER_HEIGHT)
    
    def set_y(self, y):
        self.y = y
        self.collider.topleft = (self.x, self.y)  

    def check_off_screen(self):
        return self.x < -self.assets.assets['pipe'][0].get_width()
    
    def reset_x(self):
        self.x = config.WIDTH
        self.collider = pygame.Rect(self.x, self.y, self.COLLIDER_WIDTH, self.COLLIDER_HEIGHT)
    
    def reset(self, y):
        self.set_y(y)
        self.x = config.WIDTH
        self.collider.topleft = (self.x, self.y)
        
    def update(self):
        self.x -= self.SPEED
        self.collider.topleft = (self.x, self.y)
    
    def draw(self, screen):
        screen.blit(self.assets.assets['pipe'][0], (self.x, self.y))
        if self.DRAW_COLLIDER:
            pygame.draw.rect(screen, (255, 0, 0), self.collider, 1)