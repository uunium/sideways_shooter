import pygame


class Alien(pygame.sprite.Sprite):

    def __init__(self, gameclass) -> None:
        super().__init__()

        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings
        self.ship = gameclass.ship.rect

        image_path = "images/alien.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += self.settings.alien_ver_speed * self.settings.alien_direction

    def check_edges(self):
        return (self.rect.top <= 0) or (self.rect.bottom >= self.screen_rect.bottom)
