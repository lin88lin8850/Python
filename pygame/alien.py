import os
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien, and set its starting position."""
        super(Alien, self).__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 获取脚本所在目录，构建图像文件的绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "images", "alien.bmp")

        # Load the alien image, and set its rect attribute.
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= 0:
            return True

        return False

    def update(self):
        """Move the alien right."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    # def blitme(self):
    #     """Draw the alien at its current location."""
    #     self.screen.blit(self.image, self.rect)
