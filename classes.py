import pygame
import math



import global_vars

def renderGeneric(images,screen,color=(0,0,0),rectRadius=0,rectBorder=0):
    for i in images:
        match i[0]:
            case 'image':
                screen.blit(i[1])
            case 'rect':
                pygame.draw.rect(global_vars.screen,color,i[1],rectBorder,rectRadius)


class Entity:
    def __init__(self, position, collisionDetection, hitboxes, displayImages):#DisplayImages need to be like ['circle',actual data]
        self.position = position
        self.detectCollision = collisionDetection
        self.hitboxes = hitboxes
        self.displayImages = displayImages
    def render(self,screen):
        for i in self.displayImages:
            renderGeneric(self.displayImages,screen)
    def checkCollisions(self,objects):
        for i in self.hitboxes:
            if i.Rect.collidelist(objects):
                return True
        return False

class Player(Entity):
    def __init__(self, position, hp, maxhp, detectCollision, hitboxes, displayImages,speed):
        super().__init__(position, detectCollision, hitboxes, displayImages)
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
    def renderEntities(self,screen):
        if pygame.display.get_init():
            for element in self.elements:
                if isinstance(element,Entity):
                    element.render(screen)
