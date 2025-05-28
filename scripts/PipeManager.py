import random
import config.constants as constants
from scripts.Pipe import Pipe

class PipeManager:
    """
    Singleton manager for Flappy Bird pipes.

    Handles creation, updating, resetting, and rendering of pipe pairs
    that the player must navigate through. Ensures only one instance
    exists throughout the game lifecycle.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of PipeManager and enforces the singleton pattern.

        This function is called when an instance of PipeManager is created. If the
        instance does not exist, it creates it. Otherwise, it returns the existing
        instance.

        Returns:
            PipeManager: The instance of PipeManager.
        """
        if cls._instance is None:
            cls._instance = super(PipeManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the PipeManager singleton.

        This function is called when an instance of PipeManager is created. It
        initializes the PipeManager by setting the gap between the top and
        bottom pipes and the snap points. It also creates the first two pipes
        with a random y-coordinate.

        The `get_new_snap_point()` function is used to get a new y-coordinate
        for the first pipe, and the second pipe is created with the gap
        distance above the first pipe.
        """
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        
        self.GAP = constants.GAP
        self.SNAP_POINTS = [-48,-32, -16, 0]
        
        y = self.get_new_snap_point()
        self.pipes = [Pipe(y), Pipe(y + self.GAP)]

    def get_new_snap_point(self):
        """
        Gets a new y-coordinate for the next pipe.

        This function randomly selects from the snap points and returns the
        selected y-coordinate.

        Returns:
            int: The new y-coordinate for the next pipe.
        """
        return random.choice(self.SNAP_POINTS)
    
    def get_pipes(self):
        """
        Gets the list of all pipes.

        This function returns the list of all pipes created by the
        PipeManager.

        Returns:
            list: A list of Pipe objects.
        """
        return self.pipes
    
    def reset(self):
        """
        Resets the position of the pipes.

        This function generates a new y-coordinate for the first pipe using
        the `get_new_snap_point` method and resets the position of both pipes.
        The second pipe is positioned at a distance specified by `GAP` above 
        the first pipe.
        """

        y = self.get_new_snap_point()
        self.pipes[0].reset(y)
        self.pipes[1].reset(y + self.GAP)

        
    def update(self):
        """
        Updates the position of the pipes.

        This function iterates over all pipes and updates them. If the first
        pipe is off the screen, it resets the position of both pipes and
        generates a new y-coordinate for the first pipe, positioning the
        second pipe at a distance specified by `GAP` above the first pipe.
        """
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
        """
        Draws all pipes onto the game screen.

        This function iterates over all pipes and calls their draw method,
        rendering them onto the provided screen surface.
        """

        if self.pipes:
            for pipe in self.pipes:
                pipe.draw(screen)