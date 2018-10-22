import pygame, sys, random
from pygame.locals import *

from Data import *

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("My First PyGame Windows")
mainLoop = True
x = 375
y = 550
isJump = False
jumpCount = 10
hp = 10
score = 0
flag_left = False
flag_right = False
animCount = 0
animCount2 = 0
background = False
animCount3 = 0
animCountLowLeft = 0
animCountLowRight = 0
isAttacking = False
turnToRight = False
turnToLeft = True
attack_sound = True
clock = pygame.time.Clock()
current_time = 0
k = 5000
koef = 1
gameOver = False

# Sounds/Music
sound.play(-1)
enemies = []


def draw():
    global animCount, animCount2, animCount3, isAttacking
    if hp > 0:
        if not background:
            screen.blit(bg, (0, 0))
        else:
            screen.blit(bg2, (0, 0))
        if animCount + 1 >= 30:
            animCount = 0
        if flag_left:
            if isJump:
                if isAttacking:
                    attack_to_left()
                else:
                    screen.blit(playerJumpLeft, (x, y))
            else:
                screen.blit(runLeft[animCount // 5], (x, y))
                animCount += 1
        elif flag_right:
            if isJump:
                if isAttacking:
                    attack_to_right()
                else:
                    screen.blit(playerJumpRight, (x, y))
            else:
                screen.blit(runRight[animCount // 5], (x, y))
                animCount += 1

        else:
            if isJump:
                if turnToRight:
                    if isAttacking:
                        attack_to_right()

                    else:
                        screen.blit(playerJumpRight, (x, y))
                elif turnToLeft:
                    if isAttacking:
                        attack_to_left()
                    else:
                        screen.blit(playerJumpLeft, (x, y))
            else:
                if turnToRight:
                    if isAttacking:
                        attack_to_right()
                    else:
                        screen.blit(playerIdleRight, (x, y))
                        animCount2 = 0
                        animCount3 = 0
                elif turnToLeft:
                    if isAttacking:
                        attack_to_left()
                    else:
                        screen.blit(playerIdleLeft, (x, y))
                        animCount2 = 0
                        animCount3 = 0
        for enemy in enemies:
            enemy.draw_enemy()

        draw_hp()
        draw_score()
    else:
        screen.blit(game_over, (0, 0))
        draw_score()
        for enemy in enemies:
            enemies.remove(enemy)
    pygame.display.update()


# Attack hero
def attack_to_right():
    global animCount2, animCount3, isAttacking, animCountLowRight, score, attack_sound
    if isJump:
        animCount3 = 0
        if animCount2 + 1 >= 18:
            animCount2 = 0
            isAttacking = False

        screen.blit(attackRight[animCount2 // 3], (x, y))
        animCount2 += 1
    else:
        if animCountLowRight + 1 >= 18:
            animCountLowRight = 0
            isAttacking = False

        screen.blit(attackRightLow[animCountLowRight // 3], (x, y))
        animCountLowRight += 1

        for enemy in enemies:
            if enemy.x - x < 100:
                if enemy.direction == "left":
                    enemy.hp -= 10
                    if attack_sound:
                        punch.play(1)
                        attack_sound = False
                    current_time = pygame.time.get_ticks()
                    if enemy.is_dead:
                        if current_time - enemy.start_time_death >= 250:
                            enemies.remove(enemy)
                            score += 1
                            attack_sound = True


def attack_to_left():
    global animCount3, animCount2, isAttacking, animCountLowLeft, score, attack_sound
    if isJump:
        animCount2 = 0
        if animCount3 + 1 >= 18:
            animCount3 = 0
            isAttacking = False
        screen.blit(attackLeft[animCount3 // 3], (x, y))
        animCount3 += 1
    else:
        if animCountLowLeft + 1 >= 18:
            animCountLowLeft = 0
            isAttacking = False

        screen.blit(attackLeftLow[animCountLowLeft // 3], (x, y))
        animCountLowLeft += 1
    for enemy in enemies:
        if x - enemy.x < 100:
            if enemy.direction == "right":
                enemy.hp -= 10
                if attack_sound:
                    punch.play(1)
                    attack_sound = False
                current_time = pygame.time.get_ticks()
                if enemy.is_dead:
                    if current_time - enemy.start_time_death >= 250:
                        enemies.remove(enemy)
                        score += 1
                        attack_sound = True


# Menu
class Menu:
    def __init__(self, punkts=[120, 140, u'Punkt', (250, 250, 30), (250, 30, 250), 0]):
        self.punkts = punkts

    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        global background
        screen.fill((0, 0, 0))
        done = True
        font_menu = pygame.font.Font(None, 50)
        punkt = 0
        while done:
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                    if punkt == 1:
                        sys.exit()
                    if punkt == 2:
                        font = pygame.font.Font(None, 40)
                        text = font.render(" Last Score: " + str(score), True, (250, 250, 30))
                        screen.blit(text, [50, 40])
                    if punkt == 3:
                        if not background:
                            background = True
                        else:
                            background = False

            menu.blit(screen, [0, 0])
            pygame.display.flip()


punkts = [(350, 210, u'Start', (250, 250, 30), (250, 30, 250), 0),
          (354, 370, u'Quit', (250, 250, 30), (250, 30, 250), 2),
          (344, 290, u'Score', (250, 250, 30), (250, 30, 250), 1),
          (336, 450, u'Switch', (250, 250, 30), (250, 30, 250), 3)]

game = Menu(punkts)
game.menu()


# Enemies
class Enemy(object):
    def __init__(self):
        self.x = 0
        self.y = 605
        self.is_jumping = random.choice([True, False])
        self.is_jumping_now = False
        self.width = 130
        self.height = 100
        self.jumpCount = 10
        self.direction = random.choice(["left", "right"])
        self.animEnemyRightCount = 0
        self.animEnemyLeftCount = 0
        self.hp = 100
        self.start_time = 0
        self.start_time_death = 0
        self.current_time = 0
        self.flag = True
        self.is_dead = False
        self.is_first_attack = True
        if self.direction == "right":
            self.x = -50
        else:
            self.x = 700

    def run(self):
        global x
        if not self.is_jumping:
            if self.collides():
                if self.direction == "right":
                    self.x = x - 50
                else:
                    self.x = x + 50
            else:
                if self.direction == "right":
                    self.x += 7
                else:
                    self.x -= 7
        elif self.is_jumping:
            if self.direction == "right":
                if self.x + self.width >= x - 80:
                    self.jump()
                    if self.jumpCount <= -10:
                        self.is_jumping_now = False
                    else:
                        self.is_jumping_now = True
                else:
                    self.x += 7
            else:
                if self.x - self.width <= x + 50:
                    self.jump()
                    if self.jumpCount <= -10:
                        self.is_jumping_now = False
                    else:
                        self.is_jumping_now = True
                else:
                    self.x -= 7

    def draw_enemy(self):
        if self.direction == "right":
            if self.hp > 0:
                if self.is_jumping_now:
                    screen.blit(enemyJumpRight, (self.x, self.y))
                elif self.collides():
                    if self.flag:
                        self.start_time = pygame.time.get_ticks()
                        self.flag = False
                    self.attack()
                else:
                    if self.animEnemyRightCount + 1 >= 40:
                        self.animEnemyRightCount = 0
                    screen.blit(enemyRightRun[self.animEnemyRightCount // 5], (self.x, self.y))
                    self.animEnemyRightCount += 1
                self.run()
            else:
                screen.blit(enemyDead, (self.x, 630))
                if not self.is_dead:
                    self.start_time_death = pygame.time.get_ticks()
                    self.is_dead = True
        else:
            if self.hp > 0:
                if self.is_jumping_now:
                    screen.blit(enemyJumpLeft, (self.x, self.y))
                elif self.collides():
                    if self.flag:
                        self.start_time = pygame.time.get_ticks()
                        self.flag = False
                    self.attack()
                else:
                    if self.animEnemyLeftCount + 1 >= 40:
                        self.animEnemyLeftCount = 0
                    screen.blit(enemyLeftRun[self.animEnemyLeftCount // 5], (self.x, self.y))
                    self.animEnemyLeftCount += 1
                self.run()
            else:
                screen.blit(enemyDead, (self.x, 630))
                if not self.is_dead:
                    self.start_time_death = pygame.time.get_ticks()
                    self.is_dead = True

    def collides(self):
        global x
        if self.direction == "right":
            if self.x + self.width - 50 >= x:
                return True
            else:
                return False
        else:
            if self.x - self.width + 50 <= x:
                return True
            else:
                return False

    def jump(self):
        if self.jumpCount >= -10:
            if self.jumpCount < 0:
                self.y += (self.jumpCount ** 2) / 3
            else:
                self.y -= (self.jumpCount ** 2) / 3
            self.jumpCount -= 1
            if self.direction == "right":
                self.x += 7
            else:
                self.x -= 7

    def attack(self):
        global hp
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.start_time >= 800:
            if self.direction == "right":
                if self.x > x:
                    screen.blit(enemyAttackLeft, (self.x, self.y))
                else:
                    screen.blit(enemyAttackRight, (self.x, self.y))
            else:
                if self.x < x:
                    screen.blit(enemyAttackRight, (self.x, self.y))
                else:
                    screen.blit(enemyAttackLeft, (self.x, self.y))
            if self.current_time - self.start_time >= 1000:
                self.flag = True
                hp -= 1

                print(hp)
            self.is_first_attack = False
        else:
            if self.direction == "right":
                screen.blit(enemyIdleRight, (self.x, self.y))
            else:
                screen.blit(enemyIdleLeft, (self.x, self.y))


def draw_hp():
    width = 560
    height = 50
    red = 255
    green = 0
    blue = 0
    for i in range(hp):
        if red == 255 and green < 255 and blue == 0:
            green += 51
        elif 0 < red <= 255 and green == 255:
            red -= 51
        elif green == 255 and blue <= 255:
            blue += 51
        elif 0 < green <= 255 and blue == 255:
            green -= 51
        rect_1_rect = Rect((width, height), (15, 30))
        rect_1_color = (red, green, blue)

        pygame.draw.rect(screen, rect_1_color, rect_1_rect)

        width += 22


def draw_score():
    global score
    if not hp == 0:
        font = pygame.font.Font(None, 25)
        text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(text, [20, 770])
    else:
        font = pygame.font.Font(None, 35)
        text = font.render("Score: " + str(score), True, (255, 70, 90))
        screen.blit(text, [350, 600])


# Main
while mainLoop:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            mainLoop = False
    pressedList = pygame.key.get_pressed()
    if pressedList[pygame.K_ESCAPE]:
        gameOver = True
        game.menu()
        hp = 10
        score = 0

    if pressedList[pygame.K_a] and x > 300:
        x -= 5
        flag_left = True
        flag_right = False
        turnToLeft = True
        turnToRight = False
    elif pressedList[pygame.K_d] and x < 450:
        x += 5
        flag_left = False
        flag_right = True
        turnToRight = True
        turnToLeft = False
    else:
        flag_right = False
        flag_left = False
        animCount = 0
        animCount2 = 0
        animCount3 = 0

    if not isJump:
        if pressedList[pygame.K_w]:
            isJump = True
    else:
        if jumpCount >= -10:
            if jumpCount < 0:
                y += (jumpCount ** 2) / 3
            else:
                y -= (jumpCount ** 2) / 3
            jumpCount -= 1
        else:
            isJump = False
            isAttacking = False
            jumpCount = 10

    if pressedList[pygame.K_SPACE]:
        isAttacking = True

    draw()
    if pygame.time.get_ticks() >= k:
        enemies.append(Enemy())
        k += 5000 * koef
    koef -= 0.0001

pygame.quit()
