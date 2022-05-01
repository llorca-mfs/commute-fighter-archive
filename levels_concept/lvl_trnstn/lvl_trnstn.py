import pygame
from PIL import Image

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.display.set_caption("Train Station")

WINDOW_SIZE = [256, 224] #snes native resolution

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

wall = pygame.image.load("256_wall.bmp").convert()
fg = pygame.image.load("foreground.bmp").convert()
fg.set_colorkey((0,255,0))

ceiling_gradient = pygame.image.load("ceiling_gradient.bmp").convert()

music = pygame.mixer.music.load("trnstn_loop.wav")
pygame.mixer.music.play(-1)

def dispAds(xPos):
    hakbang = pygame.image.load("hakbang.bmp").convert()
    happibee = pygame.image.load("ad_happibee.bmp").convert()
    aniqlo = pygame.image.load("ad_aniqlo.bmp").convert()

    screen.blit(aniqlo, (xPos+360, 96))
    screen.blit(hakbang, (xPos+169, 111))
    screen.blit(happibee, (xPos+24, 96))

def showTrain(xPos):
    train = pygame.image.load("train_256.bmp").convert()
    train.set_colorkey((0,255,0))
    mirror_train = pygame.transform.flip(train, True, False)
    xTrain = xPos

    screen.blit(train, (xTrain, 76))
    screen.blit(mirror_train, (xTrain+train.get_rect().width, 76))

def skew_floor(xPos, angle):

    # loading image onto PIL
    img = Image.open("floor_skewed_wide.png")

    # skewing algorithm
    width, height = img.size
    xshift = abs(angle) * width
    new_width = width + int(round(xshift))
    img = img.transform((new_width, height), Image.AFFINE,
            (1, angle, -xshift if angle > 0 else 0, 0, 1, 0), Image.BICUBIC)

    # convert PIL to pygame
    floor_pygame = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
    screen.blit(floor_pygame, (xPos-256, 163))

def dispLine(xPos):
    pygame.draw.line(screen,(0,0,0), (xPos+128,73),((xPos*2)+128,0)) # next line that will be drawn
    pygame.draw.line(screen,(255,255,255), (xPos+127,73),(((xPos*2)+128)-1,0))

    pygame.draw.line(screen,(0,0,0), (xPos,73), (xPos-(128-xPos),0)) # current line being drawn
    pygame.draw.line(screen,(255,255,255), (xPos-1,73), ((xPos-(128-xPos))-1,0))

def main():

    gameRunning = True

    camera_ctr = 0
    train_coord_x = 768
    skew_coord_x = 0
    skew_angle = 0.0

    R_scroll = False
    L_scroll = False
    trainVisible = False

    isWalk = False

    while gameRunning: #game loop, always true

        screen.fill((0,0,0))

        fg_coord_x = camera_ctr - 256
        wall_coord_x = fg_coord_x / 2

        xRel_wall = wall_coord_x % wall.get_rect().width  #relative x of wall
        screen.blit(wall, (xRel_wall - wall.get_rect().width, 75))

        if xRel_wall < WINDOW_SIZE[0]:
            screen.blit(wall, (xRel_wall, 75))
            screen.blit(wall, (xRel_wall + wall.get_rect().width, 75))

        skew_floor(skew_coord_x, skew_angle)
        dispAds(wall_coord_x)

        if trainVisible:
            showTrain(train_coord_x)
            if train_coord_x != -768:
                train_coord_x -=16
            else:
                trainVisible = False
                train_coord_x = 768

        print(skew_coord_x, skew_angle)

        screen.blit(ceiling_gradient,(0,-18))
        dispLine(skew_coord_x)
        screen.blit(fg, (fg_coord_x, 37))

        #new_player_test.main(screen, isWalk)

        if R_scroll and camera_ctr != -256:
            camera_ctr -= 8

            # looks for current position and skew angle of floor, if zero, it reinitializes them back to 128 and -1.4 respectively
            if skew_coord_x <= 0 or skew_angle >= 0.0:
                skew_coord_x = 126
                skew_angle = -1.4

            skew_coord_x -= 6
            skew_angle += 0.067

        elif L_scroll and camera_ctr != 256:
            camera_ctr += 8

            if skew_coord_x >= 126 or skew_angle <= -1.4:
                skew_coord_x = 0
                skew_angle = 0

            skew_coord_x += 6
            skew_angle -= 0.067

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # user closes the window
                gameRunning = False
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    R_scroll = True
                    isWalk = True
                elif event.key == K_LEFT:
                    L_scroll = True
                    isWalk = True
                elif event.key == K_g:
                    if not trainVisible:
                        trainVisible = True
                    else:
                        trainVisible = False
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    R_scroll = False
                    isWalk = False
                elif event.key == K_LEFT:
                    L_scroll = False
                    isWalk = False
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
