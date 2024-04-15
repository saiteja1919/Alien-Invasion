import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''A class to manage bullets fired from the ship'''

    def __init__(self, ai_settings, screen, ship):
        '''Create a bullet object at the ship's current position'''
        super().__init__()      #super(Bullet, self).__init__() py.2.7
        self.screen = screen

        #Create bullet at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
    
    def update(self):
        '''Move bullet up the screen'''
        self.y -= self.speed_factor     #update decimal position of bullet
        self.rect.y = self.y    #Update rect position
    
    def draw_bullet(self):
        '''Draw bullet on screen'''
        pygame.draw.rect(self.screen, self.color, self.rect)