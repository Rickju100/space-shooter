"""Importing the necessary libraries"""
#Import
import pygame
from random import randint as rd
from os.path import join as jn

"""Clases"""
class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load(jn("images","player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (windowWidth/2, windowHeight/2))
        self.direction = pygame.math.Vector2()
        self.speed = 300


    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recentKey = pygame.key.get_just_pressed()
        if recentKey [pygame.K_SPACE]:
            print("Space")

class Star(pygame.sprite.Sprite):
    def __init__(self,groups,starPic):
        super().__init__(groups)
        self.image = starPic
        self.rect = self.image.get_frect(center = (rd(0, windowWidth), rd(0, windowHeight)))

"""Setting up the game"""
pygame.init()
windowWidth, windowHeight = 1280,720
displaySurface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Shooting Stars")
run = True
clock = pygame.time.Clock()

"""Surface"""
surface = pygame.Surface((100, 200))
surface.fill("Orange")
x = 100

"""Sprite groups"""
allSprites = pygame.sprite.Group()

"""Objects"""
starPic = pygame.image.load(jn("images","star.png")).convert_alpha()
for i in range(20):
    Star(allSprites,starPic)
player = Player(allSprites)

"""Importing Images"""

#meteor
meteorSurface = pygame.image.load(jn("images","meteor.png")).convert_alpha()
meteorRectangle = meteorSurface.get_frect(center = (windowWidth//2, windowHeight//2))

#Laser
laserSurface = pygame.image.load(jn("images","laser.png")).convert_alpha()
laserRectangle = laserSurface.get_frect(bottomleft = (20, windowHeight-20))

""""Main Code"""
while run:
    dt = clock.tick()/1000
    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    
    allSprites.update(dt)

 

    #Drawing the game
    displaySurface.fill("Black")
    allSprites.draw(displaySurface)

    pygame.display.update()

pygame.quit()