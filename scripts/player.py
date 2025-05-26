import pygame
import random
import math
import config.config as config
import config.constants as constants
from scripts.Assets import Assets

class Player:
    def __init__(self):
        '''
        Assets
        '''
        self.assets = Assets()
        
        '''
        Constants
        '''
        self.GRAVITY = 0.1
        self.FORCE = 5
        self.MAX_VELOCITY = 2
        self.CAN_JUMP_COOLDOWN = 500
        self.COLLIDER_WIDTH = self.assets.assets['player'][0].get_width()
        self.COLLIDER_HEIGHT = self.assets.assets['player'][0].get_height()
        self.PRINT_DATA = True
        self.DRAW_COLLIDER = False
        
        '''
        Variables
        '''
        self.x = config.WIDTH // 6 - self.assets.assets['player'][0].get_width() // 2
        self.y = config.HEIGHT // 2 - self.assets.assets['player'][0].get_height() // 2
        self.velocity = 0
        self.can_jump = True
        self.jump_cooldown_timer = pygame.time.get_ticks()
        self.collider = pygame.Rect(self.x, self.y, self.COLLIDER_WIDTH, self.COLLIDER_HEIGHT)
        self.score = 0
        self.collision = False
        self.collision_cooldown_timer = pygame.time.get_ticks()
        self.collision_cooldown = 500
        self.hit = False
        self.sprite = self.assets.assets['player']
        self.distance_to_pipe = 0
        self.distance_to_pipe_only_x = 0
        self.gap_y_center = 0
        self.rel_y_to_gap = 0
        self.real_y = self.y + self.COLLIDER_HEIGHT // 2
        self.index = 0
        self.index_counter = 0
        self.animation_speed = 0.5
        self.max_index = len(self.assets.assets['player']) - 1
        self.red = 0
        self.green = 0
        self.blue = 0
        self.recolor()
    
    
    def jump(self):
        if self.can_jump:
            self.velocity -= self.FORCE 
            self.can_jump = False
    
    def print_data(self):
        print(f'[Player data: y: {self.real_y}, velocity: {self.velocity}, score: {self.score}, collision: {self.collision}, distance to pipe: {self.distance_to_pipe}, distance to pipe only x: {self.distance_to_pipe_only_x}, gap y center: {self.gap_y_center}, rel y to gap: {self.rel_y_to_gap}]')
    
    def recolor(self):
        self.sprite_to_show = self.sprite[self.index].copy()
        self.red = random.randint(0,255)
        self.green = random.randint(0,255)
        self.blue = random.randint(0,255)
        self.sprite_to_show.fill((self.red, self.green, self.blue, 255), special_flags=pygame.BLEND_RGBA_MULT)
    
    def update_animation(self):
        self.sprite_to_show = self.sprite[self.index].copy()
        self.sprite_to_show.fill((self.red, self.green, self.blue, 255), special_flags=pygame.BLEND_RGBA_MULT)
        
    def reset(self):
        self.x = config.WIDTH // 6 - self.assets.assets['player'][0].get_width() // 2
        self.y = config.HEIGHT // 2 - self.assets.assets['player'][0].get_height() // 2
        self.velocity = 0
        self.can_jump = True
        self.jump_cooldown_timer = pygame.time.get_ticks()
        self.score = 0
        self.collision = False
        self.hit = False
        self.score_cooldown_timer = pygame.time.get_ticks()
        self.can_add_score = True
        self.recolor()
        
    def update(self, pipes, gui):
        self.collision = False
        self.distance_to_pipe_only_x = (pipes[0].x + pipes[0].COLLIDER_WIDTH // 2) - (self.x + self.collider.width // 2)
        pipe_center_y = pipes[0].y + pipes[0].COLLIDER_HEIGHT + constants.GAP // 2
        player_center_y = self.y + self.collider.height // 2
        dy = pipe_center_y - player_center_y
        self.real_y = self.y + self.COLLIDER_HEIGHT // 2

        self.distance_to_pipe = math.sqrt(self.distance_to_pipe_only_x**2 + dy**2)
        self.gap_y_center = pipes[0].y + pipes[0].COLLIDER_HEIGHT + constants.GAP // 2
        
        self.index_counter += self.animation_speed
        if self.index_counter > self.max_index + 0.95:
            self.index_counter = 0
            self.index = 0
        else:
            self.index = math.floor(self.index_counter)
        
        self.update_animation()
        
        self.rel_y_to_gap = player_center_y - self.gap_y_center

        
        if self.hit:
            if pygame.time.get_ticks() - self.collision_cooldown_timer > self.collision_cooldown:
                self.hit = False
                self.collision_cooldown_timer = pygame.time.get_ticks()
        
        if pygame.time.get_ticks() - self.score_cooldown_timer > self.collision_cooldown:
            self.score_cooldown_timer = pygame.time.get_ticks()
            self.can_add_score = True
        
        self.velocity += self.GRAVITY
        if self.velocity > self.MAX_VELOCITY:
            self.velocity = self.MAX_VELOCITY
        if self.velocity < -self.MAX_VELOCITY:
            self.velocity = -self.MAX_VELOCITY
        self.y += self.velocity
        
        self.collider.topleft = (self.x, self.y)
        if not self.hit:
            if pipes:
                pipe_one_collieder = pygame.Rect(pipes[0].x, pipes[0].y, pipes[0].COLLIDER_WIDTH, pipes[0].COLLIDER_HEIGHT)
                pipe_two_collieder = pygame.Rect(pipes[1].x, pipes[1].y, pipes[1].COLLIDER_WIDTH, pipes[1].COLLIDER_HEIGHT)
                if self.collider.colliderect(pipe_one_collieder) or self.collider.colliderect(pipe_two_collieder):
                    self.collision = True
                    self.hit = True
            
        if self.can_add_score:
            if pipes[0].x < self.x < pipes[0].x + pipes[0].COLLIDER_WIDTH:
                self.score += 1
                gui.update_score(self.score)
                self.score_cooldown_timer = pygame.time.get_ticks()
                self.can_add_score = False
        
        
        if self.y > config.HEIGHT - self.COLLIDER_HEIGHT//2 or self.y < 0 - self.COLLIDER_HEIGHT//2:
            self.collision = True
        
        if pygame.time.get_ticks() - self.jump_cooldown_timer > self.CAN_JUMP_COOLDOWN:
            self.can_jump = True
            self.jump_cooldown_timer = pygame.time.get_ticks()
        
        if self.PRINT_DATA:
            self.print_data()
        
        
        return self.collision, gui
        
    def draw(self, screen):
        screen.blit(self.sprite_to_show, (self.x, self.y))
        if self.DRAW_COLLIDER:
            pygame.draw.rect(screen, (255, 0, 0), self.collider, 1)