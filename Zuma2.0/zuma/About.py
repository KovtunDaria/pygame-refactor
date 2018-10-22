import pygame
from zuma import Menu

pygame.init()

pygame.display.set_caption("About")

height = 800
width = 800
size = [width, height]
screen = pygame.display.set_mode(size)
run = True
chick = pygame.image.load('pictures/chick.png')
duck = pygame.image.load('pictures/duck.png')
parrot = pygame.image.load('pictures/parrot.png')
bg = pygame.image.load('pictures/fon.jpg')
goBack = pygame.image.load('pictures/goBack.png')
flag = False

pygame.font.init()


def drow_about():
    font_acme_l = pygame.font.Font('Acme-Regular.ttf', 80)
    font_acme_m = pygame.font.Font('Acme-Regular.ttf', 50)
    font_acme_s = pygame.font.Font('Acme-Regular.ttf', 30)

    text_surface_hello = font_acme_l.render('Hello!', True, (25, 25, 112))
    text_surface_we = font_acme_m.render('We are Niaz and Dilyara', True, (25, 25, 112))
    text_surface_hope = font_acme_m.render('We hope you enjoy our game', True, (25, 25, 112))
    text_surface_go_back = font_acme_s.render('back', True, (25, 25, 112))

    helloSize = pygame.font.Font.size(font_acme_l, 'Hello!')  # 188, 102
    weSize = pygame.font.Font.size(font_acme_m, 'We are Niaz and Dilyara')  # 473, 64
    hopeSize = pygame.font.Font.size(font_acme_m, 'We hope you enjoy our game')  # 593, 64

    screen.blit(bg, (0, 0))
    screen.blit(goBack, (0, 0))
    screen.blit(text_surface_go_back, (20, 65))
    screen.blit(text_surface_hello, (306, 150))
    screen.blit(text_surface_we, (163, 300))
    screen.blit(text_surface_hope, (120, 400))
    screen.blit(chick, (202, 650))
    screen.blit(parrot, (370, 650))
    screen.blit(duck, (538, 650))


def drow():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                global flag
                flag = True
                run = False

        drow_about()

        pygame.display.flip()
