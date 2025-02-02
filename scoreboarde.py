class Scoreboard:
    def __init__(self, gameclass) -> None:
        self.gameclass = gameclass
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings
        self.bullets = gameclass.bullets

        self.game_lost = False
        self.game_won = False
        self.game_paused = False
        self.scores_active = False

        self.alien_price = 100
        self.shot_price = 5

        self.level = 1
        self.speedup = 1

        self.score = 0
        self.high_score = self.gameclass.hsf[0]
    
    def update_score(self, hit=False, miss=False):
        if hit:
            score = self.score + (self.alien_price * self.speedup)
            self.score = round(int(score))
            print('Score increased')
            if self.score > self.high_score:
                self.high_score = self.score
        elif miss:
            score = self.score - (self.shot_price * self.speedup)
            self.score = round(int(score))
            print('Score reduced')
        else:
            raise ValueError(f'hit={hit}, miss={miss}')

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

    def bullet_hit(self, menu):
        self.update_score(hit=True)
        menu._create_score()
        menu._create_high_score()

    def bullet_missed(self, menu, bullet=None):
        self.update_score(miss=True)
        menu._create_score()
        if bullet is not None:
            self.bullets.remove(bullet)
                

    def reset_stats(self):
        self.gameclass.settings.ships_left = 3
        self.alien_price = 100
        self.level = 1
        self.speedup = 1
        self.score = 0

        # значення швидкостей визначаються тут
        self.settings.alien_hor_speed = 10
        self.settings.alien_ver_speed = 2

        self.gameclass.menu._create_menus()

        self.gameclass.shoot_bullet_mod = False
        self.game_lost = False
        self.game_won = False
        self.game_paused = False

    def save_hiscore(self):
        if self.high_score > self.gameclass.hsf[0]:
            self.gameclass.hsf.append(self.high_score)
            self.gameclass.hsf.sort(reverse=True)
        size = len(self.gameclass.hsf)
        if size > 10:
            dif = size - 10
            for _ in range(dif):
                self.gameclass.hsf.pop(10)

        with open('highscore.py', 'w',) as hs_file:
            hs_file.write(f'hiscore = {self.gameclass.hsf}')
    
    

            

    