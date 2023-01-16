import pygame, random, math
from pygame import Vector2, K_LEFT, K_RIGHT, K_SPACE


displayx, displayy = 1000, 380

boatsVelocity = -1
destroyedBoatCounter = 0

def ThereAreNoBoatsInStartArea(boats, displayx):
    ret = True
    for eachBoat in boats:
        if eachBoat.rect.right>displayx and eachBoat.Time==None:
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

        if self.position.x>displayx:
            self.kill()

        if self.position.y>displayy:
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
        self.loc_x = displayx + 100
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
    def check_time(self):
        if self.Time is not None:
            if pygame.time.get_ticks()-self.Time > self.waitTime and ThereAreNoBoatsInStartArea(boats, pygame.display):
                self.velocity  = boatsVelocity
                self.Time = None

    
