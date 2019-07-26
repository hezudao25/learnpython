import pygame
from plane_sprites import *


class GamePlay(object):

    def __init__(self):
        print("游戏初始化")
        #1.创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        #2.创建游戏的时钟
        self.clock = pygame.time.Clock()

        #3.调用私有方法，精灵
        self.__create_sprites()

        # 4 设置定时器事件 -- 创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        pygame.time.set_timer(HERO_FIRE_EVENT,500)

    def __create_sprites(self):
       bg1 = Backgroup()
       bg2 = Backgroup(True)
       self.back_group = pygame.sprite.Group(bg1,bg2)

       # 创建敌机精灵组
       self.enemy_group = pygame.sprite.Group()

       # 创建英雄的精灵组
       self.hero = Hero()
       self.hero_group = pygame.sprite.Group(self.hero)



    def game_start(self):
        print("游戏开始...")

        while True:
            # 1设置刷新频率
            self.clock.tick(FRAME_FEN)
            # 2 事件监听
            self.__event_handler()
            # 3 碰撞检测
            self.__check_collide()
            # 4 更新/绘制精灵组
            self.__updaes_sprites()
            # 5 更新显示
            pygame.display.update()
            pass

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               GamePlay.game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                #print("敌机出场。。。")
                # 创建敌机精灵
                enemy = Enemy()
                # 将敌机精灵添加的敌机精灵组
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0




    def __check_collide(self):
        # 1 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,True)
        # 2 敌机摧毁英雄
        enemies = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        # 3 判断列表是否有内容
        if len(enemies)>0 :
            #让英雄牺牲
            self.hero.kill()
            #借宿游戏
            GamePlay.__game_over()



    def __updaes_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()





if __name__ == '__main__':
    game = GamePlay()
    game.game_start()