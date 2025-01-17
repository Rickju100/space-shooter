"""Importing the necessary libraries"""
#Import
import pygame
from random import randint as rd, uniform as uni
from os.path import join as jn

"""Clases"""
class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load(jn("images","player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (windowWidth/2, windowHeight/2))
        self.direction = pygame.Vector2()
        self.speed = 300

        #Cooldown   
        self.cooldown = True
        self.laserCooldownTime = 0
        self.cooldownDuration = 2000

        #Mask
        self.mask = pygame.mask.from_surface(self.image)

    def laserTimer (self):
        if not self.cooldown:
            currrentTime = pygame.time.get_ticks()
            if currrentTime - self.laserCooldownTime >= self.cooldownDuration:
                self.cooldown = True   

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recentKey = pygame.key.get_just_pressed()
        if recentKey [pygame.K_SPACE] and self.cooldown:
            Laser(laserSurface,self.rect.midtop,(allSprites,laserSprites))
            self.cooldown = False
            self.laserCooldownTime = pygame.time.get_ticks()
            laserSound.play()

        self.laserTimer()

  
    
class Star(pygame.sprite.Sprite):
    def __init__(self,groups,starPic):
        super().__init__(groups)
        self.image = starPic
        self.rect = self.image.get_frect(center = (rd(0, windowWidth), rd(0, windowHeight)))

class Laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0: 
            self.kill()

class Meteor(pygame.sprite.Sprite):



    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.originalSurface = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.startTimer = pygame.time.get_ticks()
        self.lifeTime = 3000
        self.direction = pygame.math.Vector2(uni(-0.5,0.5),1).normalize()
        self.speed = rd(400,500)
        self.mask = pygame.mask.from_surface(self.image)
        self.rotationSpeed = rd(60,100)
        self.rotationAngle = 0

    def update(self,dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.startTimer >= self.lifeTime:
            self.kill()
        self.rotationAngle += self.rotationSpeed * dt
        self.image = pygame.transform.rotozoom(self.originalSurface,self.rotationAngle,1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.framesIndex = 0
        self.image = self.frames[self.framesIndex]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.framesIndex += 10 * dt
        if self.framesIndex < len(self.frames):
            self.image = self.frames[int(self.framesIndex)]
        else:
            self.kill()
#functions
def collisions():
    global run
    spirteCollisions = pygame.sprite.spritecollide(player,meteorSprites,True,pygame.sprite.collide_mask) #To review collision
    if spirteCollisions:
        run = False

    for laser in laserSprites:
        collidedSprites = pygame.sprite.spritecollide(laser,meteorSprites,True)

        if collidedSprites:
            laser.kill()
            for sprite in collidedSprites:
                sprite.kill()
                AnimatedExplosion(frames,laser.rect.midtop,allSprites)
                explosionSound.play()

def updateScore():
    time = pygame.time.get_ticks() // 100
    textSurface = font.render(f"{time}", True, "#3240a8")
    textRectangle = textSurface.get_frect(midbottom = (windowWidth//2,windowHeight-50))
    displaySurface.blit(textSurface,textRectangle)
    pygame.draw.rect(displaySurface,"#3240a8",textRectangle.inflate(10,10).move(0,-8),5,10)

"""Setting up the game"""
pygame.init()
windowWidth, windowHeight = 1280,720 
displaySurface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Shooting Stars")
run = True
clock = pygame.time.Clock()


"""Importing Images"""
#Star
starPic = pygame.image.load(jn("images","star.png")).convert_alpha()
#meteor
meteorSurface = pygame.image.load(jn("images","meteor.png")).convert_alpha()
#Laser
laserSurface = pygame.image.load(jn("images","laser.png")).convert_alpha()
#font
font = pygame.font.Font(jn("images","Oxanium-Bold.ttf"), 35)
#Explosion
frames = [pygame.image.load(jn("images","explosion",f"{i}.png")).convert_alpha() for i in range(21)]
#Sounds
laserSound = pygame.mixer.Sound(jn("audio","laser.wav"))
laserSound.set_volume(0.5)
explosionSound = pygame.mixer.Sound(jn("audio","explosion.wav"))
explosionSound.set_volume(0.5)
damagenSound = pygame.mixer.Sound(jn("audio","damage.ogg"))
damagenSound.set_volume(0.5)
gameMusic = pygame.mixer.Sound(jn("audio","game_music.wav"))
gameMusic.set_volume(0.3)
gameMusic.play(-1)

"""Sprite groups"""
allSprites = pygame.sprite.Group()
meteorSprites = pygame.sprite.Group()
laserSprites = pygame.sprite.Group()

"""Objects"""
starPic = pygame.image.load(jn("images","star.png")).convert_alpha()
for i in range(20):
    Star(allSprites,starPic)
    
player = Player(allSprites)


""""Main Code"""

#Custom events
#Meteor event
meteorEvent= pygame.event.custom_type()
pygame.time.set_timer(meteorEvent, 500)


try:
    while run:
        dt = clock.tick()/1000
        #Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == meteorEvent:
                x,y = rd(0,windowWidth),rd(-200,-100)
                Meteor(meteorSurface,(x,y), (allSprites,meteorSprites))
        
        #Game Updates
        allSprites.update(dt)
        collisions()
        #Drawing the game
        displaySurface.fill("Black")
        updateScore()
        allSprites.draw(displaySurface)
        
        

        pygame.display.update()

    pygame.quit()
except Exception as e:
    print(f"An error has ocurred! /n the erros is: {e}")