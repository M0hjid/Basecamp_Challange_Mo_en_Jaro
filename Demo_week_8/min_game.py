import pygame
from pygame.locals import *
import csv


pygame.init() # start pygame op


# zet het scherm op##################################
scherm_x = 1220
scherm_y = scherm_x * 9 // 16
scherm = pygame.display.set_mode((scherm_x, scherm_y))
#####################################################

clock = pygame.time.Clock() # voor FPS en de timers


# om het level op te delen in grids##################
ROWS = 14
COLS = 150
TILE_SIZE = scherm_y // ROWS
TILE_TYPES = 21
#####################################################

# alle variablen die met de speler te maken hebben###
jump_strength = -10
JUMP_TIMER = 0.07
#####################################################

# alle variablen die met de wereld te maken hebben###
gravity = 0.4
huidig_level = 0
#####################################################

# variabelen voor het scrollen#######################
SCROLL_LIM = TILE_SIZE * 6
scherm_scroll = 0
achtergrond_scroll = 0
#####################################################

# variablen voor de sprint###########################
sprint_speed = 8
sprint_duration = 3
sprint_cooldown = 60
#####################################################


# bewaar de tiles in een lijst#######################
img_lijst = []
for t in range(TILE_TYPES):
    img = pygame.image.load(f'Challange/{t}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_lijst.append(img)
#####################################################

# bouwt de wereld op#################################
#Maak lege tile lijst
wereld_data = []
for row in range(ROWS):
    r = [-1] * COLS
    wereld_data.append(r)

#vul de lijst
with open(f'Challange/Level_{huidig_level}_data.csv', newline= '') as csvfile:
    reader = csv.reader(csvfile, delimiter= ',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            wereld_data[x][y] = int(tile)
#####################################################


class Player:

    def __init__(self, x, y):
        self.dx = 0
        self.dy = 0
        img = pygame.image.load('Challange/Player.png')
        self.breedte = TILE_SIZE
        self.hoogte = 2 * TILE_SIZE
        self.image = pygame.transform.scale(img, (self.breedte, self.hoogte))
        self.rect = self.image.get_rect() # dit maakt een recht hoek om de player heen en deze wordt gebruikt voor physics
        self.rect.x = x # x en y zijn de begin positie van de speler maar de x en y zelf doen niks daarom gaat het naar de rect
        self.rect.y = y # ^^^
        self.in_de_lucht = True # geeft aan dat de speler in de lucht begint
        self.jump_timer = 0  # Coyote timer start op 0
        self.wall_jump__muur_R = False
        self.wall_jump__muur_L = False
        # voor de sprint
        self.is_sprinting = False
        self.sprint_timer = 0
        self.sprint_cooldown_timer = 5
        self.snelheid_speler = 5


    def movement(self):
        scherm_scroll = 0

        toetsen = pygame.key.get_pressed()
        if toetsen[pygame.K_d]:
            self.dx = self.snelheid_speler  # Beweeg speler naar rechts
        elif toetsen[pygame.K_a]:
            self.dx = -self.snelheid_speler  # Beweeg speler naar links
        else:
            self.dx = 0  # Stop beweging als er geen toetsen worden ingedrukt

        if toetsen[pygame.K_LSHIFT] and self.sprint_cooldown_timer == 0:
            self.is_sprinting = True
            self.snelheid_speler = sprint_speed
            self.sprint_timer = sprint_duration

        if self.is_sprinting:
                self.sprint_timer -= 1
                if self.sprint_timer <= 0:
                    self.is_sprinting = False
                    self.snelheid_speler = 5
                    self.sprint_cooldown_timer = sprint_cooldown

        if self.sprint_cooldown_timer > 0:
            self.sprint_cooldown_timer -= 1

        # Springen
        if toetsen[pygame.K_SPACE] and self.kan_springen():
            self.dy = jump_strength
            self.in_de_lucht = True
            self.jump_timer = 0
            self.wall_jump__muur_R = False
            self.wall_jump__muur_L = False

        if toetsen[pygame.K_SPACE] and self.wall_jump__muur_R:
            self.in_de_lucht = True
            self.wall_jump__muur_R = False
            self.jump_timer = 0
            self.dy = jump_strength 
        if toetsen[pygame.K_SPACE] and self.wall_jump__muur_L:
            self.in_de_lucht = True
            self.wall_jump__muur_L = False
            self.jump_timer = 0
            self.dy = jump_strength


        if self.rect.x > scherm_x - SCROLL_LIM:
            if self.dx > 0:
                scherm_scroll += self.dx
                self.dx -= self.dx
                return scherm_scroll
        
        if self.rect.x < SCROLL_LIM:
            if self.dx < 0:
                scherm_scroll += self.dx
                self.dx -= self.dx
                return scherm_scroll

    def kan_springen(self):
        # Speler kan springen als hij op de grond is of als er nog coyote time is
        return not self.in_de_lucht or self.jump_timer > 0

    def update(self):

        # Beweging X
        self.rect.x += self.dx

        # check voor wanneer er helemaal geen collisions zijn
        for tile_data in wereld.obstacle_list:
            if not tile_data[1].colliderect(self.rect):
                self.in_de_lucht = True
                self.wall_jump__muur_R = False
                self.wall_jump__muur_L = False


        # Controleer botsingen op de X-as
        for tile_data in wereld.obstacle_list:
            if tile_data[1].colliderect(self.rect):
                if self.dx > 0:  # Beweegt naar rechts
                    self.rect.right = tile_data[1].left
                    if self.in_de_lucht:
                        self.wall_jump__muur_R = True
                        self.wall_jump__muur_L = False

                elif self.dx < 0:  # Beweegt naar links
                    self.rect.left = tile_data[1].right
                    if self.in_de_lucht:
                        self.wall_jump__muur_L = True
                        self.wall_jump__muur_R = False


        # Zwaartekracht toepassen en beweging Y
        self.dy += gravity
        self.rect.y += self.dy
        self.in_de_lucht = True
        # Controleer botsingen op de Y-as
        for tile_data in wereld.obstacle_list:
            if tile_data[1].colliderect(self.rect):
                if self.dy > 0:  # Beweegt naar beneden en staat op de grond(valt)
                    self.rect.bottom = tile_data[1].top
                    self.dy = 0
                    self.in_de_lucht = False  # Speler staat op de grond
                    self.jump_timer = JUMP_TIMER
                    self.wall_jump__muur_R = False
                    self.wall_jump__muur_L = False
                elif self.dy < 0:  # Beweegt naar boven en stoopt zijn hoofd (springt)
                    self.rect.top = tile_data[1].bottom
                    self.dy = 0


        # Als de speler in de lucht is, verlaag de jump_timer
        if self.in_de_lucht and self.jump_timer > 0:
            self.jump_timer -= clock.get_time() / 1000.0  # Verminder tijd met milliseconden die zijn gepasseerd

        # Toon speler (gebeurt op het einde zodat eerst alles dat aangepast wordt ook wordt getoont)
        scherm.blit(self.image, self.rect)
        pygame.draw.rect(scherm, (255, 255, 255), self.rect, 2)
        if self.rect.y < (-1/2 * TILE_SIZE):
            pygame.draw.rect(scherm,(200, 0, 0), (self.rect.x, 20, TILE_SIZE, 10), width=0)


class Wereld():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        #ga door elke waarde in de csvfile
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_lijst[tile] 
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:  # LET OP: hier moeten alle blokken vallen die collision krijgen
                        self.obstacle_list.append(tile_data)
                    elif tile > 8 and tile < 11:  # LET OP: hier komen alle blokken dat water zijn
                        pass
                    elif tile >= 11 and tile <= 14:  # decoraties
                        pass
                    elif tile == 15:  # dit gaat de tile van de speler worden
                        player = Player(x * TILE_SIZE, (y - 1) * TILE_SIZE)
                        player.x_player = player.rect.x
                        player.y_player = player.rect.y
        return player

    def teken_obstakels(self):
        for tile_data in self.obstacle_list:
            if scherm_scroll is not None:
                tile_data[1].x -= scherm_scroll
                scherm.blit(tile_data[0], tile_data[1])
            else:
                scherm.blit(tile_data[0], tile_data[1])
            #pygame.draw.rect(scherm, (255, 255, 255), (tile_data[1].x, tile_data[1].y, TILE_SIZE, TILE_SIZE), 1)


wereld = Wereld()
player = wereld.process_data(wereld_data)

run = True
while run:
    clock.tick(60) # FPS
    scherm.fill((0,20,200)) # zorgt ervoor dat het scherm voor elke frame opnieuw wordt opgevuld

    player.movement()
    wereld.teken_obstakels()
    player.update()

    if player.movement() is not None:
        scherm_scroll = player.movement()
    else:
        scherm_scroll = 0


    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()