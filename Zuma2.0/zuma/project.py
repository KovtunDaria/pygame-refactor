import math
import pygame
import random

from zuma import About, Menu, Test

# Изменения:    почищен код
#               изменены названия с транслита на английский
#               названия по канонам питона
#               у классов убраны скобки
#               %s -> %d
#               удалены неиспользуемые переменные
#               убран хардкод (цвета, размеры окон, середина окна)
#               ball теперь родительский класс

pygame.init()

tests = True


def go_play():
    Menu.draw()
    while tests:
        if Menu.check == 1:
            start_game()
            Test.draw(scores)
        if Menu.check == 2:
            About.run = True
            About.drow()
        if About.flag:
            Menu.running = True
            Menu.draw()


def start_game():
    width = height = 800
    size = [width, height]
    screen = pygame.display.set_mode(size)
    background = pygame.image.load("pictures/fon.jpg")
    clock = pygame.time.Clock()
    speed = 5
    middle = width / 2
    CONST_100 = 100  # TODO: непонятно
    CONST_170 = 170
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    count_of_balls = 0
    moving_balls = []
    running = True
    # global scores
    # scores = 0
    count_for_music = 0
    chick = pygame.image.load('pictures/chick.png')
    duck = pygame.image.load('pictures/duck.png')
    parrot = pygame.image.load('pictures/parrot.png')

    class Barrel:
        def __init__(self):
            self.start_x = height / 2
            self.start_y = width / 2
            self.wid = 5
            self.speed = 4
            self.length = 700
            self.angle = 0
            self.end_x = math.cos(math.radians(self.angle)) * self.length + middle
            self.end_y = math.sin(math.radians(self.angle)) * self.length + middle

    class Ball:
        radius = 30

        def __init__(self):
            check = random.randint(0, 2)
            if check == 0:
                self.color = RED
            if check == 1:
                self.color = GREEN
            if check == 2:
                self.color = YELLOW

    # класс движухщихся шариков
    class MovingBall(Ball):
        def __init__(self):
            super().__init__()
            self.rect = chick.get_rect()
            self.x = width - self.radius - 5
            self.y = self.radius + 5

    # это класс шариков выстрелов
    class PlayerBall(Ball):
        def __init__(self):
            super().__init__()
            self.x = middle
            self.y = middle
            self.angle = 0
            self.speed = 30
            self.check = False

    # функция по движению и рисованию шариков, которые движутся по периметру
    def draw_moving_balls():
        running = True
        for moving_ball in moving_balls:
            if moving_ball.x > moving_ball.radius + speed + 5 and moving_ball.y == moving_ball.radius + 5:
                moving_ball.x -= speed
            elif moving_ball.y < width - moving_ball.radius - 5 and moving_ball.x == moving_ball.radius + speed + 5:
                moving_ball.y += speed
            elif moving_ball.x < height - moving_ball.radius - 5 and moving_ball.y == width - moving_ball.radius - 5:
                moving_ball.x += speed
            elif moving_ball.y > CONST_100 and moving_ball.x == height - moving_ball.radius - 5:
                moving_ball.y -= speed
            elif moving_ball.x > CONST_100 and moving_ball.y == CONST_100:
                moving_ball.x -= speed
            elif moving_ball.y < width - CONST_100 and moving_ball.x == CONST_100:
                moving_ball.y += speed
            elif moving_ball.x < height - CONST_100 and moving_ball.y == width - CONST_100:
                moving_ball.x += speed
            elif moving_ball.y > CONST_170 and moving_ball.x == height - CONST_100:
                moving_ball.y -= speed
            elif moving_ball.x > CONST_170 and moving_ball.y == CONST_170:
                moving_ball.x -= speed
            elif moving_ball.y < width - CONST_170 and moving_ball.x == CONST_170:
                moving_ball.y += speed
            elif moving_ball.x < height - CONST_170 and moving_ball.y == width - CONST_170:
                moving_ball.x += speed
            elif moving_ball.y > middle and moving_ball.x == height - CONST_170:
                moving_ball.y -= speed
            elif moving_ball.x > middle and moving_ball.y == middle:
                moving_ball.x -= speed
            elif moving_ball.x - moving_ball.radius < middle + moving_ball.radius:
                sound1 = pygame.mixer.Sound('BB.wav')
                sound1.play()
                # Test.well_done_draw(scores)
                running = False
                break  # can delete
            # pygame.draw.circle(screen,ball.color, (ball.x, ball.y), ball.r)
            if moving_ball.color == RED:
                screen.blit(parrot, (normalize(moving_ball.x), normalize(moving_ball.y)))
            elif moving_ball.color == GREEN:
                screen.blit(duck, (normalize(moving_ball.x), normalize(moving_ball.y)))
            else:
                screen.blit(chick, (normalize(moving_ball.x), normalize(moving_ball.y)))
        return running  # can delete

    def play_shoot_sound():
        sound1 = pygame.mixer.Sound('Tik.wav')
        sound1.play()

    def normalize(a):
        """
        why
        :param a:
        :return:
        """
        return a - 30

    pygame.mixer.music.load("game_proc.mp3")
    pygame.mixer.music.play()
    # sound1 = pygame.mixer.Sound('myau.wav')
    next_ball = PlayerBall()
    current_ball = PlayerBall()
    shooting_balls = []
    barrel = Barrel()
    global scores
    scores = 0

    while running:
        for event in pygame.event.get():
            # обработка пробела(выстрел)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # sound1.play()
                count_for_music += 1
                play_shoot_sound()
                current_ball = next_ball
                current_ball.angle = barrel.angle
                next_ball = PlayerBall()
                current_ball.check = True
                shooting_balls.append(current_ball)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                global tests
                tests = False

        screen.blit(background, (0, 0))
        pygame.draw.circle(screen, WHITE, (middle, middle), 30)
        # pygame.draw.circle(screen, next_ball.color, (next_ball.x, next_ball.y), next_ball.r, 5)
        if next_ball.color == RED:
            screen.blit(parrot, (normalize(next_ball.x), normalize(next_ball.y)))
        elif next_ball.color == GREEN:
            screen.blit(duck, (normalize(next_ball.x), normalize(next_ball.y)))
        else:
            screen.blit(chick, (normalize(next_ball.x), normalize(next_ball.y)))
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            barrel.angle += barrel.speed
            if barrel.angle % 360 == 0:
                barrel.angle = 0
            barrel.end_x = math.cos(math.radians(barrel.angle)) * barrel.length + middle
            barrel.end_y = math.sin(math.radians(barrel.angle)) * barrel.length + middle

        if keys[pygame.K_LEFT]:
            barrel.angle -= barrel.speed
            if barrel.angle % 360 == 0:
                barrel.angle = 360
            barrel.end_x = math.cos(math.radians(barrel.angle)) * barrel.length + middle
            barrel.end_y = math.sin(math.radians(barrel.angle)) * barrel.length + middle

        pygame.draw.line(screen, RED, (barrel.start_x, barrel.start_y), (barrel.end_x, barrel.end_y), barrel.wid)

        # пробегаемся по массиву всех выстреленных шариков, чтоб изменить координаты
        for ball in shooting_balls:
            if 0 < ball.x < width and 0 < ball.y < height and ball.check:
                ball.x += math.cos(math.radians(ball.angle)) * ball.speed
                ball.y += math.sin(math.radians(ball.angle)) * ball.speed
                if ball.color == RED:
                    screen.blit(parrot, (normalize(int(ball.x)), normalize(int(ball.y))))
                elif ball.color == GREEN:
                    screen.blit(duck, (normalize(int(ball.x)), normalize(int(ball.y))))
                else:
                    screen.blit(chick, (normalize(int(ball.x)), normalize(int(ball.y))))
            else:
                ball.check = False
                shooting_balls.pop(shooting_balls.index(ball))
            for moving_ball in moving_balls:
                if abs(ball.x - moving_ball.x) < 30 and abs(ball.y - moving_ball.y) < 30:
                    k = 1
                    if ball.color == moving_ball.color:
                        k += 1
                        index1 = moving_balls.index(moving_ball) - 1
                        index2 = index1 + 1
                        while moving_balls[index1].color == ball.color and len(moving_balls) - 1 > 0:
                            k += 1
                            moving_balls.pop(index1)
                            index1 -= 1
                            index2 -= 1
                        while moving_balls[index2].color == ball.color and len(moving_balls) > index2 + 1:
                            k += 1
                            moving_balls.pop(index2)

                        scores += 2 ** k
                    elif ball.color != moving_ball.color:
                        scores -= 5
                    shooting_balls.pop(shooting_balls.index(ball))

        if count_of_balls % 13 == 0:
            moving_balls.append(MovingBall())
        count_of_balls += 1

        if not draw_moving_balls():
            running = False

        pygame.display.flip()
        clock.tick(30)


go_play()
pygame.quit()
