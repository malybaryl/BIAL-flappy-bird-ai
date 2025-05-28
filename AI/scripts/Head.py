class Head:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Head, cls).__new__(cls)
        return cls._instance

    def __init__(self):
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
        return (self.y, self.distance_to_pipe, self.distance_to_pipe_only_x, self.gap_y_center, self.rel_y_to_gap)
        
    def save_inputs(self):
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

