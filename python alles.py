import pygame

pygame.init()

width = 1000
height = 800
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Simulated Player Movement (Camera Scrolling)")

fps = 60
timer = pygame.time.Clock()

BLUE = (0, 0, 255)
#game variabelen
bg = pygame.image.load('Achtergrond_Klad.jpg')
achtergrond = pygame.transform.scale(bg, (width, height))
achtergrond_rechts = pygame.transform.scale(bg, (width, height))
achtergrond_links = pygame.transform.scale(bg, (width, height))

wall_thickness = 1

#character creation

player_width = 50
player_height = 50
player_x = width // 2 - player_width // 2
player_y = height // 2 - player_height // 2

#world set
world_x = 0
world_x_rechts = width
world_x_links = -width
world_speed = 10

#gravety set
gravity = 1
player_velocity_y = 0
jump_strength = -20
ground_y = height - player_height

def draw_wall():
    left = pygame.draw.line(screen,'white', (0, 0),(0, height), wall_thickness)
    right = pygame.draw.line(screen,'white', (width, 0),(width, height),wall_thickness)
    top = pygame.draw.line(screen,'white',(0, 0), (width,0), wall_thickness)
    #bottom = pygame.draw.line(screen,(47, 85, 31), (0, ground_y),(width, ground_y),wall_thickness)
    wall_list = [left, right,top]
    return wall_list

ground_y = 525
player_y = ground_y

#main looop

run = True
while run:
    timer.tick(fps)

    screen.blit(achtergrond, (world_x, 0))
    screen.blit(achtergrond_rechts, (world_x_rechts, 0))
    screen.blit(achtergrond_links, (world_x_links, 0))

    
    draw_wall()

    for event in pygame.event.get():
        if event.type == pygame.quit:
            run = False
            
    player_velocity_y += gravity
    player_y += player_velocity_y #update speler met gewicht
    
    keys = pygame.key.get_pressed()
    
    if player_y >= ground_y:
        player_y = ground_y 
        player_velocity_y = 0
    if keys[pygame.K_SPACE] and player_y == ground_y:
            player_velocity_y = jump_strength

    
    if keys[pygame.K_d]:  # Move right (move the world to the left)
        world_x -= world_speed
        world_x_rechts -= world_speed
        world_x_links -= world_speed
    if world_x >= width:
        world_x = 0
        world_x_rechts = width
        world_x_links = -width
        
    if keys[pygame.K_a]:  # Move left (move the world to the right)
        world_x += world_speed
        world_x_rechts += world_speed
        world_x_links += world_speed
        
    if world_x <= -width:
        world_x = 0
        world_x_rechts = width
        world_x_links = -width
            
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    pygame.display.flip()
    
pygame.quit()
