import pygame

pygame.display.init()
DIMENSIONS = pygame.display.get_desktop_sizes()[0]

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(DIMENSIONS,pygame.DOUBLEBUF)
pygame.display.set_caption("Game")

PLAYER_HP = 3
PLAYER_RADIUS = 40
PLAYER_INSIDE_COLOR = [30,250,250]
PLAYER_OUTSIDE_COLOR = [15,170,170]
PLAYER_SPEED = 300
CURSOR_SIZE = 15
CURSOR_DISTANCE = 5
CURSOR_WIDTH = 5

RENDER_HITBOXES = True

