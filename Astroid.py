# Python Template

import pygame
import random
import os
from os import path

WIDTH = 480
HEIGHT = 600
FPS = 30
POWER_TIME = 3000

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
Olive = (128, 128, 0)
BLUEE = (0,126,192)

# PyGame Initialization
pygame.init()
pygame.mixer.init()  # Mixer for sound mixing
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Display
pygame.display.set_caption("Asteroids")  # Game Title
clock = pygame.time.Clock()  # Game Clock

# ---------------------------------Directories---------------------------------------------------------
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, ".\Assets\img")
sound_folder = os.path.join(game_folder, ".\Assets\Sounds")
explosion_folder = os.path.join(game_folder, ".\Assets\img\Explosions")
asteroids_folder = os.path.join(game_folder, ".\Assets\img\Asteroids")

# ---------------------------------Function Definitions-----------------------------------------------------------

# Text draw on screen
font_name = pygame.font.match_font("sitkasmallsitkatextsitkasubheadingsitkaheadingsitkadisplaysitkabanner")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)


# Enemy Generation
def __newmob__():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


# Health Bar
def draw_shield_bar(surf, x,y,percentage):
    if percentage < 0:  # So that Bar doesn't go lower than 0 Percentage in any case
        percentage = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage/100)*BAR_LENGTH  # How much health is respect to length of bar
    outline_rect = pygame.Rect(x,y,BAR_LENGTH, BAR_HEIGHT)  # Rectangular for bar on screen
    fill_rect = pygame.Rect(x,y,fill, BAR_HEIGHT)  # Rectangular for Filled color on bar
    pygame.draw.rect(surf, GREEN, fill_rect)  # On Screen Surface, Green Filled Rect
    pygame.draw.rect(surf, WHITE, outline_rect,2)  # On screen White Colored Outline


