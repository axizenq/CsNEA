import pygame  
import sys  
from main import *

pygame.init()  

smallfont = pygame.font.SysFont('Corbel',35)  
text = smallfont.render('quit' , True , WHITE)  

while True:  
    for ev in pygame.event.get():  
        if ev.type == pygame.QUIT:  
            pygame.quit()  
            
        #checks if a mouse is clicked  
        if ev.type == pygame.MOUSEBUTTONDOWN:  
            
            if SCREEN_WIDTH/2 <= mouse[0] <= SCREEN_WIDTH/2+140 and SCREEN_HEIGHT/2 <= mouse[1] <= SCREEN_HEIGHT/2+40:
                pygame.quit()  
        
    # fills the screen with a color  
    BUFFER.fill((60,25,60))  

    # stores the (x,y) coordinates into  
    # the variable as a tuple  
    mouse = pygame.mouse.get_pos()  
    
    # if mouse is hovered on a button it  
    # changes to lighter shade  
    if SCREEN_WIDTH/2 <= mouse[0] <= SCREEN_WIDTH/2+140 and SCREEN_HEIGHT/2 <= mouse[1] <= SCREEN_HEIGHT/2+40:  
        pygame.draw.rect(BUFFER,color_light, [SCREEN_WIDTH/2,SCREEN_HEIGHT/2,140,40])  
        
    else:  
        pygame.draw.rect(BUFFER,color_dark, [SCREEN_WIDTH/2,SCREEN_HEIGHT/2,140,40])  

    BUFFER.blit(text (SCREEN_WIDTH/2+50,SCREEN_HEIGHT/2))  
    
    pygame.display.update()  