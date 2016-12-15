import pygame, random
import fightModule


WHITE = (255,255,255)
BLACK = (35,35,35)
BLUE = (50,50,255)
GREEN = (0,255,0)

FPS = 60
SCREENWIDTH = 800
SCREENHEIGHT = 500

HALF_WIDTH = int(SCREENWIDTH / 2)
HALF_HEIGHT = int(SCREENHEIGHT / 2)

CAMERASLACK = 175


def callback (sprite1,sprite2):
    sprite3 = pygame.sprite.Sprite()
    sprite3.rect = pygame.Rect(0,0,10,5)
    sprite3.rect.width = sprite1.rect.width / 2
    sprite3.rect.midbottom = sprite1.rect.midbottom
    return pygame.sprite.collide_rect(sprite3,sprite2)


class Level():
    def __init__(self, player):
        self.block_list = None
        self.layered_list = None
        self.background_list = None
        self.transport_list = None
        self.background = None
        self.world_shift_y = 0
        self.world_shift_x = 0
        self.player = player
        self.x_limit = None
        self.y_limit = None
        self.music = None
        
    def draw(self,screen):
        screen.blit(self.background,(self.world_shift_x,self.world_shift_y))

    def drawBackLayers(self,screen,y):
        backLayers = pygame.sprite.LayeredUpdates()
        for layer in self.layered_list:
            if layer.rect.bottom <= (y):
                backLayers.add(layer)
        backLayers.draw(screen)
                
    def drawFrontLayers(self,screen,y):
        frontLayers = pygame.sprite.LayeredUpdates()
        for layer in self.layered_list:
            if layer.rect.bottom > (y):
                frontLayers.add(layer)
        frontLayers.draw(screen)

    def shift_world(self,shift_x, shift_y):
        self.world_shift_x += shift_x
        self.world_shift_y += shift_y

        for block in self.block_list:
            block.rect.x +=shift_x
            block.rect.y +=shift_y

        for layer in self.layered_list:
            layer.rect.x +=shift_x
            layer.rect.y +=shift_y

        for obj in self.background_list:
            obj.rect.x +=shift_x
            obj.rect.y +=shift_y

        for zone in self.transport_list:
            zone.rect.x +=shift_x
            zone.rect.y +=shift_y
            
    def startMusic(self):
        if self.music:
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()


class DormRoom(Level):
    def __init__(self,player):
        Level.__init__(self,player)
        factor = 3
        self.background = scale(pygame.image.load("DormRoom.gif"),factor)
        self.x_limit = self.background.get_width()
        self.y_limit = self.background.get_height()
        
        self.world_shift_y = 0
        self.world_shift_x = 0

        self.block_list = pygame.sprite.Group()
        self.background_list = pygame.sprite.Group()
        self.transport_list = pygame.sprite.Group()
        self.layered_list = pygame.sprite.Group()

        wall = Block(72,164,6,370)
        self.block_list.add(wall)

        wall = Block(60,533,175,4)
        self.block_list.add(wall)

        wall = Block(246,537,6,36)
        self.block_list.add(wall)

        wall = Block(361,537,6,36)
        self.block_list.add(wall)

        wall = Block(369,533,175,4)
        self.block_list.add(wall)

        wall = Block(532,164,6,370)
        self.block_list.add(wall)

        wall = Block(245,159,101,6)
        self.block_list.add(wall)
        wall = Block(460,159,85,6)
        self.block_list.add(wall)

        poster = Layer(345,54,scale(pygame.image.load("poster.gif"),factor))
        poster.description = ["An acappella poster."]
        self.layered_list.add(poster)
        (x,y) = poster.rect.midbottom
        block = Block(x-40,y+24,120,3)
        block.layer = poster
        self.block_list.add(block)

        bed = Layer(404,176,scale(pygame.image.load("bed.gif"),factor))
        bed.description = ["Your bed."]
        self.layered_list.add(bed)
        (x,y) = bed.rect.midbottom
        block = Block(x-54,y-140,109,140)
        block.layer = bed
        self.block_list.add(block)

        dresser = Layer(108,77,scale(pygame.image.load("dresser.gif"),factor))
        dresser.description = ["Your dresser.", "You don't use it.", "Seriously, you own one shirt."]
        self.layered_list.add(dresser)
        (x,y) = dresser.rect.midbottom
        block = Block(x-68,y-77,136,77)
        block.layer = dresser
        self.block_list.add(block)

        desk = Layer(78,353,scale(pygame.image.load("desk.gif"),factor))
        desk.description = ["Your diary is open."]
        self.layered_list.add(desk)
        (x,y) = desk.rect.midbottom
        block = Block(x-40,y-131,100,131)
        block.layer = desk
        self.block_list.add(block)
        
        zone = TransportZone(235,556,120,30)
        zone.gameLevel= Campus
        zone.levelShift = (-16,-387)
        zone.playerDir = "D"
        self.transport_list.add(zone)
        
