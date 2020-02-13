import random
import pygame

# 屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率常量
FPS = 60
# 创建定时器常量
ENEMY_EVENT = pygame.USEREVENT
# 创建定时器变量--战机发射子弹
HERO_FIRE_EVENT = pygame.USEREVENT +1

# 游戏精灵创建父类
class GameSprite(pygame.sprite.Sprite):

    def __init__(self, image_name, speed=1):

        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):

        self.rect.y += self.speed

# 游戏精灵创建==>背景创建
class Background(GameSprite):
    """
    继承GameSprite
    重写__init__方法
    重写update方法
    """

    def __init__(self, is_alt=False):
        super().__init__("./images/background.png")

        if is_alt:
            self.rect.y = -SCREEN_RECT.height

    # 重写update方法
    def update(self):
        # 调用 父类方法
        super().update()
        # 判断是否移动到界面下方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -SCREEN_RECT.height


# 敌机类
class Enemy(GameSprite):

    def __init__(self):
        """
        调用父类方法,创建敌机精灵(图片样式)
        设置敌机的不同初始位置
        设置敌机的不同变化速度
        """
        super().__init__("./images/enemy1.png")
        # 敌机随机速度
        self.speed = random.randint(1, 3)

        # 敌机初始y值屏幕之外(敌机图片下方为0)
        self.rect.bottom = 0
        # 敌机初始x值得最大范围(游戏界面大小-图片宽度)
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):

        # 调用父类刷新方法
        super().update()

        # 判断敌机是否飞出游戏界面,删除敌机,释放内存
        if self.rect.y > SCREEN_RECT.height:
            # print("超出边界,删除敌机")
            self.kill()

    def __del__(self):
        # print("删除敌机 %s" % self.rect)
        pass

# 战机类
class Hero(GameSprite):
    """
    初始化战机图片
    战机垂直速度为0
    战机初始位置在界面中心
    """
    def __init__(self):
        super().__init__("./images/me1.png", speed=0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 55

        # 创建子弹精灵组
        self.bullet_group = pygame.sprite.Group()



    def update(self):
        # 将战机的x与速度进行运算实现水平移动
        self.rect.x += self.speed

        # 保证战机不会移动到界面外部
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_RECT.width
            # 下面语句无法实现战机从左边界消失后右边界出现
            # self.rect.x = SCREEN_RECT.width + self.rect.width

        elif self.rect.x > SCREEN_RECT.width:
            self.rect.x = -self.rect.width

    def fire(self):
        # print("发射子弹...")

        # 加入for循环--一次发射三枚子弹
        # 将for循环语句下的代码格式化
        # for i in (0, 1, 2):
        # 创建子弹精灵
        bullet = Bullet()

        # 设置子弹的初始位置
        bullet.rect.bottom = self.rect.y - 5
        bullet.rect.centerx = self.rect.centerx

        # 将子弹添加到精灵组
        self.bullet_group.add(bullet)

# 子弹类
class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet1.png", speed=-2)

    def update(self):
        super().update()
        # 这里直接调用父类update方法,不用重写(忘了)
        # self.rect.y += self.speed
        if self.rect.bottom < 0:
            # print("超出边界,删除敌机")
            self.kill()

    def __del__(self):
        # print("删除敌机 %s" % self.rect)
        pass