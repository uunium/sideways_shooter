import pygame, pathlib


class Ship:

    def  __init__(self, gameclass) -> None:
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect

        self.ship_path = (r'C:\Users\uuniu\Documents\Python\Crash_course_python'
                            r'\alieninvasion\images/White_Ship_Space.png'
                        )
        # load image as surface and rotate it 90 degrees clockwise
        
        self.image = pygame.transform.rotate(
                    (pygame.image.load(self.ship_path)), -90
                    )
        
        self.rect = self.image.get_rect()

        self.rect.midleft = self.screen_rect.midleft

    def blitme(self):
        self.screen.blit(self.image, self.rect)