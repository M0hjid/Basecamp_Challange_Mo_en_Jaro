import pygame


class Knop():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def teken(self, surface):
        actie = False
        
        #muis positie
        pos = pygame.mouse.get_pos()
        
        #check for hover
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                actie = True
                self.clicked = True
            
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
            self.clicked = False
        
        surface.blit(self.image, self.rect.topleft)
        
        
        return actie