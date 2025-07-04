import pygame
import os
import config.config as config
import config.constants as constants
from scripts.Player import Player
from scripts.Background import Background
from scripts.PipeManager import PipeManager
from scripts.GUI import GUI
if config.AI:
    import neat
    from AI.scripts.Head import Head

class Main:
    """
    Main game class for Flappy Bird (manual mode).

    Handles initialization of Pygame, creation and resetting of game objects,
    and the main game loop for processing events, updating the game state,
    and rendering each frame.
    """
    def __init__(self):
        """
        Initialize Pygame, set up the game window and drawing surface,
        clock, and instantiate all game objects including Player, Background,
        PipeManager, GUI, and AI head if enabled.
        """
        '''
        Pygame variables
        '''
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption(constants.TITLE)
        self.window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.screen = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_is_on = True
        
        '''
        Objects
        '''
        self.player = Player()
        self.background = Background()
        self.pipe_manager = PipeManager()
        self.pipes = self.pipe_manager.get_pipes()
        self.gui = GUI()
        self.ai_head = Head() if config.AI else None
        
        self.objects = [
            self.background,
            self.player,
            self.pipe_manager,
            self.gui
        ]
        
        self.reset()

    def reset(self):
        '''
        Resets all objects in the game to their initial state
        '''
        for obj in self.objects:
            try:
                obj.reset()
            except Exception as e:
                pass
        self.pipes = self.pipe_manager.get_pipes()
        
    def game_loop(self):
        
        '''
        Main game loop that runs continuously while the game is active.
        
        This loop handles input events, updates game objects, and renders the game
        frame by frame. It processes user inputs such as quitting the game, jumping,
        and resetting. The loop also calls update and draw methods for each game
        object, scales the screen, and manages the frame rate.
        '''

        while self.game_is_on:
            '''
            Handle events
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_on = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_r:
                        self.reset()
            
            if pygame.mouse.get_pressed()[0]:
                self.player.jump()
            
            '''
            Update
            '''
            def update():
                '''
                Updates the state of non-player game objects.

                Iterates over all objects in the game, updating them if they are not
                instances of the Player class. Handles exceptions silently and sets
                the collision flag to False by default.
                '''
                collision = False
                for object in self.objects:
                    try:
                        if not isinstance(object, Player):
                            object.update()
                        else:
                            collision, self.gui = object.update(self.pipes, self.gui)
                    except Exception as e:
                        pass
                if collision == True:
                    self.reset()
            update()
            
            '''
            Draw
            '''
            def draw():
                '''
                Renders all game objects to the screen.

                Iterates through each object in the game and calls its draw method
                to render it onto the screen surface.
                '''

                for object in self.objects:
                    object.draw(self.screen)
            draw()
            
            
            '''
            Pygame screen blit
            '''
            scaled_surface = pygame.transform.scale(self.screen, self.window.get_size())
            self.window.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(config.FPS)

        pygame.quit()

class MainAI(Main):
    def __init__(self, genomes, config_file):
        """
        AI-powered game class using NEAT for neural network training.

        Extends Main to integrate NEAT networks, handling genome and network
        creation, per-frame AI updates, fitness evaluation, and automatic
        simulation termination when all agents are eliminated.
        """
        '''
        Pygame variables
        '''
        super().__init__()
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption(constants.TITLE)
        
        self.window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.screen = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_is_on = True
        
        '''
        AI Variables
        '''
        self.nets = []
        self.gens = []
        self.neurons = []
        
        for _, gen in genomes:
            net = neat.nn.FeedForwardNetwork.create(gen, config_file)
            self.nets.append(net)
            self.neurons.append(Player())
            gen.fitness = 0
            self.gens.append(gen)
        
        
        '''
        Variables
        '''
        self.last_score = 0
        self.score = 0
        
        '''
        Objects
        '''
        self.background = Background()
        self.pipe_manager = PipeManager()
        self.pipes = self.pipe_manager.get_pipes()
        self.gui = GUI()
        self.ai_head = Head() if config.AI else None
        
        # final self.objects:
        # [self.background, self.neuron_1, self.neuron_2..., self.pipe_manager, self.gui]
        self.objects = [self.background]
        self.objects.extend(self.neurons)
        self.objects.extend([self.pipe_manager, self.gui]) 
        
        self.reset()
        
    def game_loop(self):
        '''
        Main game loop that runs continuously while the game is active.
        
        This loop handles input events, updates game objects, and renders the game
        frame by frame. It processes user inputs such as quitting the game, jumping,
        and resetting. The loop also calls update and draw methods for each game
        object, scales the screen, and manages the frame rate.
        '''
        while self.game_is_on:
            '''
            Handle events
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()    
            '''
            Update
            '''
            def update():
                """
                Updates the state of non-player game objects.

                Iterates over all objects in the game, updating them if they are not
                instances of the Player class. Handles exceptions silently and sets
                the collision flag to False by default.
                """

                collision = False
                for index, object in enumerate(self.objects):
                    try:
                        if not isinstance(self.objects[index], Player):
                            self.objects[index].update()
                        else:
                            continue
                    except Exception as e:
                        pass
            update()
            
            '''
            AI Update
            '''
            def ai_update():
                '''
                AI update loop that runs every frame. It updates the AI's perception of the game world,
                runs the neural network, and then updates the player based on the output of the neural network.
                It also updates the fitness of each genome and removes any genomes that have a collision.
                '''
                if not self.neurons:
                    self.game_is_on = False
                    return

                self.pipe_manager.update()
                self.pipes = self.pipe_manager.get_pipes()

                prev_score = self.score

                for i in range(len(self.neurons) - 1, -1, -1):
                    neuron = self.neurons[i]
                    collision, self.gui = neuron.update(self.pipes, self.gui)
                    if collision:
                        self.gens[i].fitness -= 1
                        self.neurons.pop(i)
                        self.nets.pop(i)
                        self.gens.pop(i)
                        continue

                    data = neuron.get_stored_data()
                    self.ai_head.set_data(data)
                    inputs = self.ai_head.get_data()
                    output = self.nets[i].activate(inputs)
                    if output[0] > 0.5:
                        neuron.jump()

                    self.gens[i].fitness += 0.1

                if not self.neurons:
                    self.game_is_on = False
                    return

                self.score = self.neurons[0].get_score()
                if self.score != prev_score:
                    for gen in self.gens:
                        gen.fitness += 5

            
            if config.AI:
                ai_update()
                if self.game_is_on == False:
                    break
            
            '''
            Draw
            '''
            def draw():
                '''
                Draws all game objects onto the game screen.

                This includes the background, each neuron (AI player), the pipes, and the GUI.
                '''
                self.screen.fill((0, 0, 0))
                self.background.draw(self.screen)
                for neuron in self.neurons:
                    neuron.draw(self.screen)
                self.pipe_manager.draw(self.screen)
                self.gui.draw(self.screen)
            draw()
            
            
            '''
            Pygame screen blit
            '''
            scaled_surface = pygame.transform.scale(self.screen, self.window.get_size())
            self.window.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(config.FPS)



