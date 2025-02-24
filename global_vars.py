import pygame

pygame.display.init()
DIMENSIONS = pygame.display.get_desktop_sizes()[0]

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(DIMENSIONS,pygame.DOUBLEBUF)
pygame.display.set_caption("Game")

PLAYER_HP = 3
PLAYER_RADIUS = 30
PLAYER_COLOR = [255,50,0]
PLAYER_SPEED = 400
CURSOR_SIZE = 15
CURSOR_DISTANCE = 5
CURSOR_WIDTH = 5