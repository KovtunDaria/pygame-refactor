# <editor-fold desc="Основа">
import pygame
import time
import random

from pygame.locals import *

# Изменения: убран неиспользуемый импорт
#            всё переназвано в соответствии с пепом
#            wolfIsTop/Bottom,Left/Right -> wolf_position = (0, 1, 2, 3)

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
size = [600, 400]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Eggs Game")
# </editor-fold>

# <editor-fold desc="Переменные">
running = True
xCoord = [75.0, 515.0]
yCoord = [95.0, 150.0]
fromUpper = False
x = 0.0
y = 0.0
wolf_position = 0   # зигзагом: верх-лево, верх-право, низ-лево, низ-право
instructions = True
isFirstTime = True
menuFirstTime = True
currentScore = 0
currentLifes = 3
white = (255, 255, 255)
black = (0, 0, 0)
eggColor = (255, 255, 204)
brown = (210, 105, 30)
eggs = pygame.sprite.Group()
timer = time.clock()
fontBig = pygame.font.SysFont('Neighbor [RUS by Daymarius]', 35)
fontSmall = pygame.font.SysFont('Neighbor [RUS by Daymarius]', 20)
fontSuperSmall = pygame.font.SysFont('Neighbor [RUS by Daymarius]', 15)
fontMedium = pygame.font.SysFont('Neighbor [RUS by Daymarius]', 25)
inBag = False
toastyTime = False
toastyClockStart = 200

# картинки
chicken1 = pygame.transform.scale(pygame.image.load('images/chicken1.png').convert_alpha(), (69, 71))
chicken2 = pygame.transform.scale(pygame.image.load('images/chicken2.png').convert_alpha(), (69, 71))
left_top_wolf = pygame.transform.scale(pygame.image.load('images/left_top_wolf.png').convert_alpha(), (133, 204))
right_top_wolf = pygame.transform.scale(pygame.image.load('images/right_top_wolf.png').convert_alpha(), (133, 204))
left_bottom_wolf = pygame.transform.scale(pygame.image.load('images/left_bottom_wolf.png').convert_alpha(), (133, 204))
right_bottom_wolf = pygame.transform.scale(pygame.image.load('images/right_bottom_wolf.png').convert_alpha(),
                                           (133, 204))
grass = pygame.transform.scale(pygame.image.load('images/grass.png').convert_alpha(), (600, 130))
wood1 = pygame.image.load('images/wood1.png')
wood2 = pygame.image.load('images/wood2.png')
wood3 = pygame.transform.rotate(pygame.image.load('images/wood3.png'), 80)
wood3_2 = pygame.transform.rotate(pygame.image.load('images/wood3_2.png'), 280)
sky = pygame.image.load('images/sky.png')

# звуковые эффекты
beep = pygame.mixer.Sound('sounds/beep.ogg')
game_over = pygame.mixer.Sound('sounds/game_over.wav')
egg_cracking = pygame.mixer.Sound('sounds/egg_cracking.wav')
egg_caught = pygame.mixer.Sound('sounds/egg_caught.ogg')
toasty = pygame.mixer.Sound('sounds/toasty.wav')
beep.set_volume(0.4)
game_over.set_volume(1.0)
egg_cracking.set_volume(0.2)
egg_caught.set_volume(0.2)
toasty.set_volume(1.0)


# </editor-fold>

# <editor-fold desc="Функции">
def add_eggs(eggs):
    egg = Egg(eggColor, 30, 40)
    egg.rect.x = random.choice(xCoord)
    egg.rect.y = random.choice(yCoord)
    egg.xc = egg.rect.x
    egg.yc = egg.rect.y
    eggs.add(egg)


def draw_wolf_where_needed():
    if wolf_position == 0:
        screen.blit(left_top_wolf, (222, 130))
    elif wolf_position == 1:
        screen.blit(right_top_wolf, (245, 130))
    elif wolf_position == 2:
        screen.blit(left_bottom_wolf, (222, 130))
    elif wolf_position == 3:
        screen.blit(right_bottom_wolf, (245, 130))


