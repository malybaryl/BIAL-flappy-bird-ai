import pygame
import config.constants as constants
import config.config as config

class GUI:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("arial", 26)
        self.score_to_show = self.font.render(str(self.score), True, constants.WHITE) 
        self.x = config.WIDTH // 2 - self.score_to_show.get_width() // 2
        self.y = config.HEIGHT // 16
    
    def update_score(self, score):
        self.score = score
        self.score_to_show = self.font.render(str(self.score), True, constants.WHITE)
    
    def reset(self):
        self.score = 0
        self.score_to_show = self.font.render(str(self.score), True, constants.WHITE)
        
    def draw(self, screen):
        screen.blit(self.score_to_show, (self.x, self.y))