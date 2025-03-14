import pygame
import random

p = pygame

WIDTH = 800
HEIGHT = 800
FPS = 30
MAX_HP = 100
MAX_MANA = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (52, 183, 235)
YELLOW = (231,200,100)
PURPLE = (113, 52, 235)
IDK = (23,143,251)

running = True
game_over = False


font_name = p.font.match_font("arial")
def draw_text(surf,text,size,x,y,color):
    font = p.font.Font(font_name, size)

    text_surface = font.render(text,True,color)

    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)

    surf.blit(text_surface,text_rect)

def newmob():
    r = Mob()
    meteors.add(r)

    all_sprites.add(r)

def draw_lives(surf, x, y, lives, icon):
    for i in range(lives):
        surf.blit(icon, (x + 35 * i, y))

class Explosion(p.sprite.Sprite):
    def __init__(self, center, size):
        p.sprite.Sprite.__init__(self)
        self.width = 40
        self.height = 40
        self.size = size
        # Need shooting
        self.expl_anim = {}
        self.expl_anim['sm'] = []
        self.expl_anim['lg'] = []
        self.load_image()
        self.image = p.Surface((self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.center = center

        self.frame_rate = 75
        self.frame = 0
        self.last_update = p.time.get_ticks()

    def load_image(self):
        for i in range(1, 9):
            filename = f'All Files/Explosions/explosion{i}.png'
            img = p.image.load(filename)
            img_sm = p.transform.scale(img, (32, 32))
            self.expl_anim['sm'].append(img_sm)
            img_sm = p.transform.scale(img, (150, 150))
            self.expl_anim['lg'].append(img_sm)

    def update(self):
        now = p.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.expl_anim[self.size]):
                self.kill()
        else:
            center = self.rect.center
            self.image = self.expl_anim[self.size][self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

class Bullet(p.sprite.Sprite):
    def __init__(self,pos1,pos2,speedx):
        p.sprite.Sprite.__init__(self)
        self.height = 20
        self.width = 10
        self.initial_dmg = 1
        # self.image = p.Surface((self.width,self.height))
        # self.image.fill(RED)

        self.image = p.image.load('All Files/bullet.png')
        self.image = p.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.centerx = pos1
        self.rect.bottom = pos2
        self.speedy = 3
        self.speedx = speedx
    def update(self):
        self.rect.y -= self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom <= 0:
            self.kill()

class StatusBar(p.sprite.Sprite):
    def __init__(self, player):
        p.sprite.Sprite.__init__(self)
        self.player = player

        self.health_full = p.image.load('All Files/Art/GUI/Health_Full.png')
        self.health_empty = p.image.load('All Files/Art/GUI/Health_Empty.png')
        self.mana_full = p.image.load('All Files/Art/GUI/Mana_Full.png')
        self.mana_empty = p.image.load('All Files/Art/GUI/Mana_Empty.png')

        self.bar_width = 250
        self.bar_height = 45

        self.margin = 5
        self.spacing = (WIDTH//2) + 105


        self.health_x = (WIDTH + 207) - self.margin - self.bar_width
        self.mana_x = self.health_x - self.bar_width - self.spacing

        self.y = ((HEIGHT//8) - 50) - self.bar_height - self.margin

    def draw_bar(self, surface, full_image, empty_image, current, max_value, x, y, scale_factor=0.5):
        if max_value == 0:
            return

        new_width = int(empty_image.get_width() * scale_factor)
        new_height = int(empty_image.get_height() * scale_factor)

        empty_image = p.transform.scale(empty_image, (new_width, new_height))
        full_image = p.transform.scale(full_image, (new_width, new_height))

        filled_height = int(new_height * (current / max_value))
        filled_bar = full_image.subsurface((0, new_height - filled_height, new_width, filled_height))

        surface.blit(empty_image, (x, y))
        surface.blit(filled_bar, (x, y + (new_height - filled_height)))

    def update(self, screen):
        self.draw_bar(screen, self.health_full, self.health_empty, self.player.health, MAX_HP, self.health_x, self.y)
        self.draw_bar(screen, self.mana_full, self.mana_empty, self.player.mana, MAX_MANA, self.mana_x, self.y)

class Player(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.height = 50
        self.width = 45
        self.pw = [1,2,3,4]

        # self.image = p.Surface((self.width,self.height))
        # self.image.fill(WHITE)

        self.image = p.image.load('All Files/player.png')
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()


        self.rect.x = WIDTH//2
        self.rect.y = HEIGHT - (self.height+5)
        self.speedx = 8
        # self.speedy = 3

        self.last_shot = p.time.get_ticks()
        self.last_reload = p.time.get_ticks()
        self.last_refill = p.time.get_ticks()

        self.shoot_delay = 300
        self.reload_time = 2500
        self.refill_delay = 350

        self.reloading = False
        self.counter = 0

        # Player data
        self.score = 0
        self.ammo = 100
        self.max_ammo = 100
        self.health = MAX_HP
        self.mana = MAX_MANA
        self.lives = 3

        self.total_score = 0

        # Level data
        self.lvlup_threshold = 30
        self.lvl = 1

        # Powerups
        self.bullet_dmg = 1
        self.speedup = False
        self.dual_shot = False
        self.refilling = False

    def shoot(self):
        if self.ammo <= 0:
            self.ammo = 0
            self.reloading = True
            return

        if self.now - self.last_shot > self.shoot_delay:
            self.last_shot = self.now
            if self.dual_shot:
                b1 = Bullet(self.rect.centerx - 10, self.rect.top, -1)
                b2 = Bullet(self.rect.centerx + 10, self.rect.top, 1)
                b1.image = p.image.load("All Files/Powerups/bullet_dual.png")
                b2.image = p.image.load("All Files/Powerups/bullet_dual.png")
                all_sprites.add(b1, b2)
                bullets.add(b1, b2)
                self.mana -= 5
                if self.mana <= 0:
                    self.dual_shot = False
                    self.refilling = True
                    self.mana = 0

                self.ammo -= 2
                shoot_sound.play()

            else:
                bullet = Bullet(self.rect.centerx,self.rect.top, 0)
                all_sprites.add(bullet)
                bullets.add(bullet)
                if self.speedup:
                    bullet.image = p.image.load("All Files/Powerups/bullet_speed.png")
                self.ammo -= 1
                shoot_sound.play()
            if self.speedup:
                self.shoot_delay = 150
                self.mana -= 2
                if self.mana <= 0:
                    self.mana = 0
                    self.speedup = False
                    self.refilling = True
            else:
                self.shoot_delay = 300

    def update(self):
        self.now = p.time.get_ticks()
        k = p.key.get_pressed()
        mp = p.mouse.get_pressed()

        if k[p.K_d]:
            self.rect.x += self.speedx
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH

        if k[p.K_a]:
            self.rect.x -= self.speedx
            if self.rect.left <= 0:
                self.rect.left = 0
        if mp[0]:
            self.shoot()

        if self.refilling:
            if self.now - self.last_refill > self.refill_delay:
                self.last_refill = self.now
                self.mana += 5
                if self.mana >= MAX_MANA:
                    self.mana = MAX_MANA
                    self.refilling = False

        if self.reloading:
            if self.now - self.last_reload > self.reload_time:
                self.ammo = self.max_ammo
                self.last_reload = self.now
                self.reloading = False



class Mob(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.height = 70
        self.width = 65
        # self.image_list = []
        self.lives = random.randint(1,2)

        self.explosion_sound_list = []
        for i in range(1, 10):
            self.sound_file = p.mixer.Sound(f'All Files/Audio/Explosions/boom{i}.wav')
            self.explosion_sound_list.append(self.sound_file)

        for sound in self.explosion_sound_list:
            sound.set_volume(0.05)

        self.image = p.image.load("All Files/enemy.png")
        self.image = p.transform.scale(self.image, (self.width,self.height))

        # for i in range(1,11):
        #     filename = p.image.load(f'All Files/Mob Sprites/meteor{i}.png')
        #     self.image_list.append(filename)
        # self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, WIDTH - self.width)
        self.rect.y = random.randint(-50, -10)
        self.speedy = random.randint(3, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top >= HEIGHT:
            self.kill()
        if self.lives <= 0:
            plr.score += 1
            plr.total_score += 1
            self.kill()

class Power(p.sprite.Sprite):
    def __init__(self,x,y):
        p.sprite.Sprite.__init__(self)
        self.width = 30
        self.height = 30

        self.powerup_images = {
            1: "All Files/Powerups/reloading.png",
            2: "All Files/Powerups/double_shot.png",
            3: "All Files/Powerups/speedup.png",
            4: "All Files/Powerups/health_up.png",
        }
        self.type = random.choice([1, 2, 3, 4])
        self.load_image()

        self.rect = self.image.get_rect()

        self.rect.center = (x,y)
        # self.image.fill(WHITE)

        self.spawn_percent = 0.1
        self.spawn = False

        self.ran = random.random()

        self.speedx = random.randrange(3,8)
        self.speedy = 2
    def load_image(self):
        image_path = self.powerup_images.get(self.type, "All Files/Powerups/speedup.png")
        self.image = p.image.load(image_path)
        self.image = p.transform.scale(self.image, (self.width, self.height))

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > HEIGHT:
            self.kill()

def start_screen():
    screen.fill(BLACK)
    draw_text(screen, "WELCOME", 64, WIDTH // 2, HEIGHT // 2.5, PURPLE)
    draw_text(screen, "Press SPACE to Start", 32, WIDTH // 2, (HEIGHT // 2.5) - 25, PURPLE)
    draw_text(screen, "Press Q to Quit", 32, WIDTH // 2, (HEIGHT // 2.5) + 60, PURPLE)
    p.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in p.event.get():
            k = p.key.get_pressed()
            if event.type == p.QUIT:
                p.quit()
            if event.type == p.KEYDOWN:
                if k[p.K_SPACE]:
                    waiting = False
                if k[p.K_q]:
                    p.quit()

def level_up():
    plr.score = 0
    screen.fill(BLACK)
    draw_text(screen, "Level up!", 64, WIDTH // 2, (HEIGHT // 2.5) - 20, LIGHT_BLUE)
    draw_text(screen, f"Level {plr.lvl}", 32, WIDTH // 2, (HEIGHT // 2.5) + 55, LIGHT_BLUE)
    p.display.flip()
    waiting = True

    last = p.time.get_ticks()
    delay = 1500
    while waiting:
        clock.tick(FPS)
        now = p.time.get_ticks()
        all_sprites.empty()
        meteors.empty()
        bullets.empty()
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
        if now - last > delay:
            waiting = False
            all_sprites.add(plr)
            last = now

def boss_lvl():
    screen.fill(BLACK)
    if plr.lvl == 5:
        draw_text(screen, "Boss Level 1", 64, WIDTH // 2, (HEIGHT // 2.5) - 20, RED)
    elif plr.lvl == 10:
        draw_text(screen, "Boss Level 2", 64, WIDTH // 2, (HEIGHT // 2.5) - 20, RED)
    draw_text(screen, f"Level {plr.lvl}", 32, WIDTH // 2, (HEIGHT // 2.5) + 55, RED)
    draw_text(screen, f"Press C to Continue", 32, WIDTH // 2, (HEIGHT // 2.5) + 85, RED)
    draw_text(screen, f"Press V to Skip", 32, WIDTH // 2, (HEIGHT // 2.5) + 110, RED)
    p.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        all_sprites.empty()
        meteors.empty()
        bullets.empty()

        for event in p.event.get():
            k = p.key.get_pressed()
            if event.type == p.QUIT:
                p.quit()

            if k[p.K_c]:
                waiting = False
                all_sprites.add(plr)
            elif k[p.K_v]:
                waiting = False
                if plr.lvl != 11:
                    level_up()

p.init()
p.mixer.init()

screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Space Invaders")

icon = p.image.load("All Files/gameicon.png")
p.display.set_icon(icon)

clock = p.time.Clock()

start_screen()

all_sprites = p.sprite.Group()

meteors = p.sprite.Group()
powerups = p.sprite.Group()
bullets = p.sprite.Group()

plr = Player()

all_sprites.add(plr)

status_bar = StatusBar(plr)

meteor_spawn_delay = 600
last_meteor_spawn = p.time.get_ticks()

background = p.image.load('All Files/background.png')
background = p.transform.scale(background, (WIDTH, HEIGHT))

background_rect = background.get_rect()
p.mixer.music.load('All Files/Audio/background_audio.wav')
p.mixer.music.play(-1)

shoot_sound = p.mixer.Sound('All Files/Audio/laser_fire.wav')

life_icon = p.image.load('All Files/player.png')
life_icon = p.transform.scale(life_icon, (30, 30))

shoot_sound.set_volume(0.05)
p.mixer.music.set_volume(0.05)

while running:
    clock.tick(FPS)
    current_time = p.time.get_ticks()
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False


        if event.type == p.KEYDOWN and event.key == p.K_F11:
            p.display.toggle_fullscreen()
        if game_over:
            if event.type == p.KEYDOWN:
                if event.key == p.K_SPACE:
                    plr.lives = 5
                    plr.health = MAX_HP
                    plr.score = 0
                    plr.counter = 0
                    plr.ammo = plr.max_ammo
                    all_sprites.empty()
                    meteors.empty()
                    bullets.empty()
                    all_sprites.add(plr)
                    game_over = False
                if event.key == p.K_q:
                    running = False


    if game_over:
        p.mixer.music.stop()
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 2.5, RED)
        draw_text(screen, "Press SPACE to Restart", 32, WIDTH // 2, (HEIGHT // 2.5) - 25, PURPLE)
        draw_text(screen, "Press Q to Quit", 32, WIDTH // 2, (HEIGHT // 2.5) + 60, PURPLE)
        draw_text(screen, f"You killed {plr.total_score} mobs!", 32, WIDTH // 2, (HEIGHT // 2.5) + 100, YELLOW)
        p.display.flip()

    else:
        if current_time - last_meteor_spawn > meteor_spawn_delay:
            newmob()
            last_meteor_spawn = current_time

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False


        hit_player =  p.sprite.spritecollide(plr, meteors, True)
        hit_mob = p.sprite.groupcollide(meteors, bullets, False, True)
        hit_powers = p.sprite.spritecollide(plr, powerups, True)


        if hit_player:
            expl = Explosion(plr.rect.midtop,'sm')
            all_sprites.add(expl)
            plr.health -= 5
            if plr.health <= 0:
                plr.health = MAX_HP
                plr.lives -= 1
                if plr.lives <= 0:
                    game_over = True

        if hit_mob:
            for mob in hit_mob:
                mob.lives -= plr.bullet_dmg

                mob.explosion_sound = random.choice(mob.explosion_sound_list).play()
                if mob.lives <= 0:
                    expl = Explosion(mob.rect.center, 'lg')
                    all_sprites.add(expl)
                    pow = Power(mob.rect.centerx, mob.rect.centery)
                    if plr.lvl >= 2:
                        if pow.ran <= pow.spawn_percent:
                            pow.spawn = True
                        if pow.spawn:
                            powerups.add(pow)
                            all_sprites.add(pow)
                            pow.spawn = False

        if hit_powers:
            for power in hit_powers:
                plr.pwup = power.type

                if plr.pwup == 1:
                    plr.ammo = plr.max_ammo
                elif plr.pwup == 2:
                    plr.dual_shot = True
                    plr.bullet_dmg = 2
                elif plr.pwup == 3:
                    plr.speedup = True
                elif plr.pwup == 4:
                    plr.health += 10
                    if plr.health >= MAX_HP:
                        plr.health = MAX_HP



        if plr.score >= plr.lvlup_threshold:
            plr.score = 0
            plr.lvl += 1
            plr.counter += 1
            print(f"Count: {plr.counter}")
            if plr.lvl <= 4 or plr.lvl >= 6 and plr.lvl != 10 and plr.lvl != 11:
                level_up()

            elif plr.lvl == 5 or plr.lvl == 10:
                boss_lvl()
            elif plr.lvl >= 11:
                game_over = True

        if plr.counter == 2:
            pow.spawn_percent += 0.2
            print(f"Powerup percentage: {pow.spawn_percent}")
            plr.counter = 0
            meteor_spawn_delay -= 100
            print(f"Delay: {meteor_spawn_delay}")


        all_sprites.update()

        screen.blit(background, background_rect)
        all_sprites.draw(screen)

        status_bar.update(screen)

        draw_text(screen, f"{plr.score}/{plr.lvlup_threshold}", 32, (WIDTH // 4) - 115, 10, YELLOW)

        draw_lives(screen, WIDTH//2.25, 10, plr.lives, life_icon)
        draw_text(screen, f"{plr.ammo}/{plr.max_ammo}", 32, 60, HEIGHT - 50, IDK)

        if plr.reloading:
            draw_text(screen, "RELOADING...", 32, WIDTH // 2, HEIGHT - 40, RED)

        p.display.flip()

p.quit()