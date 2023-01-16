import pygame, sys
from pygame import *
import time
from auxiliary_functions import *
from Boat_and_cannon import *

def PygameInit():
    global screen, titlefont, bodyfont, display_x, display_y, fpsClock, FPS

    pygame.init()
    pygame.font.init()
    
    fpsClock=pygame.time.Clock()
    FPS = 30 

    
    screen = pygame.display.set_mode((display_x, display_y))
    pygame.display.set_caption("Heavy Ordenance")

    titlefont = pygame.font.SysFont('Comic Sans MS', 30)
    bodyfont = pygame.font.SysFont('Comic Sans MS', 15)

def StartScreen():

    #defines button rectangles
    start_button = pygame.Rect(display_x/2 -100, display_y/2 -45, 200, 50)
    leaderboard_button = pygame.Rect(display_x/2 - 100, display_y/2 +30, 200, 50)
    exit_button = pygame.Rect(display_x/2 - 100, display_y/2 +105, 200, 50)
    

    start = True
    while start == True:

        #checks if the event pygame.QUIT exists
        for event in pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            sys.exit()

        #Renders start menu elements
        screen.fill('black')
        
        pygame.draw.rect(screen, 'white', start_button, 1)
        pygame.draw.rect(screen, 'white', exit_button, 1)
        pygame.draw.rect(screen, 'white', leaderboard_button, 1)

        screen.blit(titlefont.render("Heavy Ordenance", False, 'white'), (display_x/2 - 124, 80))
        screen.blit(bodyfont.render("Start", False, 'white'), (start_button[0] +75, start_button[1] +15))
        screen.blit(bodyfont.render("Exit", False, 'white'), (exit_button[0] +75, exit_button[1] +15))
        screen.blit(bodyfont.render("Leaderboard", False, 'white'), (leaderboard_button[0] +45, leaderboard_button[1] +15))
        
        if checkmousestate(start_button, screen, pygame) == True:
            start = False

        elif checkmousestate(leaderboard_button, screen, pygame) == True:
            #This function renders the leaderboard with all the scores
            call_leaderboard(time, pygame, screen, display_x, sys, titlefont, bodyfont, fpsClock, FPS)

        elif checkmousestate(exit_button, screen, pygame) == True:
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        fpsClock.tick(FPS)


def GameScreen():
    global Score

    # Create custom events for adding new entities
    ADDBOAT = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDBOAT, 4000)

    # Create groups to hold sprites
    boats = pygame.sprite.Group()
    dead_boats = pygame.sprite.Group()

    #cannon creation
    cannon = Cannon()
    
    boatsVelocity = -1

    # boats creation
    for i in range(1,5):
        new_boat = Boat(random.randint(1,5), boatsVelocity)
        dead_boats.add(new_boat)

    DangerZone_X = 100

    bg = pygame.image.load("bg1.png")
    cannon_base = pygame.image.load("cannon_base.png")

    boats_count = 0

    mouse_pos = pygame.mouse.get_pos()

    cannon_power = 0
    power = 0

    Hp = 3
    Score = 0

    boatscore = 0
    boatscorelvl = 1
    destroyedBoatCounter = 0
    was_boat_destroyed = 0

    init_hp_img = pygame.image.load('Heart.png')
    hp_img = pygame.transform.scale(init_hp_img, (25, 25))

    gametime = time.time()
 


    game = True
    while game == True: 

        cannon_power = cannon_power + power
        if cannon_power>100:
            cannon_power = 100

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and len(bullets)<2:
                if event.button == 1:
                    power = 1
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if cannon.shoot_timer == None and len(bullets)<2:
                        cannon.shoot_timer = pygame.time.get_ticks()
                        new_bullet = Bullet(cannon.position + Vector2(50,-50).rotate(cannon.angle), 40+cannon_power,45 - cannon.angle)
                        bullets.add(new_bullet)
                        power = 0
                        cannon_power = 0    
                    
                
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Check for KEYDOWN event
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game = False
            

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

        if mouse_pos[0] < pygame.mouse.get_pos()[0] and mouse_pos[0]>display_x/2:
            cannon.rotateRight()

        if mouse_pos[0] > pygame.mouse.get_pos()[0] and mouse_pos[0]<display_x/2:
            cannon.rotateLeft()

        mouse_pos = pygame.mouse.get_pos()

        # Update the position of boats 
        boats.update(boats)

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
                Hp += -1
                if Hp == 0:
                    game = False

        # check if any bullet have collided with any boat
        for eachBoat in boats:
            collider_bullet = pygame.sprite.spritecollideany(eachBoat,bullets)
            if collider_bullet:
                collider_bullet.kill()
                #aumentar pontuação dependendo do tamanho do barco que sofreu a colisão
                #pontuacao = pontuacao + (6 - eachBoat.size)
                was_boat_destroyed = 1
                boatscore = 6 - eachBoat.size
                #"novo" barco aparece parado (escondido na "spawn area") re-feito (com outro tamanho aleatorio) a partir do que sofreu a colisão
                eachBoat.size = random.randint(1,5)
                eachBoat.reset()
                eachBoat.wait_to_move()
                destroyedBoatCounter = destroyedBoatCounter + 1
                


        #upgrade boats velocity and point multiplier each 10 destroyed boats
        if destroyedBoatCounter == 10:
            destroyedBoatCounter = 0
            boatsVelocity = boatsVelocity * 1.5
            boatscorelvl += 1

        #manages the score throughout the game
        current_time = time.time()
        timescore = 0
        if current_time - gametime >= 1:
            gametime = time.time()
            timescore = 1

        if was_boat_destroyed == 1:
            boatscore = boatscore * boatscorelvl

        Score = Score + timescore + boatscore
        timescore, boatscore = 0, 0

        # Fill the screen with a background
        screen.blit(bg, bg.get_rect())

        # Draw all sprites
        for entity in bullets:
            screen.blit(entity.surf, entity.rect)

        for entity in boats:
            screen.blit(entity.surf, entity.rect)

        screen.blit(cannon.surf, cannon.rect)

        screen.blit(cannon_base, (cannon.position.x-40,cannon.position.y+1))

        screen.blit(bodyfont.render(f"Score: {Score}", True, 'Black'), (display_x - 85, 50))

        screen.blit(bodyfont.render(f"ESC: Finish Game", True, "Black"),(15, 20))

        for x in range(1, Hp+1):
            screen.blit(hp_img, (display_x - 25 - 10 * x, 20))
            
        pygame.display.update()
        fpsClock.tick(FPS)

