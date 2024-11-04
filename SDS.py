import pygame, sys
from time import sleep


from shippe import Ship
from settingsu import Settings
from bullette import Bullet
from alienne import Alien
from menu import Menu
from scoreboarde import Scoreboard

# https://opengameart.org/content/space-9


class Game:

    def __init__(self) -> None:
        pygame.init()

        self.settings = Settings(self)
        self.clock = pygame.time.Clock()
        self.timer = 0

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.screen_rect = self.screen.get_rect()
        self.game_active = False
        self.background = pygame.image.load("./images/space.png").convert()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = 0
        self.shoot_bullet_mod = False
        self.aliens = pygame.sprite.Group()
        self.sb = Scoreboard(self)
        self.menu = Menu(self)
        self._create_fleet()

    def run_game(self):
        while True:
            self._update_screen()
            self._check_events()
            if self.game_active:
                timer = self.clock.get_time()
                self.timer += timer
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
                case pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.menu._button_press(mouse_pos)
                
    def _keydown_event(self, event):
        match (event.key):
            case pygame.K_UP | pygame.K_w:
                self.ship.move_up = True
            case pygame.K_DOWN | pygame.K_s:
                self.ship.move_down = True
            case pygame.K_SPACE | pygame.K_RIGHT:
                if self.game_active:
                    self.shoot_bullet()
                    self.shoot_bullet_mod = True
                elif event.key == pygame.K_SPACE:
                    self.game_active = True
            case pygame.K_q:
                sys.exit()

    def _keyup_event(self, event):
        match (event.key):
            case pygame.K_UP | pygame.K_w:
                self.ship.move_up = False
            case pygame.K_DOWN | pygame.K_s:
                self.ship.move_down = False
            case pygame.K_SPACE:
                    if self.game_active:
                        self.shoot_bullet_mod = False

    def shoot_bullet(self):
        '''Create a bullet instance and draw it,
        also save the time of the shot'''
        self.last_shot_time = pygame.time.get_ticks()
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        print('Bullet shot')

    def _update_bullets(self):
        # Get time difference betwen shots to have aftofire every self.settings.shot_delay miliseconds
        shot_time_diff = pygame.time.get_ticks() - self.last_shot_time
        if self.shoot_bullet_mod and shot_time_diff >= self.settings.shot_delay:
            self.shoot_bullet()
            
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collision:
            for kill in collision.values():
                self.sb.update_score()
                self.menu._create_score()
                self.menu._create_high_score()
                
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
                self.settings.alien_direction *= -1
                break

    def _fleet_check_earth_contact(self):
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                print('Earth reached')
                self._ship_hit()
                break

    # def _move_hor(self):
    #     '''used to continue horizontal movement of aliens'''
    #     move_duration = pygame.time.get_ticks() - self.hor_move_start
    #     if move_duration > 500:
    #             self.settings.alien_ver_speed = self._previous_ver_speed
    #             self.settings.alien_movement_counter = 0

    # def _save_ver_speed(self):
    #     '''used to save current movement speed of the ship and 
    #     nulify it for smooth alien movement'''
    #     if self.settings.alien_ver_speed != 0:
    #         self._previous_ver_speed = self.settings.alien_ver_speed
    #         self.settings.alien_ver_speed = 0
    #         print('Border reached')

    def _ship_hit(self):
        if self.settings.ships_left  > 1:
            self.settings.ships_left -= 1
            sleep(0.5)
            self.aliens.empty()
            self.bullets.empty()
            self.ship._center_ship()
            self._create_fleet()
            # self.settings._reset_stuff()
        else:
            self.game_active = False

    def _check_collision(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print('Ship hit')
            self._ship_hit()
            self.menu._create_lives()

    def _update_aliens(self):
        self._fleet_check_borders()
        self._fleet_check_earth_contact()
        self.aliens.update()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            # self.settings._reset_stuff()
            self.sb.update_game_speed()

        self._check_collision()
        
    def _update_screen(self):
        self.clock.tick(self.settings.framerate)
        self._blit_background()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.menu.show_menu()
        if not self.game_active:
            self.menu.start_button.draw_button()
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
