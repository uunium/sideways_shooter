import pygame


class Ship:

    def  __init__(self, gameclass) -> None:
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect

        self.image = pygame.image.load('../images/White_Ship_Space.png')
        self.rect = self.image.get_rect()

        self.rect.bottom = self.screen_rect.left

    def blitme(self):
        self.screen.blit(self.image, self.rect)