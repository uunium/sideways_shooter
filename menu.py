"""Module for creation of GUI."""

from pygame.sprite import Group
import sys
import pygame

from buttons import Button
from shippe import Ship
import load_save


class Menu:
    """Create GUI.

    Class have methods to pause or unpase the game. and chose the menu to show.
    """

    def __init__(self, gameclass: "Game") -> None:
        """Create the GUI."""
        self.gameclass = gameclass
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings
        self.sb = gameclass.sb
        self.scores_list: list = []
        self.prev_state: str = "Start"
        self.highest_score: Button | None = None

        # buttons initialized
        self._create_menus()

        self.game_states = {
            "Start": (self.start_button, self.scores_button, self.controls_button),
            "Pause": (
                self.resume_button,
                self.start_button,
                self.scores_button,
                self.controls_button,
            ),
            "Scores": (self._show_scores, self.back_button),
            "Controls": (self._show_controls, self.back_button),
            "Win": (
                self._game_won,
                self.chad_text,
                self.start_button,
                self.scores_button,
                self.controls_button,
            ),
            "Fail": (
                self._game_lost,
                self.looser_text,
                self.start_button,
                self.scores_button,
                self.controls_button,
            ),
            "Buttons": (
                self.start_button,
                self.scores_button,
                self.controls_button,
                self.resume_button,
                self.back_button,
            ),
            "Game Active": None,
        }

    def _button_press(self, mouse_pos: tuple[int, int]) -> None:
        # clear stuff and activate the game (start a new game)
        if not self.gameclass.game_active:
            if (
                self.start_button.rect.collidepoint(mouse_pos)
                and self.start_button.rect.x != -1000
            ):
                self.gameclass.bullets.empty()
                self.gameclass.aliens.empty()
                self.gameclass._create_fleet()
                self.gameclass.sb.reset_stats()
                load_save.load_game(self.gameclass)
                self._show_interface()
                self.gameclass.game_active = True
                self.sb.game_state = "Game Active"

            # pause or unpause
            elif self.resume_button.rect.collidepoint(mouse_pos):
                self.pause_game()
            # access scores
            elif self.scores_button.rect.collidepoint(mouse_pos):
                self.prev_state = self.sb.game_state
                self.sb.game_state = "Scores"
            elif self.controls_button.rect.collidepoint(mouse_pos):
                self.prev_state = self.sb.game_state
                self.sb.game_state = "Controls"
            elif self.back_button.rect.collidepoint(mouse_pos):
                # think on how back button will work
                self.sb.game_state = self.prev_state

    def _create_high_score(self) -> None:
        # woraround for not creating high score object everytime
        if hasattr(self, "score_counter"):
            del self.hs

        self.hs = Button(
            self.gameclass,
            f"{self.gameclass.sb.high_score:,}".replace(",", " "),
            bg_color=None,
            tx_size=48,
            height=0,
            width=0,
        )
        self.hs.msg_rect.y = 10
        self.hs.msg_rect.x = self.screen_rect.width - self.hs.msg_rect.width - 10

        return None

    def _create_score(self) -> None:
        # woraround for not creating score object everytime
        if hasattr(self, "score_counter"):
            del self.score_counter

        self.score_counter = Button(
            self.gameclass,
            f"{self.gameclass.sb.score:,}".replace(",", " "),
            bg_color=None,
            tx_size=30,
            height=0,
            width=0,
        )
        self.score_counter.msg_rect.topleft = (
            self.screen_rect.width - self.score_counter.msg_rect.width - 10,
            self.hs.msg_rect.bottomleft[1] + 10,
        )

    def _create_level(self) -> None:
        # woraround for not creating level object everytime
        if hasattr(self, "level"):
            del self.level

        self.level = Button(
            self.gameclass,
            f"{self.gameclass.sb.level}",
            bg_color=None,
            tx_size=30,
            height=0,
            width=0,
        )
        self.level.msg_rect.topleft = (
            self.screen_rect.width - self.level.msg_rect.width - 10,
            self.score_counter.msg_rect.bottomleft[1] + 10,
        )

    def _create_lives(self) -> None:
        # woraround for not creating score object everytime
        if hasattr(self, "ship"):
            del self.ship

        self.ship = Group()
        for ship_num in range(self.gameclass.settings.ships_left):
            ship = Ship(self.gameclass)
            ship.rect.x = (
                self.screen_rect.width - ship.rect.width - ship.rect.width * ship_num
            )
            ship.rect.y = self.screen_rect.height - 10 - ship.rect.height
            self.ship.add(ship)

    def _create_resume_button(self) -> None:
        """Create the resume button. Used to create the button and move text lower."""
        self.resume_button = Button(
            self.gameclass,
            "Resume",
            bg_color=(145, 145, 145),
        )
        self.resume_button.rect.y -= 70
        self.resume_button.msg_rect.center = self.resume_button.rect.center

    def _create_scores_button(self) -> None:
        """Create the score button. Used to create the button and move text lower."""
        self.scores_button = Button(
            self.gameclass,
            "Scores",
            bg_color=(145, 145, 145),
        )
        self.scores_button.rect.y = self.scores_button.rect.y + 70
        self.scores_button.msg_rect.center = self.scores_button.rect.center

    def _create_controls_button(self) -> None:
        """Create the controls button. Used to create the button and move text lower."""
        self.controls_button = Button(
            self.gameclass,
            "Controls",
            bg_color=(145, 145, 145),
        )
        self.controls_button.rect.y = self.controls_button.rect.y + 140
        self.controls_button.msg_rect.center = self.controls_button.rect.center

    def _create_back_button(self) -> None:
        """Create the back button. Used to create the button and move text lower."""
        self.back_button = Button(
            self.gameclass,
            "Back",
            bg_color=(145, 145, 145),
        )
        self.back_button.rect.y = self.screen_rect.height - 100
        self.back_button.msg_rect.center = self.back_button.rect.center

    def _create_menus(self) -> None:
        """Create all of the buttons to render later.

        Uses method defined earlier.
        Also creates the Start button.
        """
        self.start_button = Button(
            self.gameclass,
            "New game",
            bg_color=(145, 145, 145),
        )

        self._create_resume_button()
        self._create_scores_button()
        self._create_controls_button()
        self._create_back_button()

        self._create_high_score()
        self._create_score()
        self._create_level()
        self._create_lives()

        self._game_lost()
        self._game_won()

    def _game_lost(self) -> None:
        """Text to render when player looses the game."""
        self.looser_text = Button(
            self.gameclass,
            "You failed to defend The Earth",
            tx_size=60,
            bg_color=None,
            height=0,
            width=0,
        )
        self.looser_text.msg_rect.center = self.screen_rect.center
        self.looser_text.msg_rect.bottom = self.start_button.msg_rect.top - 10

    def _game_won(self) -> None:
        """Text to render when player wins the game."""
        self.chad_text = Button(
            self.gameclass,
            "You defeated the Aliens",
            tx_size=60,
            bg_color=None,
            height=0,
            width=0,
        )
        self.chad_text.msg_rect.center = self.screen_rect.center
        self.chad_text.msg_rect.bottom = self.start_button.msg_rect.top - 10

    def pause_game(self) -> None:
        """Change game_paused flag to an appropriate one.

        Hides or shows buttons depending on game_active flag
        """
        if self.gameclass.game_active:
            self.gameclass.game_active = False
            self.gameclass.shoot_bullet_mod = False
            self.sb.game_state = "Pause"
        elif not self.gameclass.game_active and self.sb.game_state == "Pause":
            self.sb.game_state = "Game Active"
            self.gameclass.game_active = True

    def _show_controls(self) -> None:
        """Render the controls screen image.

        Load the controls.png image and blits it on the screen
        """
        if self.prev_state != "Controls":
            self.controls_image = pygame.image.load(
                "./images/controls.png"
            ).convert_alpha()
            self.controls_image_rect = self.controls_image.get_rect()
            self.controls_image_rect.center = self.screen_rect.center

        self.screen.blit(self.controls_image, self.controls_image_rect)

    def _show_interface(self) -> None:
        """Draw the GUI on the screen.

        Draws high score, score, level and lives info on the screen.
        """
        self.hs.draw_button()
        self.score_counter.draw_button()
        self.level.draw_button()
        self.ship.draw(self.screen)

    def _show_scores(self) -> None:
        """Generate surfaces of Highest score to draw them on screen."""
        # Create "Highest scores" string to crown scores
        if not self.highest_score:
            self.highest_score = Button(
                self.gameclass,
                "Highest Scores",
                80,
                bg_color=None,
                height=0,
                width=0,
            )
            self.highest_score.rect.centerx = self.screen_rect.centerx
            self.highest_score.rect.y = 100
            self.highest_score.msg_rect.center = self.highest_score.rect.center

            # Create list of surfaces to show the score
            self.scores_list.clear()
            yval = self.highest_score.rect.bottom + 20
            for score in self.gameclass.hsf:
                yval += 50
                score_text_button = Button(
                    self.gameclass,
                    f"{self.gameclass.hsf.index(score) + 1}. {str(score)}",
                    tx_size=60,
                    bg_color=None,
                    height=0,
                    width=0,
                )
                score_text_button.rect.centerx = self.screen_rect.centerx
                score_text_button.rect.y = yval
                score_text_button.msg_rect.center = score_text_button.rect.center
                yval += score_text_button.rect.height
                self.scores_list.append(score_text_button)

        self.highest_score.draw_button()
        for score in self.scores_list:
            score.draw_button()

    def _screen_state(self, state: str) -> None:
        print(state)
        if self.sb.game_state != "Game Active":
            for _button in self.game_states["Buttons"]:
                if _button not in self.game_states[state] and _button.rect.x != -1000:
                    _button.save_button_loc()
                    _button.hide_button()
            for button in self.game_states[state]:
                if callable(button):
                    button()
                elif isinstance(button, Button):
                    button.show_button()
                    button.draw_button()
        elif self.sb.game_state == "Game Active":
            for _button in self.game_states["Buttons"]:
                if _button.rect.x != -1000:
                    _button.save_button_loc()
                    _button.hide_button()

    def render_state(self) -> None:
        """Draw GUI on the screen depending on the current sg.game_state."""
        self._update_menus()
        self._screen_state(self.sb.game_state)
        pygame.display.flip()

    def _update_menus(self) -> None:
        self.gameclass._check_events()
        self.gameclass.clock.tick(self.settings.framerate)
        self.gameclass._blit_background()
        self.gameclass.ship.blitme()
        self.gameclass.aliens.draw(self.screen)
        self._show_interface()
        self.gameclass.mega_shot_bar.blit_bar()
        self.gameclass.boost_bar.blit_bar()

        for bullet in self.gameclass.bullets.sprites():
            bullet.draw_bullet()
        if self.gameclass.mega_bullet is not None:
            self.gameclass.mega_bullet.draw_bullet()

    def _exit_game(self) -> None:
        self.gameclass.sb.save_hiscore()
        load_save.save_game(self.gameclass)
        sys.exit()
