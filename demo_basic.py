import pygame
import sys

pygame.init()

size = width, height = 480, 700
speed = [-2, 1]
# bg = (255, 255, 255)  # RGB
bg = pygame.image.load("./images/background.png")

clock = pygame.time.Clock()  # 实例化clock对象

# 创建指定大小的窗口Surface
screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # RESIZABLE可将允许用户将窗口大小重新设置
# 设置窗口标题
pygame.display.set_caption("pygame模块试验")

# 加载图片
plane = pygame.image.load("./images/me1.png").convert_alpha()
# 获得图像的位置矩形
position = plane.get_rect()

l_head = u_head = plane
r_head = pygame.transform.flip(plane, True, False)
d_head = pygame.transform.flip(plane, False, True)

fullscreen = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                plane = l_head
                speed = [-1, 0]
            elif event.key == pygame.K_RIGHT:
                plane = r_head
                speed = [1, 0]
            elif event.key == pygame.K_UP:
                plane = u_head
                speed = [0, -1]
            elif event.key == pygame.K_DOWN:
                plane = d_head
                speed = [0, 1]

            # 开启全屏模式
            elif event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.HWSURFACE)
                else:
                    screen = pygame.display.set_mode(size)

        # 用户调整窗口尺寸
        elif event.type == pygame.VIDEORESIZE:
            size = event.size
            width, height = size
            print(size)
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)


    # 移动图像
    position = position.move(speed)

    # 实现图片触壁回弹
    if position.left < 0 or position.right > width:
        plane = pygame.transform.flip(plane, True, False)  # 图片换向，第二个参数表示是否水平翻转，第三个图像表示是否垂直翻转
        speed[0] = - speed[0]
    elif position.top < 0 or position.bottom > height:
        speed[1] = - speed[1]

    # 填充背景
    screen.blit(bg, (0, 0))
    # 更新图像
    screen.blit(plane, position)
    # 更新界面
    pygame.display.update()
    # 延迟十毫秒。指定每次while循环完成后都会等待10毫秒。设置delay值可以单独控制游戏动画速度
    pygame.time.delay(10)
    # 设置刷新帧率。使用刷新帧率也可以单独控制游戏动画速度
    clock.tick(120)
