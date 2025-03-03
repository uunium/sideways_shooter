"""Module for creation of a bullet.

Has methods for updating the position of a bullet and drawing the bullet.
"""

import pygame
from settingsu import Settings
from shippe import Ship


class Bullet(pygame.sprite.Sprite):
    """Class for creation of a bullet."""

    screen: pygame.Surface
    screen_rect: pygame.Rect
    settings: Settings
    ship: Ship
    bullet_height: int
    bullet_width: int
    bullet_color: tuple[int, int, int]

    def __init__(self, gameclass: "Game") -> None:
        """Initialise the bullet instance and generate it's rect."""
        super().__init__()

        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings
        self.ship = gameclass.ship.rect
        # declare bullet parameters
        self.bullet_height = 5
        self.bullet_width = 20
        self.bullet_color = (255, 0, 0)

        self._generate_rect()
        # convert coordinate to a float for precision reasons
        self.x = float(self.rect.x)

    def _generate_rect(self) -> None:
        """Generate a rectagle for a bullet.

        Also move the right side of the bullet to the nose of the ship.
        """
        self.rect = pygame.Rect(0, 0, self.bullet_width, self.bullet_height)
        self.rect.midright = self.ship.midright

    def update(self) -> None:
        """Update the position of a bullet."""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self) -> None:
        """Draw a bullet to the screen."""
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)
