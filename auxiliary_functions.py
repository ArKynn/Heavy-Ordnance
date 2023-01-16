def exitgamecheck(pygame, sys): #If ESC is pressed, shutsdown program
    for event in pygame.event.get(eventtype=pygame.KEYDOWN):
        if event.key==pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

#Checks for mouse position, lights up button in red and checks if mouse is clicked
def checkmousestate(button, display, pygame):
    if button.collidepoint(pygame.mouse.get_pos()):  #Based on answer by skrx on StackOverfow (https://stackoverflow.com/questions/44998943/how-to-check-if-the-mouse-is-clicked-in-a-certain-area-pygame)
        pygame.draw.rect(display, 'red', button, 1)
        for event in pygame.event.get(eventtype=pygame.MOUSEBUTTONDOWN):
            if event.button == 1:
                return True

#Renders a leaderboard with the scores stored in leaderboard.txt
def call_leaderboard(time, pygame, screen, display_x, sys, titlefont, bodyfont, fpsClock, FPS):
    start_time = time.time()

    Leader_board_Render = True            
    while Leader_board_Render == True:
        
        for event in pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            sys.exit()

        pygame.draw.rect(screen, 'white', (display_x/2 -152, 20, 304, 340))
        pygame.draw.rect(screen, 'black', (display_x/2 -150, 22, 300, 336))
        screen.blit(titlefont.render("Top 10", False, 'white'), (display_x/2 -45, 35))

        with open('leaderboard.txt', 'r+') as fread: 
            n = 0  #Increments for every line in leaderboard.txt, rendering every line one above another
            for line in fread:
                n += 1
                screen.blit(bodyfont.render(line.replace('\n',""), False, 'white'), (display_x/2 -35, 75 + 25 * n))
        
        if (time.time() - start_time) > 6:
            Leader_board_Render = False


        pygame.display.update()
        fpsClock.tick(FPS)