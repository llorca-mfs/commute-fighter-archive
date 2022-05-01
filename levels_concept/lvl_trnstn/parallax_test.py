import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.display.set_caption("Parallax Test")

WINDOW_SIZE = [256, 224] #snes native resolution

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

wall = pygame.image.load("256_wall.bmp").convert()
fg = pygame.image.load("foreground.bmp").convert()
fg.set_colorkey((0,255,0))

R_scroll = False
L_scroll = False

wall_coord_x = 0
fg_coord_x = -256

def dispAds(xPos):
    hakbang = pygame.image.load("hakbang.bmp").convert()
    happibee = pygame.image.load("ad_happibee.bmp").convert()
    aniqlo = pygame.image.load("ad_aniqlo.bmp").convert()

    screen.blit(happibee, (xPos+368, 96))
    screen.blit(aniqlo, (xPos+232, 96))
    screen.blit(hakbang, (xPos+41, 111))
    screen.blit(happibee, (xPos-104, 96))
    screen.blit(aniqlo, (xPos-240, 96))

def floor(ite):
    floor_array = [pygame.image.load("256_floor/0.bmp"),pygame.image.load("256_floor/1.bmp"),pygame.image.load("256_floor/2.bmp"),pygame.image.load("256_floor/3.bmp"),
                   pygame.image.load("256_floor/4.bmp"),pygame.image.load("256_floor/5.bmp"),pygame.image.load("256_floor/6.bmp"),pygame.image.load("256_floor/7.bmp"),
                   pygame.image.load("256_floor/8.bmp"),pygame.image.load("256_floor/9.bmp"),pygame.image.load("256_floor/10.bmp"),pygame.image.load("256_floor/11.bmp"),
                   pygame.image.load("256_floor/12.bmp"),pygame.image.load("256_floor/13.bmp"),pygame.image.load("256_floor/14.bmp"),pygame.image.load("256_floor/15.bmp")]

    mod = ite % 16
    screen.blit(floor_array[mod], (0, 163))
    
def ceiling(ite):
    ceiling_array = [pygame.image.load("256_ceiling/0.bmp"),pygame.image.load("256_ceiling/1.bmp"),pygame.image.load("256_ceiling/2.bmp"),pygame.image.load("256_ceiling/3.bmp"),
                   pygame.image.load("256_ceiling/4.bmp"),pygame.image.load("256_ceiling/5.bmp"),pygame.image.load("256_ceiling/6.bmp"),pygame.image.load("256_ceiling/7.bmp"),
                   pygame.image.load("256_ceiling/8.bmp"),pygame.image.load("256_ceiling/9.bmp"),pygame.image.load("256_ceiling/10.bmp"),pygame.image.load("256_ceiling/11.bmp"),
                   pygame.image.load("256_ceiling/12.bmp"),pygame.image.load("256_ceiling/13.bmp"),pygame.image.load("256_ceiling/14.bmp"),pygame.image.load("256_ceiling/15.bmp")]

    mod = ite % 16
    screen.blit(ceiling_array[mod], (0, -18))

while True: #game loop, always true

    xRel_wall = wall_coord_x % wall.get_rect().width #relative x of wall
    screen.blit(wall, (xRel_wall - wall.get_rect().width, 75))

    if xRel_wall < WINDOW_SIZE[0]:
        screen.blit(wall, (xRel_wall, 75))
        screen.blit(wall, (xRel_wall + wall.get_rect().width, 75))

    floor(int(wall_coord_x/-4))
    ceiling(int(wall_coord_x/-4))
    #dispAds(wall_coord_x)

    #screen.blit(fg, (fg_coord_x, 36))

    wall_coord_x -= 4
    fg_coord_x -= 8


    #print("x: {0}, rel_x: {1}".format(wall_coord_x, xRel_wall))

    for event in pygame.event.get():
        if event.type == QUIT: # user closes the window
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(15) # game runs 60fps
