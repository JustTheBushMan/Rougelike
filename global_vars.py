import pygame

DIMENSIONS = (1920,1080)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(DIMENSIONS,pygame.DOUBLEBUF)
pygame.display.set_caption("Game")

PLAYER_HP = 3
PLAYER_RADIUS = 20
PLAYER_COLOR = [255,50,0]
PLAYER_SPEED = 100
CURSOR_SIZE = 15
CURSOR_DISTANCE = 5
CURSOR_WIDTH = 5