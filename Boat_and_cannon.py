
import pygame, sys
import numpy as np
from pygame.math import Vector2
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

# bullets group
bullets = pygame.sprite.Group()

# gravity
g = 9.8

#factor conversão graus em radianos
GTR = 0.0174533

# Define the Cannon object by extending pygame.sprite.Sprite
class Cannon(pygame.sprite.Sprite):
    def __init__(self):
        super(Cannon, self).__init__()
        self.surf: pygame.Surface = pygame.image.load("cannon.png").convert_alpha()
        self.rect: pygame.Rect = self.surf.get_rect()      
        self.position = Vector2(50,200)
        self.rect.center = (50,200)
        self.shoot_timer = None
        self.angle = 0
        self.shoot_time_interval = 1000

    def update(self, pressed_keys): 

        # timer to avoid shooting continuosly
        if self.shoot_timer is not None:
            if pygame.time.get_ticks()-self.shoot_timer > self.shoot_time_interval:
                self.shoot_timer = None

        if pressed_keys[K_SPACE] and self.shoot_timer == None:
            self.shoot_timer = pygame.time.get_ticks()
            new_bullet = Bullet(self.position + Vector2(50,-50).rotate(self.angle), 50,45 - self.angle)
            bullets.add(new_bullet)

        if pressed_keys[K_LEFT]:
            self.rotateLeft()

        if pressed_keys[K_RIGHT]:
            self.rotateRight()

    def rotateLeft(self):
        if ((self.position + Vector2(50,-50).rotate(self.angle)).x>self.position.x) and ((self.position + Vector2(50,-50).rotate(self.angle)).y>self.position.y-90):
            self.angle = self.angle - 5
            if self.angle>360:
                self.angle=0
            if self.angle<0:
                self.angle=360     
            self.rotateSprite()

    def rotateRight(self):
        if ((self.position + Vector2(50,-50).rotate(self.angle)).y<self.position.y):
            self.angle = self.angle + 5
            if self.angle>360:
                self.angle=0
            if self.angle<0:
                self.angle=360
            self.rotateSprite()
           
    # Function to rotate an image based on example in https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
    def rotateSprite(self):
        image_rect = self.rect

        offset_center_to_pivot = self.position - image_rect.center
    
        # rotated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(self.angle)

        # rotated image center
        rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)

        # get a rotated image
        self.surf = pygame.image.load("cannon.png").convert_alpha()
        self.surf = pygame.transform.rotate(self.surf, -self.angle)
        self.rect  = self.surf.get_rect(center = rotated_image_center)

# Define the Bullet object by extending pygame.sprite.Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position:Vector2, velocity, angle):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load("bullet.png").convert_alpha()
        self.angle = angle
        self.rect = self.surf.get_rect() 
        self.position = position
        self.initial_pos_x = position.x
        self.initial_pos_y = position.y
        self.velocity = velocity
        self.timeLimit = 4 #seconds
        self.rect.center = position
        self.self_timer = pygame.time.get_ticks()
        self.time = 0 #in miliseconds
        self.shield = False
    
    # Move Bullet 
    def update(self):
        self.time = (pygame.time.get_ticks() - self.self_timer)/500

        self.position.x = self.initial_pos_x + self.velocity * self.time * math.cos(self.angle * GTR)
        self.position.y = self.initial_pos_y - self.velocity * self.time * math.sin(self.angle * GTR) + 0.5 * g * self.time**2
        self.rect.center = self.position

        if self.position.x>SCREEN_WIDTH:
            self.kill()

        if self.position.y>SCREEN_HEIGHT:
            self.kill()
       

# Define the Boat object by extending pygame.sprite.Sprite
class Boat(pygame.sprite.Sprite):
    def __init__(self, size):
        super(Boat, self).__init__()
        self.size = size
        self.reset()

    def reset(self):      
        self.surf = pygame.image.load("boat"+str(self.size)+".png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf , (self.surf.get_rect().width*0.20, self.surf.get_rect().height*0.20))
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

#cannon creation
cannon = Cannon()

# boats creation
for i in range(1,5):
    new_boat = Boat(random.randint(1,5))
    dead_boats.add(new_boat)

bg = pygame.image.load("bg1.png")
cannon_base = pygame.image.load("cannon_base.png")

running = True
boats_count = 0

mouse_pos = pygame.mouse.get_pos()

cannon_power = 0
power = 0

while running: 
    cannon_power = cannon_power + power
    if cannon_power>100:
        cannon_power = 100

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                power = 0.2
                
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if cannon.shoot_timer == None:
                    cannon.shoot_timer = pygame.time.get_ticks()
                    new_bullet = Bullet(cannon.position + Vector2(50,-50).rotate(cannon.angle), 40+cannon_power,45 - cannon.angle)
                    bullets.add(new_bullet)
                    power = 0
                    cannon_power = 0
              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

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

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    if mouse_pos[0] < pygame.mouse.get_pos()[0]:
        cannon.rotateRight()

    if mouse_pos[0] > pygame.mouse.get_pos()[0]:
        cannon.rotateLeft()

    mouse_pos = pygame.mouse.get_pos()

    # Update the position of boats 
    boats.update()

    #update cannon
    cannon.update(pressed_keys)

     # Update the position of bullets 
    bullets.update()


    # check if boat as entered danger zone
    for eachBoat in boats:
        if eachBoat.rect.left < DangerZone_X:
            eachBoat.size=random.randint(1,5)
            eachBoat.reset()
            eachBoat.wait_to_move()
            destroyedBoatCounter = destroyedBoatCounter + 1
            # falta afetar a vida do player aqui!!!!!!

    # check if any bullet have collided with any boat
    for eachBoat in boats:
        collider_bullet = pygame.sprite.spritecollideany(eachBoat,bullets)
        if collider_bullet:
            collider_bullet.kill()
            eachBoat.size=random.randint(1,5)
            eachBoat.reset()
            eachBoat.wait_to_move()
            destroyedBoatCounter = destroyedBoatCounter + 1
            # falta afetar os pontos aqui!!!!!!

    #upgrade boats velocity each 10 destroyed boats
    if destroyedBoatCounter == 10:
        destroyedBoatCounter = 0
        boatsVelocity = boatsVelocity * 1.5

    # Fill the screen with a background
    screen.blit(bg, bg.get_rect())

    # Draw all sprites
    for entity in bullets:
        screen.blit(entity.surf, entity.rect)

    for entity in boats:
        screen.blit(entity.surf, entity.rect)

    screen.blit(cannon.surf, cannon.rect)

    screen.blit(cannon_base, (cannon.position.x-40,cannon.position.y+1))

    pygame.display.update()
    fpsClock.tick(FPS)