def draw_lives(surf, x,y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img.set_colorkey(BLACK)
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def show_goDisplay():
    screen.blit(background, background_rect)
    draw_text(screen, "Asteroids", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Arrow Keys Move, Space to Fire", 22,
               WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# -------------------------------Sprite Definitions--------------------------------------------------------------


# Player Sprite
class Player(pygame.sprite.Sprite):
    # Function for player self or body
    def __init__(self):  # Player Settings
        pygame.sprite.Sprite.__init__(self)  # Player Initialization
        self.image =pygame.transform.scale(player_img,(35, 35))  # Player Image
        self.image.set_colorkey(BLACK)  # So that black boundaries of player rect don't show
        self.rect = self.image.get_rect()  # Initialization of player rect
        self.radius = int(self.rect.width/2 - 4)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.x_speed = 0
        self.shield = 100
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    # Shooting Settings
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power ==1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                laser_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left + 6, self.rect.centery)  # Because of player size + 5px left of the player image
                bullet2 = Bullet(self.rect.right - 6, self.rect.centery)  # Because of player size - 5px right of the player image
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                laser_sound.play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.centerx, self.rect.centery)
                bullet3 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                laser_sound.play()

    def __powerup__(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    # How player is to be updated
    def update(self):
        # timeout for powerup
        if (self.power == 2) and pygame.time.get_ticks() - self.power_time > POWER_TIME:
            self.power -= 1
        if self.power >= 3 and pygame.time.get_ticks() - self.power_time > POWER_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT-10
        self.x_speed = 0
        keystat = pygame.key.get_pressed()
        if keystat[pygame.K_LEFT ] | keystat[pygame.K_a]:
            self.x_speed = -8
        if keystat[pygame.K_RIGHT] | keystat[pygame.K_d]:
            self.x_speed = 8
        '''if keystat[pygame.K_SPACE]:
            self.shoot()'''
        if keystat[pygame.K_SPACE] | keystat[pygame.K_x]:
            self.shoot()
        self.rect.x += self.x_speed
        # Boundary Constraints so player doesn't go off screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 200)


# Enemy Sprite
class Mob(pygame.sprite.Sprite):
    # Enemy Body Settings
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Enemy body Initialization
        self.image_orig = random.choice(meteor_images)  # Enemy Image choice from random meteors
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()  # Copy of Original Image of Enemy so when rotating, the Original image doesn't get affected
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85/2)  # Radius of Circle
        pygame.draw.circle(self.image, Olive, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.y_speed = random.randrange(5, 10)
        self.x_speed = random.randrange(-1, 8)
        self.rot = 0
        self.rot_speed = random.randrange(-10, 10)  # Rotation speed Range
        self.last_update = pygame.time.get_ticks()

    # Rotation setting for meteor Rotation
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.image = pygame.transform.rotate(self.image, self.rot_speed)
            new_image = self.image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        if (self.rect.top > HEIGHT+10) | (self.rect.left < -20) | (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH- self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.y_speed = random.randrange(1, 10)


# Bullet Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser_img, (10, 35))
        self.image.set_colorkey(WHITE)
        # self.image = pygame.Surface((10,20))
        # self.image.fill(RED)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:  # Kill the sprite if it movies out of display
            self.kill()


# Explosion Sprite
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Power-up sprite
class Powerup(pygame.sprite.Sprite):
        def __init__(self, center):
            pygame.sprite.Sprite.__init__(self)
            self.type = random.choice(['shield', 'gun'])
            self.image = powerup_images[self.type]
            self.image.set_colorkey(WHITE)
            # self.image = pygame.Surface((10,20))
            # self.image.fill(RED)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.speedy = 5

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom > HEIGHT:
                self.kill()


# -----------------------------------Graphics / Assets ---------------------------------------------

# Images===================================================End========================
backgrounds = random.choice(["Backgrounds/bg1.png", "Backgrounds/bg2.png", "Backgrounds/bg3.jpg",
                             "Backgrounds/bg4.png", "Backgrounds/bg5.jpg"])
print(" Setting Background: ", backgrounds)
background = pygame.image.load(path.join(img_folder, backgrounds)).convert()
background_rect = background.get_rect()
players = random.choice(["Players/player1.png", "Players/player2.png", "Players/player3.png", "Players/player4.png",
                         "Players/player5.png"])
print("Player is: ", players)
player_img = pygame.image.load(os.path.join(img_folder, players)).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
# meteor_img = pygame.image.load(os.path.join(img_folder, "meteor1.png")).convert()
bullet = random.choice(["Bullets/bullet0.png", "Bullets/bullet1.png", "Bullets/bullet2.png"])
laser_img = pygame.image.load(os.path.join(img_folder, bullet)).convert()
meteor_images = []
meteor_list = ["asteroids01.png", "asteroids02.png", "asteroids03.png",
               "asteroids04.png", "asteroids05.png", "asteroids06.png",
               "asteroids07.png", "asteroids08.png", "asteroids09.png",
               "asteroids10.png", "asteroids11.png", "asteroids12.png",
               "asteroids13.png", "asteroids14.png", "asteroids15.png",
               "asteroids16.png", "asteroids17.png", "asteroids18.png",
               "asteroids21.png", "asteroids20.png", "asteroids21.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(asteroids_folder, img)).convert())
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_folder, 'PowerUps/shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_folder, 'PowerUps/bolt_gold.png')).convert()
# /Images======================================================End========================

# Explosions==================================================Start====================
explosion_animation = {}
explosion_animation['large'] = []
explosion_animation['small'] = []
explosion_animation['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(explosion_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_large = pygame.transform.scale(img, (75, 75))
    explosion_animation['large'].append(img_large)
    img_small = pygame.transform.scale(img, (32, 32))
    explosion_animation['small'].append(img_small)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(explosion_folder, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_animation['player'].append(img)
# /Explosions==================================================Start=================

# Sounds======================================================Start=================
laserSounds = random.choice(["LaserSounds/laserfire01.ogg", "LaserSounds/laserfire02.ogg"])
laser_sound = pygame.mixer.Sound(path.join(sound_folder, laserSounds))
explosion_sound = []
for sound in ["ExplosionSounds/Explosion0.wav", "ExplosionSounds/Explosion1.wav"]:
    explosion_sound.append(pygame.mixer.Sound(path.join(sound_folder, sound)))
bgSound = random.choice(["BackgroundSounds/bg1.ogg", "BackgroundSounds/bg2.ogg", "BackgroundSounds/bg3.mp3",
                         "BackgroundSounds/bg4.mp3", "BackgroundSounds/bg5.mp3"])
pygame.mixer.music.load(path.join(sound_folder, bgSound))
pygame.mixer.music.set_volume(0.4)
player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))
laserPowerSnd = random.choice(["PowerUP/LPow1.wav", "PowerUP/HPow2.wav"])
shieldPowerSnd = random.choice(["PowerUP/HPow1.wav", "PowerUP/HPow2.wav"])
power_sound = pygame.mixer.Sound(path.join(sound_folder, laserPowerSnd))
shield_sound = pygame.mixer.Sound(path.join(sound_folder, shieldPowerSnd))
# /Sounds========================================================End=================

# ----------------------------------Sprite Groups-------------------------------------------------------
'''all_sprites = pygame.sprite.Group()
player = Player()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
all_sprites.add(player)
for i in range(8):
    __newmob__()
'''

# ----------------------------Things to Initialize Before Game Starts--------------------------------------
# score = 0
pygame.mixer.music.play(loops=-1)  # Background Music loop forever
game_over = True


# ---------------------------Game Loop----------------------------------------------------------------------
running = True
while running:  # While game is running
    if game_over:
        show_goDisplay()
        game_over = False
        all_sprites = pygame.sprite.Group()
        player = Player()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        all_sprites.add(player)
        for i in range(8):
            __newmob__()
        score = 0

    # 0 Keep loop running at the right speed
    clock.tick(FPS)

    # 1. Draw (Anything that is drawn on the screen goes here)
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # After drawing everything Flip the display.
    pygame.display.flip()

    # 2 Events (Inputs, Anything happens on the Screen Goes here like Button Press Even etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Close when (x) is pressed
        '''elif event.type == pygame.KEYDOWN: #Check what key is down
             if event.key == pygame.K_SPACE: #If it is space than shoot
                 player.shoot()'''
    # Check if a Mob hits the player
    hits = (pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle))
    for hit in hits:
        player.shield -= hit.radius * 2  # Health loss dependent upon the size of meteor
        random.choice(explosion_sound).play()
        expl = Explosion(hit.rect.center, 'small')
        all_sprites.add(expl)
        __newmob__()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
        # Check to see if player hit a powerups
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10,30)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.__powerup__()
            power_sound.play()
    # If the player died and the explosion has finished playing
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

# 3. Update (Anything that keeps on happening or if something changes than that goes here like Health power Update etc.)
    all_sprites.update()
    # Check if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(explosion_sound).play()
        expl = Explosion(hit.rect.center, 'large')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Powerup(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        __newmob__()

pygame.quit()
