import pygame, sys, time
from auxiliary_functions import *

def PygameInit():
    global screen, titlefont, bodyfont, displayx, displayy, fpsClock, FPS

    pygame.init()
    pygame.font.init()
    
    fpsClock=pygame.time.Clock()
    FPS = 30 
    displayx, displayy = 1920, 1080
    screen = pygame.display.set_mode((displayx, displayy))
    titlefont = pygame.font.SysFont('Comic Sans MS', 30)
    bodyfont = pygame.font.SysFont('Comic Sans MS', 15)

def StartScreen():

    #defines button rectangles
    start_button = pygame.Rect(displayx/2 -100, displayy/2 -25, 200, 50)
    exit_button = pygame.Rect(displayx/2 - 100, displayy/2 +50, 200, 50)
    

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

        screen.blit(titlefont.render("Heavy Ordenance", False, 'white'), (displayx/2 - 124, 100))
        screen.blit(bodyfont.render("Start", False, 'white'), (start_button[0] +75, start_button[1] +15))
        screen.blit(bodyfont.render("Exit", False, 'white'), (exit_button[0] +75, exit_button[1] +15))
        
        if checkmousestate(start_button, screen, pygame) == True:
            start = False
        elif checkmousestate(exit_button, screen, pygame) == True:
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        fpsClock.tick(FPS)


def GameScreen():

    game = True
    while game == True:
        for event in pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            sys.exit()
        
        #add input check
        #add update sprites
        #add render static elements
        #add render sprites

        pygame.display.flip()
        fpsClock.tick(FPS)

def EndScreen():
    
    end_time = time.time()
    end = True
    while end == True:

        for event in pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            sys.exit()

        #renders GameOver on screen
        screen.blit(titlefont.render("Game Over", True, 'White'), (displayx/2 -100, displayy/2 -25))

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
        with open('Leaderboard.txt', 'r+') as fread: #opens leaderboard.txt in read and write mode:
            leaderboardtext = fread.readlines()
            line_num = 0 #initalizes a line counter to keep track of current line
            for line in leaderboardtext: #checks each line for a score
                saved_score = line[4] + line[5] + line[6] + line[7] #temporarily saves the read score
                if int(saved_score) < Score: #checks is saved score is smaller than current score

                    initials = "" 
                    while len(initials) < 3:
                        
                        screen.fill('black')
                        
                        pygame.draw.rect(screen, 'white', (displayx/2 -152, 48, 304, 504))
                        pygame.draw.rect(screen, 'black', (displayx/2 -150, 50, 300, 500))
                        screen.blit(bodyfont.render("Insert your 3 initials", False, 'white'), (displayx/2 - 75, displayy/2 - 25))
                        screen.blit(bodyfont.render(f"Initials : {initials}", False, 'white'), (displayx/2 - 25, displayy/2))
                        
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
    
    start_time = time.time()

    Leader_board_Render = True            
    while Leader_board_Render == True:
        
        for event in pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            sys.exit()

        pygame.draw.rect(screen, 'white', (displayx/2 -152, 48, 304, 504))
        pygame.draw.rect(screen, 'black', (displayx/2 -150, 50, 300, 500))
        screen.blit(titlefont.render("Top 10", False, 'white'), (displayx/2 -25, 75))

        with open('Leaderboard.txt', 'r+') as fread: 
            n = 0  #Increments for every line in leaderboard.txt, rendering every line one above another
            for line in fread:
                n += 1
                screen.blit(bodyfont.render(line.replace('\n',""), False, 'white'), (displayx/2 -35, 150 + 25 * n))
        
        if (time.time() - start_time) > 6:
            Leader_board_Render = False


        pygame.display.update()
        fpsClock.tick(FPS)