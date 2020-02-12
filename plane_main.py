import pygame
from plane_sprites import *


class PlaneGame(object):
    """飞机大战主程序"""

    def __init__(self):
        print("游戏初始化")

        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 创建游戏时钟
        self.clock = pygame.time.Clock()
        # 调用精灵组创建的私有方法
        self.__create_sprites()

    def __create_sprites(self):

        # 背景图片交替滚动实现
        bg1 = Background()
        bg2 = Background(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

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

    def __check_collide(self):
        pass

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)


    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()

if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()