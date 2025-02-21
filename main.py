import pygame
import pyautogui
import classes
import events
import global_vars
import math_functions
from global_vars import screen

clock = pygame.time.Clock()
cursor = classes.Cursor()
player = classes.Player([global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2],global_vars.PLAYER_HP,global_vars.PLAYER_HP,math_functions.hitboxesFromCircle([global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2],global_vars.PLAYER_RADIUS),[classes.CircleImage(0,[global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2],global_vars.PLAYER_RADIUS,global_vars.PLAYER_COLOR,0)],global_vars.PLAYER_SPEED)
eventHandler = events.EventHandler()
entityHandler = classes.EntityHandler()
pygame.mouse.set_visible(False)

entityHandler.add(player)
entityHandler.add(cursor)

background = pygame.Surface(screen.get_size())
background.fill((0, 0, 20))

prev_cursor_pos = None
flicker_start = None

while True:

    pygame.event.pump()
    entityHandler.update()
    screen.blit(background, (0, 0))
    entityHandler.render()
    pygame.display.flip()
    clock.tick(30)

    cursor_pos = pygame.mouse.get_pos()

    # Detect if cursor stops updating
    if cursor_pos == prev_cursor_pos:
        if flicker_start is None:
            flicker_start = pygame.time.get_ticks()  # Log start time of flickering
    else:
        if flicker_start is not None:
            print(f"Flickering lasted {pygame.time.get_ticks() - flicker_start} ms")
            flicker_start = None  # Reset flicker timer

    prev_cursor_pos = cursor_pos



