import pygame
import sys

pygame.init()

size = width, height = 300, 200
screen = pygame.display.set_mode(size)
pygame.display.set_caption("demo_music")

pygame.mixer.music.load("./sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

button_sound = pygame.mixer.Sound("./sound/button.wav")
button_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("./sound/upgrade.wav")
upgrade_sound.set_volume(0.2)

pause = False

pause_image = pygame.image.load("./images/pause_nor.png")
resume_image = pygame.image.load("./images/resume_nor.png")
pause_rect = pause_image.get_rect()
pause_rect.left, pause_rect.top = (width - pause_rect.width)//2, (height - pause_rect.top)//2
resume_rect = resume_image.get_rect()
resume_rect.left, resume_rect.top = (width - resume_rect.width)//2, (height - resume_rect.top)//2

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button_sound.play()
            elif event.button == 3:
                upgrade_sound.play()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause

    if pause:
        screen.blit(resume_image, (resume_rect.left, resume_rect.top))
        pygame.mixer.music.pause()
        pygame.display.update()

    else:
        screen.blit(pause_image, (pause_rect.left, resume_rect.top))
        pygame.mixer.music.unpause()
        pygame.display.update()

    screen.fill((255, 255, 255))
    clock.tick(30)




