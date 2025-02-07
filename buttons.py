import pygame


class Button:
    def __init__(
        self,
        gameclass,
        msg: str,
        tx_size: int = 48,
        height: int = 50,
        width: int = 200,
        bg_color: tuple = (0, 135, 0),
        tx_color: tuple = (255, 255, 255),
    ) -> None:

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
        self.rect.center = self.screen_rect.center

        # Prepare message (render text)
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        if self.button_color != None:
            self.msg_image = self.font.render(
                msg, True, self.text_color, self.button_color
            )
        else:
            self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.center = self.rect.center

    def draw_button(self):
        if self.button_color != None:
            self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_rect)
