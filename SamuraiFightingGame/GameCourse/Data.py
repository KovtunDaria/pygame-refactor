import pygame

# Music/Sounds
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()
sound = pygame.mixer.Sound('sounds/theme.wav')
punch = pygame.mixer.Sound('sounds/punch.wav')

# Sprites
menu = pygame.image.load('sprites/menu.png')
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
attackRightLow = [pygame.image.load(r'sprites\attackright_low-1.png'), pygame.image.load(r'sprites\attackright_low-2.png'),
            pygame.image.load(r'sprites\attackright_low-3.png'),
            pygame.image.load(r'sprites\attackright_low-4.png'), pygame.image.load(r'sprites\attackright_low-5.png'),
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
bg2 = pygame.image.load(r'sprites\bg2.jpg')

game_over = pygame.image.load(r'sprites\gameover.jpg')
