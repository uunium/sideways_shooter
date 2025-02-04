import pygame

class Timer:
    def __init__(self, gameclass, colour:tuple, action_time:int, delay:int, x:int=0, y:int=0,):
        self.gameclass = gameclass
        self.screen = gameclass.screen
        self.screen_rect = gameclass.screen_rect
        self.settings = gameclass.settings

        self.bar_path = 'images/empty_bar.png'
        self.bar_image = pygame.image.load(self.bar_path).convert_alpha()

        self.bar_image_rect = self.bar_image.get_rect()
        self.bar_image_rect.x = x
        self.bar_image_rect.y = y
        
        self.action_time = action_time
        self.fill_duration = delay
        self.fill_colour = colour

        self._create_fill()
        
    def _create_fill(self, x=0):
        self.fill_tagle_sur = pygame.Surface((x,22))
        self.fill_tagle_sur.fill(color=self.fill_colour)
        self.fill_tagle_rect = self.fill_tagle_sur.get_rect()
        self.fill_tagle_rect.topleft = [(self.bar_image_rect.x+4), (self.bar_image_rect.y+4)]

    # when active should fill up untill full. step 4 pixel from each side. height is 30 pix,
    # length is 126 pix.

    def reset_bar(self, action_time):
        self._create_fill(0)
        self.action_time = action_time

    def blit_bar(self):
        time_passed = self.gameclass.timer - self.action_time

        if  time_passed <= self.fill_duration:
            perc = (time_passed / self.fill_duration) * 118
            self._create_fill(perc)

        self.screen.blit(self.bar_image, self.bar_image_rect)
        self.screen.blit(self.fill_tagle_sur, self.fill_tagle_rect)


        
