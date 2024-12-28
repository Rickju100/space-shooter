"""Importing the necessary libraries"""
#Import
import pygame
import random
from os.path import join as jn

"""Setting up the game"""
pygame.init()
windowWidth, windowHeight = 1280,720
displaySurface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Shooting Stars")
run = True

"""Surface"""
surface = pygame.Surface((windowWidth, windowHeight))
surface.fill("Orange")
x = 100

"""Importing Images"""
#Player
playerSurface = pygame.image.load(jn("images","player.png")).convert_alpha()    
playerRectange = playerSurface.get_rect(center = (windowWidth//2, windowHeight//2))
playerDirection = pygame.math.Vector2()#By default 0,0
playerSpeed = 300

#Star
starSurface = pygame.image.load(jn("images","star.png")).convert_alpha()
starPosition = [random.randint(0, windowWidth), random.randint(0, windowHeight)]

#meteor
meteorSurface = pygame.image.load(jn("images","meteor.png")).convert_alpha()
meteorRectangle = meteorSurface.get_rect(center = (windowWidth//2, windowHeight//2))

#Laser
laserSurface = pygame.image.load(jn("images","laser.png")).convert_alpha()
laserRectangle = laserSurface.get_rect(bottomleft = (20, windowHeight-20))

""""Main Code"""
while run:
    dt = clock.tick()/1000
    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #Player imputs
    keys = pygame.key.get_pressed()
    playerDirection.x = 0


    displaySurface.fill("Black")
    for pos in starPosition:
        displaySurface.blit(starSurface, pos)

    #Display onto the surface
    displaySurface.blit(meteorSurface, meteorRectangle)
    displaySurface.blit(playerSurface, playerRectange)
    displaySurface.blit(laserSurface, laserRectangle)
    displaySurface.blit(playerSurface, playerRectange)

    pygame.display.update()