class Settings:
    def __init__(self, gameclass) -> None:
        self.screen_width = 1280
        self.screen_height = 720
        self.screen_color = (0, 0, 0)
        self.framerate = 60

        self.ship_speed = 1.5

        self.bullet_speed = 3
        self.bullet_color = (255, 0, 0)

        self.alien_hor_speed = 5
        self.alien_ver_speed = 2
        #direction should be 1 or -1
        self.alien_direction = 1

        