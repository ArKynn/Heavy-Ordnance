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