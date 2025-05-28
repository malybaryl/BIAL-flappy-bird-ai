from scripts.Assets import Assets

class Background:
    """
    Manages the scrolling background image for the game.

    Handles loading the background asset and rendering it onto the game screen.
    """
    def __init__(self):
        """
        Initializes the Background object.

        This function is called when a new instance of Background is created. It
        initializes the Background by loading the background image and setting
        the x and y coordinates to 0.

        """
        self.assets = Assets()
        self.x = 0
        self.y = 0
    
    def draw(self, screen):
        """
        Draws the background onto the screen.

        Args:
            screen (pygame.Surface): The surface to draw the background onto.

        """
        screen.blit(self.assets.assets['background'][0], (self.x, self.y))