import pygame
import classes
import events
import global_vars
import math_functions
from global_vars import screen

cursor = classes.Cursor()
player = classes.Player([global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2],global_vars.PLAYER_HP,global_vars.PLAYER_HP,math_functions.hitboxesFromCircle([global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2],global_vars.PLAYER_RADIUS),[classes.CircleImage(0,[global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2],global_vars.PLAYER_RADIUS,global_vars.PLAYER_COLOR,0)],global_vars.PLAYER_SPEED)
eventHandler = events.EventHandler()
entityHandler = classes.EntityHandler()
pygame.mouse.set_visible(False)

entityHandler.add(player)
entityHandler.add(cursor)

background = pygame.Surface(screen.get_size())
background.fill((0, 0, 20))
clock = pygame.time.Clock()

while True:
    dt = clock.tick(60)
    fps = clock.get_fps() if clock.get_fps() != 0 else 30
    pygame.event.pump()
    entityHandler.update(fps)
    screen.blit(background, (0, 0))
    entityHandler.render()
    pygame.display.flip()