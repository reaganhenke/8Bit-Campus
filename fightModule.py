import pygame, random

WHITE = (255,255,255)
BLACK = (35,35,35)
BLUE = (50,50,255)
GREEN = (0,255,0)
GRAY = (200,200,200)

FPS = 60

PLAYERX = 100
PLAYERY= 250
ENEMYX= 250 
ENEMYY= 100


class GuitarHero():
    def __init__(self,screen):
        HALF_WIDTH = screen.get_width()/2
        lineDist = (HALF_WIDTH / 5)
        yBuff = 30
        self.letters = ["U", "I", "O", "P"]
        self.fills = [WHITE,WHITE,WHITE,WHITE]
        self.xpos = []
        self.highY = 30
        self.lowY = 300
        self.speed = 2
        for i in xrange(1,5):
            self.xpos.append(HALF_WIDTH + lineDist*i)
        self.notes = [(self.xpos[random.randrange(0,4)],self.highY),\
                      (self.xpos[random.randrange(0,4)],self.highY - 30),\
                      (self.xpos[random.randrange(0,4)],self.highY - 60),\
                      (self.xpos[random.randrange(0,4)],self.highY - 90),\
                      (self.xpos[random.randrange(0,4)],self.highY - 120),\
                      (self.xpos[random.randrange(0,4)],self.highY - 150)]

    def update(self):
        complete = False
        for i in xrange(len(self.notes)):
            (x,y) = self.notes[i]
            if y <= self.lowY:
                self.notes[i] = (x,y+self.speed)
                complete = True
        return complete

    def draw(self,screen):
        for i in xrange(4):
            pygame.draw.line(screen, BLACK, (self.xpos[i], self.highY), (self.xpos[i],self.lowY))
            box = pygame.Rect(0,0,30,30)
            box.midtop = (self.xpos[i],self.lowY)
            pygame.draw.rect(screen, self.fills[i], box)
            
            fontObj = pygame.font.SysFont('couriernew', 25)
            textSurfaceObj = fontObj.render(self.letters[i],False,BLACK)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.midtop = (self.xpos[i],self.lowY)
            screen.blit(textSurfaceObj,textRectObj)

        for (x,y) in self.notes:
            if (y <= self.lowY) and (y >= self.highY):
                pygame.draw.circle(screen, BLACK, (x,y), 10)
                

def moveToTarget((x,y),(tx,ty)):
    if (x <= tx) or (y >= ty):
        return (0,0)
    else:
        return (-3,3)


