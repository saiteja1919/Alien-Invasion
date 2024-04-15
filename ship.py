import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        '''Init ship and set start position'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Load ship image get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Start each new ship at bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom  = self.screen_rect.bottom

        self.center = float(self.rect.centerx)      #Store decimal for ship's center
        #Movement flag
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        '''Draw the ship at its curr location'''
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        '''Update ship's position based on the movement flag'''
        if self.moving_right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left:
            self.center -= self.ai_settings.ship_speed_factor
        
        self.rect.centerx = self.center

        if(self.rect.left < 0):
            self.rect.left = 0
            self.center = float(self.rect.centerx)
        
        if(self.rect.right > self.ai_settings.screen_width):
            self.rect.right = self.ai_settings.screen_width
            self.center = float(self.rect.centerx)
        
    def center_ship(self):
        '''Center the ship on the screen'''
        self.center = self.screen_rect.centerx