"""Module for creating and managing the Scoreboard."""

import pygame
from settingsu import Settings
from menu import Menu
from bullette import Bullet


class Scoreboard:
    """Class to handle Scoreboard stuff.

    Also updates difficuilty of the game by changing
    game speed and ship movement speed.
    Updates player's score.
    """

    gameclass: "Game"
    screen: pygame.Surface
    screen_rect: pygame.Rect
    settings: Settings
    bullets: pygame.sprite.Group
    game_state: str
    shot_price: int
    level: int
    speedup: float
    score: int
    high_score: int

    def __init__(self, gameclass: "Game") -> None:
        """Initialise the scoreboard.

        also set the game state, alien price, miss price, current level, speed, score and load the high score.
        """
        self.gameclass = gameclass
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings
        self.bullets = gameclass.bullets

        self.game_state: str = "Start"

        self.alien_price = 100
        self.shot_price = 5

        self.level = 1
        self.speedup = 1

        self.score = 0
        self.high_score = self.gameclass.hsf[0]

    def update_score(self, hit: bool = False, miss: bool = False) -> None:
        """Update the score value.

        Depending whether shot hit or missed change score value, round score and update high score if needed.
        """
        if hit:
            score = self.score + (self.alien_price * self.speedup)
            self.score = round(score)
            print("Score increased")
            if self.score > self.high_score:
                self.high_score = self.score
        elif miss:
            score = self.score - (self.shot_price * self.speedup)
            self.score = round(score)
            print("Score reduced")
        else:
            raise ValueError(f"hit={hit}, miss={miss}")

    def update_game_speed(self) -> None:
        """Increase game difficulty after beating a level.

        Also update GUI by changing the level number.
        """
        self.level += 1
        self.gameclass.menu._create_level()
        self.change_move_speed()
        self.alien_price *= self.speedup

    def change_move_speed(self) -> None:
        """Increase difficulty of the game after beating a level.

        Increase is done by increasing speedup value, alien speed and ship speed, and decreasing delay between normal shots.
        """
        if self.settings.alien_hor_speed < 15:
            self.speedup += 0.05
            self.settings.alien_hor_speed += self.speedup
        elif self.settings.alien_hor_speed > 15 and self.settings.alien_ver_speed < 7:
            self.speedup += 0.5
            self.settings.alien_ver_speed += self.speedup
            self.settings.ship_speed = 5
            self.settings.shot_delay = 200
        elif self.settings.alien_hor_speed < 20:
            self.speedup += 0.1
            self.settings.alien_hor_speed += self.speedup
            self.settings.ship_speed = 8
            self.settings.shot_delay = 150
        elif self.level == 20:
            self.settings.alien_hor_speed = 23
            self.settings.alien_ver_speed = 9
            self.settings.ship_speed = 10
            self.settings.shot_delay = 120

    # need to remove 'menu' parameter from here somehow
    def bullet_hit(self, menu: "Menu") -> None:
        """Update scores if the bullet hit an alien."""
        self.update_score(hit=True)
        menu._create_score()
        menu._create_high_score()

    def bullet_missed(self, menu: Menu, bullet: Bullet = None) -> None:
        """Update the scores if the bullet misses."""
        self.update_score(miss=True)
        menu._create_score()
        if bullet is not None:
            self.bullets.remove(bullet)

    def reset_stats(self) -> None:
        """Reset the game stats.

        Stats reset: number of lives left, alien price, current level, speed up factor, current score, alien speed.
        """
        self.gameclass.settings.ships_left = 3
        self.alien_price = 100
        self.level = 1
        self.speedup = 1
        self.score = 0

        # значення швидкостей визначаються тут
        self.settings.alien_hor_speed = 10
        self.settings.alien_ver_speed = 2

        self.gameclass.shoot_bullet_mod = False
        self.game_lost = False
        self.game_won = False

    def save_hiscore(self) -> None:
        """Save high score to a file."""
        if self.high_score > self.gameclass.hsf[0]:
            self.gameclass.hsf.append(self.high_score)
            self.gameclass.hsf.sort(reverse=True)
        size = len(self.gameclass.hsf)
        if size > 10:
            dif = size - 10
            for _ in range(dif):
                self.gameclass.hsf.pop(10)

        with open(
            "highscore.py",
            "w",
        ) as hs_file:
            hs_file.write(f"hiscore = {self.gameclass.hsf}")
