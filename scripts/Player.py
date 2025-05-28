import pygame
import random
import math
import config.config as config
import config.constants as constants
from scripts.Assets import Assets
from AI.scripts.Head import Head

class Player:
    """
    Represents the player character (the bird) in Flappy Bird.

    Manages physics (gravity, jumping), collision detection, scoring, animation,
    and provides sensory data for AI agents.
    """
    def __init__(self):
        """
        Initialize the Player by loading assets, setting physical constants,
        and initializing state variables including position, velocity, score,
        collision status, animation parameters, and stored input data.
        """
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
        self.PRINT_DATA = config.PRINT_DATA
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
        self.stored_data = []
        self.recolor()
    
    def get_score(self):
        """
        Returns the current score of the player
        
        Returns:
            int: The current score of the player
        """
        return self.score
    
    def jump(self):
        """
        Causes the player to jump by adjusting the velocity.

        This function decreases the player's velocity by a specified force,
        simulating a jump action. Jumping is only allowed if the player
        is currently able to jump, which is determined by the can_jump flag.
        Once a jump is performed, the can_jump flag is set to False to prevent
        consecutive jumps until the player is allowed to jump again.
        """

        if self.can_jump:
            self.velocity -= self.FORCE 
            self.can_jump = False
    
    def print_data(self):
        """
        Prints the current data of the player to the console.

        This function stores the current data of the player in the
        stored_data attribute and prints it to the console. The data
        includes the player's y position, velocity, score, collision
        status, distance to the next pipe, distance to the next pipe
        only in the x direction, y center of the gap of the next pipe,
        and relative y position to the gap of the next pipe.
        """
        self.stored_data = [self.real_y, self.velocity, self.score, self.collision, self.distance_to_pipe, self.distance_to_pipe_only_x, self.gap_y_center, self.rel_y_to_gap]
        print(f'[Player data: y: {self.real_y}, velocity: {self.velocity}, score: {self.score}, collision: {self.collision}, distance to pipe: {self.distance_to_pipe}, distance to pipe only x: {self.distance_to_pipe_only_x}, gap y center: {self.gap_y_center}, rel y to gap: {self.rel_y_to_gap}]')
    
    def get_stored_data(self):
        """
        Returns the stored data of the player.

        The stored data includes the player's y position, velocity, score, collision
        status, distance to the next pipe, distance to the next pipe only in the x
        direction, y center of the gap of the next pipe, and relative y position to
        the gap of the next pipe.

        Returns:
            list: The stored data of the player
        """
        return self.stored_data
    
    def recolor(self):
        """
        Recolors the player sprite with a random color by filling it with a random RGB color and blending it with the current sprite using the BLEND_RGBA_MULT special flag.

        This function is used to generate a new color for the player sprite by randomly selecting a red, green, and blue color and then blending it with the current sprite. The result is a sprite with a new color that is stored in the sprite_to_show attribute.
        """
        self.sprite_to_show = self.sprite[self.index].copy()
        self.red = random.randint(0,255)
        self.green = random.randint(0,255)
        self.blue = random.randint(0,255)
        self.sprite_to_show.fill((self.red, self.green, self.blue, 255), special_flags=pygame.BLEND_RGBA_MULT)
    
    def update_animation(self):
        """
        Updates the animation of the player sprite.

        This function updates the animation of the player sprite by increasing the index counter and setting it to the modulo of the index counter and the max index of the sprite list. The index is used to select the current frame of the sprite animation. The current frame is then recolored with the current RGB color and stored in the sprite_to_show attribute.
        """
        self.sprite_to_show = self.sprite[self.index].copy()
        self.sprite_to_show.fill((self.red, self.green, self.blue, 255), special_flags=pygame.BLEND_RGBA_MULT)
        
    def reset(self):
        """
        Resets the player to its initial state.

        This function resets the player's x and y position, velocity, jump cooldown
        timer, score, collision status, hit status, score cooldown timer, and whether
        or not the player is allowed to add score. It also recolors the player sprite
        with a new random color.

        Note: This function is called when the player collides with a pipe or when the
        game is reset.
        """
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
        """
        Updates the player's state and handles interactions with pipes.

        This function updates the player's position, velocity, and animation. It calculates
        the distance to the nearest pipe and adjusts the player's y position based on gravity.
        It checks for collisions with pipes and updates the player's score and GUI accordingly.
        The function also manages cooldowns for jumping and scoring, and prints the player's
        data if configured to do so.

        Args:
            pipes (list): A list of pipe objects to interact with.
            gui (GUI): The GUI object to update the score display.

        Returns:
            tuple: A tuple containing the collision status (bool) and the updated GUI object.
        """

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
        """
        Renders the player sprite and its collider (if enabled) onto the screen at the player's current position.

        Args:
            screen (pygame.Surface): The surface to draw the player onto
        """
        screen.blit(self.sprite_to_show, (self.x, self.y))
        if self.DRAW_COLLIDER:
            pygame.draw.rect(screen, (255, 0, 0), self.collider, 1)