def EndScreen():
    
    end_time = time.time()
    end = True
    while end == True:

        for event in pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            sys.exit()

        #renders GameOver on screen
        screen.blit(titlefont.render("Game Over", True, 'Black'), (display_x/2 -100, display_y/2 -25))

        #gets current time, if 3 seconds since gameover have passed, proceed to leaderboard
        if (time.time() - end_time) > 3:
            end = False
        
        pygame.display.update()
        fpsClock.tick(FPS)
    

"Leaderboard UI"
#Renders a leaderboard, asks for initials if score in top 10
def LeaderboardScreen():
    global Score

    for event in pygame.event.get(eventtype=pygame.QUIT):
        pygame.quit()
        sys.exit()
    
    allkeys = { #needed to input initials for score 
    pygame.K_a : "A",
    pygame.K_b : "B",
    pygame.K_c : "C",
    pygame.K_d : "D",
    pygame.K_e : "E",
    pygame.K_f : "F",
    pygame.K_g : "G",
    pygame.K_h : "H",
    pygame.K_i : "I",
    pygame.K_j : "J",
    pygame.K_k : "K",
    pygame.K_l : "L",
    pygame.K_m : "M",
    pygame.K_n : "N",
    pygame.K_o : "O",
    pygame.K_p : "P",
    pygame.K_q : "Q",
    pygame.K_r : "R",
    pygame.K_s : "S",
    pygame.K_t : "T",
    pygame.K_u : "U",
    pygame.K_v : "V",
    pygame.K_w : "W",
    pygame.K_x : "X",
    pygame.K_y : "Y",
    pygame.K_z : "Z",
}   

    if Score > 0: #if current score is above 0, it starts the leaderboard related operations
        with open('leaderboard.txt', 'r+') as fread: #opens leaderboard.txt in read and write mode:
            leaderboardtext = fread.readlines()
            line_num = 0 #initalizes a line counter to keep track of current line
            for line in leaderboardtext: #checks each line for a score
                saved_score = line[4] + line[5] + line[6] + line[7] #temporarily saves the read score
                if int(saved_score) < Score: #checks is saved score is smaller than current score

                    initials = "" 
                    while len(initials) < 3:
                        
                        screen.fill('black')
                        
                        pygame.draw.rect(screen, 'white', (display_x/2 -152, 20, 304, 340))
                        pygame.draw.rect(screen, 'black', (display_x/2 -150, 22, 300, 336))
                        screen.blit(bodyfont.render("Insert your 3 initials", False, 'white'), (display_x/2 - 75, display_y/2 - 25))
                        screen.blit(bodyfont.render(f"Initials : {initials}", False, 'white'), (display_x/2 - 35, display_y/2))
                        
                        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
                            try:
                                initials = initials + allkeys[event.key] #adds the pressed key to the initials string
                            except KeyError:
                                pass    
                        pygame.display.update()
                        fpsClock.tick(FPS)
                        
                    strscore = str(Score) #converts score to a string
                    while len(strscore) < 4: #checks if score's number of algarisms is smaller than 4 
                        strscore = "0" + strscore #adds 0s so the score gets into a 4 algarism number
                    strscore = strscore + "\n"

                    new_score = f"{initials} {strscore}" #gets initals and score together in a string
                    leaderboardtext.insert(line_num, new_score) #writes initials and score into the current line

                    Score = 0
                    del leaderboardtext[10] #deletes top 11 from leaderboard list

                    with open('Leaderboard.txt', 'w') as fwrite:
                        for line in leaderboardtext:
                            fwrite.write(line)
                    line_num += 1
    
    #This function renders the leaderboard with all the scores
    call_leaderboard(time, pygame, screen, display_x, sys, titlefont, bodyfont, fpsClock, FPS)