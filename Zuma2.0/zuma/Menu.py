import pygame

pygame.init()

pygame.display.set_caption("Menu")

height = 800
width = 800
size = [width, height]
screen = pygame.display.set_mode(size)
chick = pygame.image.load('pictures/chick.png')
duck = pygame.image.load('pictures/duck.png')
parrot = pygame.image.load('pictures/parrot.png')
bg = pygame.image.load('pictures/fon.jpg')
flag = True
pygame.font.init()


def drow_menu():
    font_acme_l = pygame.font.Font('Acme-Regular.ttf', 80)
    font_acme_m = pygame.font.Font('Acme-Regular.ttf', 50)

    text_surface_welcome = font_acme_l.render('Welcome!', True, (25, 25, 112))
    text_surface_play = font_acme_m.render('Play', True, (25, 25, 112))
    text_surface_about = font_acme_m.render('About authors', True, (25, 25, 112))
    text_surface_exit = font_acme_m.render('Exit', True, (25, 25, 112))

    wellSize = pygame.font.Font.size(font_acme_l, 'Well done!')  # 336, 102
    pointSize = pygame.font.Font.size(font_acme_m, 'You have 1000 points!')  # 439, 64
    welcomeSize = pygame.font.Font.size(font_acme_l, 'Welcome!')  # 318, 102
    playSize = pygame.font.Font.size(font_acme_m, 'Play')  # 85, 64
    aboutSize = pygame.font.Font.size(font_acme_m, 'About authors')  # 286, 64
    exitSize = pygame.font.Font.size(font_acme_m, 'Exit')  # 79, 64

    screen.blit(bg, (0, 0))
    screen.blit(text_surface_welcome, (241, 150))
    screen.blit(text_surface_play, (357, 300))
    screen.blit(text_surface_about, (257, 400))
    screen.blit(text_surface_exit, (360, 500))
    screen.blit(chick, (202, 650))
    screen.blit(parrot, (370, 650))
    screen.blit(duck, (538, 650))


check = 0


def draw():
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                global check
                check = 1
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                check = 2
                running = False

        drow_menu()

        pygame.display.flip()
