"""Module contains a Button class for GUI items."""

from __future__ import annotations
import pygame
from settingsu import Settings


class Button:
    """Class to create a button.

    Class have methods to hide, show and draw the button.
    """

    screen: pygame.Surface
    screen_rect: pygame.Rect
    settings: Settings
    width: int
    height: int
    button_color: tuple[int, int, int] | None
    text_color: tuple[int, int, int]
    font: pygame.font.Font
    name: str
    rect: pygame.Rect
    button_rect: pygame.Rect

    def __init__(
        self,
        gameclass: "Game",
        msg: str,
        tx_size: int = 48,
        height: int = 50,
        width: int = 200,
        bg_color: tuple[int, int, int] | None = (0, 135, 0),
        tx_color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        """Initialise the button."""
        # gameclass links
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings

        # button parameters
        self.width, self.height = width, height
        self.button_color = bg_color
        self.text_color = tx_color
        self.font = pygame.font.SysFont(None, tx_size)

        # rect parameters
        self.rect = pygame.Rect(0, 0, width, height)
        self.button_rect = self.rect
        self.rect.center = self.screen_rect.center

        # Prepare message (render text)
        self._prep_msg(msg)

    def _prep_msg(self, msg: str) -> None:
        """Render the text message.

        Creates the surface with the provided msg and centers it to the button rectangle.
        """
        if self.button_color is not None:
            self.msg_image = self.font.render(
                msg, True, self.text_color, self.button_color
            )
        else:
            self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.center = self.rect.center

    def hide_button(self) -> None:
        """Move the button rectangle from the screen.

        Changes the x coordinate to "-1000".
        """
        if self.rect.x != -1000:
            self.rect.x = -1000
            print("Button hid")

    def show_button(self) -> None:
        """Move the button back to the screen.

        If the button x coordiante is "-1000" moves the button back to the original coordinates.
        """
        if self.rect.x == -1000:
            print("Button checked")
            self.rect.x = self.button_rect.x

    def save_button_loc(self) -> None:
        """Save the current coordinates of the button."""
        if self.rect.x != -1000:
            self.button_rect = self.rect.copy()
            print("Button position saved")

    def draw_button(self) -> None:
        """Draw the button on the screen."""
        if self.button_color is not None:
            self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_rect)
