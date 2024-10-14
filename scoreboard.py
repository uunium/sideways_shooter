class Scoreboard:
    def __init__(self, gameclass) -> None:
        self.gameclass = gameclass
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings

        self.alien_price = 100

        self.level = 1
        self.speedup = 1.0

        self.score = 0
        self.high_score = 0

    def update_score(self):
        score = self.score + (self.alien_price * self.speedup)
        self.score = round(score, -1)
        if self.score > self.high_score:
            self.high_score = self.score

    def update_game_speed(self):
        self.speedup = self.speedup + (0.05 * self.level)
    
    