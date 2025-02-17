import pygame
import math

import events
import global_vars

class Image:
    def __init__(self,imageType,image=0):
        self.type = imageType
        self.image = image
    def render(self):
        print('No Data in Image')

class Picture(Image):
    def __init__(self,image,position):
        super().__init__('image',image)
        self.position = position
    def render(self):
        global_vars.screen.blit(self.image,self.position)

class RectImage(Image):
    def __init__(self,image,rect,color,radius,border=0):
        super().__init__('rect',image)
        self.rect = rect
        self.color = color
        self.radius = radius
        self.border = border
    def render(self):
        pygame.draw.rect(global_vars.screen,self.color,self.rect,self.border,self.radius)

class CircleImage(Image):
    def __init__(self,image,center,radius,color,border=0):
        super().__init__('circle',image)
        self.center = center
        self.radius = radius
        self.border = border
        self.color = color
    def render(self):
        pygame.draw.circle(global_vars.screen,self.color,self.center,self.radius,self.border)

class TriangleImage(Image):
    def __init__(self,coords,color,border=0):
        super().__init__('triangle')
        self.coords = coords
        self.color = color
        self.border = border
    def render(self):
        pygame.draw.polygon(global_vars.screen,self.color,self.coords,self.border)

class Text(Image):
    def __init__(self,text,font,size,position,color):
        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.Font(font,self.size)
        super().__init__('text')
        self.position = position
    def render(self):
        global_vars.screen.blit(self.font.render(self.text,True,self.color),self.position)

def detectCollision(object,handler):
    match object:
        case Projectile:
            for handlerClass in object.collideWith:
                for element in handler.classes[handlerClass]:



class Entity:
    def __init__(self, position, collisionDetection, hitboxes, displayImages,):#DisplayImages need to be like ['circle',actual data]
        self.position = position
        self.detectCollision = collisionDetection
        self.hitboxes = hitboxes
        self.displayImages = displayImages
    def render(self):
        for i in self.displayImages:
            i.render()
    def checkCollisions(self,index,handler):
        if self.detectCollision:
            match type(self):
                case Projectile:
                    for cls in handler.classes:
                        for elmt in cls.elements:
                            for hitbox in self.hitboxes:
                                if hitbox.collidelist(elmt.hitboxes) != -1:
                                    events.eventHandler.addEvent(['collision',index,elmt])
                case Enemy:





class Player(Entity):
    def __init__(self, position, hp, maxhp, hitboxes, displayImages,speed):
        super().__init__(position, True, hitboxes, displayImages)
        self.hp = hp
        self.maxhp = maxhp
        self.speed = speed
    def update(self,fps):
        diff = pygame.mouse.get_pos()
        translation = [diff[i]-self.position[i]%(self.speed/fps) for i in [0,1]]
        self.position = [self.position[i]+translation[i] for i in [0,1]]




class Projectile(Entity):
    def __init__(self, startingMomentum, position, hitboxes, collisionDetection, displayImages,collideWith,impactDeath,speed):
        super().__init__(position, collisionDetection, hitboxes, displayImages)
        self.momentum = startingMomentum
        self.collideWith = collideWith
        self.dieOnImpact = impactDeath
        self.speed = speed
    def update(self,fps):
        self.position = [self.position[x]-self.momentum[x]/fps for x in (0,1)]


class ClassEntityHandler:
    def __init__(self):
        self.elements = ['empty']
        self.availableIndexes = [0]
    def add(self,element,index):
        self.elements[index] = element
        self.availableIndexes.remove(index)
    def remove(self,index):
        self.elements[index] = 'empty'
        self.availableIndexes.append(index)
    def updateClassEntities(self):
        for i in range(len(self.elements)):
            if self.elements[i] == 'empty':
                self.availableIndexes.append(i)
            elif i in self.availableIndexes:
                self.availableIndexes.remove(i)
            if len(self.availableIndexes) == 0:
                self.elements.append('empty')
                self.availableIndexes.append(len(self.elements)-1)
        for element in self.elements:
            if isinstance(element,Entity):
                element.update()
    def renderEntities(self):
        if pygame.display.get_init():
            for element in self.elements:
                if isinstance(element,Entity):
                    element.render()

class EntityHandler:
    def __init__(self):
        self.classes = {}
    def update(self):
        for i in self.classes:
            self.classes[i].updateClassEntities()
    def render(self):
        for i in self.classes:
            self.classes[i].renderEntities()
    def collideChecks(self):
        for i in self.classes:
            self.classes[i].checkCollisions()
    def add(self,entity):
        cls = str(type(entity))
        if type(self.classes[cls]) is None:
            self.classes[cls] = ClassEntityHandler()
        self.classes[cls].add(entity,self.classes[cls].availableIndexes[0])