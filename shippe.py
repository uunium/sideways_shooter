"""Module for creating and managing the Ship."""

import pygame
from settingsu import Settings


class Ship(pygame.sprite.Sprite):
    """Class for ship creation and management.

    Has methods for ship movement, boosting and deboosting,
    """

    gamecalss: "Game"
    screen: pygame.Surface
    screen_rect: pygame.Rect
    settings: "Settings"
    ship_path: str
    image: pygame.Surface
    rect: pygame.Rect
    move_up: bool
    move_down: bool
    y: float
    boost_time: int

    def __init__(self, gameclass: "Game") -> None:
        """Create the ship and center it on the screen."""
        super().__init__()

        self.gameclass = gameclass
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings

        self.ship_path = "images/White_Ship_Space.png"

        # load image as surface and rotate it 90 degrees clockwise, and
        # scale it 20%
        self.image = pygame.image.load(self.ship_path).convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale_by(self.image, 1.5)

        self.rect = self.image.get_rect()

        self.rect.midleft = self.screen_rect.midleft

        self.move_up = False
        self.move_down = False

        self.y = float(self.rect.y)

        self.boost_time = 0

    def _moving(self) -> None:
        """Move the ship up or down."""
        if self.move_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        elif self.move_down and self.rect.bottom <= self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.y = self.y

    def _center_ship(self) -> None:
        """Center ship on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)

    def _boost_ship(self) -> None:
        """Boost ship in the direction of movement."""
        self.settings.bb_speed = self.settings.ship_speed
        self.boost_time = self.gameclass.timer
        self.settings.ship_speed *= 3
        self.settings.boost_active = True
        print("Ship boosted")

    def _deboost_ship(self) -> None:
        """Revert ship speed to normal after boost."""
        if (
            self.settings.boost_active
            and self.gameclass.timer - self.boost_time >= self.settings.boost_duration
        ):
            self.settings.ship_speed = self.settings.bb_speed
            self.settings.bb_speed = 0
            self.settings.boost_active = False
            print("Ship deboosted")

    def _update_ship(self) -> None:
        """Update the position of the ship."""
        self._moving()
        self._deboost_ship()

    def blitme(self) -> None:
        """Draw the ship on the screen."""
        self.screen.blit(self.image, self.rect)
