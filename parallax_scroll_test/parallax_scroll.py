"""
This file was created prior to taking a proper course in PyGame.
Skills presented here are not indicative of the final product.
This exists merely as a concept.
"""

import pygame

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.display.set_caption("ovpass_test_parallax")

WINDOW_SIZE = [256, 224] #snes native resolution
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

sky = pygame.image.load("ovpass_sprites/sky_seamless.bmp").convert()
traffic = pygame.image.load("ovpass_sprites/640_bg.bmp").convert()
traffic.set_colorkey((0,255,0))

harang = pygame.image.load("ovpass_sprites/harang_half.bmp").convert()
harang.set_colorkey((0,255,0))
mirror_harang = pygame.transform.flip(harang, True, False) #could probably be converted into an object

floor = pygame.image.load("ovpass_sprites/newfloor.bmp").convert()

def main():
    R_scroll = False
    L_scroll = False

    gameRunning = True

    FPS = 30
    camera_ctr = 0

    while gameRunning:
        screen.fill((166,202,240)) #blank, blue sky

        traffic_coord = [camera_ctr, -23] #only assigning y values just in case more comprehensive camera movement will be utilized

        sky_coord = [camera_ctr*0.5, -23]
        xRel_sky = sky_coord[0] % sky.get_rect().width

        harang_coord = [camera_ctr*2, 140]
        xRel_harang = harang_coord[0] % (harang.get_rect().width*2)

        floor_coord = [harang_coord[0]-harang.get_rect().width, 179]
        xRel_floor = floor_coord[0] % floor.get_rect().width

        screen.blit(sky,(xRel_sky-sky.get_rect().width, sky_coord[1])) #blits the second iteration of the sky
        if xRel_sky < WINDOW_SIZE[0]: # if sky being blitted is less than window width
            screen.blit(sky, (xRel_sky,sky_coord[1]))

        screen.blit(traffic,traffic_coord) #for blitting the foreground traffic layer

        screen.blit(floor, (xRel_floor-floor.get_rect().width, floor_coord[1]))

        if xRel_floor < WINDOW_SIZE[0]:
            screen.blit(floor, (xRel_floor, floor_coord[1]))
            screen.blit(floor, (xRel_floor+floor.get_rect().width, floor_coord[1]))


        screen.blit(mirror_harang,(xRel_harang - harang.get_rect().width,harang_coord[1]))
        screen.blit(harang,(xRel_harang - (harang.get_rect().width*2),harang_coord[1]))
        if xRel_harang < (WINDOW_SIZE[0]-harang.get_rect().width):
            for i in range(0,4):
                if i%2 == 0:
                    screen.blit(harang, (xRel_harang+(harang.get_rect().width*i), harang_coord[1]))
                else:
                    screen.blit(mirror_harang, (xRel_harang+(harang.get_rect().width*i), harang_coord[1]))


        if R_scroll == True and camera_ctr != -384:
            camera_ctr -= 4
        elif L_scroll == True and camera_ctr != 0:
            camera_ctr += 4



        for event in pygame.event.get():
            if event.type == pygame.QUIT: # user closes the window
                gameRunning = False
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
        clock.tick(FPS)

if __name__ == '__main__':
    main()