class Campus(Level):
    def __init__(self,player):
        Level.__init__(self,player)
        factor = 3
        self.background = scale(pygame.image.load("campus.gif"),factor)
        self.x_limit = self.background.get_width()
        self.y_limit = self.background.get_height()
        self.music = "./music/mercy.wav"

        self.world_shift_y = 0
        self.world_shift_x = 0

        self.block_list = pygame.sprite.Group()
        self.background_list = pygame.sprite.Group()
        self.transport_list = pygame.sprite.Group()

        treeImage = scale(pygame.image.load("tree.gif"),factor)
        #treeBlock = (40,20)
        
        self.layered_list = pygame.sprite.LayeredUpdates()
        tree = Layer(679,463,treeImage)
        self.layered_list.add(tree)
        (x,y) = tree.rect.midbottom
        block = Block(x-30,y-5,50,5)
        block.layer = tree
        self.block_list.add(block)

        tree = Layer(853,726,treeImage)
        self.layered_list.add(tree)
        (x,y) = tree.rect.midbottom
        block = Block(x-30,y-5,50,5)
        block.layer = tree
        self.block_list.add(block)

        tree = Layer(943,487,treeImage)
        tree.description = ["This tree is next to some mushrooms."]
        self.layered_list.add(tree)
        (x,y) = tree.rect.midbottom
        block = Block(x-30,y-5,50,5)
        block.layer = tree
        self.block_list.add(block)

        treeImage = scale(pygame.image.load("smallTree.gif"),factor)

        tree = Layer(1995,1045,treeImage)
        tree.description = ["this is a tree"]
        (x,y) = tree.rect.midbottom
        block = Block(x-10,y-5,50,5)
        block.layer = tree
        self.block_list.add(block)
        self.layered_list.add(tree)

        treeImage = pygame.transform.flip(scale(pygame.image.load("smallTree.gif"),factor),True,False)
        
        tree = Layer(2368,1042,treeImage)
        (x,y) = tree.rect.midbottom
        block = Block(x-40,y-5,50,5)
        block.layer = tree
        self.block_list.add(block)
        self.layered_list.add(tree)

        bushImage = scale(pygame.image.load("bush.gif"),factor)
        bushBlock = (40,10)
        bush = Layer(1844,1218,bushImage,bushBlock)
        self.layered_list.add(bush)

        bush = Layer(1923,1218,bushImage,bushBlock)
        bush.description = ["There's something in this bush!", "Oh wait, no there's not.", "Idiot."]
        self.layered_list.add(bush)
        
        bush = Layer(1769,1218,bushImage,bushBlock)
        self.layered_list.add(bush)

        ucImage = scale(pygame.image.load("UC2.gif"),factor)
        uc = Layer(1769,477,ucImage)
        uc.description = ["This is the UC.","It's not open yet"]
        self.layered_list.add(uc)
        (x,y) = uc.rect.midbottom
        block = Block(x-300,y-500,600,500)
        self.block_list.add(block)

        ucImage = scale(pygame.image.load("UC.gif"),factor)
        uc = Layer(1769,477,ucImage)
        self.layered_list.add(uc)
        (x,y) = uc.rect.midbottom
        block = Block(x-500,y-600,230,600)
        self.block_list.add(block)
        block = Block(x+270,y-600,230,600)
        self.block_list.add(block)
        
        dormImage = scale(pygame.image.load("dorm2.gif"),factor)
        dorm = Layer(2,48,dormImage)
        (x,y) = dorm.rect.midbottom
        block = Block(x-440,y-600,880,600)
        self.block_list.add(block)
        self.layered_list.add(dorm)
        
        dormImage = scale(pygame.image.load("dorm1.gif"),factor)
        dorm = Layer(2,48,dormImage)
        self.layered_list.add(dorm)
        (x,y) = dorm.rect.midbottom
        block = Block(x-160,y-600,320,600)
        self.block_list.add(block)
        
        fightImage = scale(pygame.image.load("original.gif"),factor)
        enemySprite = Enemy(20,fightImage)  
        enemyImage = fightImage
        en = Layer(1420,680,enemyImage,(20,5))        
        en.enemy = enemySprite
        en.fight = True
        self.layered_list.add(en)

        for layer in self.layered_list:
            if layer.block:
                (x,y) = layer.rect.midbottom
                (width,height) = layer.block
                block = Block(x-(width/2),y-height,width,height)
                block.layer = layer
                self.block_list.add(block)

        image1 = scale(pygame.image.load("grass1.gif"),factor)
        image2 = scale(pygame.image.load("grass2.gif"),factor)
        zoneRange = (2,5)
        grass = AnimatedObject(155,708,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        grass = AnimatedObject(231,709,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        grass = AnimatedObject(123,735,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        grass = AnimatedObject(194,739,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        grass = AnimatedObject(158,769,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        grass = AnimatedObject(228,772,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        grass = AnimatedObject(124,793,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        grass = AnimatedObject(196,796,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        grass = AnimatedObject(87,823,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        grass = AnimatedObject(159,825,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        grass = AnimatedObject(121,856,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        grass = AnimatedObject(192,859,image1,image2)
        grass.enemyImage = pygame.image.load("f.gif")
        grass.enemyLevelRange = zoneRange
        self.background_list.add(grass)

        zone = TransportZone(372,600,150,5)
        zone.gameLevel = DormRoom
        zone.levelShift = (140,-210)
        zone.playerDir = "U"
        self.transport_list.add(zone)

def scale(image,factor):
    (width,height) = image.get_size()
    return pygame.transform.scale(image, (int(float(width) * float(factor)),int(float(height) * float(factor))))

class Player(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.level = None  
        self.moving = False

        self.change_x = 0
        self.change_y = 0

        self.walking_frames_d = []
        self.walking_frames_u = []
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.direction = "D"

        factor = 3
        
        image = scale(pygame.image.load("f.gif"),factor)
        self.walking_frames_d.append(image)
        image = scale(pygame.image.load("f1.gif"),factor)
        self.walking_frames_d.append(image)
        image = scale(pygame.image.load("f.gif"),factor)
        self.walking_frames_d.append(image)
        image = scale(pygame.image.load("f2.gif"),factor)
        self.walking_frames_d.append(image)

        image = scale(pygame.image.load("b.gif"),factor)
        self.walking_frames_u.append(image)
        image = scale(pygame.image.load("b1.gif"),factor)
        self.walking_frames_u.append(image)
        image = scale(pygame.image.load("b.gif"),factor)
        self.walking_frames_u.append(image)
        image = scale(pygame.image.load("b2.gif"),factor)
        self.walking_frames_u.append(image)

        image = scale(pygame.image.load("l.gif"),factor)
        self.walking_frames_l.append(image)
        image = scale(pygame.image.load("l1.gif"),factor)
        self.walking_frames_l.append(image)

        image = scale(pygame.image.load("r.gif"),factor)
        self.walking_frames_r.append(image)
        image = scale(pygame.image.load("r1.gif"),factor)
        self.walking_frames_r.append(image)

        self.image = self.walking_frames_d[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        ###for fighting ###
        self.fightImage = scale(pygame.image.load("b.gif"),factor)
        self.maxHealth = 100
        self.health = 100
        self.items = dict([("pitch pipe",25), ("water",5), ("humidifier",15)])
        self.image = scale(pygame.image.load("b.gif"),3)
        
    def changespeed(self,x,y):
        self.change_x += x
        self.change_y += y

    def update(self):
        self.rect.x += self.change_x
        Xpos = self.rect.x + self.level.world_shift_x
        steps = 15

        if (self.change_x < 0) :
            self.direction = "L"
        elif (self.change_x > 0):
            self.direction = "R"
        
        if self.direction == "L":
            frame = (Xpos//steps) % len(self.walking_frames_l)
            if not self.moving:
                frame = 0
            self.image = self.walking_frames_l[frame]
            
        elif self.direction == "R":
            frame = (Xpos//steps) % len(self.walking_frames_r)
            if not self.moving:
                frame = 0
            self.image = self.walking_frames_r[frame]

        block_hit_list = pygame.sprite.spritecollide(self, self.blocks, False, callback)
        for block in block_hit_list:
            self.rect.x -= self.change_x
        
        self.rect.y += self.change_y
        Ypos = self.rect.y + self.level.world_shift_y

        if (self.change_y < 0) :
            self.direction = "U"
        elif (self.change_y > 0):
            self.direction = "D"
        
        if self.direction == "U":
            frame = (Ypos//steps) % len(self.walking_frames_u)
            if not self.moving:
                frame = 0
            self.image = self.walking_frames_u[frame]
            
        elif self.direction == "D":
            frame = (Ypos//steps) % len(self.walking_frames_d)
            if not self.moving:
                frame = 0
            self.image = self.walking_frames_d[frame]

        block_hit_list = pygame.sprite.spritecollide(self,self.blocks,False,callback)
        for block in block_hit_list:
            self.rect.y -= self.change_y
        
        if self.rect.left <=0:
            self.rect.left = 0
        if self.rect.right >= SCREENWIDTH:
            self.rect.right = SCREENWIDTH
        if self.rect.top <=0:
            self.rect.top = 0
        if self.rect.bottom >= SCREENHEIGHT:
            self.rect.bottom = SCREENHEIGHT

    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))

def getFacing(player):
    tempy = player.rect.y
    tempx = player.rect.x
        
    if player.direction == "U":
        player.rect.y -= 5
    if player.direction == "D":
        player.rect.y += 5
    if player.direction == "R":
        player.rect.x += 5
    if player.direction == "L":
        player.rect.x -= 5

    block_hit_list = pygame.sprite.spritecollide(player, player.blocks, False)
    player.rect.y = tempy
    player.rect.x = tempx

    if block_hit_list:
        return block_hit_list[0].layer

class Layer(pygame.sprite.Sprite):
    def __init__(self,x,y,image,block = None):
        pygame.sprite.Sprite.__init__(self)
        self.block = block
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.description = []
        self._layer = y
        self.fight = False
        self.enemy = None

class Enemy(pygame.sprite.Sprite):
    def __init__(self,level,image):
        self.level = level
        self.maxHealth = 25 * level
        self.health = 25 * level
        self.image = image
        self.noteOrigin = (30,40)
        self.descriptionOptions = [["What are you looking at?"],["Ready to try again?"],\
                                 [["Haha! I knew I could beat you."],["Look who's back for more!"]],\
                                  ["Leave me alone. You already won."]]
        self.status = 0 #unplayed, run, you lost, you won
        self.description = self.descriptionOptions[self.status]

    def getAttackDamage(self):
        return random.randrange(1,self.level)

class AnimatedObject(pygame.sprite.Sprite):
    def __init__(self,x,y,image1,image2):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image1 = image1
        self.image2 = image2
        self.image = image1 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.enemyLevelRange = (1,50)
        self.enemyImage = None

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def generateEnemy(self):
        (a,b) = self.enemyLevelRange
        lev = random.randint(a,b)
        return Enemy(lev,self.enemyImage)
        

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,width,height)
        self.layer = None
        
    def draw(self,screen):
        pygame.draw.rect(screen, BLACK, self.rect)

class TransportZone(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,width,height)
        self.gameLevel = None
        self.levelShift = None
        self.playerStart = None
        
    def transport(self,player):
        level = setLevel(player, self.gameLevel)
        (x,y) = self.levelShift
        level.shift_world(x,y)
        level.startMusic()
        return level

    def draw(self,screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        

def dead(player):
    level = setLevel(player,DormRoom)
    level.shift_world(150,0)
    player.direction = "L"
    player.health = player.maxHealth
    level.startMusic()
    return level                               
                                   

def drawDescription(screen,description,index):
    disBufferX = 30
    disHeight = 100
    disBufferY = 10
    disWidth = SCREENWIDTH - (2*disBufferX)
    disY = SCREENHEIGHT - (disBufferY + disHeight)
    displayBackground = pygame.Rect(disBufferX,disY,disWidth,disHeight)
    menubar = pygame.image.load("menuBar.gif")
    screen.blit(menubar,displayBackground)

    fontObj = pygame.font.SysFont('couriernew', 32)
    textSurfaceObj = fontObj.render(description[index],False,BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (HALF_WIDTH, disY+(disHeight/2))
    screen.blit(textSurfaceObj,textRectObj)

    if index < (len(description) - 1):
        pulse = (pygame.time.get_ticks()//100) % 10
        if pulse > 5:
            pulse = 10 - pulse
        ymid = disY + (disHeight/2)
        xbase = (disBufferX + disWidth) - 50
        pygame.draw.polygon(screen,BLACK,[(xbase+pulse,ymid - 5),\
                                          (xbase + 5 + pulse,ymid),\
                                          (xbase+pulse,ymid + 5)])

def setLevel(player,curr_level):
    level = curr_level(player)
    player.level = level
    player.blocks = level.block_list
    return level

def main():
    pygame.init()

    screen = pygame.display.set_mode([SCREENWIDTH,SCREENHEIGHT])
    pygame.display.set_caption('Test')

    player = Player(HALF_WIDTH,HALF_HEIGHT)
    level = setLevel(player,DormRoom)
    level.shift_world(130,-75)

    clock = pygame.time.Clock()
    done = False
    displayDescription = False
    descriptionIndex = 0

    level.startMusic()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            elif event.type == pygame.KEYDOWN:
                if not displayDescription:
                    if event.key == pygame.K_LEFT:
                        player.changespeed(-3,0)
                        player.moving = True
                    elif event.key == pygame.K_RIGHT:
                        player.changespeed(3,0)
                        player.moving = True
                    elif event.key == pygame.K_UP:
                        player.changespeed(0,-3)
                        player.moving = True
                    elif event.key == pygame.K_DOWN:
                        player.changespeed(0,3)
                        player.moving = True
                    
                if event.key == pygame.K_a:
                    hitObject = getFacing(player)
                    if hitObject:
                        player.change_y = 0
                        player.change_x = 0
                        if hitObject.enemy:
                            description = hitObject.enemy.descriptionOptions[hitObject.enemy.status]
                            # hit enemy
                        else:
                            description = hitObject.description
                    else:
                        description = None
                    if displayDescription and description:
                        if descriptionIndex == len(description) - 1:
                            displayDescription = False
                            descriptionIndex = 0
                            if hitObject.fight:
                                hitObject.enemy.status = fightModule.fight(screen,player,hitObject.enemy)                                
                                if hitObject.enemy.status == 3:
                                    hitObject.fight = False
                                elif hitObject.enemy.status == 2:
                                   level = dead(player)
                                level.startMusic()
                                
                        else:
                            descriptionIndex += 1
                    elif description:
                        displayDescription= True
                
                    
            elif event.type == pygame.KEYUP:
                if not displayDescription:
                    if event.key == pygame.K_LEFT:
                        player.change_x = 0
                    elif event.key == pygame.K_RIGHT:
                        player.change_x = 0
                    elif event.key == pygame.K_UP:
                        player.change_y = 0
                    elif event.key == pygame.K_DOWN:
                        player.change_y = 0
                    elif event.key == pygame.K_a:
                        player.change_y = 0
                        player.change_x = 0
                
                
        keys = pygame.key.get_pressed()
        if (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]) and \
            (not keys[pygame.K_UP]) and (not keys[pygame.K_DOWN]):
                player.moving = False

        player.update()
        screen.fill(BLACK)

        if player.rect.right > (HALF_WIDTH + CAMERASLACK):
            diff = player.rect.right - (HALF_WIDTH + CAMERASLACK)
            shift = level.world_shift_x - diff
            if (shift > -(level.x_limit-SCREENWIDTH)):
                player.rect.right = HALF_WIDTH + CAMERASLACK
                level.shift_world(-diff,0)

        if player.rect.left < HALF_WIDTH - CAMERASLACK:
            diff = (HALF_WIDTH - CAMERASLACK) - player.rect.left
            shift = level.world_shift_x + diff
            if (shift < 0):
                player.rect.left = (HALF_WIDTH - CAMERASLACK)
                level.shift_world(diff,0)

        if player.rect.bottom > (HALF_HEIGHT + CAMERASLACK):
            diff = player.rect.bottom - (HALF_HEIGHT + CAMERASLACK)
            shift = level.world_shift_y - diff
            if (shift > -(level.y_limit - SCREENHEIGHT)):
                player.rect.bottom = (HALF_HEIGHT + CAMERASLACK)
                level.shift_world(0,-diff)

        if player.rect.top < (HALF_HEIGHT - CAMERASLACK):
            diff = (HALF_HEIGHT - CAMERASLACK) - player.rect.top
            shift = level.world_shift_y + diff
            if (shift < 0):
                player.rect.top = (HALF_HEIGHT - CAMERASLACK)
                level.shift_world(0,diff)


        obj_hit_list = pygame.sprite.spritecollide(player, level.background_list, False, callback)
        remaining = level.background_list.copy()
        remaining.remove(obj_hit_list)
        for obj in remaining:
            obj.image = obj.image1
        for obj in obj_hit_list:
            if obj.image == obj.image1:
                rand = random.randint(0,5)
                # this number generation will be used to spawn
                # random enemies, but it's disabled until those
                # graphics are created
                if rand == 6:
                    status = fightModule.fight(screen,player,obj.generateEnemy())
                    player.change_x = 0
                    player.change_y = 0
                    if status == 2:
                        level = dead(player)
                    level.startMusic()

            obj.image = obj.image2

        zone_hit_list = pygame.sprite.spritecollide(player, level.transport_list, False)
        if zone_hit_list:
            player.rect.x = HALF_WIDTH
            player.rect.y = HALF_HEIGHT
            (player.change_x,player.change_y) = (0,0)
            player.direction = zone_hit_list[0].playerDir
            level = zone_hit_list[0].transport(player)
            

        playerFoot = player.rect.bottom
        level.draw(screen)
        level.background_list.draw(screen)
        level.drawBackLayers(screen,playerFoot)
        player.draw(screen)
        level.drawFrontLayers(screen,playerFoot)


        if displayDescription and description:
            drawDescription(screen,description,descriptionIndex)
        
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