def draw_background_in_game():
    screen.blit(sky, (0, 0))
    screen.blit(grass, (0, 270))
    screen.blit(wood1, (0, 75))
    screen.blit(wood1, (525, 75))
    screen.blit(wood2, (0, 120))
    screen.blit(wood2, (0, 180))
    screen.blit(wood2, (525, 120))
    screen.blit(wood2, (525, 180))
    screen.blit(wood3, (67, 120))
    screen.blit(wood3, (67, 180))
    screen.blit(wood3_2, (385, 120))
    screen.blit(wood3_2, (385, 180))
    fontBerlin30 = pygame.font.SysFont('Berlin Sans FB', 30)
    score = fontMedium.render('Score: ' + str(currentScore), True, white)
    lifes = fontMedium.render('Lifes: ' + str(currentLifes), True, white)
    screen.blit(chicken1, (5, 70))  # верхняя левая курица
    screen.blit(chicken1, (5, 130))  # нижняя левая курица
    screen.blit(chicken2, (525, 70))  # верхняя правая курица
    screen.blit(chicken2, (525, 130))  # нижняя правая курица
    screen.blit(score, [445, 10])  # Score
    screen.blit(lifes, [445, 40])  # Lifes
    screen.blit(grass, (0, 270))


def draw_lines(color1, color2, color3):
    pygame.draw.line(screen, color1, (140, 208), (190, 208), 3)  # играть
    pygame.draw.line(screen, color1, (411, 208), (461, 208), 3)  # играть
    pygame.draw.line(screen, color2, (140, 258), (190, 258), 3)  # об игре
    pygame.draw.line(screen, color2, (411, 258), (461, 258), 3)  # об игре
    pygame.draw.line(screen, color3, (140, 308), (190, 308), 3)  # рекорды
    pygame.draw.line(screen, color3, (411, 308), (461, 308), 3)  # рекорды


def make_start_menu():
    global running, menuFirstTime
    if menuFirstTime:
        pygame.mixer.music.load('songs/metal.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1, 0.0)
        menuFirstTime = False
    on_play_button = True
    on_about_button = False
    on_records_button = False
    screen.fill(black)
    pygame.draw.rect(screen, (240, 230, 140), ((100, 40), (400, 15)))
    pygame.draw.rect(screen, (240, 230, 140), ((100, 40), (15, 100)))
    pygame.draw.rect(screen, (240, 230, 140), ((100, 125), (400, 15)))
    pygame.draw.rect(screen, (240, 230, 140), ((485, 40), (15, 100)))
    pygame.draw.line(screen, white, (140, 208), (190, 208), 3)  # играть
    pygame.draw.line(screen, white, (411, 208), (461, 208), 3)  # играть
    pygame.draw.line(screen, white, (10, 10), (590, 10), 3)
    pygame.draw.line(screen, white, (10, 10), (10, 390), 3)
    pygame.draw.line(screen, white, (10, 390), (590, 390), 3)
    pygame.draw.line(screen, white, (590, 10), (590, 390), 3)
    screen.blit(fontBig.render('волк ловит яйца', True, brown), (124, 75))
    screen.blit(fontSmall.render('играть', True, brown), (258, 200))
    screen.blit(fontSmall.render('правила', True, brown), (250, 250))
    screen.blit(fontSmall.render('рекорды', True, brown), (248, 300))
    screen.blit(fontSuperSmall.render('2018', True, brown), (282, 370))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # <editor-fold desc="Обработка нажатия клавиш">
        pressed_list = pygame.key.get_pressed()
        if pressed_list[pygame.K_UP]:
            if on_about_button:
                beep.play()
                if flag_up:
                    draw_lines(white, black, black)
                    on_play_button = True
                    on_about_button = False
                    on_records_button = False
                    pygame.display.flip()
                flag_up = False
            if on_records_button:
                beep.play()
                if flag_up:
                    draw_lines(black, white, black)
                    on_play_button = False
                    on_about_button = True
                    on_records_button = False
                    pygame.display.flip()
                flag_up = False
        else:
            flag_up = True

        if pressed_list[pygame.K_DOWN]:
            if on_play_button:
                beep.play()
                if flag_down:
                    draw_lines(black, white, black)
                    on_play_button = False
                    on_about_button = True
                    on_records_button = False
                    pygame.display.flip()
                flag_down = False
            if on_about_button:
                beep.play()
                if flag_down:
                    draw_lines(black, black, white)
                    on_play_button = False
                    on_about_button = False
                    on_records_button = True
                    pygame.display.flip()
                flag_down = False
        else:
            flag_down = True

        if pressed_list[pygame.K_SPACE] or pressed_list[pygame.K_RETURN]:
            if flag_space_return:
                if on_play_button:
                    beep.play()
                    pygame.mixer.music.load('songs/ofuzake.mp3')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1, 0.0)
                    time.sleep(0.3)
                    return
                if on_about_button:
                    beep.play()
                    screen.fill(black)
                    make_about_menu()
                    break
                if on_records_button:
                    beep.play()
                    screen.fill(black)
                    make_records_menu()
                    break
            flag_space_return = False
        else:
            flag_space_return = True
        # </editor-fold>


