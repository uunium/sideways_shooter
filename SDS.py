import pygame, sys


from ship import Ship


class Game:
    
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()

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
        self.clock.tick(60)
        self.screen.fill((0, 0, 0))
        self.ship.blitme()
        pygame.display.flip()
