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

        self.alien_hor_speed = 10
        self.alien_ver_speed = 1
        self.alien_movement_counter = 0
        #direction should be 1 or -1
        self.alien_direction = -1
      
    # def _reset_stuff(self):
    #     '''Used to reset speeds, counters and other stuff before new game cycle'''
    #     self.alien_ver_speed =  self.gameclass._previous_ver_speed
    #     self.alien_movement_counter = 0
    #     self.alien_direction = -1


