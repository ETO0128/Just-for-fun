"""
子弹类
"""
#导入标准库
import pygame
from pygame.sprite import Sprite
import random
#导入模块
from settings import Settings
from plane import Enemy


class Bullet(Sprite):
    def __init__(self, game):
        super().__init__()
        self.settings = Settings()
        self.screen = game.screen


        #子弹参数
        self.width = self.settings.bullet_width
        self.height = self.settings.bullet_height
        self.speed = self.settings.bullet_speed
        self.color = 30, 30, 30
        self.damage = self.settings.bullet_damage
        #设置正确位置
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        midbottomx, midbottomy = game.plane.rect.midtop#偏移调整，因为贴图问题
        self.rect.midbottom = midbottomx , midbottomy


        self.y = float(self.rect.y)


    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
        pygame.draw.rect(self.screen, self.color, self.rect)
        if self.rect.y < 0:
            self.kill()


class Mybullet(Bullet):
    def __init__(self, game):
        super().__init__(game)


#大招子弹
class BigBullet(Bullet):
    def __init__(self, game):
        super().__init__(game)
        self.width = self.settings.bullet_width * 100
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = game.plane.rect.midtop
        self.y = float(self.rect.y)
        self.color = 255, 100, 100
        self.speed = self.settings.bullet_speed * 0.1

class EnemyBullet(Bullet):
    def __init__(self, game, enemy):
        super().__init__(game)
        self.speed = self.settings.bullet_speed * (- 0.1)
        self.rect.centerx = enemy.rect.centerx
        self.rect.centery = enemy.rect.centery

        self.y = float(self.rect.y)
        self.damage = 10



