import copy
import math
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

class DisplayImage: # a list of lists of images and state call [[state1,[img1,img2,img3]],[state2,[img1,img2]]]
    def __init__(self,images,currentState):
        self.state = currentState
        self.imgs = {}
        for i in range(len(images)):
            self.imgs[images[i][0]] = images[i][1]
        self.imgs['none'] = []
    def render(self):
        for img in self.imgs[self.state]:
            img.render()
    def translate(self,translation):
            for key in self.imgs.keys():
                for img in self.imgs[key]:
                    translateImage(img,translation)





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

def translateHitbox(hitbox,translation):
    hitbox[0] += translation[0]
    hitbox[1] += translation[1]

class Entity:
    def __init__(self, position, collisionDetection, hitboxes, displayImages):#DisplayImages need to be like ['circle',actual data]
        self.position = position
        self.detectCollision = collisionDetection
        self.hitboxes = hitboxes
        self.displayImages = displayImages
        self.address = None
        self.kill = False
    def render(self):
        for i in self.displayImages:
            i.render()
    def checkCollisions(self):
        classes = None
        otherBoxes = []
        if classes is None:
            classes = entityManager.classes
        for cls in classes:
            for entity in entityManager.classes[cls].elements:
                if isinstance(entity,Entity):
                    for box in entity.hitboxes:
                        otherBoxes.append(box)
        returns = []
        for ownBox in self.hitboxes:
            for otherBox in otherBoxes:
                if ownBox.colliderect(otherBox):
                    returns.append([type(otherBox).__name__,otherBox.address])
        return returns

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
        for box in self.hitboxes:
            box.x += translation[0]
            box.y += translation[1]
        self.gun.update(fps,self.position)

class Enemy(Entity):
    def __init__(self,position,hitboxes,displayImages,speed,playerTargetDistance,health,lamdas):
        super().__init__(position,False,hitboxes,displayImages)
        self.speed = speed
        self.playerTargetDistance = playerTargetDistance
        self.maxHealth = health
        self.health = health
        self.hitBy = []
        self.dict = {}
        self.stateFor = 0
        self.lamdas = lamdas
        self.knockback = 0
    def update(self, fps):
        self.stateFor = max(0, self.stateFor - 1 / fps)
        if self.stateFor == 0:
            self.displayImages.state = 'normal'
        if self.health <= 0:
            self.kill = True
        playerPos = entityManager.classes['Player'].elements[0].position
        xyDiff = [playerPos[0] - self.position[0], playerPos[1] - self.position[1]]
        zDistance = math.sqrt(xyDiff[0] ** 2 + xyDiff[1] ** 2)
        direction = [xyDiff[0] / zDistance, xyDiff[1] / zDistance]
        distanceToMove = zDistance - self.playerTargetDistance
        if self.knockback > 0:
            self.knockback -= 1
            speedMultiplier = -3
        elif distanceToMove < 0:
            direction = [-direction[0], -direction[1]]  # move away if too close
            speedMultiplier = 0.5  # move at half speed when moving away
        else:
            speedMultiplier = 1.0
        momentum = [direction[0] * min(abs(distanceToMove), self.speed / fps * speedMultiplier),
                    direction[1] * min(abs(distanceToMove), self.speed / fps * speedMultiplier)]
        self.position = [self.position[0] + momentum[0], self.position[1] + momentum[1]]
        self.displayImages.translate(momentum)
        for box in self.hitboxes:
            translateHitbox(box,momentum)
        for x in 0,1:
            mom = [0,0]
            if self.position[x] < 30:
                mom[x] = 30-self.position[x]
                self.position[x] = 30
            elif self.position[x] > global_vars.DIMENSIONS[x]-30:
                mom[x] = global_vars.DIMENSIONS[x] - self.position[x] -30
                self.position[x] = global_vars.DIMENSIONS[x]-30
            self.displayImages.translate(mom)
            for box in self.hitboxes:
                translateHitbox(box,mom)
            self.checkCollisions()
    def checkCollisions(self):
        for i in self.hitBy:
            i[1] -= .03
            if i[1] <= 0:
                del i
        for entity in entityManager.classes["Projectile"].elements.values():
            if type(entity).__name__ == "Projectile":
                if entity.friendly and entity.address not in [i[0] for i in self.hitBy]:
                    for box in entity.hitboxes:
                        if box.collidelist(self.hitboxes) != -1:
                            self.knockback = 3
                            self.displayImages.state="hit"
                            self.stateFor = 1
                            self.health -= entity.damage
                            self.hitBy.append([entity.address,2])
        for entity in entityManager.classes["Player"].elements.values():
            if type(entity).__name__ == "Player":
                for box in entity.hitboxes:
                    if box.collidelist(self.hitboxes) != -1:
                        self.knockback = 3

