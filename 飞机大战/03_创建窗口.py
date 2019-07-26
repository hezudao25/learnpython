import pygame
from sprint import *
pygame.init()

screen = pygame.display.set_mode((400,700))

#绘制背景图像
bg = pygame.image.load("./image/background.png")

#加载图像
screen.blit(bg,(0,0))

hero = pygame.image.load("./image/me1.png")

screen.blit(hero,(150,500))
#更新屏幕显示
pygame.display.update()

#创建时钟对象
clock = pygame.time.Clock()


hero_rect = pygame.Rect(150,300,102,126)
#精灵
enemy = GameSprite("./image/enemy1.png")
enemy1 = GameSprite("./image/enemy1.png",2)
enemy_gorup = pygame.sprite.Group(enemy,enemy1)

#循环

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("退出游戏...")
            pygame.quit()
            exit()

    hero_rect.y -=1
    if hero_rect.y<=-126:
        hero_rect.y =700
    screen.blit(bg,(0,0))
    screen.blit(hero,hero_rect)
    #让精灵组调用两个方法
    enemy_gorup.update()
    enemy_gorup.draw(screen)

    pygame.display.update()


pygame.quit()