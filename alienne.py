"""Module contains a Class called Alien to create alien instances.

This class is superceded by pygame's Sprite class.
It includes method to udpate the position of an alien
and a method to check wheter an alien have reached top or bottom of the screen.
"""

import pygame


class Alien(pygame.sprite.Sprite):
    """Class to create, move and check the position of an alien."""

    screen: pygame.Surface
    screen_rect: pygame.Rect
    settings: "Settings"
    ship: pygame.Rect
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, gameclass: "Game") -> None:
        """Initialise the alien sprite."""
        super().__init__()

        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings
        self.ship = gameclass.ship.rect
        # declare the image path and load the image
        image_path = "images/alien.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self) -> None:
        """Update the coordinates of an alien."""
        self.rect.y += self.settings.alien_ver_speed * self.settings.alien_direction

    def check_edges(self) -> bool:
        """Check if alien reached top or bottom of the screen.

        Return True if alien sprite touches top or bottom of the screen
        """
        return (self.rect.top <= 0) or (self.rect.bottom >= self.screen_rect.bottom)
