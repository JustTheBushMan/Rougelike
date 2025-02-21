import pygame

def hitboxesFromCircle(center,radius):
    return [pygame.Rect(center[0]-radius,center[1]+radius,radius*2,radius/2),pygame.Rect(center[0]-radius/2,center[1]+radius,radius,radius*2)]

def vectAdd(vect1,vect2):
    return [vect1[0]+vect2[0],vect1[1]+vect2[1]]