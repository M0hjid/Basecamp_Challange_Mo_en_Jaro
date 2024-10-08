import pygame
import knop

pygame.init()

klok = pygame.time.Clock()
FPS = 60


scherm_breedte = 800
scherm_hoogte = scherm_breedte * 9 // 16


scherm = pygame.display.set_mode((scherm_breedte, scherm_hoogte ))
pygame.display.set_caption('Knop Demo')

img = pygame.image.load('Challange/Player.png')
shrek = pygame.transform.scale(img, (100, 150))

shrek_knop = knop.Knop(400, 300, shrek)

        

run = True
while run:
    klok.tick(FPS)
    
    scherm.fill((65, 232, 143))
    if shrek_knop.teken(scherm) == True:
        print('DE KNOP WERKT')
    
    
    for event in pygame.event.get():
        
        #check of het programma wordt gesloten
        if event.type == pygame.QUIT:
            run = False
    
    
    
    pygame.display.update()
        
pygame.quit()