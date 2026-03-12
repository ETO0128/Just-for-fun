"""
一个模仿《Alien Invasion》写的小游戏
"""
#导入标准库
import pygame
import sys

#导入模块
from settings import Settings
from plane import *
from bullet import *


class PlaneWars:
    #构造函数
    def __init__(self):
        pygame.init() #初始化
        self.settings = Settings() #导入设置
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))#设置屏幕

        self.clock = pygame.time.Clock() #设置帧率

        self.plane = Myplane(self) #飞机
        self.bullets = pygame.sprite.Group() #子弹
        self.enemybullets = pygame.sprite.Group()
        self.enemys =pygame.sprite.Group() #敌人

        self.game_active = True # 记录游戏状态

        #记录时间,计算发射冷却
        self.last_shot_time = 0 #普通子弹冷却
        self.last_big_shot_time = -5000 # 大招子弹

    """
    事件检测
    """
    # 检测主函数
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.check_keyboard_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.check_mouse_events(event)


    #键盘事件检测
    def check_keyboard_events(self, event=None):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            # elif event.key == pygame.:



    #鼠标事件检测
    def check_mouse_events(self, event=None):
        if event.button == 1:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_big_shot_time > self.settings.big_bullet_cool_down:
                new_bullet = BigBullet(self)
                # new_bullet.draw_bullet()
                self.bullets.add(new_bullet)
                self.last_big_shot_time = current_time


    """
    发射子弹与刷怪
    """

    #发射子弹
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time- self.last_shot_time > self.settings.bullet_cool_down:
            new_bullet = Mybullet(self)
            new_bullet.draw_bullet()
            self.bullets.add(new_bullet)
            self.last_shot_time = current_time

    def enemy_shoot(self):
        current_time = pygame.time.get_ticks()
        for enemy in self.enemys:
            if current_time - enemy.last_shot_time > enemy.cool_down:
                new_bullet = EnemyBullet(self, enemy)
                self.enemybullets.add(new_bullet)
                new_bullet.draw_bullet()
                enemy.last_shot_time = current_time


    #子弹位置更新
    def update_bullet(self):
        for bullet in self.bullets:
            bullet.update()
        for enemy_bullet in self.enemybullets:
            enemy_bullet.update()

    #刷怪
    def enemy_spawn(self):
        while (len(self.enemys) < 10):
            new_enemy = Enemy(self)
            new_enemy.draw_plane()
            self.enemys.add(new_enemy)

    #怪物位置更新
    def update_enemy(self):
        for enemy in self.enemys:
            enemy.update()
            if enemy.rect.right > self.settings.screen_width or enemy.rect.left < 0:
                enemy.speed_x *= -1
            if enemy.rect.bottom > self.settings.screen_height:
                self.plane.health -= 5

    """
    碰撞判定
    """
    #敌方碰撞判定
    def check_enemy_collide(self):
        for enemy in self.enemys:
            for bullet in self.bullets:
                if pygame.sprite.collide_rect(enemy, bullet):
                    if isinstance(bullet, Mybullet):
                        self.bullets.remove(bullet)
                        enemy.health -= bullet.damage
                    elif isinstance(bullet, BigBullet):
                        self.enemys.remove(enemy)
                    if enemy.health <= 0:
                        self.enemys.remove(enemy)

    #我方碰撞判定
    def check_my_collide(self):
        for enemy in self.enemys:
            if enemy.rect.colliderect(self.plane.collide_rect):  #使用缩小的碰撞箱
                self.plane.health -= 50
                self.enemys.remove(enemy)
                if self.plane.health <= 0:
                    sys.exit()

        for bullet in self.enemybullets:
            if bullet.rect.colliderect(self.plane.collide_rect):
                self.enemybullets.remove(bullet)
                self.plane.health -= bullet.damage
                if self.plane.health <= 0:
                    sys.exit()
    """
    屏幕更新相关
    """
    #屏幕初始化
    def init_screen(self):
        pygame.display.set_caption("PlaneWars")
        self.screen.fill(self.settings.bg_color)
        self.plane.draw_plane()
        pygame.display.flip() #让绘制的屏幕可见

    #屏幕更新
    def update_screen(self):
        #pygame.display.set_caption("PlaneWars")
        self.screen.fill(self.settings.bg_color) #刷新画布
        self.shoot()
        self.enemy_shoot()
        self.update_bullet()
        self.plane.update()
        if len(self.enemys) == 0:
            self.enemy_spawn()
        self.update_enemy()
        self.check_enemy_collide()
        self.check_my_collide()
        pygame.display.flip()

    """
    运行游戏
    """
    def run_game(self):
        self.init_screen()
        while True:
            self.check_events()
            if self.game_active:
                self.clock.tick(self.settings.FPS)
                self.update_screen()



# 主函数
def main():
    wars = PlaneWars()
    wars.run_game()


if __name__ == '__main__':
    main()
