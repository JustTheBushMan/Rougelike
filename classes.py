import copy
import math
import random
from symtable import Class

import pygame
import global_vars
import math_functions

class Image:
    def render(self):
        print('No Data in Image')

class Picture(Image):
    def __init__(self,position,image):
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

class Hitboxes:
    def __init__(self,center,boxes):
        self.center = center
        self.boxes = boxes
    def collideCheck(self,hitbox):
        for box in self.boxes:
            if box.collidelist([i for i in hitbox.boxes])!=-1:
                return True
        return False
    def recenter(self,pos):
        self.center = pos
        for box in self.boxes:
            box.center = self.center
    def translate(self,translation):
        for box in self.boxes:
            box.move(translation[0],translation[1])
    def render(self):
        for box in self.boxes:
            pygame.draw.rect(global_vars.screen,(255,0,0),box,1,1)

class CircleHitboxes(Hitboxes):
    def __init__(self, center, radius):
        boxes = [
            pygame.Rect(0,0,radius,radius*2),
            pygame.Rect(0,0,radius*2,radius),
            pygame.Rect(0,0,radius*1.5,radius*1.5)
        ]
        super().__init__(center, boxes)

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

class Hearts(Entity):
    def __init__(self):
        positions = [
            [20,990],
            [20,920],
            [20,850]
        ]
        image = DisplayImage( [
            [3,[Picture(positions[0],global_vars.HEART),Picture(positions[1],global_vars.HEART),Picture(positions[2],global_vars.HEART)]],
            [2,[Picture(positions[0],global_vars.HEART),Picture(positions[1],global_vars.HEART),Picture(positions[2],global_vars.DEAD_HEART)]],
            [1,[Picture(positions[0],global_vars.HEART),Picture(positions[1],global_vars.DEAD_HEART),Picture(positions[2],global_vars.DEAD_HEART)]]
        ],3 )
        super().__init__([0,0], False, Hitboxes([0,0],[]), image)
    def update(self,fps):
        self.displayImages.state = entityManager.classes["Player"].elements[0].hp


class Burst(Entity):
    def __init__(self, position,startRadius,color):
        super().__init__(position, False, Hitboxes(position,[]), None)
        self.radius = startRadius
        self.speed = 1
        self.color = color
    def update(self,fps):
        self.radius += self.speed/fps*300
        self.speed *= .85
        if self.speed < .05:
            self.kill = True
        self.displayImages = DisplayImage( [['normal',[CircleImage(self.position,self.radius,self.color,5)]]],'normal')

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
        self.speed = speed * 50
        self.gun = gun
        self.dash = 0
        self.dashCooldownMax = 2
        self.dashCooldown = 0
        self.dashTime = .2
        self.dashMomentum = None
        self.knockbackMomentum = [0,0]
        self.dashInvulnerability = False
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
        translation = [translation[0]/fps,translation[1]/fps]
        translation = [
            max(global_vars.PLAYER_RADIUS,min(self.position[0]+translation[0],global_vars.DIMENSIONS[0]-global_vars.PLAYER_RADIUS))-self.position[0],
            max(global_vars.PLAYER_RADIUS,min(self.position[1]+translation[1],global_vars.DIMENSIONS[1]-global_vars.PLAYER_RADIUS))-self.position[1]
        ]
        self.position = [self.position[0]+translation[0],self.position[1]+translation[1]]
        for i in self.displayImages:
            translateImage(i,translation)
        self.hitboxes.recenter(self.position)
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
        self.checkCollisions()
        self.stateFor = max(0, self.stateFor - 1 / fps)
        if self.stateFor == 0:
            self.displayImages.state = 'normal'
        if self.health <= 0:
            self.kill = True
            entityManager.add(Burst(self.position, 10, self.displayImages.imgs['normal'][0].color))
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
        for x in 0,1:
            mom = [0,0]
            if self.position[x] < 30:
                mom[x] = 30-self.position[x]
                self.position[x] = 30
            elif self.position[x] > global_vars.DIMENSIONS[x]-30:
                mom[x] = global_vars.DIMENSIONS[x] - self.position[x] -30
                self.position[x] = global_vars.DIMENSIONS[x]-30
            self.displayImages.translate(mom)
            self.hitboxes.recenter(self.position)
            self.lamdas(self,fps)
    def checkCollisions(self):
        for i in self.hitBy:
            i[1] -= 1
            if i[1] <= 0:
                del i
        for entity in entityManager.classes["Projectile"].elements.values():
            if type(entity).__name__ == "Projectile":
                if entity.friendly and entity.signature not in [i[0] for i in self.hitBy]:
                        if self.hitboxes.collideCheck(entity.hitboxes):
                            self.knockback = 3
                            self.displayImages.state="hit"
                            self.stateFor = .2
                            self.health -= entity.damage
                            sig = random.randrange(0,32767)
                            self.hitBy.append([sig,10])
                            entity.signature = sig
                            if self.health <= 0 and entity.dieOnImpact:
                                entity.kill = True
        for entity in entityManager.classes["Player"].elements.values():
            if type(entity).__name__ == "Player":
                    if self.hitboxes.collideCheck(entity.hitboxes) and not (entity.dashInvulnerability and entity.dash != 0):
                        self.knockback = 10
        for entity in entityManager.classes["Enemy"].elements.values():
            if type(entity).__name__ == "Enemy" and entity != self:
                    oldPos = self.position
                    if self.hitboxes.collideCheck(entity.hitboxes):
                        self.position = math_functions.vectAdd(self.position,math_functions.normalizeVect([self.position[0]-entity.position[0],self.position[1]-entity.position[1]],2))
                    self.position = math_functions.bound(self.position,self.hitboxes.boxes[0].width)
                    self.displayImages.translate([self.position[0]-oldPos[0],self.position[1]-oldPos[1]])

