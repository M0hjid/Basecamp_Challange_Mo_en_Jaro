import pygame

scherm = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("Salam")


x = 300
y = 500
widht = 10
height = 70
vel = 5



run = True

while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.quit:
            run = False


    bewegen = pygame.key.get_pressed()

    if bewegen[pygame.K_w]:
        pygame.draw.ellipse(scherm, (0, 0, 0), (x, y, widht, height) )
        y -= 10

    if bewegen[pygame.K_a]:
        pygame.draw.ellipse(scherm, (0, 0, 0), (x, y, widht, height) )
        x -= 10

    if bewegen[pygame.K_s]:
        pygame.draw.ellipse(scherm, (0, 0, 0), (x, y, widht, height) )
        y += 10

    if bewegen[pygame.K_d]:
        pygame.draw.ellipse(scherm, (0, 0, 0), (x, y, widht, height) )
        x += 10

    if x <= 50:
        x = 1229

    if x >= 1230:
        x = 51
        
    if y <= 50:
        y = 669
        
    if y >= 670:
        y = 51
    
    



        

    pygame.draw.ellipse(scherm, (0, 0, 0), (x, y, widht, height) )
    pygame.draw.ellipse(scherm, (93, 148, 80), (x, y, widht, height) )

    pygame.display.update()



    

    

pygame.quit()
