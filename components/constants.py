import os
import pygame


pygame.font.init()
STAT_FONT = pygame.font.SysFont('comicsans', 50)

WIN_WIDTH = 500
WIN_HEIGHT = 800

ENV_VEL = 5

FLOOR_HEIGHT = 730

ROOT_DIR = os.path.dirname(os.path.abspath("main.py"))
print(ROOT_DIR)
IMG_DIR = ROOT_DIR + '/images/'
print(IMG_DIR)

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(IMG_DIR + 'bird1.png')),
    pygame.transform.scale2x(pygame.image.load(IMG_DIR + 'bird2.png')),
    pygame.transform.scale2x(pygame.image.load(IMG_DIR + 'bird3.png'))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(IMG_DIR + 'pipe.png'))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(IMG_DIR + 'base.png'))
BG_IMG = pygame.transform.scale2x(pygame.image.load(IMG_DIR + 'bg.png'))
