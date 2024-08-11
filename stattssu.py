class GameStats:

    def __init__(self, gameclass) -> None:
        self.settings = gameclass.settings
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ships_amount