class Notes():
    def __init__(self,(x,y),(targetX,targetY),number):
        self.notes = [((x-5,y),True),((x,y-10),True),((x-20,y-20),True),((x,y-30),True),((x-20,y-40),True) ]
        (self.originx, self.originy) = (x,y)
        for i in xrange(len(self.notes)):
            ((xpos,ypos),status) = self.notes[i]
            self.notes[i] = ((xpos,ypos),((xpos<=x) and (ypos>=y)))
            
        self.target = (targetX,targetY)
        self.damage = number
        self.image = scale(pygame.image.load("note.gif"),3)

    def update(self, player):
        pulse = (pygame.time.get_ticks()//100) % 6
        if pulse > 3:
            pulse = 6 - pulse

        complete = True
        
        for i in xrange(len(self.notes)):
            status = True
            ((x,y),display) = self.notes[i]
            (dx,dy) = moveToTarget((x,y),self.target)
            
            if (dx,dy) != (0,0):
                if not display:
                    if ((x+dx <= self.originx) and (y+dy>=self.originy)):
                        display = True
                    self.notes[i] = ((x, y + dy), display)
                    
            if display:
                if (dx,dy) == (0,0):
                    player.health -= self.damage
                    pygame.mixer.music.load("./music/hit.wav")
                    pygame.mixer.music.play()
                    status = False                
                self.notes[i] = ((x + dx, y + dy + pulse), status)
                if (dx,dy) != (0,0):
                    complete = False

        return complete  
    
    def drawNotes(self,screen):
        for (note,status) in self.notes:
            if status:
                (x,y) = note
                screen.blit(self.image,(x-5,y-25))

def scale(image,factor):
    (width,height) = image.get_size()
    return pygame.transform.scale(image, (int(float(width) * float(factor)),int(float(height) * float(factor))))


def drawDescription(screen,menuItems,(i,j)):
    (SCREENWIDTH,SCREENHEIGHT) = screen.get_size()
    disBufferX = 30
    disHeight = 100
    disBufferY = 10
    disWidth = SCREENWIDTH - (2*disBufferX)
    disY = SCREENHEIGHT - (disBufferY + disHeight)
    displayBackground = pygame.Rect(disBufferX,disY,disWidth,disHeight)
    menubar = pygame.image.load("menuBar.gif")
    screen.blit(menubar,displayBackground)
#    pygame.draw.rect(screen, WHITE, displayBackground)

    textshift = disHeight/4
    textLeft = disBufferX + 100
    textRight = disBufferX +disWidth - 200

    y = disY+textshift
    for row in xrange(0,len(menuItems)):
        x = textLeft
        for col in xrange(0,len(menuItems[row])):
            fontObj = pygame.font.SysFont('couriernew', 25)
            textSurfaceObj = fontObj.render(menuItems[row][col],False,BLACK)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.midleft = (x, y)
            screen.blit(textSurfaceObj,textRectObj)

            if (row,col) == (i,j):
                xbase = x - 15
                pygame.draw.polygon(screen,BLACK,[(xbase,y - 5),\
                                          (xbase + 5,y),\
                                          (xbase,y + 5)])
            x = textRight
        y = disY+(3*textshift)

def loadItems(items):
    menuList = [[],[]]
    itemList = items.keys()
    for i in xrange(4):
        row = i//2
        if i < len(itemList):
            menuList[row].append(itemList[i])
    return menuList    
    
def fight(screen, player, enemy):
    (SCREENWIDTH, SCREENHEIGHT) = screen.get_size()

    HALF_WIDTH = int(SCREENWIDTH / 2)
    HALF_HEIGHT = int(SCREENHEIGHT / 2)
    
    mode = "ActiveMenu"
    menuActions = [["Fight","Run"],["Item"]]
    itemItems = loadItems(player.items)
    (i,j) = (0,0)
    clock = pygame.time.Clock()
    done = False
    enemyNotes = False
    enemyNotesPos = (ENEMYX,ENEMYY)
    fighting = False
    pygame.mixer.music.stop()

    while not done:
        itemItems = loadItems(player.items)
        if mode == "Item":
            menuItems = itemItems
        else:
            menuItems = menuActions

        if mode == "FightInit" :
            fighting = True
            guitarHero = GuitarHero(screen)
            mode = "Fight"

        if mode == "OppTurnInit":
            (dx,dy) = enemy.noteOrigin
            notes = Notes((ENEMYX+dx,ENEMYY+dy),(PLAYERX+dx,PLAYERY+dy),enemy.getAttackDamage())
            enemyNotes = True
            mode = "OppTurn"

        if mode == "ActiveMenu" or mode == "Item" :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    
                elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            if j != 0:
                                pygame.mixer.music.load("./music/Select.wav")
                                pygame.mixer.music.play()
                            j = 0
                        elif event.key == pygame.K_RIGHT:
                            if len(menuItems[i]) > 1:
                                if j != 1:
                                    pygame.mixer.music.load("./music/Select.wav")
                                    pygame.mixer.music.play()
                                j = 1
                        elif event.key == pygame.K_UP:
                            if i != 0:
                                pygame.mixer.music.load("./music/Select.wav")
                                pygame.mixer.music.play()
                            i = 0
                        elif event.key == pygame.K_DOWN:
                            if len(menuItems[1]) > j:
                                if i != 1:
                                    pygame.mixer.music.load("./music/Select.wav")
                                    pygame.mixer.music.play()
                                i = 1
                        elif event.key == pygame.K_b:
                            if mode == "Item":
                                (i,j) = (0,0)
                                mode = "ActiveMenu"
                        elif event.key == pygame.K_RETURN:
                            if mode == "ActiveMenu":
                                if menuItems[i][j] == "Fight":
                                    mode = "FightInit"
                                else:
                                    mode = menuItems[i][j]
                                if mode == "Item":
                                    if len(player.items)==0 :
                                        mode = "ActiveMenu"
                                        print "No items left"
                                        
                                (i,j) = (0,0)
                            elif mode == "Item":
                                heal = player.items.pop(menuItems[i][j])
                                if (player.health + heal) > player.maxHealth:
                                    player.health = player.maxHealth
                                    print "your health was maxed out"
                                else:
                                    player.health += heal
                                    print "you healed " + str(heal) + "points"
                                pygame.mixer.music.load("./music/heal.wav")
                                pygame.mixer.music.play()
                                pygame.time.wait(250)
                                mode = "OppTurnInit"
                                
        if mode == "Fight":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        guitarHero.fills[0] = GRAY
                        for (x,y) in guitarHero.notes:
                            if x == guitarHero.xpos[0] and (y < (guitarHero.lowY+5)) and (y > (guitarHero.lowY-5)):
                                guitarHero.notes.remove((x,y))
                                enemy.health -= 5
                                pygame.mixer.music.load("./music/note0.wav")
                                pygame.mixer.music.play()
                    elif event.key == pygame.K_i:
                        guitarHero.fills[1] = GRAY
                        for (x,y) in guitarHero.notes:
                            if x == guitarHero.xpos[1] and (y < (guitarHero.lowY+5)) and (y > (guitarHero.lowY-5)):
                                guitarHero.notes.remove((x,y))
                                enemy.health -= 5
                                pygame.mixer.music.load("./music/note1.wav")
                                pygame.mixer.music.play()
                    elif event.key == pygame.K_o:
                        guitarHero.fills[2] = GRAY
                        for (x,y) in guitarHero.notes:
                            if x == guitarHero.xpos[2] and (y < (guitarHero.lowY+5)) and (y > (guitarHero.lowY-5)):
                                guitarHero.notes.remove((x,y))
                                enemy.health -= 5
                                pygame.mixer.music.load("./music/note2.wav")
                                pygame.mixer.music.play()
                    elif event.key == pygame.K_p:
                        guitarHero.fills[3] = GRAY
                        for (x,y) in guitarHero.notes:
                            if x == guitarHero.xpos[3] and (y < (guitarHero.lowY+5)) and (y > (guitarHero.lowY-5)):
                                guitarHero.notes.remove((x,y))
                                enemy.health -= 5
                                pygame.mixer.music.load("./music/note3.wav")
                                pygame.mixer.music.play()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_u:
                        guitarHero.fills[0] = WHITE
                    elif event.key == pygame.K_i:
                        guitarHero.fills[1] = WHITE
                    elif event.key == pygame.K_o:
                        guitarHero.fills[2] = WHITE
                    elif event.key == pygame.K_p:
                        guitarHero.fills[3] = WHITE

        pulse = (pygame.time.get_ticks()//100) % 10
        if pulse > 5:
            pulse = 10 - pulse

        screen.fill(BLACK)
        screen.blit(scale(pygame.image.load("fightBackground.gif"),3.02),(0,0))
        drawDescription(screen,menuItems,(i,j))
        screen.blit(player.fightImage,(PLAYERX,PLAYERY-pulse))

        healthRect = pygame.Rect(203,270,125,30)
        fullhearts = scale(pygame.image.load("hearts.gif"),3)
        (heartwidth,heartheight) = fullhearts.get_size()
        cropped = pygame.Surface((heartwidth,heartheight))
        cropped.fill(WHITE)
        newWidth = (float(player.health)/player.maxHealth) * heartwidth
        cropped.blit(fullhearts,(0,0),(0,0,newWidth,heartheight))       
        screen.blit(cropped,healthRect)
        

        screen.blit(enemy.image,(ENEMYX,ENEMYY+pulse))
        
        healthRect = pygame.Rect(56,113,125,30)
        cropped = pygame.Surface((heartwidth,heartheight))
        cropped.fill(WHITE)
        newWidth = (float(enemy.health)/enemy.maxHealth) * heartwidth
        cropped.blit(fullhearts,(0,0),(0,0,newWidth,heartheight))       
        screen.blit(cropped,healthRect)

        

        if enemyNotes == True:
            notes.drawNotes(screen)
            enemyNotes = not notes.update(player)
            if not enemyNotes:
                mode = "ActiveMenu"

        if fighting == True:
            guitarHero.draw(screen)
            fighting = guitarHero.update()
            if not fighting:
                mode = "OppTurnInit"

        if mode == "Run":
            return 1
            done = True

        if player.health <= 0:
            pygame.mixer.music.load("./music/die.wav")
            pygame.mixer.music.play()
            pygame.time.wait(1000)
            return 2
            done = True
            
        elif enemy.health <= 0:
            pygame.mixer.music.load("./music/die.wav")
            pygame.mixer.music.play()
            pygame.time.wait(1000)
            return 3
            done = True

        pygame.display.flip()
        clock.tick(FPS)
