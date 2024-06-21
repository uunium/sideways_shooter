import pygame, sys


from ship import Ship
from settings import Settings


class Game:
    
    def __init__(self) -> None:
        pygame.init()

        self.settings = Settings(self)
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.screen_rect = self.screen.get_rect()
        
        self.ship = Ship(self)



    

    def run_game(self):
        while True:
            self._update_screen()
            self._check_events()

    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
    
    def _update_screen(self):
        self.clock.tick(self.settings.framerate)
        self.screen.fill(self.settings.screen_color)
        self.ship.blitme()
        pygame.display.flip()


if __name__ == '__main__':
    gameinst = Game()
    gameinst.run_game()