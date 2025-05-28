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
        for obj in self.objects:
            try:
                obj.reset()
            except Exception as e:
                pass
        self.pipes = self.pipe_manager.get_pipes()
        
    def game_loop(self):
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
        print(self.objects)
        
        
        self.reset()
    def game_loop(self):
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
            
            def ai_update():
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
    game = MainAI(genomes, config_file)
    game.game_loop()


def run(config_path):
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
            assert "No config file found"
    else:
        game = Main()
        game.game_loop()
