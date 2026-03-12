#标准库导入
import pygame
from pygame.sprite import Sprite
import random
#模块导入
# from settings import Settings

class Plane(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.settings = game.settings
        self.screen = game.screen

        #加载图像
        self.image = pygame.image.load('image/plane.bmp')
        self.rect = self.image.get_rect()

        #血量
        self.health = 100
        # self.collide_rect = self.rect


        #碰撞箱
        # def collide(self):
        self.collide_rect = self.rect.copy()
        self.collide_scale_factor = self.settings.collide_scale_factor #缩放倍率
        self.update_collide_rect()

    def update_collide_rect(self):
        self.collide_rect.width = int(self.rect.width * self.collide_scale_factor)
        self.collide_rect.height = int(self.rect.height * self.collide_scale_factor)
        self.collide_rect.center = self.rect.center

    #画图
    def draw_plane(self):
        self.screen.blit(self.image, self.rect)

    #位置更新（随鼠标移动）
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.centerx = mousex #偏移调整，因为贴图问题
        self.rect.centery = mousey + 10
        # self.screen.blit(self.image, self.rect)
        self.update_collide_rect()
        self.screen.blit(self.image, self.rect)


"""
子类：我方飞机
"""
class Myplane(Plane):
    def __init__(self, game):
        super().__init__(game)


"""
子类：敌方飞机
"""

class Enemy(Plane):
    def __init__(self, game):
        super().__init__(game)

        #加载图像
        self.image = pygame.image.load('image/enemy.bmp')

        #速度
        self.speed_x, self.speed_y = 0.1 * random.randint(-5,5), 0.1 * random.randint(1, 3)

        #设置初始位置
        screen_rect = self.screen.get_rect()
        self.rect.top = screen_rect.top
        self.rect.x = random.randint(0, screen_rect.width - self.rect.width)
        self.x, self.y = self.rect.x, self.rect.y

        #碰撞箱
        # def collide(self):
        self.collide_rect = self.rect.copy()
        self.collide_scale_factor = 1 # 缩放倍率
        self.update_collide_rect()
        #子弹相关
        self.last_shot_time = 0
        self.cool_down = random.randint(4000, 8000)
        self.damage = 10


    def draw_plane(self):
        self.screen.blit(self.image, self.rect)


    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x, self.rect.y = self.x, self.y
        self.update_collide_rect()
        self.screen.blit(self.image, self.rect)

