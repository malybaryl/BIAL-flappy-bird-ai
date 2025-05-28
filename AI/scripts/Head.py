class Head:
    """
    Singleton manager for collecting and preparing agent sensory data.

    Ensures only one instance of Head exists, and stores raw and formatted
    input data for AI neural networks. Handles data setting, extraction,
    and mapping to named inputs.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of Head and enforces the singleton pattern.

        This function is called when an instance of Head is created. If the
        instance does not exist, it creates it. Otherwise, it returns the existing
        instance.

        Returns:
            Head: The instance of Head.
        """
        if cls._instance is None:
            cls._instance = super(Head, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the Head singleton.

        This function is called when an instance of Head is created. If the
        instance does not exist, it initializes the Head by creating an empty
        list to store the data and an empty dictionary to store the inputs.

        Attributes:
            data (list): A list to store the data. It stores the data in the
                following format:
                [y, velocity, score, collision, distance_to_pipe, distance_to_pipe_only_x, gap_y_center, rel_y_to_gap]
            inputs (dict): A dictionary to store the inputs. The keys are the
                index of the data and the values are the inputs.
        """
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        
        '''
        Data
        
        #? Example data
        #
        # [Player data: y: 72.70000000000013, 
        #               velocity: 2, 
        #               score: 1, 
        #               collision: False, 
        #               distance to pipe: 159.85771798696487, 
        #               distance to pipe only x: 158, 
        #               gap y center: 97, 
        #               rel y to gap: -24.29999999999987
        # ]
        #
        #? How to get to data
        # index -> self.data[index] -> [y, velocity, score, collision, distance_to_pipe, distance_to_pipe_only_x, gap_y_center, rel_y_to_gap]
        '''
        self.data = []
        self.inputs = {}
    
    def set_data(self, data):
        """
        Sets the data of the Head singleton.

        This function sets the data of the Head singleton and updates the
        corresponding attributes.

        Args:
            data (list): The data to set. The format of the data is the
                following:
                [y, velocity, score, collision, distance_to_pipe, distance_to_pipe_only_x, gap_y_center, rel_y_to_gap]

        Attributes:
            data (list): The data of the Head singleton.
            y (int): The y position of the player.
            velocity (int): The velocity of the player.
            score (int): The score of the player.
            collision (bool): The collision status of the player.
            distance_to_pipe (int): The distance to the next pipe.
            distance_to_pipe_only_x (int): The distance to the next pipe only in the x direction.
            gap_y_center (int): The y center of the gap of the next pipe.
            rel_y_to_gap (int): The relative y position to the gap of the next pipe.
        """
        self.data = data
        self.y = data[0] if self.data else 0
        self.velocity = data[1] if self.data else 0
        self.score = data[2] if self.data else 0
        self.collision = data[3] if self.data else False
        self.distance_to_pipe = data[4] if self.data else 0
        self.distance_to_pipe_only_x = data[5] if self.data else 0
        self.gap_y_center = data[6] if self.data else 0
        self.rel_y_to_gap = data[7] if self.data else 0
        
        self.save_inputs()
    
    def get_data(self):
        """
        Retrieves a subset of the player's data for neural network input.

        This function returns a tuple containing specific data attributes of 
        the player that are used as inputs for the neural network. The data 
        includes the player's y position, distance to the next pipe, distance 
        to the next pipe only in the x direction, y center of the gap of the 
        next pipe, and relative y position to the gap of the next pipe.

        Returns:
            tuple: A tuple with the player's y position, distance to the next pipe, 
            distance to the next pipe only in the x direction, y center of the gap 
            of the next pipe, and relative y position to the gap of the next pipe.
        """

        return (self.y, self.distance_to_pipe, self.distance_to_pipe_only_x, self.gap_y_center, self.rel_y_to_gap)
        
    def save_inputs(self):
        """
        Map all stored data fields to a descriptive input dictionary for
        debugging or extended processing.

        Populates `self.inputs` with keys:
            'y', 'velocity', 'score', 'collision',
            'distance_to_pipe', 'distance_to_pipe_only_x',
            'gap_y_center', 'rel_y_to_gap'
        """
        '''
        Define inputs of neural network
        '''
        self.inputs = {
            'y': self.y,
            'velocity': self.velocity,
            'score': self.score,
            'collision': self.collision,
            'distance_to_pipe': self.distance_to_pipe,
            'distance_to_pipe_only_x': self.distance_to_pipe_only_x,
            'gap_y_center': self.gap_y_center,
            'rel_y_to_gap': self.rel_y_to_gap
        }

