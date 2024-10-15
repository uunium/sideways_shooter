class GameStats:

    def __init__(self, gameclass) -> None:
        self.gameclass = gameclass
        self.settings = gameclass.settings
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ships_amount
        self.settings.alien_price = 100
        self.gameclass.sb.level = 1
        self.gameclass.sb.speedup = 1
        self.gameclass.sb.score = 0