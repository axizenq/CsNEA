import pygame  
import sys  
from main import *

pygame.init()  

# making text
smallfont = pygame.font.SysFont('Corbel',35)  
text = smallfont.render('quit' , True , WHITE) 

# button text 
play_text = smallfont.render('Play', True, WHITE)
quit_text = smallfont.render('Quit', True, WHITE)


def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # check if mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # check if the play button is clicked
                if SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 <= mouse[1] <= SCREEN_HEIGHT / 2 + 40:
                    return "play"  
                # check if the quit button is clicked
                if SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 + 60 <= mouse[1] <= SCREEN_HEIGHT / 2 + 100:
                    pygame.quit()
                    sys.exit()

        # fill the screen
        BUFFER.fill((60, 25, 60))

        # get mouse position
        mouse = pygame.mouse.get_pos()

        # play button hovered
        if SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 <= mouse[1] <= SCREEN_HEIGHT / 2 + 40:
            pygame.draw.rect(BUFFER, color_light, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 140, 40])
        else:
            pygame.draw.rect(BUFFER, color_dark, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 140, 40])

        # quit button hovered
        if SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 + 60 <= mouse[1] <= SCREEN_HEIGHT / 2 + 100:
            pygame.draw.rect(BUFFER, color_light, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60, 140, 40])
        else:
            pygame.draw.rect(BUFFER, color_dark, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60, 140, 40])

        # render button texts
        BUFFER.blit(play_text, (SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT / 2))
        BUFFER.blit(quit_text, (SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT / 2 + 60))

        pygame.display.update()