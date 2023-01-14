
import pygame, sys
import numpy as np
from pygame.locals import *
import math
import random

from pygame.locals import (
    K_ESCAPE
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 388

boatsVelocity = -1
destroyedBoatCounter = 0

def ThereAreNoBoatsInStartArea():
    ret = True
    for eachBoat in boats:
        if eachBoat.rect.right>SCREEN_WIDTH and eachBoat.Time==None:
            ret = False
            break
    return ret

# Define the Boat object by extending pygame.sprite.Sprite
class Boat(pygame.sprite.Sprite):
    def __init__(self, size):
        super(Boat, self).__init__()
        self.size = size
        self.reset()

    def reset(self):      
        self.surf = pygame.image.load("boat"+str(self.size)+".png").convert_alpha()
        #pygame.transform.scale(self.image1, (50, 50))
        self.surf = pygame.transform.scale(self.surf , (self.surf.get_rect().width*0.20, self.surf.get_rect().height*0.20))
        #self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.loc_x = SCREEN_WIDTH + 100
        self.loc_y = 300
        self.rect = self.surf.get_rect(
            center=(
                (self.loc_x , self.loc_y),
            )
        )
        self.velocity = boatsVelocity
        self.wasHited = False
        self.Time = None
        self.NotDead = True
        self.waitTime = random.randint(0,8000)

    def wait_to_move(self):
        self.velocity = 0
        self.Time = pygame.time.get_ticks()

    def update(self):
        # Move the sprite based on velocity
        if self.NotDead: 
            if self.wasHited:
                pass
            else:
                self.loc_x = self.loc_x + self.velocity
                self.rect = self.surf.get_rect(
                    center=(
                        (self.loc_x , self.loc_y),
                    )
                )
                #self.rect.move_ip(self.velocity, 0)

        if self.Time is not None:
            if pygame.time.get_ticks()-self.Time > self.waitTime and ThereAreNoBoatsInStartArea():
                self.velocity  = boatsVelocity
                self.Time = None


# Initialize pygame
pygame.init()
pygame.display.set_caption("Heavy Ordenance")
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

fpsClock=pygame.time.Clock()
FPS = 30 

DangerZone_X = 100

# Create custom events for adding new entities
ADDBOAT = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBOAT, 4000)

# Create groups to hold sprites

boats = pygame.sprite.Group()
dead_boats = pygame.sprite.Group()

# boats creation
for i in range(1,5):
    new_boat = Boat(random.randint(1,5))
    dead_boats.add(new_boat)


bg = pygame.image.load("bg1.png")


running = True


while running: 
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #keys = pygame.key.get_pressed()
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            
        elif event.type == QUIT:
            running = False

        # Add a new boat?
        elif event.type == ADDBOAT:
            # spawn a new boat
            if len(dead_boats)>0 and boats_count<4:
                boats_count = boats_count + 1
                aboat = random.choice(list(dead_boats))
                boats.add(aboat)
                aboat.size=random.randint(1,5)
                aboat.reset()
                dead_boats.remove(aboat)


    # Update the position of boats 
    boats.update()

    # check if boat as entered danger zone
    for eachBoat in boats:
        if eachBoat.rect.left < DangerZone_X:
            eachBoat.size=random.randint(1,5)
            eachBoat.reset()
            eachBoat.wait_to_move()
            destroyedBoatCounter = destroyedBoatCounter + 1
            # falta afetar a vida do player aqui!!!!!!

    #upgrade boats velocity each 10 destroyed boats
    if destroyedBoatCounter == 10:
        destroyedBoatCounter = 0
        boatsVelocity = boatsVelocity * 1.5

    # Fill the screen with a background
    screen.blit(bg, bg.get_rect())

    # Draw all sprites
 
    for entity in boats:
        screen.blit(entity.surf, entity.rect)

    pygame.display.update()
    fpsClock.tick(FPS)