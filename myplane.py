import pygame


class MyPlane(pygame.sprite.Sprite):

    def __init__(self, bg_size):
        super().__init__()

        self.image1 = pygame.image.load("./images/me1.png").convert_alpha()
        self.image2 = pygame.image.load("./images/me2.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("./images/me_destroy_1.png").convert_alpha(),
            pygame.image.load("./images/me_destroy_2.png").convert_alpha(),
            pygame.image.load("./images/me_destroy_3.png").convert_alpha(),
            pygame.image.load("./images/me_destroy_4.png").convert_alpha()
            ])
        self.rect = self.image1.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = (self.bg_width - self.rect.width)//2,\
                                        self.bg_height - self.rect.height - 60

        self.speed = 10
        self.active = True
        self.invincible = False
        self.mask = pygame.mask.from_surface(self.image1)

    def move_up(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def move_down(self):
        if self.rect.bottom >= self.bg_height - 60:
            self.rect.bottom = self.bg_height - 60
        else:
            self.rect.bottom += self.speed

    def move_left(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def move_right(self):
        if self.rect.right >= self.bg_width:
            self.rect.right = self.bg_width
        else:
            self.rect.right += self.speed

    def reset(self):
        self.rect.left, self.rect.top = (self.bg_width - self.rect.width)//2, self.bg_height - self.rect.height - 60
        self.active = True
        self.invincible = True
