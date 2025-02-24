import math

import pygame

def hitboxesFromCircle(center,radius):
    return [pygame.Rect(center[0]-radius,center[1]+radius,radius*2,radius/2),pygame.Rect(center[0]-radius/2,center[1]+radius,radius,radius*2)]

def vectAdd(vect1,vect2):
    return [vect1[0]+vect2[0],vect1[1]+vect2[1]]

def rotate(point, angle, center):
    angle = math.radians(angle)
    return [center[0] + (point[0] - center[0]) * math.cos(angle) - (point[1] - center[1]) * math.sin(angle), center[1] + (point[0] - center[0]) * math.sin(angle) + (point[1] - center[1]) * math.cos(angle)]