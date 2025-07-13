import csv
import os

class Head:
    """
    Singleton manager for collecting and preparing agent sensory data.

    Ensures only one instance of Head exists, and stores raw and formatted
    input data for AI neural networks. Handles data setting, extraction,
    mapping to named inputs, and logging data to a CSV file.
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
        list to store the data, an empty dictionary to store the inputs, and
        ensures the CSV file is ready for logging.

        Attributes:
            data (list): A list to store the data. It stores the data in the
                following format:
                [y, velocity, score, collision, distance_to_pipe, distance_to_pipe_only_x, gap_y_center, rel_y_to_gap]
            inputs (dict): A dictionary to store the inputs. The keys are the
                index of the data and the values are the inputs.
            csv_file (str): The name of the CSV file where data will be logged.
        """
        if getattr(self, '_initialized', False):
            return
        self._initialized = True

        self.data = []
        self.inputs = {}
        self.csv_file = "game_data.csv"
        self.ensure_csv_file()

    def ensure_csv_file(self):
        """
        Ensures the CSV file exists and writes the header if it doesn't.

        This method checks if the CSV file exists. If not, it creates the file
        and writes the header row with column names.
        """
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "generation", "living_birds", "y", "velocity", "score",
                    "collision", "distance_to_pipe", "distance_to_pipe_only_x",
                    "gap_y_center", "rel_y_to_gap"
                ])

    def set_data(self, data, generation, living_birds):
        """
        data: [y, velocity, score, collision, distance_to_pipe, ...]
        generation: numer generacji
        living_birds: ile agentów żyje w tej klatce
        """
        self.data      = data
        self.y         = data[0]
        self.velocity  = data[1]
        self.score     = data[2]
        self.collision = data[3]
        self.distance_to_pipe        = data[4]
        #self.distance_to_pipe_only_x = data[5]
        self.gap_y_center            = data[6]
        self.rel_y_to_gap            = data[7]

        # zapisz do CSV właściwe wartości
        self.save_inputs()
        self.log_to_csv(generation, living_birds)

    def log_to_csv(self, generation, living_birds):
        """
        Logs the current data to the CSV file.

        This method appends the current data along with the generation number
        and the number of living birds to the CSV file.

        Args:
            generation (int): The current generation number.
            living_birds (int): The number of living birds.
        """
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                generation, living_birds, self.y, self.score, self.distance_to_pipe,self.gap_y_center
            ]) # , self.distance_to_pipe_only_x self.rel_y_to_gap, self.velocity, self.collision

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
        return (self.y, self.distance_to_pipe, self.gap_y_center, self.rel_y_to_gap) #, self.distance_to_pipe_only_x,  

    def save_inputs(self):
        """
        Map all stored data fields to a descriptive input dictionary for
        debugging or extended processing.self.rel_y_to_gap

        Populates `self.inputs` with keys:
            'y', 'velocity', 'score', 'collision',
            'distance_to_pipe', 'distance_to_pipe_only_x',
            'gap_y_center', 'rel_y_to_gap'
        """
        self.inputs = {
            'y': self.y,
            #'velocity': self.velocity,
            'score': self.score,
            'collision': self.collision,
            'distance_to_pipe': self.distance_to_pipe,
            #'distance_to_pipe_only_x': self.distance_to_pipe_only_x,
            'gap_y_center': self.gap_y_center,
            'rel_y_to_gap': self.rel_y_to_gap
        }