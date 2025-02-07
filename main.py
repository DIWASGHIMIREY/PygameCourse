import pygame
import random

WIDTH = 800
HEIGHT = 800
FPS = 30
MAX_HP = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font_name = pygame.font.match_font("arial")
def draw_text(surf,text,size,x,y,color):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos1,pos2):
        pygame.sprite.Sprite.__init__(self,)
        self.height = 20
        self.width = 10
        # self.image = pygame.Surface((self.width,self.height))
        # self.image.fill(RED)
        self.image = pygame.image.load('All Game Art/laserBlue03.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = pos1
        self.rect.bottom = pos2
        self.speedy = 3

    def update(self):
            self.rect.y -= self.speedy

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.height = 40
        self.width = 15
        # self.image = pygame.Surface((self.width,self.height))
        # self.image.fill(WHITE)
        self.image = pygame.image.load('All Game Art/playerShip1_orange.png')
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2
        self.rect.y = HEIGHT - (self.height+5)
        self.speedx = 8
        self.speedy = 3
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 300
        self.score = 0
        self.health = MAX_HP
        self.lives = 5
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullet)
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
        self.height = 30
        self.width = 30
        self.image_list = []

        # self.image = pygame.Surface((self.height,self.width))
        # self.image.fill(WHITE)
        for i in range(1,11):
            self.image = pygame.image.load(f'All Game Art/meteor{i}.png')
            self.image_list.append(self.image)
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
bullets = pygame.sprite.Group()

ship = Player()
all_sprites.add(ship)


meteor_spawn_delay = 500
last_meteor_spawn = pygame.time.get_ticks()

background = pygame.image.load('All Game Art/starfield.png')
background = pygame.transform.scale(background, (WIDTH,HEIGHT))
background_rect = background.get_rect()

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
    hit_player =  pygame.sprite.spritecollide(ship,meteors,True)
    hit_mob = pygame.sprite.groupcollide(meteors,bullets,True,True)
    if hit_player:
        ship.health -= 5
        if ship.health <= 0:
            ship.health = MAX_HP
            ship.lives -= 1
        if ship.lives <= 0:
            running = False
    if hit_mob:
        ship.score += 1


    all_sprites.update()

    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(ship.score), 32, WIDTH// 4, 10, WHITE)
    draw_text(screen, str(ship.health), 32, (WIDTH // 2.5) + (WIDTH//2.5), 10, WHITE)
    draw_text(screen, str(ship.lives), 32, WIDTH // 2, 10, WHITE)


    pygame.display.flip()

pygame.quit()