def main_ai(genomes, config_file):
    """
    Initializes the AI version of the game and starts the game loop.

    Parameters:
    genomes (list): A list of genome tuples provided by the NEAT library, representing AI players.
    config_file (neat.config.Config): The NEAT configuration file used to set up the neural networks.

    This function creates an instance of MainAI with the given genomes and configuration, and then
    calls the game_loop method to run the game.
    """

    game = MainAI(genomes, config_file)
    game.game_loop()


def run(config_path):
    """
    Runs the AI version of the game with the given NEAT configuration file.

    Parameters:
    config_path (str): The path to the NEAT configuration file.

    This function creates a NEAT population with the given configuration, adds the
    standard reporters (StdOutReporter and StatisticsReporter), and runs the population
    for 50 generations, calling the main_ai function for each generation.
    """
    config_file = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation, 
                                config_path)

    population = neat.Population(config_file)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    winner = population.run(main_ai, 50)

if __name__ == "__main__":
    if config.AI:
        local_dir = os.path.dirname(__file__) if config.AI else None
        config_path = os.path.join(local_dir, 'AI/config/config.txt') if config.AI else None
        if config_path:
            run(config_path)
        else:
            assert Exception, "No config file found"
    else:
        game = Main()
        game.game_loop()
import pygame
import os
import config.config as config
import config.constants as constants
from scripts.Player import Player
from scripts.Background import Background
from scripts.PipeManager import PipeManager
from scripts.GUI import GUI
if config.AI:
    import neat
    from AI.scripts.Head import Head

