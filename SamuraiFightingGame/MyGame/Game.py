import pygame, sys, time, random, math
from pygame.locals import *

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
animCount3 = 0
animCountLowLeft = 0
animCountLowRight = 0
isAttacking = False
turnToRight = False
turnToLeft = True
clock = pygame.time.Clock()
current_time = 0
k = 5000
koef = 1
playerIdleRight = pygame.image.load('sprites\idle2.png')
playerIdleLeft = pygame.image.load('sprites\idle_left.png')

playerJumpRight = pygame.image.load('sprites\jump2.png')
playerJumpLeft = pygame.image.load('sprites\jump_left.png')

enemyJumpRight = pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningleft-5.png'), (130, 100))
enemyJumpLeft = pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningright-5.png'), (130, 100))

enemyAttackRight = pygame.transform.scale(pygame.image.load(r'sprites\enemies\attackright.png'), (130, 100))
enemyAttackLeft = pygame.transform.scale(pygame.image.load(r'sprites\enemies\attackleft.png'), (130, 100))
enemyIdleRight = pygame.transform.scale(pygame.image.load(r'sprites\enemies\attackright-2.png'), (130, 100))
enemyIdleLeft = pygame.transform.scale(pygame.image.load(r'sprites\enemies\attackleft-2.png'), (130, 100))
enemyDead = pygame.transform.scale(pygame.image.load(r'sprites\enemies\enemy-dead.png'), (130, 100))

runRight = [pygame.image.load(r'sprites\running-1.png'), pygame.image.load(r'sprites\running-2.png'),
            pygame.image.load(r'sprites\running-3.png'),
            pygame.image.load(r'sprites\running-4.png'), pygame.image.load(r'sprites\running-5.png'),
            pygame.image.load(r'sprites\running-6.png')]
runLeft = [pygame.image.load(r'sprites\runningleft-1.png'), pygame.image.load(r'sprites\runningleft-2.png'),
           pygame.image.load(r'sprites\runningleft-3.png'),
           pygame.image.load(r'sprites\runningleft-4.png'), pygame.image.load(r'sprites\runningleft-5.png'),
           pygame.image.load(r'sprites\runningleft-6.png')]
attackRight = [pygame.image.load(r'sprites\attackright-1.png'), pygame.image.load(r'sprites\attackright-2.png'),
               pygame.image.load(r'sprites\attackright-3.png'),
               pygame.image.load(r'sprites\attackright-4.png'), pygame.image.load(r'sprites\attackright-5.png'),
               pygame.image.load(r'sprites\attackright-6.png')]
attackLeft = [pygame.image.load(r'sprites\attackleft-1.png'), pygame.image.load(r'sprites\attackleft-2.png'),
              pygame.image.load(r'sprites\attackleft-3.png'),
              pygame.image.load(r'sprites\attackleft-4.png'), pygame.image.load(r'sprites\attackleft-5.png'),
              pygame.image.load(r'sprites\attackleft-6.png')]
attackRightLow = [pygame.image.load(r'sprites\attackright_low-1.png'),
                  pygame.image.load(r'sprites\attackright_low-2.png'),
                  pygame.image.load(r'sprites\attackright_low-3.png'),
                  pygame.image.load(r'sprites\attackright_low-4.png'),
                  pygame.image.load(r'sprites\attackright_low-5.png'),
                  pygame.image.load(r'sprites\attackright_low-6.png')]
attackLeftLow = [pygame.image.load(r'sprites\attackleft_low-1.png'), pygame.image.load(r'sprites\attackleft_low-2.png'),
                 pygame.image.load(r'sprites\attackleft_low-3.png'),
                 pygame.image.load(r'sprites\attackleft_low-4.png'), pygame.image.load(r'sprites\attackleft_low-5.png'),
                 pygame.image.load(r'sprites\attackleft_low-6.png')]
enemyRightRun = [pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningleft-1.png'), (130, 100)),
                 pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningleft-2.png'), (130, 100)),
                 pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningleft-3.png'), (130, 100)),
                 pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningleft-4.png'), (130, 100)),
                 pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningleft-5.png'), (130, 100)),
                 pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningleft-6.png'), (130, 100)),
                 pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningleft-7.png'), (130, 100)),
                 pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningleft-8.png'), (130, 100))]
enemyLeftRun = [pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningright-1.png'), (130, 100)),
                pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningright-2.png'), (130, 100)),
                pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningright-3.png'), (130, 100)),
                pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningright-4.png'), (130, 100)),
                pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningright-5.png'), (130, 100)),
                pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningright-6.png'), (130, 100)),
                pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningright-7.png'), (130, 100)),
                pygame.transform.scale(pygame.image.load(r'sprites\enemies\runningright-8.png'), (130, 100))]

bg = pygame.image.load(r'sprites\bgg2.jpg')

game_over = pygame.image.load(r'sprites\gameover.jpg')

enemies = []


def draw():
    global animCount, animCount2, animCount3, isAttacking
    if (hp > 0):
        screen.blit(bg, (0, 0))
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
    pygame.display.update()


def attack_to_right():
    global animCount2, animCount3, isAttacking, animCountLowRight, score
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
            # print(math.fabs(enemy.y - y))
            if enemy.x - x < 100:
                if enemy.direction == "left":
                    enemy.hp -= 10
                    current_time = pygame.time.get_ticks()
                    if enemy.is_dead:
                        if current_time - enemy.start_time_death >= 250:
                            enemies.remove(enemy)
                            score += 1


def attack_to_left():
    global animCount3, animCount2, isAttacking, animCountLowLeft, score
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
                current_time = pygame.time.get_ticks()
                if enemy.is_dead:
                    if current_time - enemy.start_time_death >= 250:
                        enemies.remove(enemy)
                        score += 1


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

        # pygame.draw.rect(screen, (0, 0, 0), [self.x, self.y, self.width, self.height])

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
    w = 560
    h = 50
    r = 255
    g = 0
    b = 0
    for i in range(hp):
        if r == 255 and g < 255 and b == 0:
            g += 51
        elif r <= 255 and g == 255 and r > 0:
            r -= 51
        elif g == 255 and b <= 255:
            b += 51
        elif g <= 255 and b == 255 and g > 0:
            g -= 51
        rect_1_rect = Rect((w, h), (15, 30))
        rect_1_color = (r, g, b)

        pygame.draw.rect(screen, rect_1_color, rect_1_rect)

        w += 22


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


while mainLoop:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            mainLoop = False
    pressedList = pygame.key.get_pressed()
    if pressedList[pygame.K_ESCAPE]:
        gameOver = True

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
