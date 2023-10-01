import pygame
import sys

pygame.init()

size = width, height = 480, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("test")

bg = pygame.image.load("./images/background.png").convert()
me = pygame.image.load("./images/me1.png").convert_alpha()
me_rect = me.get_rect()
me_rect.left, me_rect.top = (size[0] - me_rect.width)//2, (size[1] - me_rect.height)//2

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg, (0, 0))
    screen.blit(me, (me_rect.left, me_rect.top))

    pygame.display.update()
    clock.tick(30)

