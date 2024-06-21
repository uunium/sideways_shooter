import pygame, sys


from shippe import Ship
from settings import Settings
from bullette import Bullet

# https://opengameart.org/content/space-9

class Game:
    
    def __init__(self) -> None:
        pygame.init()

        self.settings = Settings(self)
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.screen_rect = self.screen.get_rect()
        self.background = pygame.image.load('./images/space.png').convert()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()


    def run_game(self):
        while True:
            self._update_screen()
            self._check_events()
            self.ship._update_ship()
            self._update_bullets()

    
    def _check_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.KEYDOWN:
                    self._keydown_event(event)
                case pygame.KEYUP:
                    self._keyup_event(event)


    def _keydown_event(self, event):
        match (event.key):
            case pygame.K_UP | pygame.K_w:
                self.ship.move_up = True
            case pygame.K_DOWN | pygame.K_s:
                self.ship.move_down = True
            case pygame.K_SPACE | pygame.K_RIGHT:
                self._shoot_bullet()


    def _shoot_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)


    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen_rect.right:
                self.bullets.remove(bullet)


    def _keyup_event(self, event):
        match (event.key):
            case pygame.K_UP | pygame.K_w:
                self.ship.move_up = False
            case pygame.K_DOWN | pygame.K_s:
                self.ship.move_down = False

    
    def _update_screen(self):
        self.clock.tick(self.settings.framerate)
        self._fill_background()
        # self.screen.fill(self.settings.screen_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()


    def _fill_background(self):
        for y in range(0, self.screen.get_height(), self.background.get_height()):
            for x in range(0, self.screen.get_width(), self.background.get_width()):
                self.screen.blit(self.background, (x, y))

if __name__ == '__main__':
    gameinst = Game()
    gameinst.run_game()