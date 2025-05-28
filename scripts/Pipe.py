import pygame
import config.config as config
from scripts.Assets import Assets

class Pipe:
    """
    Represents a single pipe obstacle in Flappy Bird.

    Manages position, movement, collision detection, and rendering for
    both top and bottom pipe instances. Handles automatic reset when
    moving off-screen.
    """
    def __init__(self, y):
        """
        Initialize the Pipe at a given vertical position.

        Args:
            y (int): The starting y-coordinate of the pipe.
        """
        self.assets = Assets()
        
        self.SPEED = 1
        self.COLLIDER_WIDTH = self.assets.assets['pipe'][0].get_width()
        self.COLLIDER_HEIGHT = self.assets.assets['pipe'][0].get_height()
        self.DRAW_COLLIDER = False
        
        self.y = y
        self.x = config.WIDTH
        self.collider = pygame.Rect(self.x, self.y, self.COLLIDER_WIDTH, self.COLLIDER_HEIGHT)
    
    def set_y(self, y):
        """
        Sets the y position of the pipe and updates the collider.
        
        Parameters
        ----------
        y : int
            The y position of the pipe
        """
        self.y = y
        self.collider.topleft = (self.x, self.y)  

    def check_off_screen(self):
        """
        Checks if the pipe has moved off the left side of the screen.

        Returns:
            bool: True if the pipe is off the screen, False otherwise.
        """

        return self.x < -self.assets.assets['pipe'][0].get_width()
    
    def reset_x(self):
        """
        Resets the x position of the pipe and updates the collider.

        This function is used when the pipe has moved off the left side of the screen.
        It resets the x position of the pipe to the right side of the screen and
        updates the collider accordingly.
        """
        self.x = config.WIDTH
        self.collider = pygame.Rect(self.x, self.y, self.COLLIDER_WIDTH, self.COLLIDER_HEIGHT)
    
    def reset(self, y):
        """
        Resets the pipe to the right side of the screen with the given y position.

        Parameters
        ----------
        y : int
            The y position of the pipe
        """
        self.set_y(y)
        self.x = config.WIDTH
        self.collider.topleft = (self.x, self.y)
        
    def update(self):
        """
        Updates the pipe's position and collider.

        This function moves the pipe to the left by decreasing its x position
        by the specified speed. It also updates the position of the pipe's 
        collider to match the new x and y coordinates.
        """

        self.x -= self.SPEED
        self.collider.topleft = (self.x, self.y)
    
    def draw(self, screen):
        """
        Draws the pipe onto the screen.

        This function draws the pipe image onto the screen surface at the pipe's
        current x and y coordinates. If the DRAW_COLLIDER flag is set to True,
        the function also draws a red rectangle around the pipe's collider to
        help with debugging.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the pipe onto
        """
        screen.blit(self.assets.assets['pipe'][0], (self.x, self.y))
        if self.DRAW_COLLIDER:
            pygame.draw.rect(screen, (255, 0, 0), self.collider, 1)