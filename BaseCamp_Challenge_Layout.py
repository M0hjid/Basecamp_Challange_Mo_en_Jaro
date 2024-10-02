import pygame

scherm_x = 600
scherm_y = 300

achtergrond = pygame.image.load('Achtergrond_Klad.jpg')

scherm = pygame.display.set_mode((scherm_x, scherm_y))

clock = pygame.time.Clock()

x = 0
y = 0

breedte_pop = 40
hoogte_pop = 60

snelheid = 5

max_scherm_x = scherm_x - breedte_pop - snelheid
max_scherm_y = scherm_y - hoogte_pop - snelheid


def update_scherm():
    scherm.fill('black')
    scherm.blit(achtergrond, (x,y))
    pygame.draw.rect(scherm, (255, 255, 255), (280, 200, breedte_pop, hoogte_pop))
    pygame.display.update()
    
    

run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    toetsen = pygame.key.get_pressed()

    if toetsen[pygame.K_a]:
        x += snelheid

    if toetsen[pygame.K_d]:
        x -= snelheid
    if toetsen[pygame.K_w]:
        y += snelheid
    if toetsen[pygame.K_s] and y > 0:
        y -= snelheid

    update_scherm()


    
