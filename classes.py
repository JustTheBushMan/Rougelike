import copy
import random
import pygame
import global_vars
import math_functions

class Image:
    def render(self):
        print('No Data in Image')

class Picture(Image):
    def __init__(self,image,position):
        self.position = position
        self.image = image
    def render(self):
        global_vars.screen.blit(self.image,self.position)

class LineImage(Image):
    def __init__(self,start,end,color,border=0):
        self.start = start
        self.end = end
        self.color = color
        self.border = border
    def render(self):
        pygame.draw.line(global_vars.screen,self.color,self.start,self.end,self.border)

class RectImage(Image):
    def __init__(self,rect,color,radius,border=0):
        self.rect = rect
        self.color = color
        self.radius = radius
        self.border = border
    def render(self):
        pygame.draw.rect(global_vars.screen,self.color,self.rect,self.border,self.radius)

class CircleImage(Image):
    def __init__(self,center,radius,color,border=0):
        self.center = tuple((float(i) for i in center))
        self.radius = radius
        self.border = border
        self.color = color
    def render(self):
        pygame.draw.circle(global_vars.screen,self.color,self.center,self.radius,self.border)

class TriangleImage(Image):
    def __init__(self,coords,color,border=0):
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
        self.position = position
    def render(self):
        global_vars.screen.blit(self.font.render(self.text,True,self.color),self.position)

class CircleGradient(Image):
    def __init__(self,radius,innerColor,outerColor,center):
        self.radius = radius
        self.innerColor = innerColor
        self.outerColor = outerColor
        self.center = center
    def render(self):
        for x in range(self.radius,0,-1):
            ringColor = math_functions.mixColors([[self.innerColor,self.radius-x],[self.outerColor,x]])
            pygame.draw.circle(global_vars.screen,ringColor,self.center,x)

class SquareGradient(Image):
    def __init__(self,rect,colors,position):
        self.rect = rect
        self.colors = colors
    def render(self):
        for x in range(0,self.rect[2]):
            for y in range(0,self.rect[3]):
                weights = [(self.rect[2]-x)*(self.rect[3]-y),x*(self.rect[3]-y),(self.rect[2]-x)*y,x*y]
                combined = [[self.colors[i],weights[i]] for i in (0,1,2,3)]
                global_vars.screen.screen.set_at((self.rect[0]+x,self.rect[1]+y),math_functions.mixColors(combined))

class Bar(Image):
    def __init__(self,rect,insideColor,baseColor,border,ratio=1):
        self.rect = rect
        self.insideColor = insideColor
        self.baseColor = baseColor
        self.border = border
        self.ratio = ratio
    def render(self):
        pygame.draw.rect(global_vars.screen,self.baseColor,self.rect,self.border,0,self.rect[3]/2)
        pygame.draw.rect(global_vars.screen,self.insideColor,(self.rect[0]+self.border,self.rect[1]+self.border,self.rect[2]*self.ratio-self.border*2,self.rect[3]-self.border*2),0,(self.rect[3]-self.border)/2)

class DisplayImages: # a list of lists of images and state call [[state1,[img1,img2,img3]],[state2,[img1,img2]]]
    def __init__(self,images):
        for i in range(len(images)):
            self.__dict__[images[i][0]] = images[i][1]


def translateImage(image,translation):
    match type(image).__name__:
        case 'Picture' | 'Text':
            image.position[0] += translation[0]
            image.position[1] += translation[1]
        case 'CircleImage' | 'CircleGradient':
            if type(image.center).__name__ == 'tuple':
                image.center = list(image.center)
            image.center[0] += translation[0]
            image.center[1] += translation[1]
        case 'LineImage':
            image.start[0] += translation[0]
            image.start[1] += translation[1]
            image.end[0] += translation[0]
            image.end[1] += translation[1]
        case 'RectImage' | 'SquareGradient':
            image.rect[0] += translation[0]
            image.rect[1] += translation[1]
        case 'TriangleImage':
            for i in image.coords:
                i[0] += translation[0]
                i[1] += translation[1]

class Entity:
    def __init__(self, position, collisionDetection, hitboxes, displayImages):#DisplayImages need to be like ['circle',actual data]
        self.position = position
        self.detectCollision = collisionDetection
        self.hitboxes = hitboxes
        self.displayImages = displayImages
    def render(self):
        for i in self.displayImages:
            i.render()
    def checkCollisions(self,handler):
        return

class Cursor(Entity):
    def __init__(self):
        super().__init__([0,0],False,[],[])
        self.color = (40,100,255)
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
            self.displayImages.append(LineImage( start, end, self.color, self.width))

