import pygame
from time import sleep


from shippe import Ship
from settingsu import Settings
from bullette import Bullet
from alienne import Alien
from menu import Menu
from scoreboarde import Scoreboard
from bar_timer import Timer
from highscore import hiscore as hiscore_file


# https://opengameart.org/content/space-9
# https://opengameart.org/content/sleek-bars
# https://opengameart.org/content/ship-space-0
# https://opengameart.org/content/space-shooter-top-down-2d-pixel-art


class Game:
    """Main class to run the game."""

    def __init__(self) -> None:
        """Create all needed instances to run the game."""
        pygame.init()

        self.settings = Settings(self)
        self.clock = pygame.time.Clock()
        self.timer = 0
        self.hsf = hiscore_file

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        # Give the game window a name
        pygame.display.set_caption("Sideways Alien Shooter")
        # Get screen rect
        self.screen_rect = self.screen.get_rect()
        self.game_active = False
        self.background = pygame.image.load("./images/space.png").convert()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.last_shot_time: int = 0
        self.last_mega_shot_time: int = 0
        self.shoot_bullet_mod: bool = False
        self.aliens = pygame.sprite.Group()
        self.sb = Scoreboard(self)
        self.menu = Menu(self)
        self.mega_bullet = None

        self.mega_shot_bar = Timer(
            self,
            (0, 255, 0),
            action_time=self.last_mega_shot_time,
            delay=self.settings.mega_shot_delay,
            x=(self.screen_rect.width - 136),
            y=(self.screen_rect.height - 100),
        )

        self.boost_bar = Timer(
            self,
            (0, 153, 255),
            action_time=self.ship.boost_time,
            delay=self.settings.boost_delay,
            x=(self.screen_rect.width - 136),
            y=(self.screen_rect.height - 150),
        )

        self._create_fleet()

    def run_game(self) -> None:
        """Run the game.

        Update the screen with self._update_screen
        Check for events with self_check events
        and update the positions of srites and images if self.game_active is True
        """
        while True:
            self._update_screen()
            self._check_events()
            if self.game_active:
                timer = self.clock.get_time()
                self.timer += timer
                self.ship._update_ship()
                self._update_bullets()
                self._update_aliens()

    def _check_events(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.menu._exit_game()
                case pygame.KEYDOWN:
                    self._check_keydown_event(event)
                case pygame.KEYUP:
                    self._check_keyup_event(event)
                case pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.menu._button_press(mouse_pos)

    def _check_keydown_event(self, event: pygame.event.EventType) -> None:
        match event.key:
            case pygame.K_UP | pygame.K_w:
                self.ship.move_up = True
            case pygame.K_DOWN | pygame.K_s:
                self.ship.move_down = True
            case pygame.K_SPACE | pygame.K_RIGHT:
                if self.game_active:
                    self.shoot_bullet()
                    self.shoot_bullet_mod = True
                elif event.key == pygame.K_SPACE and self.sb.game_state != "Pause":
                    self.menu._button_press(self.menu.start_button.rect.center)
            case pygame.K_LSHIFT:
                self.boost_ship()
            case pygame.K_LCTRL:
                self.mega_shot()
            case pygame.K_ESCAPE | pygame.K_PAUSE | pygame.K_p:
                if self.sb.game_state == "Start":
                    self.menu._button_press(self.menu.start_button.rect.center)
                else:
                    self.menu.pause_game()
            case pygame.K_q:
                self.menu._exit_game()

    def _check_keyup_event(self, event: pygame.event.EventType) -> None:
        match event.key:
            case pygame.K_UP | pygame.K_w:
                self.ship.move_up = False
            case pygame.K_DOWN | pygame.K_s:
                self.ship.move_down = False
            case pygame.K_SPACE:
                if self.game_active:
                    self.shoot_bullet_mod = False

    def shoot_bullet(self) -> None:
        """Create a bullet instance and draw it.

        Also save the time of the shot
        """
        # save the shot time
        self.last_shot_time = pygame.time.get_ticks()
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        print("Bullet shot")

    def mega_shot(self) -> None:
        """Create mega bullet."""
        # check whether mega shot timer is reset
        if self.timer - self.last_mega_shot_time >= self.settings.mega_shot_delay:
            # save the shot time
            self.last_mega_shot_time = self.timer
            # create the bullet and change it's size and colour
            self.mega_bullet = Bullet(self)
            self.mega_bullet.bullet_height *= 5
            self.mega_bullet.bullet_width *= 5
            self.mega_bullet.bullet_color = (0, 255, 0)
            self.mega_bullet._generate_rect()
            # reset the progres of Bar GUI
            self.mega_shot_bar.reset_bar(self.last_mega_shot_time)
            print("Mega bullet shot")

    def _update_bullets(self) -> None:
        """Process the bullet position and check for collisions.

        Also get the time difference betwen shots to have
        autofire every self.settings.shot_delay miliseconds
        """
        # get the time difference betwen shots
        shot_time_diff = pygame.time.get_ticks() - self.last_shot_time
        if self.shoot_bullet_mod and shot_time_diff >= self.settings.shot_delay:
            self.shoot_bullet()

        # work with bullets
        # check for collision
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collision:
            for _ in collision.values():
                # for each collision call sb.bullet_hit()
                # which rises the score and removes a bullet and an alien
                self.sb.bullet_hit(self.menu)
        # update the coordinates of the bullets
        self.bullets.update()
        # if a bullet leaves the screen coordinates - delete it
        # also call sb.bullet_missed()
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen_rect.right:
                self.sb.bullet_missed(self.menu, bullet)
                print("Bullet deleted")

        # work with Mega Shot if it is alive
        # logic is similar to the standard bullet
        if self.mega_bullet is not None:
            mega_collision = pygame.sprite.spritecollide(
                self.mega_bullet, self.aliens, True
            )
            if mega_collision:
                for _ in mega_collision:
                    self.sb.bullet_hit(self.menu)
            self.mega_bullet.update()

            if self.mega_bullet.rect.left >= self.screen_rect.right:
                self.mega_bullet = None

    def _create_fleet(self) -> None:
        """Create a fleet of aliens.

        Create a fleet of aliens 8 by 4 in size.
        """
        # create the first alien to position everything else
        adam = Alien(self)
        # position the first alien 15 ship widthes away from the ship
        x = self.ship.rect.width * 15
        # position the first alien 8 alien heights from the screen center
        y = self.screen_rect.centery - adam.rect.height * 8

        # 4 rows of aliens
        for _ in range(4):
            # 8 lines of aliens
            for _ in range(8):
                new_alien = Alien(self)
                new_alien.rect.y = y
                new_alien.rect.x = x
                self.aliens.add(new_alien)
                # space the aliens lines 2 alien heights apart
                y += new_alien.rect.height * 2
                print("Alien created")
            # space the alien rows 2 alien widthes apart
            x += adam.rect.width * 2
            # reset the y position
            y = self.screen_rect.centery - adam.rect.height * 8
            print("New Fleet row created")

    def _check_fleet_borders(self) -> None:
        """Reverse the direction of alien movement.

        If one of the aliens in the group reaches top or bottom of the screen
        turn the whole group back.
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                for each_alien in self.aliens.sprites():
                    each_alien.rect.x -= self.settings.alien_hor_speed
                self.settings.alien_direction *= -1
                break

    def _check_fleet_earth_contact(self) -> None:
        """Check if aliens reached the earth."""
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                print("Earth reached")
                self._ship_hit()
                break

    def _ship_hit(self) -> None:
        """Restart level if ship is hit.

        If ship has more than 1 life left:
        - lover the number of lives.
        - restart the level by clearing everything and centering the ship.

        If not:
        Deactivate the game via game_active and
        change the sb.game_state to 'Fail'.
        """
        if self.settings.ships_left > 1:
            self.settings.ships_left -= 1
            sleep(0.5)
            self.aliens.empty()
            self.bullets.empty()
            self.ship._center_ship()
            self._create_fleet()

            # _create_lives() should be here to update the number of lives
            # after every contact with the aliens
            self.menu._create_lives()
        else:
            self.game_active = False
            self.sb.game_state = "Fail"

    def _check_collision(self) -> None:
        """Check whether ship and aliens rectangles touch.

        If they are - call _ship_hit() and redraw lives GUI.
        """
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit")
            self._ship_hit()
            self.menu._create_lives()

    def boost_ship(self) -> None:
        """Check if boost was replenished.

        Use ship.boost_ship() and then reset boost meter progres with boost_bar.reset_bar().
        """
        if self.timer - self.ship.boost_time >= self.settings.boost_delay:
            self.ship._boost_ship()
            self.boost_bar.reset_bar(self.ship.boost_time)

    def _update_aliens(self) -> None:
        self._check_fleet_borders()
        self._check_fleet_earth_contact()
        self.aliens.update()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.sb.update_game_speed()
            if self.sb.level == 21:
                self.game_active = False
                self.sb.game_state = "Win"
                self.sb.save_hiscore()

        self._check_collision()

    def _blit_background(self) -> None:
        for y in range(0, self.screen.get_height(), self.background.get_height()):
            for x in range(0, self.screen.get_width(), self.background.get_width()):
                self.screen.blit(self.background, (x, y))

    def _update_screen(self) -> None:
        """Call methods to draw all the necessary stuff on the screen."""
        self.clock.tick(self.settings.framerate)
        self._blit_background()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.menu._show_interface()
        self.mega_shot_bar.blit_bar()
        self.boost_bar.blit_bar()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        if self.mega_bullet is not None:
            self.mega_bullet.draw_bullet()
        if not self.game_active:
            self.menu.choose_state()
        pygame.display.flip()


if __name__ == "__main__":
    gameinst = Game()
    gameinst.run_game()