def make_about_menu():
    global running, isFirstTime
    pygame.draw.line(screen, white, (10, 10), (590, 10), 3)
    pygame.draw.line(screen, white, (10, 10), (10, 390), 3)
    pygame.draw.line(screen, white, (10, 390), (590, 390), 3)
    pygame.draw.line(screen, white, (590, 10), (590, 390), 3)
    screen.blit(fontBig.render('правила', True, brown), (215, 75))
    file = open("instructions.txt")
    z = 120
    lines = file.read().split(r'\n')
    for line in lines:
        z += 18
        screen.blit(fontSuperSmall.render(line, True, white), (30, z))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isFirstTime = False
                running = False
                return False

        pressed_list = pygame.key.get_pressed()

        if pressed_list[pygame.K_ESCAPE]:
            if flag_escape:
                beep.play()
                screen.fill(black)
                make_start_menu()
                break
            flag_escape = False
        else:
            flag_escape = True


def make_records_menu():
    global running, isFirstTime
    pygame.draw.line(screen, white, (10, 10), (590, 10), 3)
    pygame.draw.line(screen, white, (10, 10), (10, 390), 3)
    pygame.draw.line(screen, white, (10, 390), (590, 390), 3)
    pygame.draw.line(screen, white, (590, 10), (590, 390), 3)
    screen.blit(fontBig.render('Рекорды', True, brown), (215, 75))
    file = open("records.txt")
    z = 120
    counter = 1
    point_start_x = 230
    lines = file.readlines()
    for line in lines:
        z += 22
        if counter == 10:
            screen.blit(fontSmall.render(str(counter), True, white), (194, z))
        else:
            screen.blit(fontSmall.render(str(counter), True, white), (200, z))
        counter += 1
        for i in range(16):
            screen.blit(fontSmall.render('.', True, white), (point_start_x, z))
            point_start_x += 10
        point_start_x = 225
        screen.blit(fontSmall.render(line, True, white), (390, z))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isFirstTime = False
                running = False
                return False

        pressed_list = pygame.key.get_pressed()

        if pressed_list[pygame.K_ESCAPE]:
            if flag_escape:
                beep.play()
                screen.fill(black)
                make_start_menu()
                break
            flag_escape = False
        else:
            flag_escape = True


