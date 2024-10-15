import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, gameclass) -> None:
        super().__init__()

        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings
        self.ship = gameclass.ship.rect

        self.bullet_height = 700
        self.bullet_width = 10
        self.rect = pygame.Rect(0, 0,
                                self.bullet_width, 
                                self.bullet_height
                                )
        self.rect.midright = self.ship.midright
        self.x = float(self.rect.x)


    def update(self):
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.settings.bullet_color,
                         self.rect
                         )
    

