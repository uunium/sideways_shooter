import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, gameclass,) -> None:
        super().__init__()

        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings
        self.ship = gameclass.ship.rect

        self.bullet_height = 5
        self.bullet_width = 20
        self.bullet_color = (255, 0, 0)

        self.generate_rect()

        self.x = float(self.rect.x)

    def generate_rect(self):
        self.rect = pygame.Rect(0, 0,
                        self.bullet_width, 
                        self.bullet_height
                        )
        self.rect.midright = self.ship.midright

    def update(self):
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.bullet_color,
                         self.rect
                         )
    

