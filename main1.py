import pygame
import sys
import traceback
import random
import bullet
import enemy
import myplane
import supply

pygame.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("OK全体目光向我看齐 我宣布个事")

clock = pygame.time.Clock()

background = pygame.image.load("./images/background.png").convert()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_large_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.LargeEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


def increase_speed(target, increase):
    for each in target:
        each.speed += increase


def main():

    pygame.mixer.music.play(-1)  # music模块调用play，只能播放之前加载在music模块中的音乐

    # 用于切换我方飞机图片（必须要放在while循环之前的位置）
    switch_image = True

    # 用于延迟我方飞机的不同图片的切换频率但又不影响游戏循环的正常运作
    # 通用延迟变量
    delay = 100

    # 生成我方飞机
    me = myplane.MyPlane(bg_size)

    # 构造敌方飞机总精灵组
    enemies = pygame.sprite.Group()

    # 生成小型敌方飞机，构造相应子精灵组
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # 生成敌方中型飞机，构造相应子精灵组
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    # 生成敌方大型飞机，构造相应子精灵组
    large_enemies = pygame.sprite.Group()
    add_large_enemies(large_enemies, enemies, 2)

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    # 超级子弹定时器
    DOUBLE_BULLET_TIME: int = pygame.USEREVENT + 1

    # 标记是否使用超级子弹
    is_double_bullet = False

    # 解除我方无敌状态定时器
    INVINCIBLE_TIME = pygame.USEREVENT + 2

    # 生命数量
    life_image = pygame.image.load("./images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # 游戏结束画面
    gameover_font = pygame.font.Font("./font/font.ttf", 48)
    again_image = pygame.image.load("./images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("./images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    DOUBLE_BULLET_TIME = pygame.USEREVENT + 1

    # 用于防止反复打开记录文件
    recorded = False

    # 每30秒发放一个补给包
    bullet_supply = supply.BulletSupply(bg_size)
    bomb_supply = supply.BombSupply(bg_size)
    SUPPLY_TIME = pygame.USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

    # 统计得分
    score = 0
    score_font = pygame.font.Font("./font/font.ttf", 36)

    # 标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load("./images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("./images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("./images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("./images/resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    # 设置难度级别
    level = 1
    # 设置全屏炸弹
    bomb_image = pygame.image.load("./images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("./font/font.ttf", 48)
    bomb_num = 3

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)  # 将set_timer的第二个参数设置为0表示停止计时器工作
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                        # 注意mixer.music.pause()和mixer.pause()是不一样的，music专指背景音乐，
                        # mixer.pause()则涵盖特殊动作的音效
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == pygame.MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if random.choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        # 根据用户得分增加难度
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            # 增加3架小型敌机， 2架中型敌机，1架大型敌机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_large_enemies(large_enemies, enemies, 1)
            # 提升小型敌机速度
            increase_speed(small_enemies, 1)

        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            # 增加5架小型敌机， 3架中型敌机，2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # 提升小型及中型敌机速度
            increase_speed(small_enemies, 1)
            increase_speed(small_enemies, 1)

        elif level == 3 and score > 500000:
            level = 4
            upgrade_sound.play()
            # 增加5架小型敌机， 3架中型敌机，2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # 提升小型及中型敌机速度
            increase_speed(small_enemies, 1)
            increase_speed(small_enemies, 1)

        elif level == 3 and score > 1000000:
            level = 4
            upgrade_sound.play()
            # 增加5架小型敌机， 3架中型敌机，2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # 提升小型及中型敌机速度
            increase_speed(small_enemies, 1)
            increase_speed(small_enemies, 1)

        # 绘制背景
        screen.blit(background, (0, 0))

        if life_num and not paused:

            # 扫描用户的键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
                me.move_up()
            elif key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                me.move_down()
            elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                me.move_left()
            elif key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                me.move_right()

            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            # 绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bomb_supply.active = False

            # 发射子弹
            if not (delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in large_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            # 绘制敌机
            # 注意：同一循环内应当首先编写大型敌机，之后中型，之后小型，
            # 这样python绘制的时候会将小型和中型绘制在大型敌机上方，大型机才不会遮挡中小型机

            # 绘制大型敌机
            for each in large_enemies:
                if each.active:
                    each.move()

                    # 绘制大型敌机被击中后的画面
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False  # 确保只有在被击中的瞬间才显示受击效果
                    else:  # 绘制大型敌机的正常状态
                        # 绘制大型敌机的动态效果
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 当大型敌机即将出现在屏幕中时，播放音效
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)

                    # 绘制大型敌机的生命值
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    # 当生命值大于20%时显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.LargeEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                     2)

                else:  # 启动毁灭过程
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()

            # 绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    each.move()

                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制中型敌机的生命值
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    # 当生命值大于20%时显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                     2)

                else:  # 启动毁灭过程
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()

            # 绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)

                else:  # 启动毁灭过程
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # 碰撞检测：我方飞机与敌方
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False

            # 绘制我方飞机:
            # 注意：
            # 1. 此处blit函数无法直接绘制me对象，只能指定me对象的image属性（是一个surface对象）之后才能绘制；
            # 2. 此处我方飞机的绘制必须要晚于背景图的绘制，否则飞机图片将会被背景图片所遮挡。
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:  # 启动毁灭过程
                if not (delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # 绘制全屏炸弹状态栏
            bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            # 绘制剩余生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (width-10-(i+1)*life_rect.width, height-10-life_rect.height))

            # 绘制玩家得分
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

        # 绘制游戏结束画面
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()

            # 停止全部音效
            pygame.mixer.stop()

            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)

            if not recorded:
                recorded = True
                # 读取历史最高分
                with open("record.txt", "r") as f:
                    record_score = int(f.read())

                # 如果玩家得分高于历史最高得分，则存档
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))

            # 绘制结束界面
            record_score_text = score_font.render("Best: %d" % record_score, True, WHITE)
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score: ", True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (width - gameover_text1_rect.width) // 2, height // 2
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                (width - again_rect.width) // 2, \
                gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (width - again_rect.width) // 2, \
                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    main()
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()

        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        # 用于延迟我方飞机两张图片切换的频率的模块
        # delay = 5
        # delay -= 1
        # if not delay: (实际上就是delay=0)
        #     delay = 5
        if not(delay % 5):  # <-> if not (delay%5)=True <-> if not (delay%5)=1 <-> if (delay%5)=0
            switch_image = not switch_image
        delay -= 1
        if not delay:  # <-> if not delay = 1 <-> if delay != 1 <-> if delay = 0
            delay = 100

        pygame.display.update()

        clock.tick(60)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except Exception as result:
        traceback.print_exc()
        pygame.quit()
        print("出现未知错误 %s" % result)
        input()
