import pygame
import random

WIDTH = 800
HEIGHT = 800
FPS = 30
MAX_HP = 50

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

def newmob():
    r = Meteor()
    meteors.add(r)

    all_sprites.add(r)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos1,pos2):
        pygame.sprite.Sprite.__init__(self,)
        self.height = 20
        self.width = 10

        # self.image = pygame.Surface((self.width,self.height))
        # self.image.fill(RED)

        self.image = pygame.image.load('All Files/laserBlue03.png')
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

        self.image = pygame.image.load('All Files/playerShip1_orange.png')
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.rect = self.image.get_rect()


        self.rect.x = WIDTH//2
        self.rect.y = HEIGHT - (self.height+5)
        self.speedx = 8
        self.speedy = 3

        self.last_shot = pygame.time.get_ticks()
        self.last_reload = pygame.time.get_ticks()


        self.shoot_delay = 500
        self.reload_time = 2500

        self.reloading = False

        self.score = 0
        self.ammo = 40
        self.max_ammo = 40
        self.health = MAX_HP
        self.lives = 5

    def shoot(self):
        now = pygame.time.get_ticks()

        if self.reloading:
            if now - self.last_reload > self.reload_time:
                self.ammo = self.max_ammo
                self.reloading = False
            return

        if self.ammo <= 0:
            self.ammo = 0
            self.reloading = True
            self.last_reload = now

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now

            bullet = Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullet)

            bullets.add(bullet)
            self.ammo -= 1
            shoot_sound.play()

    def update(self):
        k = pygame.key.get_pressed()
        mp = pygame.mouse.get_pressed()

        if k[pygame.K_d]:
            self.rect.x += self.speedx
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH

        if k[pygame.K_a]:
            self.rect.x -= self.speedx
            if self.rect.left <= 0:
                self.rect.left = 0
        if mp[0]:
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
            filename = pygame.image.load(f'All Files/Meteor Sprites/meteor{i}.png')
            self.image_list.append(filename)
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, WIDTH - self.width)
        self.rect.y = random.randint(-50, -10)
        self.speedy = random.randint(3, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

icon = pygame.image.load("All Files/gameicon.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

meteors = pygame.sprite.Group()
bullets = pygame.sprite.Group()

r = Meteor()
ship = Player()

all_sprites.add(ship)

meteor_spawn_delay = 500
last_meteor_spawn = pygame.time.get_ticks()

background = pygame.image.load('All Files/starfield.png')
background = pygame.transform.scale(background, (WIDTH,HEIGHT))

background_rect = background.get_rect()
pygame.mixer.music.load('All Files/Audio/background_audio.wav')
pygame.mixer.music.play(-1)

shoot_sound = pygame.mixer.Sound('All Files/Audio/laser_fire.wav')

explosion_sound_list = []
for i in range(1, 10):
    soundfile = pygame.mixer.Sound(f'All Files/Audio/Explosions/boom{i}.wav')
    explosion_sound_list.append(soundfile)

shoot_sound.set_volume(0.05)
pygame.mixer.music.set_volume(0.05)

for sound in explosion_sound_list:
    sound.set_volume(0.05)


running = True
game_over = False

while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ship.lives = 5
                    ship.health = MAX_HP
                    ship.score = 0
                    ship.ammo = ship.max_ammo
                    all_sprites.empty()
                    meteors.empty()
                    bullets.empty()
                    all_sprites.add(ship)
                    game_over = False
                if event.key == pygame.K_q:
                    running = False
    if game_over:
        pygame.mixer.music.stop()
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 2.5, RED)
        draw_text(screen, "Press SPACE to Restart", 32, WIDTH // 2, (HEIGHT // 2.5) - 20, RED)
        draw_text(screen, "Press Q to Quit", 32, WIDTH // 2, (HEIGHT // 2.5) + 55, RED)
        pygame.display.flip()
    else:

        if current_time - last_meteor_spawn > meteor_spawn_delay:
            newmob()
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
                    game_over = True

        if hit_mob:
            ship.score += 5
            explosion_sound = random.choice(explosion_sound_list).play()


        all_sprites.update()

        screen.blit(background, background_rect)
        all_sprites.draw(screen)

        draw_text(screen, f"Score: {ship.score}", 32, WIDTH // 4, 10, WHITE)
        draw_text(screen, f"HP: {ship.health}", 32, WIDTH // 2, 10, WHITE)

        draw_text(screen, f"Lives: {ship.lives}", 32, WIDTH - 100, 10, WHITE)
        draw_text(screen, f"{ship.ammo}/40", 32, WIDTH - 100, HEIGHT - 50, WHITE)

        if ship.reloading:
            draw_text(screen, "RELOADING...", 32, WIDTH // 2, HEIGHT - 40, RED)

        pygame.display.flip()

pygame.quit()