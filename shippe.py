import pygame


class Ship:

    def  __init__(self, gameclass) -> None:
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings

        self.ship_path = (r'C:\Users\uuniu\Documents\Python\Crash_course_python'
                            r'\alieninvasion\images/White_Ship_Space.png'
                        )

        # load image as surface and rotate it 90 degrees clockwise, and
        # scale it 20%
        self.image = pygame.image.load(self.ship_path)
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale_by(self.image, 1.2)
        
        self.rect = self.image.get_rect()

        self.rect.midleft = self.screen_rect.midleft

        self.move_up = False
        self.move_down = False

        self.y = float(self.rect.y)

    def moving(self):
        '''Move the ship up or down'''

        if self.move_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        elif self.move_down and self.rect.bottom <= self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.y = self.y


    def _update_ship(self):
        self.moving()


    def blitme(self):
        self.screen.blit(self.image, self.rect)