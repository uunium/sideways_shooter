"""Module contains Settings class with game settings."""


class Settings:
    """Class to initialize game settings.

    Contains settings for:
    Game window size
    Framerate
    Ship speed
    Number of lives
    Bullet speed
    Delay between shots if space bar is constantly pressed
    Abilities cooldown duration
    Alien speed and movement direction
    """

    def __init__(self, gameclass: "Game") -> None:
        """Initialise the class and all it's attributes."""
        self.gameclass = gameclass
        self.screen_width = 1280
        self.screen_height = 720
        self.screen_color = (0, 0, 0)
        self.framerate = 60

        self.ship_speed = 3
        # bb - before boost speed
        self.bb_speed = 0
        self.ships_left = 3

        self.bullet_speed = 20
        self.shot_delay = 250
        self.boost_active = False
        self.boost_duration = 250
        self.boost_delay = 7000
        self.mega_shot_delay = 10000

        # фактичні значення швидкостей визначаються у бібліотеці scoreboarde.py
        self.alien_hor_speed = 0
        self.alien_ver_speed = 0

        # direction should be 1 or -1
        self.alien_direction = -1
