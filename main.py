import pygame
import classes
import global_vars
import math_functions
from global_vars import screen
from pathlib import Path



playerPos = [global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2]
playerBox = classes.CircleHitboxes([global_vars.DIMENSIONS[0]/2,global_vars.DIMENSIONS[1]/2],global_vars.PLAYER_RADIUS)
playerPics = [
    classes.CircleGradient(global_vars.PLAYER_RADIUS, global_vars.PLAYER_INSIDE_COLOR, global_vars.PLAYER_OUTSIDE_COLOR,[global_vars.DIMENSIONS[0] / 2, global_vars.DIMENSIONS[1] / 2]),
    classes.CircleImage([global_vars.DIMENSIONS[0] / 2, global_vars.DIMENSIONS[1] / 2], global_vars.PLAYER_RADIUS,global_vars.PLAYER_OUTSIDE_COLOR, 7)
              ]


bulletPic = [classes.CircleImage([0,0],15,[255,255,255],0)]
playerGun = classes.Gun(.6,bulletPic,60,10)


cursor = classes.Cursor()
player = classes.Player(playerPos,global_vars.PLAYER_HP,global_vars.PLAYER_HP,playerBox,playerPics,global_vars.PLAYER_SPEED,playerGun)


enemyPic = classes.DisplayImage([['normal',[classes.CircleImage([300,300],30,[150,0,0],0)]],
                                 ['hit',[classes.CircleImage([300,300],30,[255,0,0],0)]]], 'normal')



boxes = classes.CircleHitboxes([300,300],30)
enemy = classes.Enemy([300,300],boxes,enemyPic,200,150,3,[])

#heart = classes.Hearts()

pygame.mouse.set_visible(False)

classes.entityManager.add(player)
classes.entityManager.add(cursor)
classes.entityManager.add(enemy)
#classes.entityManager.add(heart)



background = pygame.Surface(screen.get_size())
background.fill((0, 0, 20))
clock = pygame.time.Clock()
pygame.mixer.init()
#music = pygame.mixer.Sound(r"C:\Users\IanSt\Downloads\Pygame Sprites\335571__magntron__gamemusic.mp3")
#music.play(-1)

while True:
    dt = clock.tick(60)
    fps = clock.get_fps() if clock.get_fps() != 0 else 30
    pygame.event.pump()
    classes.entityManager.update(fps)
    screen.blit(background, (0, 0))
    classes.entityManager.render()
    pygame.display.flip()