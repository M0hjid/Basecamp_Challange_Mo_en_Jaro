import pygame

pygame.init()

width = 1000
height = 800
screen = pygame.display.set_mode([width, height])

fps = 60
timer = pygame.time.Clock()

BLUE = (0, 0, 255)
#game variabelen

wall_thickness = 10

#character creation

player_width = 50
player_height = 50
player_x = width // 2 - player_width // 2
player_y = height // 2 - player_height // 2

#gravety set
gravity = 0.5
player_velocity_y = 0
jump_strength = -10

ground_y = height - player_height

def draw_wall():
    left = pygame.draw.line(screen,'white', (0, 0),(0, height), wall_thickness)
    right = pygame.draw.line(screen,'white', (width, 0),(width, height),wall_thickness)
    top = pygame.draw.line(screen,'white',(0, 0), (width,0), wall_thickness)
    bottom = pygame.draw.line(screen,'white', (0, height),(width, height),wall_thickness)
    wall_list = [left, right,top, bottom]
    return wall_list


#main looop

run = True
while run:
    timer.tick(fps)
    screen.fill('white')

    wall = draw_wall()

    for event in pygame.event.get():
        if event.type == pygame.quit:
            run = False
            
    player_velocity_y += gravity #meer gewicht zorgt voor een hardere val
    player_y += player_velocity_y #update speler met gewicht

#is de speler op de grond
    if player_y >= ground_y:
        player_y = ground_y
        player_velocity_y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and player_y == ground_y:
            player_velocity_y = jump_strength
        
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    pygame.display.flip()
    
pygame.quit()


            


