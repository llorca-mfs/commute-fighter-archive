import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.display.set_caption("Overpass")

WINDOW_SIZE = [256, 224]
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

bg = pygame.image.load("512_bg.bmp").convert()
harang = pygame.image.load("harang_half.bmp").convert()
floor = pygame.image.load("gradient_blue.bmp").convert()
harang.set_colorkey((0,255,0))

mirror_harang = pygame.transform.flip(harang, True, False)

R_scroll = False
L_scroll = False

camera_ctr = 0

music = pygame.mixer.music.load("ovpass_loop.wav")
pygame.mixer.music.play(-1)

def dispBabala(xPos): #203
    kalat = pygame.image.load("kalat.bmp").convert()
    sakayan = pygame.image.load("sakayan.bmp").convert()

    screen.blit(kalat, (xPos+75, 154))
    screen.blit(sakayan, (xPos+587, 154))

def dispLine(xPos):
    pygame.draw.line(screen,(0,0,0), (xPos+128,192),((xPos*2)+128,240)) # next line that will be drawn
    pygame.draw.line(screen,(255,255,255), (xPos+127,192),(((xPos*2)+128)-1,240))

    pygame.draw.line(screen,(0,0,0), (xPos,192), (xPos-(128-xPos),240)) # current line being drawn
    pygame.draw.line(screen,(255,255,255), (xPos-1,192), ((xPos-(128-xPos))-1,240))


while True:
    bg_coord_x = camera_ctr - 128
    harang_coord_x = bg_coord_x * 2

    screen.blit(bg,(bg_coord_x,0))

    xRel_harang = harang_coord_x % (harang.get_rect().width*2)
    screen.blit(floor,(0,189))

    screen.blit(mirror_harang,(xRel_harang - harang.get_rect().width,150))
    screen.blit(harang,(xRel_harang - (harang.get_rect().width*2),150))

    dispLine(xRel_harang)

    if xRel_harang < (WINDOW_SIZE[0]-harang.get_rect().width):
        for i in range(0,4):
            if i%2 == 0:
                screen.blit(harang, (xRel_harang+(harang.get_rect().width*i), 150))
            else:
                screen.blit(mirror_harang, (xRel_harang+(harang.get_rect().width*i), 150))

    dispBabala(harang_coord_x)

    if R_scroll == True and bg_coord_x != -256:
        camera_ctr -= 4
    elif L_scroll == True and bg_coord_x != 0:
        camera_ctr += 4

    #print("camera_ctr: {0}, bg_coord_x: {1}, harang_coord_x: {2}, xRel_harang: {3}".format(camera_ctr, bg_coord_x, harang_coord_x, xRel_harang))

    for event in pygame.event.get():
        if event.type == QUIT: # user closes the window
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                R_scroll = True
            elif event.key == K_LEFT:
                L_scroll = True
        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                R_scroll = False
            elif event.key == K_LEFT:
                L_scroll = False
    pygame.display.update()
    clock.tick(30)
