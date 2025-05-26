from scripts.Assets import Assets

class Background:
    def __init__(self):
        self.assets = Assets()
        self.x = 0
        self.y = 0
    
    def draw(self, screen):
        screen.blit(self.assets.assets['background'][0], (self.x, self.y))