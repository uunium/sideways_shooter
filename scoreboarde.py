class Scoreboard:
    def __init__(self, gameclass) -> None:
        self.gameclass = gameclass
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings

        self.game_lost = False
        self.game_won = False
        self.game_paused = False

        self.alien_price = 100

        self.level = 19
        self.speedup = 1

        self.score = 0
        self.high_score = 0
    
    def update_score(self):
        score = self.score + (self.alien_price * self.speedup)
        self.score = round(int(score), -1)
        if self.score > self.high_score:
            self.high_score = self.score

    def update_game_speed(self):
        self.level += 1
        self.gameclass.menu._create_level()
        self.change_move_speed()
        self.alien_price *= self.speedup

    def change_move_speed(self):
        if self.settings.alien_hor_speed < 15:
            self.speedup += 0.05
            self.settings.alien_hor_speed += self.speedup
        elif (self.settings.alien_hor_speed > 15 and 
              self.settings.alien_ver_speed < 7):
            self.speedup += 0.5
            self.settings.alien_ver_speed +=  self.speedup
        elif self.settings.alien_hor_speed < 20:
            self.speedup += 0.1
            self.settings.alien_hor_speed += self.speedup
        elif self.level == 20:
            self.settings.alien_hor_speed = 23
            self.settings.alien_ver_speed = 9
            
    def reset_stats(self):
        self.gameclass.settings.ships_left = 3
        self.alien_price = 100
        self.level = 1
        self.speedup = 1
        self.score = 0
        self.gameclass.menu._create_menus()

        self.game_lost = False
        self.game_won = False
        self.game_paused = False
    