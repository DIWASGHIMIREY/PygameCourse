import pygame
import random
pg = pygame
WIDTH = 800
HEIGHT = 800
FPS = 30
MAX_HP = 50
MAX_MANA = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (231,200,100)
IDK = (23,143,251)
font_name = pg.font.match_font("arial")
def draw_text(surf,text,size,x,y,color):
    font = pg.font.Font(font_name,size)

    text_surface = font.render(text,True,color)

    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)

    surf.blit(text_surface,text_rect)

def newmob():
    r = Meteor()
    meteors.add(r)

    all_sprites.add(r)
class Power(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.height = 20
        self.width = 20


        self.image = pg.Surface((self.width,self.height))
        self.image.fill(IDK)
        self.rect = self.image.get_rect()

class Bullet(pg.sprite.Sprite):
    def __init__(self,pos1,pos2):
        pg.sprite.Sprite.__init__(self)
        self.height = 20
        self.width = 10
        self.initial_dmg = 1
        # self.image = pg.Surface((self.width,self.height))
        # self.image.fill(RED)

        self.image = pg.image.load('All Files/bullet.png')
        self.image = pg.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.centerx = pos1
        self.rect.bottom = pos2
        self.speedy = 3

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom <= 0:
            self.kill()

class StatusBar(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.player = player

        self.health_full = pg.image.load('Art/GUI/Health_Full.png')
        self.health_empty = pg.image.load('Art/GUI/Health_Empty.png')
        self.mana_full = pg.image.load('Art/GUI/Mana_Full.png')
        self.mana_empty = pg.image.load('Art/GUI/Mana_Empty.png')

        self.bar_width = 45
        self.bar_height = 250

        self.margin = 5
        self.spacing = -5

        self.health_x = WIDTH - self.margin - self.bar_width
        self.mana_x = self.health_x - self.bar_width - self.spacing

        self.y = HEIGHT - self.bar_height - self.margin

    def draw_bar(self, surface, full_image, empty_image, current, max_value, x, y, scale_factor=0.5):
        if max_value == 0:
            return

        new_width = int(empty_image.get_width() * scale_factor)
        new_height = int(empty_image.get_height() * scale_factor)

        empty_image = pg.transform.scale(empty_image, (new_width, new_height))
        full_image = pg.transform.scale(full_image, (new_width, new_height))

        filled_height = int(new_height * (current / max_value))
        filled_bar = full_image.subsurface((0, new_height - filled_height, new_width, filled_height))

        surface.blit(empty_image, (x, y))
        surface.blit(filled_bar, (x, y + (new_height - filled_height)))

    def update(self, screen):
        self.draw_bar(screen, self.health_full, self.health_empty, self.player.health, MAX_HP, self.health_x, self.y)
        self.draw_bar(screen, self.mana_full, self.mana_empty, self.player.mana, MAX_MANA, self.mana_x, self.y)

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.height = 40
        self.width = 25

        # self.image = pg.Surface((self.width,self.height))
        # self.image.fill(WHITE)

        self.image = pg.image.load('All Files/player.png')
        self.image = pg.transform.scale(self.image, (self.width,self.height))
        self.rect = self.image.get_rect()


        self.rect.x = WIDTH//2
        self.rect.y = HEIGHT - (self.height+5)
        self.speedx = 8
        # self.speedy = 3

        self.last_shot = pg.time.get_ticks()
        self.last_reload = pg.time.get_ticks()

        self.shoot_delay = 500
        self.reload_time = 2500

        self.reloading = False

        self.score = 0
        self.ammo = 40
        self.max_ammo = 40
        self.health = MAX_HP
        self.mana = MAX_MANA
        self.lives = 5

    def shoot(self):
        self.now = pg.time.get_ticks()

        if self.reloading:
            if self.now - self.last_reload > self.reload_time:
                self.ammo = self.max_ammo
                self.reloading = False
            return

        if self.ammo <= 0:
            self.ammo = 0
            self.reloading = True
            self.last_reload = self.now

        if self.now - self.last_shot > self.shoot_delay:
            self.last_shot = self.now

            bullet = Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullet)

            bullets.add(bullet)
            self.ammo -= 1
            shoot_sound.play()

    def update(self):
        kb = pg.key.get_pressed()
        m = pg.mouse.get_pressed()

        if kb[pg.K_d]:
            self.rect.x += self.speedx
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH

        if kb[pg.K_a]:
            self.rect.x -= self.speedx
            if self.rect.left <= 0:
                self.rect.left = 0
        if m[0]:
            self.shoot()


class Meteor(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.height = 30
        self.width = 30
        self.image_list = []
        self.lives = random.randint(1,3)
        self.k = False

        # self.image = pg.Surface((self.height,self.width))
        # self.image.fill(WHITE)

        for i in range(1,11):
            filename = pg.image.load(f'All Files/Meteor Sprites/meteor{i}.png')
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
        if self.lives <= 0:
            ship.score += 5
            self.k = True
        if self.k:
            self.kill()

pg.init()
pg.mixer.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Invaders")

icon = pg.image.load("All Files/gameicon.png")
pg.display.set_icon(icon)

clock = pg.time.Clock()

all_sprites = pg.sprite.Group()

meteors = pg.sprite.Group()
bullets = pg.sprite.Group()

r = Meteor()
ship = Player()

all_sprites.add(ship)

status_bar = StatusBar(ship)

meteor_spawn_delay = 500
last_meteor_spawn = pg.time.get_ticks()

background = pg.image.load('All Files/starfield.png')
background = pg.transform.scale(background, (WIDTH,HEIGHT))

background_rect = background.get_rect()
pg.mixer.music.load('All Files/Audio/background_audio.wav')
pg.mixer.music.play(-1)

shoot_sound = pg.mixer.Sound('All Files/Audio/laser_fire.wav')

explosion_sound_list = []
for i in range(1, 10):
    soundfile = pg.mixer.Sound(f'All Files/Audio/Explosions/boom{i}.wav')
    explosion_sound_list.append(soundfile)

shoot_sound.set_volume(0.05)
pg.mixer.music.set_volume(0.05)

for sound in explosion_sound_list:
    sound.set_volume(0.05)


running = True
game_over = False

while running:
    clock.tick(FPS)
    current_time = pg.time.get_ticks()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if game_over:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    ship.lives = 5
                    ship.health = MAX_HP
                    ship.score = 0
                    ship.ammo = ship.max_ammo
                    all_sprites.empty()
                    meteors.empty()
                    bullets.empty()
                    all_sprites.add(ship)
                    game_over = False
                if event.key == pg.K_q:
                    running = False
    if game_over:
        pg.mixer.music.stop()
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 2.5, RED)
        draw_text(screen, "Press SPACE to Restart", 32, WIDTH // 2, (HEIGHT // 2.5) - 20, RED)
        draw_text(screen, "Press Q to Quit", 32, WIDTH // 2, (HEIGHT // 2.5) + 55, RED)
        pg.display.flip()
    else:

        if current_time - last_meteor_spawn > meteor_spawn_delay:
            newmob()
            last_meteor_spawn = current_time

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        hit_player =  pg.sprite.spritecollide(ship,meteors,True)
        hit_mob = pg.sprite.groupcollide(meteors,bullets,False,True)


        if hit_player:
            ship.health -= 5
            if ship.health <= 0:
                ship.health = MAX_HP
                ship.lives -= 1
                if ship.lives <= 0:
                    game_over = True

        if hit_mob:
            for mob in hit_mob:
                mob.lives -= 1
            explosion_sound = random.choice(explosion_sound_list).play()



        all_sprites.update()

        screen.blit(background, background_rect)
        all_sprites.draw(screen)

        status_bar.update(screen)

        draw_text(screen, f"Score: {ship.score}", 32, (WIDTH // 4) - 100, 10, YELLOW)

        draw_text(screen, f"Lives: {ship.lives}", 32, WIDTH - 100, 10, WHITE)
        draw_text(screen, f"{ship.ammo}/40", 32, 50, HEIGHT - 50, WHITE)

        if ship.reloading:
            draw_text(screen, "RELOADING...", 32, WIDTH // 2, HEIGHT - 40, RED)

        pg.display.flip()

pg.quit()