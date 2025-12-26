"""
按 Q 键退出游戏
"""

import sys
from time import sleep

import pygame

from ship import Ship
from bullet import Bullet
from alien import Alien
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # 创建游戏状态实例和记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # set game mode
        self.game_active = False

        # 创建 play 按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏的主循环"""

        while True:
            # 侦听键盘和鼠标事件
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _start_game(self):
        # 重置游戏设置
        self.settings.initialize_dynamic_settings()

        # 重置游戏的统计信息
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_active = True

        # 清空外星人列表和子弹列表
        self.bullets.empty()
        self.aliens.empty()

        # 创建一个新的外星舰队, 并将飞船放在屏幕底部的中央
        self._create_fleet()
        self.ship.center_ship()

        # 隐藏光标
        pygame.mouse.set_visible(False)

    def _create_fleet(self):
        """创建一个外星人舰队"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_postion):
        """创建一个外星人并将其放在当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x, new_alien.rect.y = x_position, y_postion
        self.aliens.add(new_alien)

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        # 调用这个函数时, 表示已经发生了碰撞
        self.stats.ships_left -= 1

        if self.stats.ships_left > 0:
            self.sb.prep_ships()  # 屏幕左上角显示剩余的飞船

            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()

            # 创建新的外星人舰队, 并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _change_fleet_direction(self):
        """将整个外星人舰队向下移动, 并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """有外星人达到边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_play_button(self, mouse_pos):
        """在玩家单击 Play 按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # 返回单击鼠标的 (x, y) 坐标
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # 按下右方向键
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # 按下左方向键
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # 按下 Q 键退出
        elif event.key == pygame.K_q:
            sys.exit()
        # 按下 P 键开始 Play
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        # 释放右方向键
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        # 释放左方向键
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""

        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            # 捕捉多个外星人同时被子弹击中的情况
            for aliens in collisions.values():
                # len(aliens) 考虑到若子弹太宽, 同时与多个外星人碰撞
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 删除现有的子弹并创建一个新的外星舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _fire_bullet(self):
        """创建一颗子弹, 并加入 bullets"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置, 并删除已消失的子弹"""

        self.bullets.update()

        # 删除已消失的子弹, 否则消耗系统的内存
        """
            使用 for 循环遍历列表, Python 要求该列表的长度在整个循环中保存不变
            因此使用 self.bullets.copy() 来遍历
        """
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘, 并更新外星人舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检查外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()

    def _update_screen(self):
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        # 为防止子弹出现在飞船上, 在飞船前面绘画子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态, 就绘制 Play 按钮
        if not self.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == "__main__":
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
