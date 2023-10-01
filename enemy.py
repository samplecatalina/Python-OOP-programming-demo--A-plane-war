import pygame
import random


class SmallEnemy(pygame.sprite.Sprite):

    def __init__(self, bg_size):
        super().__init__()

        self.image = pygame.image.load("./images/enemy1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("./images/enemy1_down1.png").convert_alpha(),
            pygame.image.load("./images/enemy1_down2.png").convert_alpha(),
            pygame.image.load("./images/enemy1_down3.png").convert_alpha(),
            pygame.image.load("./images/enemy1_down4.png").convert_alpha()
        ])
        self.rect = self.image.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.speed = 2
        self.rect.left, self.rect.top = \
            random.randint(0, self.bg_width - self.rect.width),\
            random.randint(-5 * self.bg_height, 0)
        # 上一行此处通过对敌人生成位置的纵坐标范围进行控制来控制敌人生成的密度；纵坐标范围越大，敌人密度越大

        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        # pygame中封装的mask.from_surface()方法可以将在括号中传入的图片的非透明部分作出标注，
        # 配合pygame.sprite.spritecollide()方法可以实现有边框图片的具体内容的碰撞检测

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = \
            random.randint(0, self.bg_width - self.rect.width), \
            random.randint(-5 * self.bg_height, 0)


class MidEnemy(pygame.sprite.Sprite):
    energy = 8

    def __init__(self, bg_size):
        super().__init__()

        self.image = pygame.image.load("./images/enemy2.png").convert_alpha()
        self.image_hit = pygame.image.load("./images/enemy2_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("./images/enemy2_down1.png").convert_alpha(),
            pygame.image.load("./images/enemy2_down2.png").convert_alpha(),
            pygame.image.load("./images/enemy2_down3.png").convert_alpha(),
            pygame.image.load("./images/enemy2_down4.png").convert_alpha()
        ])
        self.rect = self.image.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.top = \
            random.randint(0, self.bg_width - self.rect.width),\
            random.randint(-10 * self.bg_height, - self.bg_height)
        # 上一行此处通过对敌人生成位置的纵坐标范围进行控制来控制敌人生成的密度；纵坐标范围越大，敌人密度越大
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = MidEnemy.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left, self.rect.top = \
            random.randint(0, self.bg_width - self.rect.width), \
            random.randint(-10 * self.bg_height, - self.bg_height)


class LargeEnemy(pygame.sprite.Sprite):
    energy = 20

    def __init__(self, bg_size):
        super().__init__()

        self.image1 = pygame.image.load("./images/enemy3_n1.png").convert_alpha()
        self.image2 = pygame.image.load("./images/enemy3_n2.png").convert_alpha()
        self.image_hit = pygame.image.load("./images/enemy3_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("./images/enemy3_down1.png").convert_alpha(),
            pygame.image.load("./images/enemy3_down2.png").convert_alpha(),
            pygame.image.load("./images/enemy3_down3.png").convert_alpha(),
            pygame.image.load("./images/enemy3_down4.png").convert_alpha(),
            pygame.image.load("./images/enemy3_down5.png").convert_alpha(),
            pygame.image.load("./images/enemy3_down6.png").convert_alpha()
        ])
        self.rect = self.image1.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.top = \
            random.randint(0, self.bg_width - self.rect.width),\
            random.randint(-10 * self.bg_height, -5 * self.bg_height)
        # 上一行此处通过对敌人生成位置的纵坐标范围进行控制来控制敌人生成的密度；纵坐标范围越大，敌人密度越大

        self.active = True
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy = LargeEnemy.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = LargeEnemy.energy
        self.rect.left, self.rect.top = \
            random.randint(0, self.bg_width - self.rect.width), \
            random.randint(-15 * self.bg_height, -5 * self.bg_height)