class Projectile(Entity):
    def __init__(self, startingMomentum, position, hitboxes, collisionDetection, displayImages,friendly,impactDeath):
        super().__init__(position, collisionDetection, hitboxes, displayImages)
        self.momentum = startingMomentum
        self.friendly = friendly
        self.dieOnImpact = impactDeath
        self.damage = 1
    def update(self,fps):
        self.position = [self.position[x]-self.momentum[x]/fps for x in (0,1)]
        if self.position[0] // global_vars.DIMENSIONS[0] != 0 or self.position[1] // global_vars.DIMENSIONS[1] != 0:
            self.kill = True
        for box in self.hitboxes:
            translateHitbox(box,[-self.momentum[0]/fps,-self.momentum[1]/fps])
        self.displayImages.translate([-self.momentum[0]/fps,-self.momentum[1]/fps])
        print(self.position,self.displayImages.imgs['normal'][0].center)
        self.checkCollisions()
    def checkCollisions(self):
        if self.dieOnImpact:
            otherBoxes = []
            match self.friendly:
                case True:
                    classes = ["Enemy"]
                case False:
                    classes = ["Player"]
                case None | _ :
                    classes = []
            for cls in classes:
                for entity in entityManager.classes[cls].elements.values():
                    if isinstance(entity,Entity):
                        for box in entity.hitboxes:
                            otherBoxes.append(box)
            for ownBox in self.hitboxes:
                if ownBox.collidelist(otherBoxes)!=-1:
                    self.displayImages.state = 'none'
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
            image = DisplayImage([['normal',[CircleImage(newPos,10,[255,255,255],0)]]],'normal')
            bullet = Projectile(movement, newPos, math_functions.hitboxesFromCircle(newPos,self.displayImages[0].radius), False, image, True, True)
            entityManager.add(copy.deepcopy(bullet))

class ClassEntityHandler:
    def __init__(self):
        self.elements = {}
        self.usedIndexes = []
    def getIndex(self):
        num = 0
        while num in self.usedIndexes:
            num+=1
        return num
    def add(self,element):
        newIndex = self.getIndex()
        self.elements[newIndex] = element
        element.address = newIndex
        self.usedIndexes.append(newIndex)
    def remove(self,index):
        del self.elements[index]
        self.usedIndexes.remove(index)
    def updateClassEntities(self,fps):
        scheduleKill = []
        for element in self.elements.values():
            element.update(fps)
            if element.kill:
                scheduleKill.append(element.address)
        for x in scheduleKill:
            del self.elements[x]
    def renderEntities(self):
        if pygame.display.get_init():
            for element in self.elements.values():
                if isinstance(element,Entity):
                    match type(element.displayImages).__name__:
                        case 'DisplayImage':
                            element.displayImages.render()
                        case 'list':
                            for pic in element.displayImages:
                                pic.render()

class EntityHandler:
    def __init__(self):
        self.classes = {
            'Player':ClassEntityHandler(),
            'Enemy': ClassEntityHandler(),
            'Projectile':ClassEntityHandler(),
            'Cursor': ClassEntityHandler(),
            'Explosion': ClassEntityHandler()
        }
    def update(self,fps):
        for i in self.classes.values():
            i.updateClassEntities(fps)
    def render(self):
        for i in self.classes:
            self.classes[i].renderEntities()
    def add(self,entity):
        cls = type(entity).__name__
        self.classes[cls].add(entity)

def i0(self,fps):
    pass

def i1(self,fps):
    pass

def i2(self,fps):
    pass


def r1(self,fps):
    pass


def r2(self,fps):
    pass


def t(self,fps):
    pass


def l(self,fps):
    pass


def b1(self,fps):
    pass


def b2(self,fps):
    pass


def b3(self,fps):
    pass


def h(self,fps):
    pass


def i0i(pos):
    return DisplayImage(
        [
            ['normal',[
                CircleImage(pos,30,[255,0,255],0),
                CircleImage(pos,30,[170,0,170],3),
            ],
             'hit',[
                CircleImage(pos,30,[255,100,255],0),
                CircleImage(pos,30,[170,60,170],3),
             ]
             ]
        ]
    )

i1 = i1
i2 = i2
r1 = r1
r2 = r2
t = t
l = l
b1 = b1
b2 = b2
b3 = b3
h = h










##########################################################################################################

entityManager = EntityHandler()