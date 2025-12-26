import os
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 获取脚本所在目录，构建图像文件的绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "images", "ship.bmp")

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        # 每艘飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性 x 中存储一个浮点数
        self.x = float(self.rect.x)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 根据 self.x 更新 rect 对象
        self.rect.x = self.x

    def blitme(self):
        """初始化飞船并设置其初始位置"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船放在屏幕底部的中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
