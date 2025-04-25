import pygame
import os

pygame.display.init()
DIMENSIONS = pygame.display.get_desktop_sizes()[0]


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(DIMENSIONS,pygame.DOUBLEBUF)
pygame.display.set_caption("Game")
pygame.display.toggle_fullscreen()

PLAYER_HP = 3
PLAYER_RADIUS = 40
PLAYER_INSIDE_COLOR = [30,250,250]
PLAYER_OUTSIDE_COLOR = [15,170,170]
PLAYER_INSIDE_COLOR_HIT = [10,210,220]
PLAYER_OUTSIDE_COLOR_HIT = [0,120,120]
PLAYER_INSIDE_COLOR_HIT_ALT = [0,170,170]
PLAYER_OUTSIDE_COLOR_HIT_ALT = [0,70,70]
PLAYER_SPEED = 500
CURSOR_SIZE = 15
CURSOR_DISTANCE = 5
CURSOR_WIDTH = 5

wave = 0

HACKS = True
RENDER_HITBOXES = False

def scale(image,scaleFactor):
    return pygame.transform.scale(image,(int(image.get_width()*scaleFactor),int(image.get_height()*scaleFactor)))




SPRITE_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\Rougelike Sprites'


HEART = pygame.image.load(SPRITE_BASE_PATH + r'\heart.png')
HEART = scale(HEART,1/6)

DEAD_HEART = pygame.image.load(SPRITE_BASE_PATH + r'\deadheart.png')
DEAD_HEART = scale(DEAD_HEART,1/6)

STAR = pygame.image.load(SPRITE_BASE_PATH + r'\star.png')
STAR = scale(STAR,1/16)



