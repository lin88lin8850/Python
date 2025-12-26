class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)  # 设置背景色

        # 飞船的设置
        self.ship_limit = 4

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # 外星人设置
        self.fleet_drop_speed = 10

        # 以什么速度加快游戏的节奏
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 3
        self.bullet_speed = 4
        self.alien_speed = 1.0

        # fleet_direction 为 1 表示向右移动, 为 -1 表示向左移动
        self.fleet_direction = 1

        # score setting
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置的值"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
