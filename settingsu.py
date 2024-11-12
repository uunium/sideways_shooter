class Settings:
    def __init__(self,gameclass) -> None:
        self.gameclass = gameclass
        self.screen_width = 1280
        self.screen_height = 720
        self.screen_color = (0, 0, 0)
        self.framerate = 60
        
        self.ship_speed = 1.5
        self.ships_left = 3

        self.bullet_speed = 20
        self.shot_delay = 100
        self.bullet_color = (255, 0, 0)

        # фактичні значення швидкостей визначаються у бібліотеці scoreboarde.py
        self.alien_hor_speed = 0
        self.alien_ver_speed = 0

        # direction should be 1 or -1
        self.alien_direction = -1