def make_game_over_menu():
    global running, records
    if currentScore > records[9]:
        records[9] = currentScore
        records.sort()
        records.reverse()
        file_to_write = open('records.txt', 'w')
        for record in records:
            file_to_write.write(str(record) + '\n')
        file_to_write.close()
    game_over.play()
    on_play_button = True
    on_menu_button = False
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, white, (10, 10), (590, 10), 3)
    pygame.draw.line(screen, white, (10, 10), (10, 390), 3)
    pygame.draw.line(screen, white, (10, 390), (590, 390), 3)
    pygame.draw.line(screen, white, (590, 10), (590, 390), 3)
    screen.blit(fontBig.render('Конец игры', True, brown), (178, 75))
    screen.blit(fontMedium.render('Score: ' + str(currentScore), True, white), (238, 140))
    pygame.draw.line(screen, white, (140, 208), (190, 208), 3)  # играть
    pygame.draw.line(screen, white, (411, 208), (461, 208), 3)  # играть
    screen.blit(fontSmall.render('заново', True, brown), (256, 200))
    screen.blit(fontSmall.render('главное меню', True, brown), (214, 250))
    pygame.display.flip()
    eggs.empty()
    timer = time.clock() + 15
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # <editor-fold desc="Обработка нажатия клавиш">
        pressed_list = pygame.key.get_pressed()
        if pressed_list[pygame.K_UP] and on_menu_button:
            beep.play()
            if flag_up:
                draw_lines(white, black, black)
                on_play_button = True
                on_menu_button = False
                pygame.display.flip()
            flag_up = False
        else:
            flag_up = True
        if pressed_list[pygame.K_DOWN] and on_play_button:
            beep.play()
            if flag_down:
                draw_lines(black, white, black)
                on_play_button = False
                on_menu_button = True
                pygame.display.flip()
            flag_down = False
        else:
            flag_down = True
        if pressed_list[pygame.K_SPACE] or pressed_list[pygame.K_RETURN]:
            if flag_space_return:
                if on_play_button:
                    running = True
                    pygame.mixer.music.play(-1, 0.0)
                    time.sleep(0.3)
                    return
                if on_menu_button:
                    pygame.mixer.music.load('songs/metal.mp3')
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1, 0.0)
                    time.sleep(0.15)  # опять же единственный выход, который я вижу, чтобы не было коллизий с кнопками
                    make_start_menu()
                    break
            flag_space_return = False
        else:
            flag_space_return = True
        if pressed_list[pygame.K_ESCAPE]:
            if flag_esc:
                running = False
                return
            flag_esc = False
        else:
            flag_esc = True
        # </editor-fold>


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
        screen.fill(black)
        screen.blit(fontSmall.render('пауза', True, brown), (262, 150))
        screen.blit(fontSmall.render('для продолжения нажмите клавишу ПРОБЕЛ', True, white), (26, 230))
        pygame.display.update()
    timer = time.clock()


def key_handler(pressed_list):
    global wolf_position
    if pressed_list[K_DOWN] and wolf_position == 1:
        wolf_position = 3
    if pressed_list[K_DOWN] and wolf_position == 0:
        wolf_position = 2
    if pressed_list[K_UP] and wolf_position == 3:
        wolf_position = 1
    if pressed_list[K_UP] and wolf_position == 2:
        wolf_position = 0
    if pressed_list[K_RIGHT]:
        if wolf_position == 0:
            wolf_position = 1
        elif wolf_position == 2:
            wolf_position = 3
        elif not (0 <= wolf_position <= 3):
            wolf_position = 1
    if pressed_list[K_LEFT]:
        if wolf_position == 1:
            wolf_position = 0
        elif wolf_position == 3:
            wolf_position = 2
        elif not (0 <= wolf_position <= 3):
            wolf_position = 0
    if pressed_list[K_p]:
        pause()


# </editor-fold>

