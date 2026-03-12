
"""
存储设置的模块
"""
import random

class Settings():
    def __init__(self):

        #窗口长宽
        self.screen_width = 800
        self.screen_height = 600
        #背景色
        self.bg_color = (230, 230, 230)

        #帧率
        self.FPS = 120

        #飞机碰撞箱体积缩放
        self.collide_scale_factor = 0.5

        #我方子弹相关
        self.bullet_speed = 10
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_cool_down = 50
        self.big_bullet_cool_down = 5000
        self.bullet_damage = 20