class Projectile(Entity):
    def __init__(self, startingMomentum, position, hitboxes, collisionDetection, displayImages,friendly,impactDeath):
        super().__init__(position, collisionDetection, hitboxes, displayImages)
        self.momentum = startingMomentum
        self.friendly = friendly
        self.dieOnImpact = impactDeath
        self.damage = 1
        self.signature = None
    def update(self,fps):
        self.checkCollisions()
        self.position = [self.position[x]-self.momentum[x]/fps for x in (0,1)]
        if self.position[0] // global_vars.DIMENSIONS[0] != 0 or self.position[1] // global_vars.DIMENSIONS[1] != 0:
            self.kill = True
        self.hitboxes.recenter(self.position)
        self.displayImages.translate([-self.momentum[0]/fps,-self.momentum[1]/fps])
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
                            otherBoxes.append(entity.hitboxes)
            for box in otherBoxes:
                if self.hitboxes.collideCheck(box):
                    self.displayImages.state = 'none'
                    self.kill = True

class Gun:
    def __init__(self,fireRate,bulletSpeed,speedMod):
        self.fireRate = fireRate
        self.bulletSpeed = bulletSpeed
        self.speedMod = speedMod
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
            image = DisplayImage([['normal',[CircleImage(newPos,15,[255,255,255],0)]]],'normal')
            bullet = Projectile(movement, newPos, CircleHitboxes(newPos,15), False, image, True, True)
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
        for element in self.elements.values():
            element.update(fps)
    def killCheck(self):
        scheduleKill = []
        for element in self.elements.values():
            if element.kill:
                scheduleKill.append(element.address)
        for x in scheduleKill:
            del self.elements[x]
            self.usedIndexes.remove(x)
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
                    if hasattr(element, 'hitboxes') and global_vars.RENDER_HITBOXES:
                        if hasattr(element.hitboxes, 'render'):
                            element.hitboxes.render()

class EntityHandler:
    def __init__(self):
        self.classes = {
            'Burst': ClassEntityHandler(),
            'Player':ClassEntityHandler(),
            'Projectile': ClassEntityHandler(),
            'Enemy': ClassEntityHandler(),
            'Cursor': ClassEntityHandler(),
            'Hearts': ClassEntityHandler()
        }
        self.waveCooldown = -1
    def update(self,fps):
        for i in self.classes.values():
            i.updateClassEntities(fps)
        for i in self.classes.values():
            i.killCheck()
        if self.classes['Enemy'].elements == {} and self.waveCooldown == -1:
            self.waveCooldown = 5
        if self.waveCooldown == 0:
            self.waveCooldown = -1
            wave()
        if self.waveCooldown != -1:
            self.waveCooldown = max(self.waveCooldown - 1 / fps, 0)
    def render(self):
        for i in self.classes:
            self.classes[i].renderEntities()
    def add(self,entity):
        cls = type(entity).__name__
        self.classes[cls].add(entity)


def i1(self,fps):
    pass


def i2(self,fps):
    pass


