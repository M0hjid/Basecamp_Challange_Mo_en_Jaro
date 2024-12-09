import pygame
from pygame.locals import *
import csv
# import pil # type: ignore


pygame.init() # start pygame op


# zet het scherm op##################################
scherm_x = 1220
scherm_y = scherm_x * 9 // 16
scherm = pygame.display.set_mode((scherm_x, scherm_y))
#####################################################

clock = pygame.time.Clock() # voor FPS en de timers


# om het level op te delen in grids##################
ROWS = 14
COLS = 500
TILE_SIZE = scherm_y // ROWS
TILE_TYPES = 21
#####################################################

# alle variablen die met de speler te maken hebben###
jump_strength = -10
JUMP_TIMER = 0.07
#####################################################

# alle variablen die met de wereld te maken hebben###
gravity = 0.4
huidig_level = 1
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


class Achtergrond():
    def __init__(self, x, y):
        img = pygame.image.load('Challange/Achtergrond_test.png')
        self.image = pygame.transform.scale(img, (scherm_x, scherm_y))
        self.image_r = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = x - achtergrond_scroll * 0.5
        self.rect.y = y

    def update(self):
        global achtergrond_scroll
        scherm.blit(self.image, (-achtergrond_scroll * 0.2, 0))
        scherm.blit(self.image_r, (scherm_x - achtergrond_scroll * 0.2, 0))
        scherm.blit(self.image_r, (-scherm_x - achtergrond_scroll * 0.2, 0))
        if self.rect.x == scherm_x:
            achtergrond_scroll = 0
        if self.rect.x == -scherm_x:
            achtergrond_scroll = 0


bg = Achtergrond(0,0)


class Player:

    def __init__(self, x, y):
        self.dx = 0
        self.dy = 0
        img = pygame.image.load('Challange/Player.png')
        self.breedte = 0.7 * TILE_SIZE
        self.hoogte = 1.4 * TILE_SIZE
        self.image = pygame.transform.scale(img, (self.breedte, self.hoogte))
        self.rect = self.image.get_rect() # dit maakt een recht hoek om de player heen en deze wordt gebruikt voor physics
        self.rect.x = x # x en y zijn de begin positie van de speler maar de x en y zelf doen niks daarom gaat het naar de rect
        self.rect.y = y # ^^^
        self.in_de_lucht = True # geeft aan dat de speler in de lucht begint
        self.jump_timer = 0  # Coyote timer start op 0
        self.wall_jump__muur_R = False
        self.wall_jump__muur_L = False
        self.kan_bewegen_L = True
        self.kan_bewegen_R = True

        # voor de sprint
        self.is_sprinting = False
        self.sprint_timer = 0
        self.sprint_cooldown_timer = 5
        self.snelheid_speler = 5
        # voor de wall jump
        self.wall_jump_sprong_timer = 150


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
            self.kan_bewegen_L = True
            self.wall_jump__muur_R = False
            self.jump_timer = 0
            self.dy = jump_strength
            if self.wall_jump_sprong_timer > 0:
                self.wall_jump__muur_R = False
                # self.dx = 1 * self.snelheid_speler

        if toetsen[pygame.K_SPACE] and self.wall_jump__muur_L:
            self.in_de_lucht = True
            self.kan_bewegen_R = True
            self.wall_jump__muur_L = False
            self.jump_timer = 0
            self.dy = jump_strength
            if self.wall_jump_sprong_timer > 0:
                self.wall_jump__muur_L = False
                # self.dx = 1 * self.snelheid_speler

        if self.wall_jump_sprong_timer > 0:
            self.wall_jump_sprong_timer -= 1
            if self.wall_jump_sprong_timer == 0:
                self.wall_jump__muur_L = True
                self.wall_jump__muur_R = True
                self.wall_jump_sprong_timer = 150

        if self.rect.x > scherm_x - SCROLL_LIM:
            if self.dx > 0:
                scherm_scroll += self.dx
                for pos, tile in enumerate(blokken.obstakels):
                    toekomstige_rect = self.rect.copy()
                    toekomstige_rect.x += self.dx  # Simuleer nieuwe x-positie
                    toekomstige_rect.y += self.dy
                    if toekomstige_rect.colliderect(tile[1]):
                        return None
                    if pos == len(blokken.obstakels) - 1:
                        blokken.beweeg_alles(scherm_scroll)
                        self.dx -= self.dx
                return scherm_scroll

        if self.rect.x < SCROLL_LIM:
            if self.dx < 0:
                scherm_scroll += self.dx
                for pos, tile in enumerate(blokken.obstakels):
                    toekomstige_rect = self.rect.copy()
                    toekomstige_rect.x += self.dx  # Simuleer nieuwe x-positie
                    toekomstige_rect.y += self.dy
                    if toekomstige_rect.colliderect(tile[1]):
                        return None
                    if pos == len(blokken.obstakels) - 1:
                        blokken.beweeg_alles(scherm_scroll)
                        self.dx -= self.dx
                return scherm_scroll

    def kan_springen(self):
        # Speler kan springen als hij op de grond is of als er nog coyote time is
        return not self.in_de_lucht or self.jump_timer > 0

    def update(self):
        global scherm_scroll

        # Beweging X
        self.rect.x += self.dx

        # check voor wanneer er helemaal geen collisions zijn
        for tile_data in wereld.obstacle_list:
            if not tile_data[1].colliderect(self.rect):
                self.in_de_lucht = True
                self.wall_jump__muur_R = False
                self.wall_jump__muur_L = False

        # Controleer botsingen op de X-as
        for tile_data in blokken.obstakels:
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

                if scherm_scroll is not None:
                    scherm_scroll = 0


        # Zwaartekracht toepassen en beweging Y
        self.dy += gravity
        self.rect.y += self.dy
        self.in_de_lucht = True
        # Controleer botsingen op de Y-as
        for tile_data in blokken.obstakels:
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
        blokken.teken_obstakels()


class Blocks_met_Collision():
    def __init__(self, obstakels: list):
        self.obstakels = obstakels

    def beweeg_alles(self, dx):
        for tile_data in self.obstakels:
            tile_data[1].x -= int(dx/2)

    def teken_obstakels(self):
        for tile_data in self.obstakels:
            scherm.blit(tile_data[0], tile_data[1])
            #pygame.draw.rect(scherm, (255, 255, 255), (tile_data[1].x, tile_data[1].y, TILE_SIZE, TILE_SIZE), 1)


wereld = Wereld()
player = wereld.process_data(wereld_data)
blokken = Blocks_met_Collision(wereld.obstacle_list)

if huidig_level != 2:
    clock.tick(60) # FPS
    scherm.fill((0, 0, 0)) # zorgt ervoor dat het scherm voor elke frame opnieuw wordt opgevuld
    bg.update()
    wereld.teken_obstakels()
    player.update()



    cam_pos = 7000
    print(cam_pos)

    blokken.beweeg_alles(cam_pos)
    pygame.display.update()


run = True
while run:
    clock.tick(60) # FPS
    scherm.fill((0, 0, 0)) # zorgt ervoor dat het scherm voor elke frame opnieuw wordt opgevuld
    bg.update()
    wereld.teken_obstakels()
    player.update()

    # print(player.rect.x)
    # print(player.rect.y)

    try:
        if player.movement() is not None:
            achtergrond_scroll += player.movement() * 0.3
        else:
            scherm_scroll = 0
    except TypeError:
        pass

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
