import pygame, sys
from time import sleep


from shippe import Ship
from settingsu import Settings
from bullette import Bullet
from alienne import Alien
from stattssu import GameStats

# https://opengameart.org/content/space-9


class Game:

    def __init__(self) -> None:
        pygame.init()

        self.settings = Settings()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.screen_rect = self.screen.get_rect()
        self.stats = GameStats(self)
        self.game_active = True
        self.background = pygame.image.load("./images/space.png").convert()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        while True:
            self._update_screen()
            self._check_events()
            if self.game_active:
                self.ship._update_ship()
                self._update_bullets()
                self._update_aliens()

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
            case pygame.K_q:
                sys.exit()

    def _keyup_event(self, event):
        match (event.key):
            case pygame.K_UP | pygame.K_w:
                self.ship.move_up = False
            case pygame.K_DOWN | pygame.K_s:
                self.ship.move_down = False

    def _shoot_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        print('Bullet shot')

    def _update_bullets(self):
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen_rect.right:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        adam = Alien(self)
        x = self.ship.rect.width * 15
        y = self.screen_rect.centery - adam.rect.height * 8

        for row in range(4):
            for line in range(8):
                new_alien = Alien(self)
                new_alien.rect.y = y
                new_alien.rect.x = x
                self.aliens.add(new_alien)
                y += new_alien.rect.height * 2
                print("Alien created")

            x += adam.rect.width * 2
            y = self.screen_rect.centery - adam.rect.height * 8
            print("New Fleet row created")

    def _fleet_check_borders(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                for alien in self.aliens.sprites():
                    alien.rect.x -= self.settings.alien_hor_speed
                self._save_ver_speed()
                self.settings.alien_movement_counter += 1
                self._count_hor_movement()
                break

    def _fleet_check_earth_contact(self):
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                print('Earth reached')
                self._ship_hit()
                break

    def _count_hor_movement(self):
        '''used to continue horizontal movement of aliens'''
        if self.settings.alien_movement_counter == 10:
                self.settings.alien_direction *= -1
                self.settings.alien_ver_speed = self._previous_ver_speed
                self.settings.alien_movement_counter = 0

    def _save_ver_speed(self):
        '''used to save current movement speed of the ship and 
        nulify it for smooth alien movement'''
        if self.settings.alien_ver_speed != 0:
            self._previous_ver_speed = self.settings.alien_ver_speed
            self.settings.alien_ver_speed = 0
            print('Border reached')

    def _ship_hit(self):
        if self.stats.ships_left  > 0:
            self.stats.ships_left -= 1
            sleep(0.5)
            self.aliens.empty()
            self.bullets.empty()
            self.ship._center_ship()
            self._create_fleet()
            self.settings._reset_stuff(self)
        else:
            self.game_active = False

    def _check_collision(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print('Ship hit')
            self._ship_hit()

    def _update_aliens(self):
        self._fleet_check_borders()
        self._fleet_check_earth_contact()
        self.aliens.update()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
        self._check_collision()
        
    def _update_screen(self):
        self.clock.tick(self.settings.framerate)
        self._blit_background()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()

    def _blit_background(self):
        for y in range(0, self.screen.get_height(), self.background.get_height()):
            for x in range(0, self.screen.get_width(), self.background.get_width()):
                self.screen.blit(self.background, (x, y))


if __name__ == "__main__":
    gameinst = Game()
    gameinst.run_game()
