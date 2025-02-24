import pygame
import math
import events
import global_vars
import main
import math_functions


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

class LineImage(Image):
    def __init__(self,image,start,end,color,border=0):
        super().__init__('line',image)
        self.start = start
        self.end = end
        self.color = color
        self.border = border
    def render(self):
        pygame.draw.line(global_vars.screen,self.color,self.start,self.end,self.border)

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
        self.center = tuple((float(i) for i in center))
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
                    for hitbox in object.hitboxes:
                        if hitbox.collidelist(element.hitboxes) != -1:
                            events.eventHandler.addEvent(['collision',object.hitAttributes,element])
                            return True
    return False


class Entity:
    def __init__(self, position, collisionDetection, hitboxes, displayImages,):#DisplayImages need to be like ['circle',actual data]
        self.position = position
        self.detectCollision = collisionDetection
        self.hitboxes = hitboxes
        self.displayImages = displayImages
        self.index = (None,None)
    def render(self):
        for i in self.displayImages:
            i.render()
    def checkCollisions(self,handler):
        if self.detectCollision:
            match type(self):
                case Projectile:
                    for cls in handler.classes:
                        for elmt in cls.elements:
                            for hitbox in self.hitboxes:
                                if hitbox.collidelist(elmt.hitboxes) != -1:
                                    events.eventHandler.addEvent(['collision',self.index,elmt.index])
                                    return

def getMouseRel():
    return pygame.mouse.get_rel()



class Cursor(Entity):
    def __init__(self):
        super().__init__([0,0],False,[],[])
        self.color = (66,16,126)
        self.size = global_vars.CURSOR_SIZE
        self.distance = global_vars.CURSOR_DISTANCE
        self.width = global_vars.CURSOR_WIDTH
        self.angle = 0
    def update(self,fps):
        self.position = pygame.mouse.get_pos()
        self.displayImages = []
        self.angle += 40/fps
        self.angle = self.angle%360
        for a in (0,90,180,270):
            start = math_functions.rotate(math_functions.vectAdd(self.position, [self.distance, self.distance]),self.angle + a, self.position)
            end = math_functions.rotate(math_functions.vectAdd(self.position, [self.size, self.size]), self.angle + a,self.position)
            self.displayImages.append(LineImage(0, start, end, self.color, self.width))





class Player(Entity):
    def __init__(self, position, hp, maxhp, hitboxes, displayImages,speed):
        super().__init__(position, True, hitboxes, displayImages)
        self.hp = hp
        self.maxhp = maxhp
        self.speed = speed
    def getMovement(self):
        keys = pygame.key.get_pressed()
        x = keys[pygame.K_d]-keys[pygame.K_a]
        y = keys[pygame.K_s]-keys[pygame.K_w]
        if x != 0 and y != 0:
            x/=1.44
            y/=1.44
        return [x*self.speed,y*self.speed]
    def update(self,fps):
        diff = self.getMovement()
        self.position = [self.position[0]+diff[0]/fps,self.position[1]+diff[1]/fps]
        self.position = [max(global_vars.PLAYER_RADIUS,min(self.position[0],global_vars.DIMENSIONS[0]-global_vars.PLAYER_RADIUS)),max(global_vars.PLAYER_RADIUS,min(self.position[1],global_vars.DIMENSIONS[1]-global_vars.PLAYER_RADIUS))]
        self.displayImages = [CircleImage(0,[self.position[0],self.position[1]],global_vars.PLAYER_RADIUS,global_vars.PLAYER_COLOR,0)]


class Projectile(Entity):
    def __init__(self, startingMomentum, position, hitboxes, collisionDetection, displayImages,collideWith,impactDeath,speed):
        super().__init__(position, collisionDetection, hitboxes, displayImages)
        self.momentum = startingMomentum
        self.collideWith = collideWith
        self.dieOnImpact = impactDeath
        self.speed = speed
    def update(self,fps):
        self.position = [self.position[x]-self.momentum[x]/fps for x in (0,1)]

class Gun:
    def __init__(self,fireRate,projectile,angle,displayImages,speed):
        self.fireRate = fireRate
        self.projectile = projectile
        self.speed = speed
        self.displayImages = displayImages
        self.projectile.momentum = math_functions.rotate(self.projectile.momentum,angle, [0,0])
        self.projectile.speed *= self.speed
        self.angle = angle
        self.displayImages = displayImages
        self.cooldown = 0
    def getShoot(self):
        return pygame.mouse.get_pressed()
    def update(self,fps):
        self.cooldown = max(self.cooldown-1/fps,0)
        if self.cooldown == 0 and self.getShoot()[0]:
            self.cooldown = self.fireRate
            main.entityHandler.add(self.projectile)

class ClassEntityHandler:
    def __init__(self):
        self.elements = ['empty']
        self.availableIndexes = [0]
    def add(self,element,index):
        self.elements[index] = element
        self.availableIndexes.remove(index)
        for i in range(len(self.elements)):
            if self.elements[i] == 'empty':
                self.availableIndexes.append(i)
            elif i in self.availableIndexes:
                self.availableIndexes.remove(i)
            if len(self.availableIndexes) == 0:
                self.elements.append('empty')
                self.availableIndexes.append(len(self.elements)-1)
    def remove(self,index):
        self.elements[index] = 'empty'
        self.availableIndexes.append(index)
    def updateClassEntities(self,fps):
        for i in range(len(self.elements)):
            if self.elements[i] == 'empty':
                self.availableIndexes.append(i)
            elif i in self.availableIndexes:
                self.availableIndexes.remove(i)
            if len(self.availableIndexes) == 0:
                self.elements.append('empty')
                self.availableIndexes.append(len(self.elements)-1)
        for element in self.elements:
            if element != 'empty':
                element.update(fps)
    def renderEntities(self):
        if pygame.display.get_init():
            for element in self.elements:
                if isinstance(element,Entity):
                    for pic in element.displayImages:
                        pic.render()

class EntityHandler:
    def __init__(self):
        self.classes = {
            'Player':ClassEntityHandler(),
            'Cursor':ClassEntityHandler()
        }
    def update(self,fps):
        for i in self.classes.values():
            i.updateClassEntities(fps)
    def render(self):
        for i in self.classes:
            self.classes[i].renderEntities()
    def collideChecks(self):
        for i in self.classes:
            self.classes[i].checkCollisions()
    def add(self,entity):
        cls = type(entity).__name__
        entity.index = (cls,self.classes[cls].availableIndexes[0])
        self.classes[cls].add(entity,self.classes[cls].availableIndexes[0])