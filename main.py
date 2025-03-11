import pygame
import classes
import global_vars
import math_functions
from global_vars import screen

playerPos = [global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2]
playerBox = math_functions.hitboxesFromCircle([global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2],global_vars.PLAYER_RADIUS)

playerPics = [
    classes.CircleGradient(global_vars.PLAYER_RADIUS, global_vars.PLAYER_INSIDE_COLOR, global_vars.PLAYER_OUTSIDE_COLOR,[global_vars.DIMENSIONS[0] / 2, global_vars.DIMENSIONS[1] / 2]),
    classes.CircleImage([global_vars.DIMENSIONS[0] / 2, global_vars.DIMENSIONS[1] / 2], global_vars.PLAYER_RADIUS,global_vars.PLAYER_OUTSIDE_COLOR, 7)
              ]

bulletPic = [classes.CircleImage([0,0],15,[255,255,255],0)]
playerGun = classes.Gun(.2,bulletPic,60,10)


cursor = classes.Cursor()
player = classes.Player(playerPos,global_vars.PLAYER_HP,global_vars.PLAYER_HP,playerBox,playerPics,global_vars.PLAYER_SPEED,playerGun)




pygame.mouse.set_visible(False)

classes.entityManager.add(player)
classes.entityManager.add(cursor)

background = pygame.Surface(screen.get_size())
background.fill((0, 0, 20))
clock = pygame.time.Clock()

while True:
    dt = clock.tick(60)
    fps = clock.get_fps() if clock.get_fps() != 0 else 30
    pygame.event.pump()
    classes.entityManager.update(fps)
    screen.blit(background, (0, 0))
    classes.entityManager.render()
    pygame.display.flip()

