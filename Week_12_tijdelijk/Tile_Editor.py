import pygame
from Challange import knop
import csv


pygame.init()

klok = pygame.time.Clock()
FPS = 60


scherm_breedte = 800
scherm_hoogte = scherm_breedte * 9 // 16
lagere_stuk = 100
zij_stuk = 300

scherm = pygame.display.set_mode((scherm_breedte + zij_stuk, scherm_hoogte + lagere_stuk))
pygame.display.set_caption('Level Editor')

#def game variabelen
ROWS = 13
MAX_COLS = 150
TILE_SIZE = scherm_hoogte // ROWS

'''LET OP'''
TILE_TYPES = 21  #Ligt aan het aantal Tiles dat wij willen maken 

huidige_tile = 0
huidige_level = 0

scroll_links = False
scroll_rechts = False
scroll = 0
scroll_snelheid = 1

#kleuren
groen = (24, 245, 149)
wit = (240, 240, 240)
rood = (240, 60, 60)
blauw = (45, 231, 237)
zwart = (0,0,0)

font = pygame.font.SysFont('Futura', 30)


#achtergrond laden
bg = pygame.image.load('Challange/Achtergrond_test.png')
achtergrond = pygame.transform.scale(bg, (scherm_breedte, scherm_hoogte))
Rachtergrond = pygame.transform.scale(bg, (scherm_breedte, scherm_hoogte))
Rachtergrond = pygame.transform.flip(Rachtergrond, True, False)
opslaan_plaatje_laden = pygame.image.load('Challange/save_knop.png')
opslaan_plaatje = pygame.transform.scale(opslaan_plaatje_laden, (2 * TILE_SIZE, TILE_SIZE))
laad_plaatje_laden = pygame.image.load('Challange/laad_knop.png')
laad_plaatje = pygame.transform.scale(laad_plaatje_laden, (2 * TILE_SIZE, 2* TILE_SIZE))
#bewaar de tiles in een lijst
tiles_lijst = []
for t in range(TILE_TYPES):
    img = pygame.image.load(f'Challange/{t}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tiles_lijst.append(img)


#lege tile lijst
wereld_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    wereld_data.append(r)
wereld_data.append([0] * MAX_COLS)


#functie voor tekst schrijven
def teken_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    scherm.blit(img, (x,y))
    

#Teken de achtergronden
def teken_bg():
    scherm.fill(groen)
    breedte = achtergrond.get_width()
    for x in range(10):
        if x % 2 == 1:
            scherm.blit(achtergrond, ((x * breedte) -scroll, 0))
        if x % 2 == 0:
            scherm.blit(Rachtergrond, ((x * breedte) -scroll, 0))


#Teken de grid        
def teken_grid():
    #verticale lijnen
    for c in range(MAX_COLS + 1):
        pygame.draw.line(scherm, wit, (TILE_SIZE * c - scroll, 0), (TILE_SIZE * c - scroll, scherm_hoogte))
    #horizontale
    for c in range(ROWS + 1):
        pygame.draw.line(scherm, wit, (0 , TILE_SIZE * c), (scherm_breedte, TILE_SIZE * c))


#Teken de wereld
def teken_wereld():
    for y, row in enumerate(wereld_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                scherm.blit(tiles_lijst[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))
        

#create buttons
#make a button list
knoppen_lijst = []
knop_rij = 0
knop_col = 0
for i in range(len(tiles_lijst)):
    tile_knop = knop.Knop(scherm_breedte + (70 * knop_col + 50), 75 * knop_rij + 50, tiles_lijst[i])
    knoppen_lijst.append(tile_knop)
    knop_col += 1
    if knop_col >= 3:
        knop_col = 0
        knop_rij += 1
opslaan_knop = knop.Knop(500, scherm_hoogte + 50, opslaan_plaatje)
laad_knop = knop.Knop(600, scherm_hoogte + 33, laad_plaatje)
        


#main loop

run = True
while run:
    klok.tick(FPS)
    
    
    
    teken_bg() #Teken de achtergronden
    teken_grid()
    teken_wereld()
    
    teken_text(f'Level: {huidige_level}', font, zwart, 10, scherm_hoogte + 30)
    teken_text('Pijl omhoog/laag om lvl wisselen', font, zwart, 10, scherm_hoogte + 52)
    
    pygame.draw.rect(scherm, groen, (scherm_breedte, 0, zij_stuk, scherm_hoogte + lagere_stuk)) #bedekt een lelijk stukje rechts
    
    
    if opslaan_knop.teken(scherm) == True:
        with open(f'Challange/Level_{huidige_level}_data.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in wereld_data:
                writer.writerow(row)
        print('opgeslagen')
        
    if laad_knop.teken(scherm) == True:
        try:
            with open(f'Challange/Level_{huidige_level}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                wereld_data = []
                for row in reader:
                    wereld_data.append([int(tile) for tile in row])
            print('geladen')
        except FileNotFoundError:
            print(f'Geen Level gevonden')
    
        
        
        
    
    #kies een tile
    knop_nummer = 0
    for knop_nummer, i in enumerate(knoppen_lijst):
        if i.teken(scherm):
            huidige_tile = knop_nummer
    
    #highlight huidige tile
    pygame.draw.rect(scherm, rood, knoppen_lijst[huidige_tile].rect, 5)
    
    #voeg nieuwe tiles toe
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = (pos[1]) // TILE_SIZE
    
    if pos[0] < scherm_breedte and pos[1] < scherm_hoogte:
        if pygame.mouse.get_pressed()[0] == 1:
            if wereld_data[y][x] != huidige_tile:
                wereld_data[y][x] = huidige_tile
                
        if pygame.mouse.get_pressed()[2] == 1:
                wereld_data[y][x] = -1
    
                
    
    
    #scroll de map
    if scroll_links == True and scroll > 0:
        scroll -= 5 * scroll_snelheid
    if scroll_rechts == True:
        scroll += 5 * scroll_snelheid
    
    
    for event in pygame.event.get():
        
        #check of het programma wordt gesloten
        if event.type == pygame.QUIT:
            run = False
        
        #check voor toetsen ingedrukt    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_links = True
            if event.key == pygame.K_RIGHT:
                scroll_rechts = True
            if event.key == pygame.K_LSHIFT:
                scroll_snelheid = 5
            if event.key == pygame.K_UP:
                huidige_level += 1
            if event.key == pygame.K_DOWN:
                huidige_level -= 1
        
        #check voor toetsen losgelaten
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_links = False
            if event.key == pygame.K_RIGHT:
                scroll_rechts = False
            if event.key == pygame.K_LSHIFT:
                scroll_snelheid = 1

            
    pygame.display.update()
        
pygame.quit()