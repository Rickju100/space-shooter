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
            Laser(laserSurface,self.rect.midtop,allSprites)
            self.cooldown = False
            self.laserCooldownTime = pygame.time.get_ticks()

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

    def update(self,dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0: 
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.startTimer = pygame.time.get_ticks()
        self.lifeTime = 3000
        self.direction = pygame.math.Vector2(uni(-0.5,0.5),1).normalize()
        self.speed = rd(400,500)

    def update(self,dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.startTimer >= self.lifeTime:
            self.kill()



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

"""Sprite groups"""
allSprites = pygame.sprite.Group()

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
                Meteor(meteorSurface,(x,y), allSprites)
        
        allSprites.update(dt)

    

        #Drawing the game
        displaySurface.fill("Black")
        allSprites.draw(displaySurface)
        
        #Collitions
        print(player.rect.collidepoint(100,200))

        pygame.display.update()

    pygame.quit()
except Exception as e:
    print(f"An error has ocurred! /n the erros is: {e}")