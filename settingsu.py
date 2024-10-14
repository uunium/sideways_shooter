class Settings:
    def __init__(self) -> None:
        self.screen_width = 1280
        self.screen_height = 720
        self.screen_color = (0, 0, 0)
        self.framerate = 60
        
        self.ship_speed = 1.5
        self.ships_amount = 3

        self.bullet_speed = 3
        self.bullet_color = (255, 0, 0)

        self.alien_hor_speed = 1
        self.alien_ver_speed = 1
        self.alien_movement_counter = 0
        #direction should be 1 or -1
        self.alien_direction = -1

       
    def _reset_stuff(self, gameclass):
        '''Used to reset speeds, counters and other stuff before new game cycle'''
        self.alien_ver_speed = gameclass._previous_ver_speed
        self.alien_movement_counter = 0
        self.alien_direction = -1

        