import pygame

dimensions = pygame.display.get_window_size()
pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Game")

PLAYER_HP = 3
PLAYER_RADIUS = 20
PLAYER_COLOR = [255,50,0]