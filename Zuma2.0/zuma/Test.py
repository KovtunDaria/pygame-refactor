import pygame

pygame.init()

pygame.display.set_caption("Test")

height = 800
width = 800
size = [width, height]
screen = pygame.display.set_mode(size)
run = True
chick = pygame.image.load('pictures/chick.png')
duck = pygame.image.load('pictures/duck.png')
parrot = pygame.image.load('pictures/parrot.png')

# Всё, что потом надо вставить в код игры
pygame.font.init()


def well_done_draw(score):
    font_acme_l = pygame.font.Font('Acme-Regular.ttf', 80)
    font_acme_m = pygame.font.Font('Acme-Regular.ttf', 50)
    player_score_st = 'You have %d points!' % score
    player_score_st_empty = 'You have %d point!' % score

    text_surface_well = font_acme_l.render('Well done!', True, (25, 25, 112))
    text_surface_point = font_acme_m.render(player_score_st, True, (25, 25, 112))
    text_surface_point_empty = font_acme_m.render(player_score_st_empty, True, (25, 25, 112))

    # эти две строчки не надо
    well_size = pygame.font.Font.size(font_acme_l, 'Well done!')  # 336, 102
    point_size = pygame.font.Font.size(font_acme_m, 'You have %s points!' % (score))  # 439, 64

    screen.fill((255, 255, 255))
    screen.blit(text_surface_well, (232, 200))
    screen.blit(chick, (202, 650))
    screen.blit(parrot, (370, 650))
    screen.blit(duck, (558, 650))
    if (score == 0) or (score == -1) or (score == 1):
        screen.blit(text_surface_point_empty, (229, 400))
    else:
        screen.blit(text_surface_point, (190, 400))


def draw(score):
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

        well_done_draw(score)
        pygame.display.flip()
