import pygame
from plane_sprites import *

# mixer的初始化
pygame.init()
pygame.mixer.init()

class PlaneGame(object):
    """飞机大战主程序"""

    def __init__(self):
        print("游戏初始化")

        # 载入背景音乐
        pygame.mixer.music.load("./music/game_music.mp3")
        # 播放背景音乐
        pygame.mixer.music.play()
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 创建游戏时钟
        self.clock = pygame.time.Clock()
        # 调用精灵组创建的私有方法
        self.__create_sprites()

        # 创建定时器事件==> 创建敌机
        pygame.time.set_timer(ENEMY_EVENT, 1000)    # 时间单位为毫秒
        # 创建定时器事件==> 发射子弹
        pygame.time.set_timer(HERO_FIRE_EVENT, 200)

    def __create_sprites(self):

        # 背景图片交替滚动实现
        bg1 = Background()
        bg2 = Background(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机精灵组:--敌机精灵在监听方法-定时器中创建
        self.eneny_group = pygame.sprite.Group()

        # 创建战机精灵
        self.hero = Hero()
        # 创建战机精灵组
        self.hero_group = pygame.sprite.Group(self.hero)


    def start_game(self):
        print("开始游戏===>>")
        while True:
            # 刷新帧率
            self.clock.tick(FPS)
            # 事件监听
            self.__event_handler()
            # 碰撞检测
            self.__check_collide()
            # update/draw精灵组
            self.__update_sprites()
            # update显示
            pygame.display.update()


    # 事件监听
    def __event_handler(self):
        for event in pygame.event.get():
            # --> 退出游戏
            if event.type == pygame.QUIT:
                self.__game_over()
            elif event.type == ENEMY_EVENT:
                self.eneny_group.add(Enemy())
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

            # 控制战机左右移动的两种监听方式
            # 1.====>>>灵活性差,每次键盘落下抬起算一次响应
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #     self.hero.rect.x += 1
            #     print("战机右移==>")
        # 2.===>>>灵活性好,可以按下不放,持续响应
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2

            # self.hero.rect.x += 2
            # print("战机右移===>")

        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2

            # self.hero.rect.x -= 2
            # print("<===战机左移")

        else:
            self.hero.speed = 0

    # 碰撞检测
    def __check_collide(self):

        # 子弹和敌机"同归于尽"
        while pygame.sprite.groupcollide(self.hero.bullet_group, self.eneny_group, True, True):
            pygame.mixer.music.stop()
            # 载入击中音乐
            pygame.mixer.music.load("./music/bullet.mp3")
            # 播放击中音乐
            pygame.mixer.music.play()


        # 敌机与战机发生碰撞-->发生碰撞返回列表
        enemies = pygame.sprite.spritecollide(self.hero, self.eneny_group, True)
        # 判断列表值--确定战机状态
        if len(enemies) > 0:
            # 消除战机
            self.hero.kill()

            # 游戏结束
            PlaneGame.__game_over()

    # 精灵/精灵组的更新
    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.eneny_group.update()
        self.eneny_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)
    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()

if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()