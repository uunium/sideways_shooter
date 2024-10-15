import pygame
from pygame.sprite import Group

from buttons import Button
from shippe import Ship



class Menu:
    def __init__(self, gameclass) -> None:
        self.gameclass = gameclass
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings

        self.start_button = Button(gameclass, 'Start', bg_color=(145, 145, 145))
        
        self.create_menus()

    def _button_press(self, mouse_pos):
        if self.start_button.rect.collidepoint(mouse_pos):
            self.gameclass.bullets.empty()
            self.gameclass.aliens.empty()
            self.gameclass._create_fleet()
            self.gameclass.sb.reset_stats()
            self.settings._reset_stuff(self.gameclass)
            self.gameclass.game_active = True

    def _create_high_score(self):
        self.hs = Button(
            self.gameclass, f'{self.gameclass.sb.high_score}', bg_color=None,tx_size=48,
            height=0, width=0,
        )
        self.hs.msg_rect.y = 10
        self.hs.msg_rect.x = (
            self.screen_rect.width - self.hs.msg_rect.width - 10
        )

    def _create_score(self):
        self.score_counter = Button(
            self.gameclass, f'{self.gameclass.sb.score}', bg_color=None, tx_size=30,
            height=0, width=0,
            )
        self.score_counter.msg_rect.topleft = (
            self.screen_rect.width - self.score_counter.msg_rect.width - 10,
            self.hs.msg_rect.bottomleft[1] + 10
        )

    def _create_level(self):
        self.level = Button(
            self.gameclass, f'{self.gameclass.sb.level}', bg_color=None, tx_size=30,
            height=0, width=0,
        )
        self.level.msg_rect.topleft = (
            self.screen_rect.width - self.level.msg_rect.width - 10,
            self.score_counter.msg_rect.bottomleft[1] + 10
        )

    def _create_lives(self):
        self.ship = Group()
        for ship_num in range(self.gameclass.settings.ships_left):
            ship = Ship(self.gameclass)
            ship.rect.x = self.screen_rect.width - ship.rect.width - ship.rect.width * ship_num
            ship.rect.y = self.screen_rect.height - 10 - ship.rect.height
            self.ship.add(ship)

    def show_menu(self):
        self.hs.draw_button()
        self.score_counter.draw_button()
        self.level.draw_button()

        self.ship.draw(self.screen)

    def create_menus(self):
        self._create_high_score()
        self._create_score()
        self._create_level()
        self._create_lives()
