"""Module for creation of a progress bar for an ability.

Has methods to reset the bar progress, and draw the bar to the screen.
"""

import pygame
from settingsu import Settings


class Timer:
    """Class for a progress bar for an ability."""

    gameclass: "Game"
    screen: pygame.Surface
    screen_rect: pygame.Rect
    settings: Settings
    bar_path: str
    bar_image_rect: pygame.Rect
    action_time: int
    fill_colour: tuple[int, int, int]
    fill_tagle_sur: pygame.Surface
    fill_tagle_rect: pygame.Rect

    def __init__(
        self,
        gameclass: "Game",
        colour: tuple,
        action_time: int,
        delay: int,
        x: int = 0,
        y: int = 0,
    ) -> None:
        """Initialize the progress bar."""
        self.gameclass = gameclass
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings
        # declare empty bar path and load the bar image
        self.bar_path = "images/empty_bar.png"
        self.bar_image = pygame.image.load(self.bar_path).convert_alpha()

        self.bar_image_rect = self.bar_image.get_rect()
        self.bar_image_rect.x = x
        self.bar_image_rect.y = y
        # declare the bar parameters
        # action time is the time when the bar was reset
        self.action_time = action_time
        # how long is the cooldown
        self.fill_duration = delay
        self.fill_colour = colour

        self._create_fill()

    def _create_fill(self, x: float = 0) -> None:
        """Create a texture which fills the bar.

        x is the texture width. It should be invisible at the beginning
        so the initial width is 0.
        """
        self.fill_tagle_sur = pygame.Surface((x, 22))
        self.fill_tagle_sur.fill(color=self.fill_colour)
        self.fill_tagle_rect: pygame.Rect = self.fill_tagle_sur.get_rect()
        bar_image_side_width: int = 4
        self.fill_tagle_rect.topleft = (
            (self.bar_image_rect.x + bar_image_side_width),
            (self.bar_image_rect.y + bar_image_side_width),
        )

    # when active should fill up untill full. step 4 pixel from each side.
    # height is 30 pix, length is 126 pix.

    def reset_bar(self, action_time: int) -> None:
        """Reset the filling width in the bar."""
        self._create_fill(0)
        self.action_time = action_time

    def blit_bar(self) -> None:
        """Draw the bar and it's filling."""
        time_passed: int = self.gameclass.timer - self.action_time

        if time_passed <= self.fill_duration:
            # 118 is the width of the fillable space inside a bar (in pixels)
            perc: float = (time_passed / self.fill_duration) * 118
            self._create_fill(perc)

        self.screen.blit(self.bar_image, self.bar_image_rect)
        self.screen.blit(self.fill_tagle_sur, self.fill_tagle_rect)
