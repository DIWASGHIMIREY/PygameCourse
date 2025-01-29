import pygame
import random

WIDTH = 800
HEIGHT = 800
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.height = 40
        self.width = 15
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2
        self.rect.y = HEIGHT - (self.height+5)
        self.speedx = 8
        self.speedy = 3

    def update(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_d]:
            self.rect.x += self.speedx
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH

        if k[pygame.K_a]:
            self.rect.x -= self.speedx
            if self.rect.left <= 0:
                self.rect.left = 0


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.height = 10
        self.width = 10
        self.image = pygame.Surface((self.height,self.width))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.width)
        self.rect.y = random.randint(-50, -10)
        self.speedy = random.randint(3, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# initialize pygame and create window
pygame.init()

#pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()

ship = Player()
all_sprites.add(ship)

meteor_spawn_delay = 500
last_meteor_spawn = pygame.time.get_ticks()

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    current_time = pygame.time.get_ticks()

    if current_time - last_meteor_spawn > meteor_spawn_delay:
        meteor = Meteor()
        all_sprites.add(meteor)
        meteors.add(meteor)
        last_meteor_spawn = current_time

    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()