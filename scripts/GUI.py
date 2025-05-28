import pygame
import config.constants as constants
import config.config as config

class GUI:
    """
    Graphical User Interface manager for displaying the game score.

    Handles font initialization, score rendering, and positioning
    of the score display on the screen.
    """
    def __init__(self):
        """
        Initializes the GUI class, setting up the font, initial score display, and 
        its position on the screen.

        This constructor creates a Pygame font object for displaying the score,
        renders the initial score to be shown, and calculates the x, y coordinates
        to center the score on the screen.
        """

        self.score = 0
        self.font = pygame.font.SysFont("arial", 26)
        self.score_to_show = self.font.render(str(self.score), True, constants.WHITE) 
        self.x = config.WIDTH // 2 - self.score_to_show.get_width() // 2
        self.y = config.HEIGHT // 16
    
    def update_score(self, score):
        """
        Updates the score to be shown on the GUI.

        Parameters:
        score (int): The new score to be shown.
        """
        self.score = score
        self.score_to_show = self.font.render(str(self.score), True, constants.WHITE)
    
    def reset(self):
        """
        Resets the score to 0 and updates the GUI to show the new score.

        This method is called when the player loses a life and the game is reset.
        """
        self.score = 0
        self.score_to_show = self.font.render(str(self.score), True, constants.WHITE)
        
    def draw(self, screen):
        """
        Draws the current score onto the given screen surface.

        Args:
            screen (pygame.Surface): The surface to draw the score onto.
        """

        screen.blit(self.score_to_show, (self.x, self.y))