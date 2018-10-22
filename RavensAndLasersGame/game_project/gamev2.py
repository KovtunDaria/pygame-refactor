import os
import random

import pygame
from pygame.locals import *

# названия классов и констант по пепу, шрифт вынесен в константы
# изменён шрифт, добавлено сглаживание шрифта
# перенесена инициализация игры наверх

pygame.init()
pygame.font.init()

WIDTH = 400
HEIGHT = 680
BACKGROUND_COLOR = (78, 167, 187)
ENEMY_SIZE = (30, 30)
SCORE = 0
PLAYER_SHOT_SIZE = (17, 35)
SCREEN_RECT = Rect(0, 0, WIDTH, HEIGHT)
FONT_40 = pygame.font.SysFont('Ubuntu', 40)
FONT_20 = pygame.font.SysFont('Ubuntu', 20)


game_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(file):
    file = os.path.join(game_dir, 'sprites', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('image loading error')
    return surface.convert()


class Player(pygame.sprite.Sprite):
    speed = 12
    images = []
    gun_offset = 8

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREEN_RECT.midbottom)
        self.collideRect = pygame.rect.Rect((0, 0), (12, 12))
        self.collideRect.midbottom = self.rect.midbottom

    def move(self, horiz_direction, vert_direction):
        self.rect.move_ip(horiz_direction * self.speed, vert_direction * self.speed)
        self.rect = self.rect.clamp(SCREEN_RECT)
        self.collideRect.move_ip(horiz_direction * self.speed, vert_direction * self.speed)
        self.collideRect = self.rect.clamp(SCREEN_RECT)

    def left_gun_pos(self):
        pos = self.rect.centerx - self.gun_offset + PLAYER_SHOT_SIZE[0] / 2
        return pos, self.rect.top

    def right_gun_pos(self):
        pos = self.rect.centerx + self.gun_offset + PLAYER_SHOT_SIZE[0] / 2
        return pos, self.rect.top


class PlayerShot(pygame.sprite.Sprite):
    speed = -15
    images = []
    GUN_RELOAD = 5

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midtop=position)
        self.image = pygame.transform.scale(self.image, PLAYER_SHOT_SIZE)
        self.collideRect = pygame.rect.Rect((0, 0), (32, 32))
        self.collideRect.midbottom = self.rect.midbottom

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    speed = 4
    images = []
    SPAWN_COOLDOWN = 4
    CROW_SOUND_COOLDOWN = 30

    def __init__(self):
        self.x = random.randrange(0, WIDTH, WIDTH // 10)
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(self.x, 0))
        self.image = pygame.transform.scale(self.image, ENEMY_SIZE)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top >= HEIGHT:
            self.kill()


def load_sound(file):
    file = os.path.join(game_dir, 'sounds', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print('Warning, unable to load, %s' % file)


class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = FONT_40
        self.font.set_italic(1)
        self.color = Color('red')
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(0, 0)

    def update(self):
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, True, self.color)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('My_game')
    clock = pygame.time.Clock()

    # sprites
    img = load_image('player.png')
    Player.images = [img]
    img = load_image('player_shot.png')
    PlayerShot.images = [img]
    img = load_image('enemy_new.png')
    Enemy.images = [img]

    # sounds
    crow_sound = load_sound('crow.wav')
    shot_sound = load_sound('shot.wav')
    shot_sound.set_volume(0.1)

    background = pygame.Surface(SCREEN_RECT.size)
    background.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0))

    pygame.display.flip()

    # Создание контейнеров
    all = pygame.sprite.RenderUpdates()
    shots = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Присвоение контейнеров
    Player.containers = all
    PlayerShot.containers = all, shots
    Enemy.containers = all, enemies

    player = Player()
    # Таймеры появлений объектов
    gun_timer = 0
    enemy_spawn_timer = 0
    crow_sound_timer = 0
    game_over = False

    global SCORE

    if pygame.font:
        all.add(Score())

    while player.alive():
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return

        key_state = pygame.key.get_pressed()
        horiz_direction = key_state[K_RIGHT] - key_state[K_LEFT]
        vert_direction = key_state[K_DOWN] - key_state[K_UP]
        player.move(horiz_direction, vert_direction)

        for shot in shots:
            enemies_hit_list = pygame.sprite.spritecollide(shot, enemies, True)
            if len(enemies_hit_list) > 0:
                if crow_sound_timer <= 0:
                    crow_sound.play()
                    crow_sound_timer = Enemy.CROW_SOUND_COOLDOWN
                shot.kill()
                SCORE += len(enemies_hit_list)
        crow_sound_timer -= 1

        d = pygame.sprite.spritecollide(player, enemies, True)
        if len(d) > 0:
            player.kill()
            game_over = True

        if key_state[K_x]:
            if gun_timer != 0:
                gun_timer = gun_timer - 1
            else:
                PlayerShot(player.left_gun_pos())
                PlayerShot(player.right_gun_pos())
                shot_sound.play()
                gun_timer = PlayerShot.GUN_RELOAD

        if enemy_spawn_timer != 0:
            enemy_spawn_timer = enemy_spawn_timer - 1
        else:
            Enemy()
            enemy_spawn_timer = Enemy.SPAWN_COOLDOWN

        all.clear(screen, background)
        all.update()
        pygame.display.update(all.draw(screen))
        clock.tick(60)

    while game_over:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
        pygame.font.init()
        myfont = FONT_40
        myfontbot = FONT_20
        textover = myfont.render('Game over', True, (0, 0, 0))
        textscore = myfont.render('Score: ' + str(SCORE), True, (0, 0, 0))
        instruction = myfontbot.render('Press S to start a new game ', True, (0, 0, 0))

        key_state = pygame.key.get_pressed()
        if key_state[K_s]:
            SCORE = 0
            main()
            return
        screen.blit(background, (0, 0))
        screen.blit(textover, (100, 0))
        screen.blit(textscore, (125, 100))
        screen.blit(instruction, (50, 600))
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__': main()
