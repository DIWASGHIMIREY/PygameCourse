import pygame
import random

WIDTH = 800
HEIGHT = 800
FPS = 30


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.height = 20
        self.width = 10
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = 3

    def update(self):
            self.rect.y -= self.speedy

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
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 300

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets = pygame.sprite.Group()
            bullets.add(bullet)

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
        if k[pygame.K_SPACE]:
            self.shoot()


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



pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()


ship = Player()
all_sprites.add(ship)

meteor_spawn_delay = 500
last_meteor_spawn = pygame.time.get_ticks()


running = True
while running:
    clock.tick(FPS)

    current_time = pygame.time.get_ticks()

    if current_time - last_meteor_spawn > meteor_spawn_delay:
        meteor = Meteor()
        all_sprites.add(meteor)
        meteors.add(meteor)
        last_meteor_spawn = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    all_sprites.update()

    screen.fill(BLACK)
    all_sprites.draw(screen)


    pygame.display.flip()

pygame.quit()