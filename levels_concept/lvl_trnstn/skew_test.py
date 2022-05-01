import pygame
from PIL import Image

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.display.set_caption("Skew Test")

WINDOW_SIZE = [768, 93]
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

def skew_image(img, angle):
    width, height = img.size
    xshift = abs(angle) * width
    new_width = width + int(round(xshift))
    img = img.transform((new_width, height), Image.AFFINE,
            (1, angle, -xshift if angle > 0 else 0, 0, 1, 0), Image.BICUBIC)

    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)


def main():

    gameRunning = True
    R_scroll = False
    L_scroll = False

    skew_ctr = 0.0
    x = 0

    #max skew is -1.4, max x is 128

    while gameRunning:

        screen.fill((0,0,0))

        floor_skewed = Image.open("floor_skewed_wide.png")
        floor_pygame = skew_image(floor_skewed, skew_ctr)

        screen.blit(floor_pygame, (x, 0))
        print(x, skew_ctr)

        if R_scroll:

            x -= 6
            skew_ctr += 0.067

            # looks for current position and skew angle of floor, if zero, it reinitializes them back to 128 and -1.4 respectively
            if x <= 0 or skew_ctr >= 0.0:
                x = 128
                skew_ctr = -1.4

        elif L_scroll:
            x += 6
            skew_ctr -= 0.067

            if x > 128 and skew_ctr < -1.4:
                x %= 128
                skew_ctr %= -1.4

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
        clock.tick(30)
if __name__ == '__main__':
    main()
