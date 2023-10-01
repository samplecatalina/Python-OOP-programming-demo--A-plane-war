import pygame
import sys

pygame.init()

size = width, height = 600, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption("demo_font")
bg = (0, 0, 0)

font = pygame.font.Font(None, 20)  # 实例化字体模块；“None”表示使用默认字体；"20"表示将字体设置为20号
position = 0
line_height = font.get_linesize()


screen.fill(bg)  # 以RGB颜色填充背景;

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # pygame.font.Font.render()的参数：
        # 第一个参数位置填写要渲染的文字的内容，第二个参数为True时表示开启抗锯齿；
        # 第三个参数以RGB格式指定文本颜色
        # 此函数最后输出的是一个Surface对象
        # (0, position)用于指定渲染后的字体在屏幕上绘制的位置
        screen.blit(font.render(str(event), True, (0, 255, 0)), (0, position))
        position += line_height  # 写完每一行后另起一行

        if position > height:  # 若写完本屏幕
            position = 0       # 则从头开始
            screen.fill(bg)    # 并将整个屏幕刷黑来掩盖之前的字迹

    pygame.display.update()  # 完成游戏循环中所有内容后刷新页面显示内容
