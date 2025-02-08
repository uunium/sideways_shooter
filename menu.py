from pygame.sprite import Group
import sys
import pygame

from buttons import Button
from shippe import Ship


class Menu:
    def __init__(self, gameclass) -> None:
        self.gameclass = gameclass
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings
        self.sb = self.gameclass.sb
        self.scores_list = []

        self._create_menus()

    def _button_press(self, mouse_pos):
        # дії для початку гри
        if (
            self.start_button.rect.collidepoint(mouse_pos)
            and not self.sb.game_paused
            and not self.sb.scores_active
            and not self.gameclass.game_active
        ) or (
            self.again_button.rect.collidepoint(mouse_pos)
            and not self.sb.game_paused
            and not self.sb.scores_active
            and self.sb.game_won
        ):
            self.gameclass.bullets.empty()
            self.gameclass.aliens.empty()
            self.gameclass._create_fleet()
            self.gameclass.sb.reset_stats()
            self.gameclass.game_active = True
        # дії для зняття паузи
        elif (
            self.resume_button.rect.collidepoint(mouse_pos)
            and self.sb.game_paused
            and not self.sb.scores_active
            and not self.gameclass.game_active
        ):
            self.pause_game()
        # access scores
        elif (
            (
                self.scores_button.rect.collidepoint(mouse_pos)
                and not self.sb.game_paused
                and not self.gameclass.game_active
            )
            or self.scores_button.rect.collidepoint(mouse_pos)
            and self.sb.game_paused
            and not self.gameclass.game_active
        ):
            self.sb.scores_active = True
        elif (
            (
                self.controls_button.rect.collidepoint(mouse_pos)
                and not self.sb.game_paused
                and not self.gameclass.game_active
            )
            or self.controls_button.rect.collidepoint(mouse_pos)
            and self.sb.game_paused
            and not self.gameclass.game_active
        ):
            self.sb.controls_active = True
        elif (
            self.back_button.rect.collidepoint(mouse_pos)
            and not self.sb.game_paused
            and not self.gameclass.game_active
        ) or (
            self.back_button.rect.collidepoint(mouse_pos)
            and self.sb.game_paused
            and not self.gameclass.game_active
        ):
            self.sb.scores_active = False
            self.sb.controls_active = False

    def _create_high_score(self):
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

    def _create_score(self):
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

    def _create_level(self):
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

    def _create_lives(self):
        self.ship = Group()
        for ship_num in range(self.gameclass.settings.ships_left):
            ship = Ship(self.gameclass)
            ship.rect.x = (
                self.screen_rect.width - ship.rect.width - ship.rect.width * ship_num
            )
            ship.rect.y = self.screen_rect.height - 10 - ship.rect.height
            self.ship.add(ship)

    def _game_lost(self):
        """Text to render when player looses the game"""
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

    def _game_won(self):
        """Text to render when player wins the game"""
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

    def pause_game(self):
        """Changes game_paused flag to an appropriate one"""
        if (self.sb.game_paused
            and not self.gameclass.game_active 
            and not self.sb.scores_active
            and not self.sb.controls_active
        ):
            self.sb.game_paused = False
            self.gameclass.game_active = True
        elif(
            self.sb.game_paused
            and not self.gameclass.game_active
            and (self.sb.scores_active or self.sb.controls_active)
        ):
            self.sb.game_paused = False
            self.gameclass.game_active = True
            self.sb.scores_active = False
            self.sb.controls_active = False
        elif self.gameclass.game_active and not self.sb.game_paused:
            self.sb.game_paused = True
            self.gameclass.game_active = False
            self.gameclass.shoot_bullet_mod = False

    def create_controls_button(self):
        """Function to for score button creation. Used to create the button and move text lover"""
        self.controls_button = Button(self.gameclass, "Controls", bg_color=(145, 145, 145))
        self.controls_button.rect.center = self.gameclass.screen_rect.center
        self.controls_button.rect.y = self.controls_button.rect.y + 140
        self.controls_button.msg_rect.center = self.controls_button.rect.center

    def _controls_menu(self):
        image = pygame.image.load('./images/controls.png').convert_alpha()
        image_rect = image.get_rect()
        image_rect.center = self.screen_rect.center
        
        self.screen.blit(image, image_rect)

    def menu_logic(self):
        """Decides which menu combo to show"""
        if self.sb.scores_active:
            self.highest_score.draw_button()
            self.back_button.draw_button()
            for score in self.scores_list:
                score.draw_button()
        elif self.sb.controls_active:
            self._controls_menu()
            self.back_button.draw_button()
        elif not self.sb.game_lost and not self.sb.game_won and not self.sb.game_paused:
            self.start_button.draw_button()
            self.scores_button.draw_button()
            self.controls_button.draw_button()
        elif self.sb.game_lost:
            self.again_button.draw_button()
            self.looser_text.draw_button()
            self.scores_button.draw_button()
        elif self.sb.game_won:
            self.again_button.draw_button()
            self.chad_text.draw_button()
            self.scores_button.draw_button()
        elif self.sb.game_paused:
            self.resume_button.draw_button()
            self.scores_button.draw_button()
            self.controls_button.draw_button()

    def show_interface(self):
        self.hs.draw_button()
        self.score_counter.draw_button()
        self.level.draw_button()
        self.ship.draw(self.screen)

    def create_scores_button(self):
        """Function to for score button creation. Used to create the button and move text lover"""
        self.scores_button = Button(self.gameclass, "Scores", bg_color=(145, 145, 145))
        self.scores_button.rect.center = self.gameclass.screen_rect.center
        self.scores_button.rect.y = self.scores_button.rect.y + 70
        self.scores_button.msg_rect.center = self.scores_button.rect.center

    def show_scores(self):
        """Generates surfaces of Highest score to draw them on screen"""
        # Create "Highest scores" string to crown scores
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

        # Create back button
        self.back_button = Button(self.gameclass, "Back", bg_color=(145, 145, 145))
        self.back_button.rect.centerx = self.screen_rect.centerx
        self.back_button.rect.y = self.screen_rect.height - 100
        self.back_button.msg_rect.center = self.back_button.rect.center

    def _create_menus(self):
        self.start_button = Button(self.gameclass, "Start", bg_color=(145, 145, 145))
        self.again_button = Button(
            self.gameclass, "Play again", bg_color=(145, 145, 145)
        )
        self.resume_button = Button(self.gameclass, "Resume", bg_color=(145, 145, 145))

        self.create_scores_button()
        self.create_controls_button()
        self.show_scores()

        self._create_high_score()
        self._create_score()
        self._create_level()
        self._create_lives()

        self._game_lost()
        self._game_won()

    def exit_game(self):
        self.gameclass.sb.save_hiscore()
        sys.exit()
