import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption("demo_paint")

clock = pygame.time.Clock()

position = size[0]//2, size[1]//2
moving = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                moving = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                moving = False

    if moving:
        position = pygame.mouse.get_pos()

    screen.fill(WHITE)

    pygame.draw.circle(screen, RED, position, 25, 1)
    pygame.draw.circle(screen, GREEN, position, 75, 1)
    pygame.draw.circle(screen, BLUE, position, 125, 1)

    pygame.display.update()

    clock.tick(120)


