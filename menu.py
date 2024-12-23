from pygame.sprite import Group

from buttons import Button
from shippe import Ship



class Menu:
    def __init__(self, gameclass) -> None:
        self.gameclass = gameclass
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings
        self.sb = self.gameclass.sb

        self._create_menus()

    def _button_press(self, mouse_pos):
        # дії для початку гри
        if ((self.start_button.rect.collidepoint(mouse_pos) or 
            self.again_button.rect.collidepoint(mouse_pos)) and
            not self.sb.game_paused
            ):
            self.gameclass.bullets.empty()
            self.gameclass.aliens.empty()
            self.gameclass._create_fleet()
            self.gameclass.sb.reset_stats()
            self.gameclass.game_active = True
        # дії для зняття паузи
        elif (self.resume_button.rect.collidepoint(mouse_pos) and 
            self.sb.game_paused):
            self.pause_game()

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

    def _game_lost(self):
        '''Text to render when player looses the game'''
        self.looser_text = Button(
            self.gameclass, 'You failed to defend The Earth', tx_size=60,
            bg_color=None, height=0, width=0,
            )
        self.looser_text.msg_rect.center = self.screen_rect.center
        self.looser_text.msg_rect.bottom = self.start_button.msg_rect.top - 10

    def _game_won(self):
        '''Text to render when player wins the game'''
        self.chad_text = Button(
            self.gameclass, 'You defeated the Aliens', tx_size=60,
            bg_color=None, height=0, width=0,
            )
        self.chad_text.msg_rect.center = self.screen_rect.center
        self.chad_text.msg_rect.bottom = self.start_button.msg_rect.top - 10

    def pause_game(self):
        '''Changes game_paused flag to appropriate one'''
        if self.sb.game_paused and not self.gameclass.game_active:
            self.sb.game_paused = False
            self.gameclass.game_active = True
        elif self.gameclass.game_active and not self.sb.game_paused:
            self.sb.game_paused = True
            self.gameclass.game_active = False

    def menu_logic(self):
        '''Decides which menu combo to show'''
        if not self.sb.game_lost and not self.sb.game_won and not self.sb.game_paused:
            self.start_button.draw_button()
        elif self.sb.game_lost:
            self.again_button.draw_button()
            self.looser_text.draw_button()
        elif self.sb.game_won:
            self.again_button.draw_button()
            self.chad_text.draw_button()
        elif self.sb.game_paused:
            self.resume_button.draw_button()

    def show_interface(self):
        self.hs.draw_button()
        self.score_counter.draw_button()
        self.level.draw_button()
        self.ship.draw(self.screen)

    def _create_menus(self):
        self.start_button = Button(self.gameclass, 'Start', bg_color=(145, 145, 145))
        self.again_button = Button(self.gameclass, 'Play again', bg_color=(145, 145, 145))
        self.resume_button = Button(self.gameclass, 'Resume', bg_color=(145, 145, 145))
                
        self._create_high_score()
        self._create_score()
        self._create_level()
        self._create_lives()
        self._game_lost()
        self._game_won()
