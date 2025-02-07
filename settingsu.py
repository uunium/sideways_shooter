class Settings:
    def __init__(self, gameclass) -> None:
        self.gameclass = gameclass
        self.screen_width = 1280
        self.screen_height = 720
        self.screen_color = (0, 0, 0)
        self.framerate = 60

        self.ship_speed = 3
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
