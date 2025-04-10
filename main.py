import pygame
import random
import sys

# Inicjalizacja
pygame.init()
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 32)

# Kolory
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)

# Stałe gry
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_GAP = 150
PIPE_WIDTH = 60
PIPE_SPEED = 3
GROUND_HEIGHT = 80

# Obraz ptaka (prosty prostokąt)
BIRD_WIDTH = 34
BIRD_HEIGHT = 24

# Klasa ptaka
class Bird:
    def __init__(self):
        self.x = 60
        self.y = HEIGHT // 2
        self.vel = 0
        self.rect = pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # losowy kolor

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.y = int(self.y)

    def flap(self):
        self.vel = JUMP_STRENGTH

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)

# Klasa rury
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, HEIGHT - PIPE_GAP - GROUND_HEIGHT - 50)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP - GROUND_HEIGHT)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        pygame.draw.rect(SCREEN, GREEN, self.top_rect)
        pygame.draw.rect(SCREEN, GREEN, self.bottom_rect)

# Funkcja do rysowania tekstu
def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.SysFont("Arial", size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y)) if center else surface.get_rect(topleft=(x, y))
    SCREEN.blit(surface, rect)

# Funkcja główna
def main():
    bird = Bird()
    pipes = [Pipe(WIDTH + 100)]
    score = 0
    running = True
    game_over = False

    while running:
        CLOCK.tick(60)
        SCREEN.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                if event.key == pygame.K_r and game_over:
                    main()

        if not game_over:
            bird.update()

            # Dodaj nową rurę
            if pipes[-1].x < WIDTH - 200:
                pipes.append(Pipe(WIDTH + random.randint(50, 100)))

            # Aktualizuj i rysuj rury
            for pipe in pipes:
                pipe.update()
                pipe.draw()

                # Sprawdź punkt
                if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                    score += 1
                    pipe.passed = True

                # Kolizja
                if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                    game_over = True

            # Usuń niewidoczne rury
            pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

            # Kolizja z ziemią
            if bird.y + BIRD_HEIGHT > HEIGHT - GROUND_HEIGHT:
                game_over = True

        bird.draw()

        # Rysuj ziemię
        pygame.draw.rect(SCREEN, (222, 184, 135), (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        draw_text(f"Score: {score}", 32, WHITE, WIDTH // 2, 40)

        if game_over:
            draw_text("Game Over", 48, (255, 0, 0), WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("Press R to Restart", 28, WHITE, WIDTH // 2, HEIGHT // 2 + 10)

        pygame.display.flip()

# Start gry
if __name__ == "__main__":
    main()
