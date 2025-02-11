import pygame
import math



import global_vars

class Circle:
    def __init__(self,center,radius):
        self.center

def renderGeneric(images,color=(0,0,0),radius=0,border=0):
    for i in images:
        match i[0]:
            case 'image':
                global_vars.screen.blit(i[1])
            case 'rect':
                pygame.draw.rect(global_vars.screen,color,i[1],border,radius)
            case 'circle':
                pygame.draw.circle(global_vars.screen,color,i[1],radius,border)


class Entity:
    def __init__(self, position, collisionDetection, hitboxes, displayImages):#DisplayImages need to be like ['circle',actual data]
        self.position = position
        self.detectCollision = collisionDetection
        self.hitboxes = hitboxes
        self.displayImages = displayImages
    def render(self):
        renderGeneric(self.displayImages)
    def checkCollisions(self,objects):
        for i in self.hitboxes:
            if i.Rect.collidelist(objects):
                return True
        return False

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
    def __init__(self, startingMomentum, position, hitboxes, collisionDetection, displayImages,friendly,impactDeath,speed):
        super().__init__(position, collisionDetection, hitboxes, displayImages)
        self.momentum = startingMomentum
        self.friendly = friendly
        self.dieOnImpact = impactDeath
        self.speed = speed
    def update(self,fps):
        self.position = [self.position[x]-self.momentum[x]/fps for x in (0,1)]
    def liveCheck(self,collisionWith):
        if self.dieOnImpact:
            for i in self.hitboxes:
                if i.collidelist(collisionWith):
                    return False
        return True

class EntityHandler:
    def __init__(self):
        self.elements = ['empty']
        self.availableIndexes = [0]
    def scan(self):
        for i in range(len(self.elements)):
            if self.elements[i] == 'empty':
                self.availableIndexes.append(i)
            elif i in self.availableIndexes:
                self.availableIndexes.remove(i)
            if len(self.availableIndexes) == 0:
                self.elements.append('empty')
                self.availableIndexes.append(len(self.elements)-1)
        return self.availableIndexes
    def add(self,element,index):
        self.elements[index] = element
        self.availableIndexes.remove(index)
    def remove(self,index):
        self.elements[index] = 'empty'
        self.availableIndexes.append(index)
    def update(self):
        for element in self.elements:
            if isinstance(element,Entity):
                element.update()
    def renderEntities(self):
        if pygame.display.get_init():
            for element in self.elements:
                if isinstance(element,Entity):
                    element.render()