def r1(self,fps):
    if 'cooldown' not in self.dict:
        self.dict['cooldown'] = random.randint(2,4)
    self.dict['cooldown'] = max(0,self.dict['cooldown']-1/fps)
    if self.dict['cooldown'] == 0:
        self.dict['cooldown'] = random.randint(2,4)
        playerPos = entityManager.classes['Player'].elements[0].position
        vect = [playerPos[0]-self.position[0],playerPos[1]-self.position[1]]
        movement = math_functions.normalizeVect(vect,400)
        movement = [-movement[0],-movement[1]]
        newPos = [self.position[0]-movement[0]/8,self.position[1]-movement[1]/8]
        image = DisplayImage([['normal',[CircleImage(newPos,15,[150,40,40])]]],'normal')
        bullet = Projectile(movement, newPos, CircleHitboxes(newPos,15), False, image, False, True)
        entityManager.add(copy.deepcopy(bullet))



def r2(self,fps):
    if 'cooldown' not in self.dict:
        self.dict['cooldown'] = random.randint(2,4)
    self.dict['cooldown'] = max(0, self.dict['cooldown'] - 1 / fps)
    if self.dict['cooldown'] == 0:
        self.dict['cooldown'] = random.randint(2,4)
        for a in (-15,0,15):
            playerPos = entityManager.classes['Player'].elements[0].position
            playerPos = math_functions.rotate(playerPos, a, self.position)
            vect = [playerPos[0] - self.position[0], playerPos[1] - self.position[1]]
            movement = math_functions.normalizeVect(vect, 400)
            movement = [-movement[0], -movement[1]]
            newPos = [self.position[0] - movement[0] / 8, self.position[1] - movement[1] / 8]
            image = DisplayImage([['normal', [CircleImage(newPos, 15, [150, 40, 40])]]], 'normal')
            bullet = Projectile(movement, newPos, CircleHitboxes(newPos, 15), False, image, False, True)
            entityManager.add(copy.deepcopy(bullet))


def t(self, fps):
    if self.kill:
        for angle in range(0, 360, 36):  # 10 equally spaced angles
            vect = [0,100]
            vect = math_functions.rotate(vect, angle, [0,0])
            movement = math_functions.normalizeVect(vect, 150)
            newPos = [self.position[0] - movement[0] / 8, self.position[1] - movement[1] / 8]
            image = DisplayImage([['normal', [CircleImage(newPos, 15, [150, 40, 40])]]], 'normal')
            bullet = Projectile(movement, newPos, CircleHitboxes(newPos, 15), False, image, False, True)
            entityManager.add(copy.deepcopy(bullet))



def b1(self,fps):
    pass


def b2(self,fps):
    pass


def b3(self,fps):
    pass


def h(self,fps):
    if 'cooldown' not in self.dict:
        self.dict['cooldown'] = random.randint(5,7)
    self.dict['cooldown'] = max(0, self.dict['cooldown'] - 1 / fps)
    if self.dict['cooldown'] == 0:
        missingHealth,idx = 0,None
        for element in entityManager.classes['Enemy'].elements.keys():
            if entityManager.classes['Enemy'].elements[element].maxHealth - entityManager.classes['Enemy'].elements[element].health < missingHealth:
                missingHealth = entityManager.classes['Enemy'].elements[element].maxHealth - entityManager.classes['Enemy'].elements[element].health
                idx = element

def l(self,fps):
    pass

def i1i(pos):
    return DisplayImage(
        [
            ['normal',[
                CircleImage(pos,30,[60,0,150],0),
                CircleImage(pos,30,[40,0,110],3)
            ]],
             ['hit',[
                CircleImage(pos,30,[40,0,130],0),
                CircleImage(pos,30,[20, 0, 70],3)
             ]
             ]
        ],'normal'
    )

def i2i(pos):
    return DisplayImage(
        [
            ['normal', [
                CircleImage(pos, 40, [60,0,150], 0),
                CircleImage(pos, 40, [40,0,110], 3),
            ]],
             ['hit', [
                 CircleImage(pos, 40, [40,0,110], 0),
                 CircleImage(pos, 40, [20, 0, 70], 3),
             ]
             ]
        ],'normal'
    )

def r1i(pos):
    return DisplayImage(
        [
            ['normal', [
                CircleImage(pos, 30, [100, 20, 100], 0),
                CircleImage(pos, 30, [70, 10, 70], 3),
            ]],
             ['hit', [
                 CircleImage(pos, 30, [150, 30, 150], 0),
                 CircleImage(pos, 30, [110, 20, 110], 3),
             ]
             ]
        ],'normal'
    )

def r2i(pos):
    return DisplayImage(
        [
            ['normal', [
                CircleImage(pos, 40, [100, 20, 100], 0),
                CircleImage(pos, 40, [70, 10, 70], 3),
            ]],
             ['hit', [
                 CircleImage(pos, 40, [150, 30, 150], 0),
                 CircleImage(pos, 40, [110, 20, 110], 3),
             ]
             ]
        ],'normal'
    )

