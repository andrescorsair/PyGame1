import pygame
pygame.init()
#Größe des Spiel Displays 500x480
win = pygame.display.set_mode((500, 480))
#Name des Spiel "Displays"
pygame.display.set_caption("First Game")
#Bilder für lauf Animationen (jeweils 9 Stück+ "Standbild)
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg') #Hintergrunfbild
char = pygame.image.load('standing.png') #Charakter Steht (Bild)

clock = pygame.time.Clock() #Framerate clock ?
#Sounds (die während dem Spiel getriggert werden
bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')


#musik (läuft die ganze zeit im hintegrund)
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1) #lässt musik als loop laufen
score = 0
#definition des "Spielers"
class player(object):
    def __init__(self, x, y, width, height): #argumente bekommen self.
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5 #geschwindigkeit des spielcharakters ?
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # definiert Hitbox bereich um den charakter


    def draw(self,win): #laufanimation ?
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):#charakter läuft links oder rechts
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255,0,0), self.hitbox,2) #hitbox für charakter

    def hit(self): #charakter wird getroffen
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('- 5 Points', 1, (255, 0, 0)) # in rot : -5 punkte wenn getroffen
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 300: #wartezeit nach treffer (3ms?)
            pygame.time.delay(10) #hängt mit wartezeit zusammen
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()



class projectile(object): #projktile die charakter verschießt
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius) #projektile als runder schwarzer kreis


class enemy(object): #feindlicher charakter wird definiert (gleich wie vorher)
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3 #geschwindigkeit des feindl. char.
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10 #feindl. char. hat 10 lebenspunkte
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount +1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            # pygame.draw.rect(win,  (255,0,0), self.hitbox, 2) #hitbox an/aus



    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')#in der console wird "hit" gedruckt bei jedem treffer



def redrawGameWindow(): #objekte die im spielfenster dargestellt werden
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0,0,0)) #punkteanzeige
    win.blit(text, (350, 10))
    Andres.draw(win) #charakter
    goblin.draw(win) #feindl. char.
    for bullet in bullets:
        bullet.draw(win) #projektile


    pygame.display.update()

#mainloop #schleife die dauerhaft im hintegrund läuft
font = pygame.font.SysFont('comicsans', 30, True)
Andres = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27) #framerate (27)

    if goblin.visible == True:
        if Andres.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and Andres.hitbox[1] + Andres.hitbox[3] > goblin.hitbox[1]:
            if Andres.hitbox[0] + Andres.hitbox[2] > goblin.hitbox[0] and Andres.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                Andres.hit()
                score -= 5 #wenn vom goblin getroffen -5 punkte

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                hitSound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet)) #projektile verschwinden wenn sie goblin treffen

    keys = pygame.key.get_pressed() #festelegung der steuerrung

    if keys[pygame.K_SPACE] and shootLoop == 0: #leertaste verschießt projektile
        bulletSound.play( )
        if Andres.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5: #es können nur 5 projektile auf einmal auf dem display sein
            bullets.append(projectile(round(Andres.x + Andres.width//2),
            round(Andres.y + Andres.height//2), 6, (0,0,0), facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and Andres.x > Andres.vel: #links laufen
        Andres.x -= Andres.vel
        Andres.left = True
        Andres.right = False
        Andres.standing = False
    elif keys[pygame.K_RIGHT] and Andres.x < 500 - Andres.width - Andres.vel: #rechts laufen
        Andres.x += Andres.vel
        Andres.right = True
        Andres.left = False
        Andres.standing = False

    else:
        Andres.standing = True
        Andres.walkCount = 0

    if not(Andres.isJump): #springen
        if keys[pygame.K_UP]:
            Andres.isJump = True
            Andres.right = False
            Andres.left = False
            Andres.walkCount = 0
    else:
        if Andres.jumpCount >= -10: #fall animation ?
            neg = 1
            if Andres.jumpCount < 0:
                neg = -1
            Andres.y -= (Andres.jumpCount ** 2) * 0.5 * neg
            Andres.jumpCount -= 1
        else:
            Andres.isJump = False
            Andres.jumpCount = 10

    redrawGameWindow()



pygame.quit()
