import pygame
import random

SCREEN_RECT = pygame.Rect(0,0,480,700)
FRAME_FEN = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):


    """飞机大战游戏精灵"""
    def __init__(self,image_name,speed=1):

        #条用父类的初始化方法
        super().__init__()

        #定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的锤子方向移动
        self.rect.y += self.speed



class Backgroup(GameSprite):
    """游戏背景精灵"""

    def __init__(self,is_alt=False):
        super().__init__("./image/background.png")
        if is_alt is True:
           self.rect.y = -self.rect.height

    def update(self):
        # 1 调用父类的方法
        super().update()
        # 2 判断是否移出屏幕
        if self.rect.y >=SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    def __init__(self):
        # 1 调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__("./image/enemy1.png")
        # 2 指定敌机的初始随机速度
        self.speed = random.randint(1,3)
        # 3 指定敌机的初始随机位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0,max_x)

    def update(self):

        # 1 调用父类方法，保持垂直方向的飞行
        super().update()

        if self.rect.y >= SCREEN_RECT.height:
            #print("敌机超出屏幕")
            self.kill()


    def __del__(self):
        #print("敌机挂了 %s" % self.rect)
        pass


class Hero(GameSprite):
    """英雄精灵"""
    def __init__(self):
        # 1. 调用父类方法，设志image及speed
        super().__init__("./image/me1.png",0)
        # 2.设置英雄的初始位置
        self.rect.x = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.height - 120

        # 3 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()


    def update(self):
        # 英雄在水平移动
        self.rect.x += self.speed

        # 控制位置范围
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        #print("开火")
        for i in (0,1,2):
            # 1 创建子弹精灵
            bullet = Bullet()
            # 2 设置位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # 3 将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹精灵"""
    def __init__(self):
        super().__init__("./image/bullet1png.png",-2)

    def update(self):
        #调用父类方法.让子弹垂直飞行
        super().update()
        #判断子弹是否飞出屏幕

        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        #print("子弹被销毁。。。")
        pass