def ti(pos):
    return DisplayImage(
        [
            ['normal', [
                CircleImage(pos, 50, [120, 20, 180], 0),
                CircleImage(pos, 50, [80, 10, 80], 3),
            ]],
             ['hit', [
                 CircleImage(pos, 50, [180, 40, 180], 0),
                 CircleImage(pos, 50, [120, 20, 120], 3),
             ]
             ]
        ],'normal'
    )

def hi(pos):
    return DisplayImage(
        [
            ['normal', [
                CircleImage(pos, 30, [50, 100, 90], 0),
                CircleImage(pos, 30, [30, 80, 70], 3),
            ]],
             ['hit', [
                 CircleImage(pos, 30, [80, 130, 120], 0),
                 CircleImage(pos, 30, [50, 100, 90], 3),
             ]
             ]
        ],'normal'
    )

def li(pos):
    return DisplayImage(
        [
            ['normal', [
                CircleImage(pos, 20, [200, 0, 140], 0),
                CircleImage(pos, 20, [150, 0, 90], 3),
            ]],
             ['hit', [
                 CircleImage(pos, 20, [250, 0, 190], 0),
                 CircleImage(pos, 20, [200, 0, 140], 3),
             ]
             ]
        ],'normal'
    )

lambdas = {
    'i1':lambda self,fps: i1(self,fps),
    'i2':lambda self,fps: i2(self,fps),
    'r1':lambda self,fps: r1(self,fps),
    'r2':lambda self,fps: r2(self,fps),
    't':lambda self,fps: t(self,fps),
    'h':lambda self,fps: h(self,fps),
    'l':lambda self,fps: l(self,fps)
}


radii = {
    'i1': 30,
    'i2': 40,
    'r1': 30,
    'r2': 40,
    't': 50,
    'h' : 30,
    'l': 20

}

speeds = { 
    'i1': 200,
    'i2': 175,
    'r1': 100,
    'r2': 75,
    't': 125,
    'h' : 100,
    'l': 250
}

target = { 
    'i1': 0,
    'i2': 0,
    'r1': 600,
    'r2': 650,
    't': 0,
    'h' : 400,
    'l': 0
}

hp = {
    'i1': 4,
    'i2': 7,
    'r1': 3,
    'r2': 5,
    't': 12,
    'h' : 4,
    'l': 1
}

def lpos(pos):
    return [
        pos,
        [pos[0],pos[1]+20],
        [pos[0],pos[1]-20],
        [pos[0]+20,pos[1]],
        [pos[0]-20,pos[1]],
        [pos[0]+15,pos[1]+15],
        [pos[0]+15,pos[1]-15],
        [pos[0]-15,pos[1]+15],
        [pos[0]-15,pos[1]-15]
    ]

def wave():
    probList = ['i1','i1','i2','r1','r1','r2','t','l','h']
    spawnPoints = 10
    pointVals = {
        'i1': 1,
        'i2': 2,
        'r1': 1,
        'r2': 2,
        't': 3,
        'h' : 2,
        'l': 3
    }
    spawns = []
    usedPositions = []
    positions = [[320,270],[640,135],[960,135],[1280,135],[1600,270],[160,540],[1760,540],[320,810],[640,945],[960,945],[1280,945],[1600,810]]
    for i in positions:
        if math_functions.pythag(i,entityManager.classes["Player"].elements[0].position) <= 300:
            usedPositions.append(i)
    while spawnPoints > 0:
        pick = random.choice(probList)
        if pointVals[pick] > spawnPoints:
            continue
        else:
            spawns.append(pick)
            spawnPoints -= pointVals[pick]
    for i in spawns:
        while True:
            pos = random.choice(positions)
            if pos not in usedPositions:
                usedPositions.append(pos)
                break
        if i != 'l':
            enemy = Enemy(pos,CircleHitboxes(pos,radii[i]),eval(f'{i}i({pos})'),speeds[i],target[i],hp[i],lambdas[i])
            entityManager.add(copy.deepcopy(enemy))
        else:
            for newPos in lpos(pos):
                enemy = Enemy(newPos,CircleHitboxes(newPos,radii[i]),eval(f'{i}i({newPos})'),speeds[i],target[i],hp[i],lambdas[i])
                entityManager.add(copy.deepcopy(enemy))
                
    global_vars.wave += 1

entityManager = EntityHandler()