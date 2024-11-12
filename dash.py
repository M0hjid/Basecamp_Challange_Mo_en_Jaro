import pygame

pygame.init()

# Scherminstellingen
width = 1000
height = 800
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Simulated Player Movement (Camera Scrolling)")

fps = 60
timer = pygame.time.Clock()

BLUE = (0, 0, 255)

# Spelerinstellingen
player_width = 50
player_height = 50
player_x = width // 2 - player_width // 2
player_y = height // 2 - player_height // 2

# Zwaartekrachtinstellingen
gravity = 1
player_velocity_y = 0
jump_strength = -20
ground_y = 525

# Achtergrondinstellingen
bg = pygame.image.load('Achtergrond_Klad.jpg')
achtergrond = pygame.transform.scale(bg, (width, height))

# Wereldinstellingen
world_x = 0
world_speed = 10

# Sprintinstellingen
sprint_speed = 15
sprint_duration = 3
sprint_cooldown = 60
is_sprinting = False
sprint_timer = 0
sprint_cooldown_timer = 5


run = True
while run:
    timer.tick(fps)

    # Achtergrond tekenen (eindeloos scrollend)
    screen.blit(achtergrond, (world_x % width - width, 0))
    screen.blit(achtergrond, (world_x % width, 0))
    screen.blit(achtergrond, (world_x % width + width, 0))

    # Gebeurtenissen verwerken
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Zwaartekracht toepassen
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Speler op de grond houden
    if player_y >= ground_y:
        player_y = ground_y
        player_velocity_y = 0

    # Invoer verwerken
    keys = pygame.key.get_pressed()

    # Springen
    if keys[pygame.K_SPACE] and player_y == ground_y:
        player_velocity_y = jump_strength

    # Beweging naar rechts
    if keys[pygame.K_d]:
        world_x -= world_speed

    # Beweging naar links
    if keys[pygame.K_a]:
        world_x += world_speed

    # Sprinten
    if keys[pygame.K_LSHIFT] and sprint_cooldown_timer == 0:
        is_sprinting = True
        world_speed = sprint_speed
        sprint_timer = sprint_duration


    if is_sprinting:
        sprint_timer -= 1
        if sprint_timer <= 0:
            is_sprinting = False
            world_speed = 10
            sprint_cooldown_timer = sprint_cooldown


    if sprint_cooldown_timer > 0:
        sprint_cooldown_timer -= 1


    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))


    pygame.display.flip()

pygame.quit()