class Player(Entity):
    def __init__(self, position, hp, maxhp, hitboxes, displayImages,speed,gun):
        super().__init__(position, True, hitboxes, displayImages)
        self.hp = hp
        self.maxhp = maxhp
        self.speed = speed
        self.gun = gun
        self.dash = 0
        self.dashCooldownMax = 2
        self.dashCooldown = 0
        self.dashTime = .2
        self.dashMomentum = None
        self.knockbackMomentum = [0,0]
    def getMovement(self):
        keys = pygame.key.get_pressed()
        x = keys[pygame.K_d]-keys[pygame.K_a]
        y = keys[pygame.K_s]-keys[pygame.K_w]
        if x != 0 and y != 0:
            x/=1.44
            y/=1.44
        return [x*self.speed,y*self.speed]
    def update(self,fps):
        self.dash = max(0,self.dash-1/fps)
        self.dashCooldown = max(0,self.dashCooldown-1/fps)
        diff = self.getMovement()
        translation = [diff[0]/fps,diff[1]/fps]
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.dashCooldown == 0:
            self.dashMomentum =  translation = [translation[0]*4,translation[1]*4]
            self.dash = self.dashTime
            self.dashCooldown = self.dashCooldownMax + self.dashTime
        if self.dash > 0:
            translation = self.dashMomentum
        translation = [translation[0]+self.knockbackMomentum[0],translation[1]+self.knockbackMomentum[1]]
        translation = [
            max(global_vars.PLAYER_RADIUS,min(self.position[0]+translation[0],global_vars.DIMENSIONS[0]-global_vars.PLAYER_RADIUS))-self.position[0],
            max(global_vars.PLAYER_RADIUS,min(self.position[1]+translation[1],global_vars.DIMENSIONS[1]-global_vars.PLAYER_RADIUS))-self.position[1]
        ]
        self.position = [self.position[0]+translation[0],self.position[1]+translation[1]]
        for i in self.displayImages:
            translateImage(i,translation)
        self.gun.update(fps,self.position)

class Enemy(Entity):
    def __init__(self,position,displayImages,hitboxes,speed,playerTargetDistance,health):
        super().__init__(position,False,hitboxes,displayImages)
        self.speed = speed
        self.playerTargetDistance = playerTargetDistance
        self.maxHealth = health
        self.health = health

class Projectile(Entity):
    def __init__(self, startingMomentum, position, hitboxes, collisionDetection, displayImages,collideWith,impactDeath):
        super().__init__(position, collisionDetection, hitboxes, displayImages)
        self.momentum = startingMomentum
        self.collideWith = collideWith
        self.dieOnImpact = impactDeath
        self.val = random.randint(0,100)
        self.kill = False
    def update(self,fps):
        for pic in self.displayImages:
            pic.center = self.position
        self.position = [self.position[x]-self.momentum[x]/fps for x in (0,1)]
        if self.position[0] // global_vars.DIMENSIONS[0] != 0 or self.position[1] // global_vars.DIMENSIONS[1] != 0:
            self.kill = True

class Gun:
    def __init__(self,fireRate,displayImages,bulletSpeed,speedMod):
        self.fireRate = fireRate
        self.bulletSpeed = bulletSpeed
        self.speedMod = speedMod
        self.displayImages = displayImages
        self.displayImages = displayImages
        self.cooldown = 0
        self.spread = 1
    def update(self,fps,pos):
        self.cooldown = max(self.cooldown - 1 / fps, 0)
        if self.cooldown == 0 and pygame.mouse.get_pressed()[0]:
            self.cooldown = self.fireRate
            cursor = pygame.mouse.get_pos()
            speed = self.speedMod * self.bulletSpeed
            vect = [cursor[0] - pos[0], cursor[1] - pos[1]]
            movement = math_functions.normalizeVect(vect,speed)
            movement = [-movement[0],-movement[1]]
            movement = math_functions.rotate(movement,random.randint(-self.spread,self.spread),pos)
            newPos = [pos[0] - movement[0]/12, pos[1] - movement[1]/12]
            bullet = Projectile(movement, newPos, [], False, self.displayImages, [], False)
            entityManager.add(copy.deepcopy(bullet))

class ClassEntityHandler:
    def __init__(self):
        self.elements = []
        self.usedIndexes = []
    def getIndex(self):
        while True:
            newIndex = random.randint(0,len(self.elements))
            if newIndex not in self.usedIndexes:
                return newIndex
    def add(self,element):
        newIndex = self.getIndex()
        self.elements.append([newIndex,element])
        self.usedIndexes.append(newIndex)
    def remove(self,index):
        for i in self.elements:
            if i[0] == index:
                self.elements.remove(i)
                self.usedIndexes.remove(index)
                break
    def updateClassEntities(self,fps):
        for element in self.elements:
            element[1].update(fps)
            if hasattr(element[1],'kill'):
                if element[1].kill:
                    self.remove(element[0])
    def renderEntities(self):
        if pygame.display.get_init():
            for element in self.elements:
                if isinstance(element[1],Entity):
                    for pic in element[1].displayImages:
                        pic.render()

class EntityHandler:
    def __init__(self):
        self.classes = {
            'Player':ClassEntityHandler(),
            'Projectile':ClassEntityHandler(),
            'Cursor': ClassEntityHandler()
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
        self.classes[cls].add(entity)

##########################################################################################################

entityManager = EntityHandler()