# <editor-fold desc="Классы">
class Egg(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.xc = 0.0
        self.yc = 0.0
        self.move_time = 0.005

    def become_caught(self):
        global currentScore, fromUpper, toastyTime, toastyClockStart, rabbit
        egg_caught.play()
        currentScore += 1
        if currentScore % 13 == 0 and currentScore > 0:
            toasty.play()
            toastyClockStart = 200
            rabbit.reset_pos()
            toastyTime = True
        s = "I'm in!"
        fromUpper = False
        instructions = pygame.font.SysFont("Times New Roman", 15)
        if self.rect.x < 210:
            self.xc += 140
        else:
            self.xc -= 160
        screen.blit(instructions.render(s, True, (0, 255, 0)), (self.xc, self.yc + 21))
        pygame.display.update()
        if currentScore % 3 == 0 and self.move_time > 0:
            self.move_time -= 0.001
        if self.move_time < 0.002:
            self.move_time = 0
        time.sleep(self.move_time)
        self.rect.x = random.choice(xCoord)
        self.rect.y = random.choice(yCoord)
        self.xc = self.rect.x
        self.yc = self.rect.y
        fromUpper = False

    def update(self):
        global currentLifes, currentScore, fromUpper
        shelf_finished = False
        if self.rect.x < 200 or self.rect.x > 380:
            if self.rect.x < 210:
                self.rect.x += 1
                x_fin = self.xc + 125
            else:
                self.rect.x -= 1
                x_fin = self.xc - 125
            y_fin = self.yc + 21
            a = (y_fin - self.yc) / (x_fin - self.xc)
            b = self.yc - a * self.xc
            self.rect.y = a * self.rect.x + b

        else:
            shelf_finished = True
            if 220 > self.rect.x >= 190 and self.rect.y < 150:
                if wolf_position == 0:
                    self.become_caught()
                else:
                    fromUpper = True

            elif 375 <= self.rect.x <= 400 and self.rect.y < 150:
                if wolf_position == 1:
                    self.become_caught()
                else:
                    fromUpper = True

            elif 220 > self.rect.x >= 190 and wolf_position == 2 and 215 > self.rect.y >= 190 and not fromUpper:
                self.become_caught()

            elif 375 <= self.rect.x <= 400 and wolf_position == 3 and 215 > self.rect.y >= 190 and not fromUpper:
                self.become_caught()

        if shelf_finished:
            if self.rect.y < 300 and shelf_finished:
                self.rect.y += 10
            if self.rect.y >= 300:
                egg_cracking.play()
                s = "Crack!"
                fromUpper = False
                instructions = pygame.font.SysFont("Times New Roman", 18)
                currentLifes -= 1
                screen.blit(instructions.render(s, True, eggColor), (self.rect.x, self.rect.y))
                pygame.display.update()
                self.rect.x = self.xc = random.choice(xCoord)
                self.rect.y = self.yc = random.choice(yCoord)
        time.sleep(self.move_time)


class Rabbit(pygame.sprite.Sprite):

    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('images/toasty.png').convert_alpha(), (180, 119))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.rect.x < 0:
            self.rect.x += 3.5

    def reset_pos(self):
        self.rect.x = -170
        self.rect.y = 280


# </editor-fold>

fileToRead = open('records.txt')
lines = fileToRead.readlines()
records = []
for line in lines:
    if line.strip():
        records.append(int(line))

rabbit = Rabbit()
add_eggs(eggs)
make_start_menu()

# <editor-fold desc="Игровой цикл">
while running and currentLifes > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    draw_background_in_game()
    draw_wolf_where_needed()
    pressedList = pygame.key.get_pressed()
    eggs.update()
    eggs.draw(screen)
    key_handler(pressedList)

    if toastyTime and toastyClockStart > 0:
        rabbit.draw()
        rabbit.update()
        toastyClockStart -= 3

    pygame.display.update()

    if time.clock() - timer > 15 and len(eggs) < 4:
        timer = time.clock()
        add_eggs(eggs)

    if currentLifes == 0:
        pygame.mixer.music.stop()
        make_game_over_menu()
        if running and len(eggs) == 0:
            add_eggs(eggs)
        currentScore = 0
        currentLifes = 3
# </editor-fold>
