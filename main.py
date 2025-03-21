import pygame
import classes
import global_vars
import math_functions
from global_vars import screen
from pathlib import Path



playerPos = [global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2]
playerBox = math_functions.hitboxesFromCircle([global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2],global_vars.PLAYER_RADIUS)
playerPics = [
    classes.CircleGradient(global_vars.PLAYER_RADIUS, global_vars.PLAYER_INSIDE_COLOR, global_vars.PLAYER_OUTSIDE_COLOR,[global_vars.DIMENSIONS[0] / 2, global_vars.DIMENSIONS[1] / 2]),
    classes.CircleImage([global_vars.DIMENSIONS[0] / 2, global_vars.DIMENSIONS[1] / 2], global_vars.PLAYER_RADIUS,global_vars.PLAYER_OUTSIDE_COLOR, 7)
              ]


bulletPic = [classes.CircleImage([0,0],15,[255,255,255],0)]
playerGun = classes.Gun(.6,bulletPic,60,10)


cursor = classes.Cursor()
player = classes.Player(playerPos,global_vars.PLAYER_HP,global_vars.PLAYER_HP,playerBox,playerPics,global_vars.PLAYER_SPEED,playerGun)

enemyPic = classes.DisplayImage([['normal',[classes.CircleImage([100,100],30,[150,0,0],0)]],
                                 ['hit',[classes.CircleImage([100,100],30,[255,0,0],0)]]], 'normal')



boxes = math_functions.hitboxesFromCircle([100,100],30)
enemy = classes.Enemy([100,100],boxes,enemyPic,200,150,3,[])



pygame.mouse.set_visible(False)

classes.entityManager.add(player)
classes.entityManager.add(cursor)
classes.entityManager.add(enemy)



background = pygame.Surface(screen.get_size())
background.fill((0, 0, 20))
clock = pygame.time.Clock()

while True:
    dt = clock.tick(60)
    fps = clock.get_fps() if clock.get_fps() != 0 else 30
    pygame.event.pump()
    classes.entityManager.update(fps)
    classes.entityManager.collideChecks()
    screen.blit(background, (0, 0))
    classes.entityManager.render()
    pygame.draw.rect(global_vars.screen, (255, 0, 0),  classes.entityManager.classes["Player"].elements[0].hitboxes[1],1)
    pygame.display.flip()

