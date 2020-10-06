#Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
#Art from Kenney.nl
import pygame
import random
from os import path

pygame.init()
pygame.mixer.init()
pygame.font.init()

width = 750
height = 350
scr_size = (width, height)
FPS = 60
gravity = 0.6

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

background_col = (235, 35, 235)

high_score = 0

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("AlienShooter ")

img_png = path.join(path.dirname(__file__), 'sprites')
snd_wav = path.join(path.dirname(__file__), 'sprites')

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 90
    BAR_HEIGHT = 10
    fill = (pct / 90) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)


def disp_gameOver_msg(retbutton_image, gameover_image):
    retbutton_rect = retbutton_image.get_rect()
    retbutton_rect.centerx = width / 2
    retbutton_rect.top = height*0.52

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height*0.35

    screen.blit(retbutton_image, retbutton_rect)
    screen.blit(gameover_image, gameover_rect)


def extractDigits(number):
    if number > -1:
        digits = []
        i = 0
        while(number/10 != 0):
            digits.append(number % 10)
            number = int(number/10)

        digits.append(number % 10)
        for i in range(len(digits), 5):
            digits.append(0)
        digits.reverse()
        return digits


# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.Surface((20, 10))
#         self.image.fill(yellow)
#         self.rect = self.image.get_rect()
#         self.rect.bottom = y
#         self.rect.centerx = x
#         self.speedx = 10
#
#     def update(self):
#         self.rect.x += self.speedx
#         if self.rect.bottom < 0:
#             self.kill()


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(grass_img, (750, 75))
        self.rect = self.image.get_rect()
        self.rect.y = 275
        self.rect.x = 0
        self.speed = 0

    def update(self):
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = enemy_img
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.bottom = int(0.79*height)
        self.rect.left = width + self.rect.width
        self.movement = [-1*speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Bat(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = bat_img
        self.images.set_colorkey(black)
        self.rect = self.images.get_rect()
        self.bat_height = [height*0.44, height*0.40, height*0.35]
        self.rect.centery = self.bat_height[random.randrange(0, 3)]
        self.rect.left = width + self.rect.width
        self.image = self.images
        self.movement = [-1*speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1) % 2
        self.image = self.images
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hide_timer = pygame.time.get_ticks()
        self.hidden = False
        self.image = alien_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = int(0.79 * height)
        self.rect.left = width / 15
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 13.6
        self.shield = 90

        self.stand_pos_width = self.rect.width

    def checkbounds(self):
        if self.rect.bottom > int(0.79 * height):
            self.rect.bottom = int(0.79 * height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2

        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.isDead:
           self.index = 4

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()

        self.counter = (self.counter + 1)

    def draw(self):
        pass

    # def shoot(self):
    #     bullet = Bullet(self.rect.centerx, self.rect.centery)
    #     bullets.add(bullet)
    #     all_sprites.add(bullet)

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (79, 230.5)


class Bush(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = bush_img1
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = int(0.79*height)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = width


alien_img = pygame.image.load(path.join(img_png, "p1_stand.png")).convert()
alien1_img = pygame.image.load(path.join(img_png, "p1_duck.png")).convert()
enemy_img = pygame.image.load(path.join(img_png, "enemy.png"))
enemy_img1 = pygame.transform.scale(enemy_img, (63, 85))
bat_img = pygame.image.load(path.join(img_png, "bat_fly.png")).convert()
bush_img = pygame.image.load(path.join(img_png, "bush.png")).convert()
bush_img1 = pygame.transform.scale(bush_img, (125, 43))
grass_img = pygame.image.load(path.join(img_png, "grass1.png")).convert()
alienLaser_img = pygame.image.load(path.join(img_png, "laserBlue01.png")).convert()
spiderLaser_img = pygame.image.load(path.join(img_png, "laserRed01.png"))
numbers_img = pygame.image.load(path.join(img_png, "numbers.png")).convert()
gameOver_img = pygame.image.load(path.join(img_png, "game_over.png")).convert()
replayButton_img = pygame.image.load(path.join(img_png, "replay_button.png")).convert()
background_img = pygame.image.load(path.join(img_png, "blue.png")).convert()
background = pygame.transform.scale(background_img, (750, 350))
background_rect = background.get_rect()

jump_sound = pygame.mixer.Sound(path.join(snd_wav, "Jump.wav"))
checkPoint_sound = pygame.mixer.Sound(path.join(snd_wav, 'checkPoint.wav'))
shoot_sound = pygame.mixer.Sound(path.join(snd_wav, 'Laser_Shoot4.wav'))
die_sound = pygame.mixer.Sound(path.join(snd_wav, 'Hit_Hurt5.wav'))
pygame.mixer.music.load(path.join(snd_wav, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.6)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "AlienShooter", 64, width / 2, height / 4)
    draw_text(screen, "direct by Andrey Solovey", 22,
              width / 2, height / 2)
    draw_text(screen, "Press a key to begin", 18, width / 2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


#bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
alien = Alien()
ground = Ground()
all_sprites.add(alien)
all_sprites.add(ground)
bush = Bush()
all_sprites.add(bush)
#all_sprites.add(bullets)
mobs = pygame.sprite.Group()


def gameplay():
    global high_score
    gamespeed = 7
    startMenu = False
    gameOver = False
    gameQuit = False
    counter = 0


    bullets = pygame.sprite.Group()
    bat = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    alien = Alien()
    bush = Bush()
    ground = Ground()
    Enemy.containers = enemy
    Bat.containers = bat

    all_sprites.add(alien)
    all_sprites.add(ground)
    all_sprites.add(bush)
    #all_sprites.add(e)
    #all_sprites.add(b)

    retbutton_image = replayButton_img
    retbutton_image.set_colorkey(white)
    retbutton_rect = retbutton_image.get_rect()
    gameover_image = gameOver_img
    gameover_image.set_colorkey(black)
    gameover_rect = gameover_image.get_rect()
    pygame.mixer.music.play(loops=-1)
    while not gameQuit:
        while startMenu:
            pass
        while not gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if alien.rect.bottom == int(0.79*height):
                                alien.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                alien.movement[1] = -1*alien.jumpSpeed

                        if event.key == pygame.K_DOWN:
                            if not (alien.isJumping and alien.isDead):
                                alien.isDucking = True
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            alien.isDucking = False
            if alien.score > 200:
                gamespeed = 8
            if alien.score > 300:
                gamespeed = 8.5
            if alien.score > 400:
                gamespeed = 9
            if alien.score > 550:
                gamespeed = 9.3
            for e in enemy:
                e.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(alien, e):
                    alien.shield -= 30
                    alien.hide()
                    if alien.shield <= 0:
                        alien.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()
            for b in bat:
                b.movement[0] = -1*(gamespeed + 1.5)
                if pygame.sprite.collide_mask(alien, b):
                    alien.shield -= 30
                    alien.hide()
                    if alien.shield <= 0:
                        alien.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

            if len(enemy) < 2:
                if len(enemy) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Enemy(gamespeed, 40, 40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width*0.7 and random.randrange(0, 50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Enemy(gamespeed, 40, 40))

            if len(bat) == 0 and random.randrange(0, 200) == 10 and counter > 500:
                for l in last_obstacle:
                    if l.rect.right < width*0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Bat(gamespeed + 1.5, 46, 40))

            enemy.update()
            bullets.update()
            bat.update()
            all_sprites.update()

            if pygame.display.get_surface() != None:
                screen.fill(black)
                screen.blit(background, background_rect)
                all_sprites.draw(screen)
                bullets.draw(screen)
                bat.draw(screen)
                enemy.draw(screen)
                draw_shield_bar(screen, 5, 5, alien.shield)
                draw_text(screen, str(alien.score), 20, width / 2, 30)
                pygame.display.update()
            clock.tick(FPS)

            if alien.isDead:
                gameOver = True
                if alien.score > high_score:
                    high_score = alien.score

            counter = (counter + 1)

        if gameQuit:
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameplay()
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(retbutton_image, gameover_image)
                pygame.display.update()
            clock.tick(FPS)
    pygame.quit()
    quit()


def main():
    isGameQuit = show_go_screen()
    if not isGameQuit:
        gameplay()


main()