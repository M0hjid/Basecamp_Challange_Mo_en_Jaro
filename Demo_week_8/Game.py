import pygame
from pygame.locals import *
import csv


pygame.init()

#zet het scherm op

scherm_x = 1220
scherm_y = scherm_x * 9 // 16
scherm = pygame.display.set_mode((scherm_x, scherm_y))

clock = pygame.time.Clock()#voor het fps

snelheid = 5 #bewegings snelheid


scroll_links = False
scroll_rechts = False
scroll = 0
scroll_snelheid = 1


huidig_level = 0
ROWS = 14
COLS = 150
TILE_SIZE = scherm_y // ROWS
TILE_TYPES = 21
gravity = 0.4
jump_strength = -10

SCROLL_TRESH = TILE_SIZE * 4
scherm_scroll = 0
achtergrond_scroll = 0


ground_y = scherm_y // 3

JUMP_TIMER = 0.07




#bewaar de tiles in een lijst
img_lijst = []
for t in range(TILE_TYPES):
    img = pygame.image.load(f'Challange/{t}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_lijst.append(img)


#achtergrond in laden
class Achtergrond:

    #de setup
        def __init__(self, x, y):
            img = pygame.image.load('Challange/Achtergrond_Klad.jpg')
            self.image = pygame.transform.scale(img, (scherm_x, scherm_y))
            self.rect = self.image.get_rect()
            self.rect.x = x - scroll * 0.5
            self.rect.y = y

    #functie dat gebruikt moet worden om te updaten   
        def update(self, scroll):
        # Toon achtergrond op scherm, scoll op basis van scroll
            for x in range(10):  # Laat de achtergrond 10 keer herhalen in de breedte
                scherm.blit(self.image, ((x * scherm_x) - scroll * 0.5, 0))


achtergrond = Achtergrond(0 - scroll ,0)




class Player:

    def __init__(self, x, y):
        self.dx = 0
        self.dy = 0
        img = pygame.image.load('Challange/Player.png')
        flip_img = pygame.transform.flip(img, True, False)
        self.breedte = TILE_SIZE
        self.hoogte = 2 * TILE_SIZE
        self.image = pygame.transform.scale(flip_img, (self.breedte, self.hoogte))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.in_de_lucht = True
        self.op_de_grond = False
        self.jump_timer = 0  # Coyote timer start op 0
        self.wall_jump_horizontaal_rechter_muur = False
        self.wall_jump_horizontaal_linker_muur = False
        

    def movement(self):
        toetsen = pygame.key.get_pressed()
        if toetsen[pygame.K_d]:
            self.dx = snelheid  # Beweeg speler naar rechts
        elif toetsen[pygame.K_a]:
           self.dx = -snelheid  # Beweeg speler naar links
        else:
            self.dx = 0  # Stop beweging als er geen toetsen worden ingedrukt
        
        # Springen
        if toetsen[pygame.K_SPACE] and self.kan_springen():
            self.dy = jump_strength
            self.in_de_lucht = True
            self.jump_timer = 0  # Reset de coyote timer

    def kan_springen(self):
        # Speler kan springen als hij op de grond is of als er nog coyote time is
        return not self.in_de_lucht or self.jump_timer > 0

    def update(self):
        
        toetsen = pygame.key.get_pressed()

        # Beweging X
        self.rect.x += self.dx
        
        # Controleer botsingen op de X-as
        for tile_data in wereld.obstacle_list:
            if tile_data[1].colliderect(self.rect):
                if self.dx > 0:  # Beweegt naar rechts
                    self.rect.right = tile_data[1].left
                        
                elif self.dx < 0:  # Beweegt naar links
                    self.rect.left = tile_data[1].right
                    

        # Zwaartekracht toepassen en beweging Y
        self.dy += gravity
        self.rect.y += self.dy

        # Controleer botsingen op de Y-as
        for tile_data in wereld.obstacle_list:
            if tile_data[1].colliderect(self.rect):
                if self.dy > 0:  # Beweegt naar beneden en staat op de grond(valt)
                    self.rect.bottom = tile_data[1].top
                    self.dy = 0
                    self.in_de_lucht = False  # Speler staat op de grond
                    self.op_de_grond = True  # Speler is op de grond
                    self.jump_timer = JUMP_TIMER  # Reset de coyote timer als de speler op de grond is
                elif self.dy < 0:  # Beweegt naar boven en stoopt zijn hoofd (springt)
                    self.rect.top = tile_data[1].bottom
                    self.dy = 0
        
        # Als de speler in de lucht is, verlaag de jump_timer
        if self.in_de_lucht and self.jump_timer > 0:
            self.jump_timer -= clock.get_time() / 1000.0  # Verminder tijd met milliseconden die zijn gepasseerd

        # Toon speler
        scherm.blit(self.image, self.rect)
        pygame.draw.rect(scherm, (255, 255, 255), self.rect, 2)
        if self.rect.y < (-1/2 * TILE_SIZE):
            pygame.draw.rect(scherm,(200, 0, 0), (self.rect.x, 20, TILE_SIZE, 10), width=0)

        

class Wereld():
    def __init__(self):
        self.obstacle_list = []
        self.scroll_wereld = 0
        
    
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
            scherm.blit(tile_data[0], tile_data[1])
            #pygame.draw.rect(scherm, (255, 255, 255), (tile_data[1].x, tile_data[1].y, TILE_SIZE, TILE_SIZE), 1)
    
    def scroll_de_wereld(self):
        for tile_data in self.obstacle_list:
            # Pas de positie van elke obstacle aan met scroll
            tile_data[1].x -= self.scroll_wereld


                    
                    
def teken_grid():
    #verticale lijnen
    for c in range(COLS + 1):
        pygame.draw.line(scherm, (0,0,0), (TILE_SIZE * c - scroll , 0), (TILE_SIZE * c - scroll , scherm_y))
    #horizontale
    for c in range(ROWS + 1):
        pygame.draw.line(scherm, (0,0,0), (0 , TILE_SIZE * c), (scherm_x, TILE_SIZE * c))                    
                        



      
        
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

wereld = Wereld()
player = wereld.process_data(wereld_data)    
    



''' Main Loop '''
run = True
while run:
    clock.tick(60)
    scherm.fill('black')
    
    
    # Update achtergrond met scroll
    achtergrond.update(scroll)
    
    player.movement()
    
    # Teken obstakels
    wereld.scroll_de_wereld()
    wereld.teken_obstakels()
    
    #teken_grid()
    
    # Update spelerpositie
    player.update()
    
    

    # Scroll logica
    if scroll_links and scroll > 0:
        scroll -= 5 * scroll_snelheid
        wereld.scroll_wereld -= 0.2
    if scroll_rechts:
        scroll += 5 * scroll_snelheid
        wereld.scroll_wereld += 0.2

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Toetsen indrukken
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                scroll_links = True

            if event.key == pygame.K_d:
                scroll_rechts = True

        # Toetsen loslaten
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                scroll_links = False
                
            if event.key == pygame.K_d:
                player.dx = 0
                scroll_rechts = False

    

    wereld.scroll_wereld = 0

    pygame.display.update()

pygame.quit()