import math
import global_vars

import pygame

def hitboxesFromCircle(center,radius):
    return [pygame.Rect(center[0]-radius,center[1]+radius,radius*2,radius),pygame.Rect(center[0]-radius/2,center[1]+radius,radius,radius*2)]

def vectAdd(vect1,vect2):
    return [vect1[0]+vect2[0],vect1[1]+vect2[1]]


def pythag(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

def rotate(point, angle, center):
    x, y = point[0], point[1]
    cx , cy = center[0],center[1]
    rad = math.radians(-angle)
    x, y = x - cx, y - cy
    x_new = x * math.cos(rad) - y * math.sin(rad)
    y_new = x * math.sin(rad) + y * math.cos(rad)
    return x_new + cx, y_new + cy




def mixColors(colorsAndWeights):
    numColors = len(colorsAndWeights)
    weightTotal = sum(colorsAndWeights[i][1] for i in range(numColors))
    return [sum(colorsAndWeights[i][0][j]*colorsAndWeights[i][1]/weightTotal for i in range(numColors)) for j in range(3)]

def normalizeVect(vect,maxDist):
    dist = pythag(vect,[0,0])
    returnVect = [0,0]
    try:
        returnVect[0] = vect[0]/dist*maxDist
    except:
        returnVect[0] = 0
    try:
        returnVect[1] = vect[1]/dist*maxDist
    except:
        returnVect[1] = 0
    return returnVect

def bound(pos,radius):
    x = max(radius,min(pos[0],global_vars.DIMENSIONS[0]-radius))
    y = max(radius,min(pos[1],global_vars.DIMENSIONS[1]-radius))
    return [x,y]