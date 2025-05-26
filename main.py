import pygame
import config.config as config
import config.constants as constants
from scripts.player import Player
from scripts.Background import Background
from scripts.PipeManager import PipeManager
from scripts.GUI import GUI

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
                    print('collision', collision)
                    self.reset()
            update()
            
            '''
            Draw
            '''
            self.screen.fill((0, 0, 0))
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

if __name__ == "__main__":
    game = Main()
    game.game_loop()