class Main:
    def __init__(self):
        '''
        Pygame variables
        '''
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption(constants.TITLE)
        self.window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.screen = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_is_on = True
        
        '''
        Objects
        '''
        self.player = Player()
        self.background = Background()
        self.pipe_manager = PipeManager()
        self.pipes = self.pipe_manager.get_pipes()
        self.gui = GUI()
        self.ai_head = Head() if config.AI else None
        
        self.objects = [
            self.background,
            self.player,
            self.pipe_manager,
            self.gui
        ]
        
        self.reset()

    def reset(self):
        '''
        Resets all objects in the game to their initial state
        '''
        for obj in self.objects:
            try:
                obj.reset()
            except Exception as e:
                pass
        self.pipes = self.pipe_manager.get_pipes()
        
    def game_loop(self):
        
        '''
        Main game loop that runs continuously while the game is active.
        
        This loop handles input events, updates game objects, and renders the game
        frame by frame. It processes user inputs such as quitting the game, jumping,
        and resetting. The loop also calls update and draw methods for each game
        object, scales the screen, and manages the frame rate.
        '''

        while self.game_is_on:
            '''
            Handle events
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_on = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_r:
                        self.reset()
            
            if pygame.mouse.get_pressed()[0]:
                self.player.jump()
            
            '''
            Update
            '''
            def update():
                '''
                Updates the state of non-player game objects.

                Iterates over all objects in the game, updating them if they are not
                instances of the Player class. Handles exceptions silently and sets
                the collision flag to False by default.
                '''
                collision = False
                for object in self.objects:
                    try:
                        if not isinstance(object, Player):
                            object.update()
                        else:
                            collision, self.gui = object.update(self.pipes, self.gui)
                    except Exception as e:
                        pass
                if collision == True:
                    self.reset()
            update()
            
            '''
            Draw
            '''
            def draw():
                '''
                Renders all game objects to the screen.

                Iterates through each object in the game and calls its draw method
                to render it onto the screen surface.
                '''

                for object in self.objects:
                    object.draw(self.screen)
            draw()
            
            
            '''
            Pygame screen blit
            '''
            scaled_surface = pygame.transform.scale(self.screen, self.window.get_size())
            self.window.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(config.FPS)

        pygame.quit()

class MainAI(Main):
    def __init__(self, genomes, config_file):
        '''
        Pygame variables
        '''
        super().__init__()
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption(constants.TITLE)
        
        self.window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.screen = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_is_on = True
        
        '''
        AI Variables
        '''
        self.nets = []
        self.gens = []
        self.neurons = []
        
        for _, gen in genomes:
            net = neat.nn.FeedForwardNetwork.create(gen, config_file)
            self.nets.append(net)
            self.neurons.append(Player())
            gen.fitness = 0
            self.gens.append(gen)
        
        
        '''
        Variables
        '''
        self.last_score = 0
        self.score = 0
        
        '''
        Objects
        '''
        self.background = Background()
        self.pipe_manager = PipeManager()
        self.pipes = self.pipe_manager.get_pipes()
        self.gui = GUI()
        self.ai_head = Head() if config.AI else None
        
        # final self.objects:
        # [self.background, self.neuron_1, self.neuron_2..., self.pipe_manager, self.gui]
        self.objects = [self.background]
        self.objects.extend(self.neurons)
        self.objects.extend([self.pipe_manager, self.gui]) 
        
        self.reset()
        
    def game_loop(self):
        '''
        Main game loop that runs continuously while the game is active.
        
        This loop handles input events, updates game objects, and renders the game
        frame by frame. It processes user inputs such as quitting the game, jumping,
        and resetting. The loop also calls update and draw methods for each game
        object, scales the screen, and manages the frame rate.
        '''
        while self.game_is_on:
            '''
            Handle events
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()    
            '''
            Update
            '''
            def update():
                """
                Updates the state of non-player game objects.

                Iterates over all objects in the game, updating them if they are not
                instances of the Player class. Handles exceptions silently and sets
                the collision flag to False by default.
                """

                collision = False
                for index, object in enumerate(self.objects):
                    try:
                        if not isinstance(self.objects[index], Player):
                            self.objects[index].update()
                        else:
                            continue
                    except Exception as e:
                        pass
            update()
            
            '''
            AI Update
            '''
            def ai_update():
                '''
                AI update loop that runs every frame. It updates the AI's perception of the game world,
                runs the neural network, and then updates the player based on the output of the neural network.
                It also updates the fitness of each genome and removes any genomes that have a collision.
                '''
                if not self.neurons:
                    self.game_is_on = False
                    return

                self.pipe_manager.update()
                self.pipes = self.pipe_manager.get_pipes()

                prev_score = self.score

                for i in range(len(self.neurons) - 1, -1, -1):
                    neuron = self.neurons[i]
                    collision, self.gui = neuron.update(self.pipes, self.gui)
                    if collision:
                        self.gens[i].fitness -= 1
                        self.neurons.pop(i)
                        self.nets.pop(i)
                        self.gens.pop(i)
                        continue

                    data = neuron.get_stored_data()
                    self.ai_head.set_data(data)
                    inputs = self.ai_head.get_data()
                    output = self.nets[i].activate(inputs)
                    if output[0] > 0.5:
                        neuron.jump()

                    self.gens[i].fitness += 0.1

                if not self.neurons:
                    self.game_is_on = False
                    return

                self.score = self.neurons[0].get_score()
                if self.score != prev_score:
                    for gen in self.gens:
                        gen.fitness += 5

            
            if config.AI:
                ai_update()
                if self.game_is_on == False:
                    break
            
            '''
            Draw
            '''
            def draw():
                '''
                Draws all game objects onto the game screen.

                This includes the background, each neuron (AI player), the pipes, and the GUI.
                '''
                self.screen.fill((0, 0, 0))
                self.background.draw(self.screen)
                for neuron in self.neurons:
                    neuron.draw(self.screen)
                self.pipe_manager.draw(self.screen)
                self.gui.draw(self.screen)
            draw()
            
            
            '''
            Pygame screen blit
            '''
            scaled_surface = pygame.transform.scale(self.screen, self.window.get_size())
            self.window.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(config.FPS)



def main_ai(genomes, config_file):
    """
    Initializes the AI version of the game and starts the game loop.

    Parameters:
    genomes (list): A list of genome tuples provided by the NEAT library, representing AI players.
    config_file (neat.config.Config): The NEAT configuration file used to set up the neural networks.

    This function creates an instance of MainAI with the given genomes and configuration, and then
    calls the game_loop method to run the game.
    """

    game = MainAI(genomes, config_file)
    game.game_loop()


def run(config_path):
    """
    Runs the AI version of the game with the given NEAT configuration file.

    Parameters:
    config_path (str): The path to the NEAT configuration file.

    This function creates a NEAT population with the given configuration, adds the
    standard reporters (StdOutReporter and StatisticsReporter), and runs the population
    for 50 generations, calling the main_ai function for each generation.
    """
    config_file = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation, 
                                config_path)

    population = neat.Population(config_file)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    winner = population.run(main_ai, 50)

if __name__ == "__main__":
    if config.AI:
        local_dir = os.path.dirname(__file__) if config.AI else None
        config_path = os.path.join(local_dir, 'AI/config/config.txt') if config.AI else None
        if config_path:
            run(config_path)
        else:
            assert Exception, "No config file found"
    else:
        game = Main()
        game.game_loop()
