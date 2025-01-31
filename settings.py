class Settings():
    """A class to store settings for Alien Invasion"""

    def __init__(self):
        '''Initialize game's settings'''
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed_factor = 0.6
        self.fleet_drop_speed = 15
        self.fleet_direction = 1 #right = 1, left = -1

        # How quickly game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.8

        # fleet direction of 1 represents right; -1 for left
        self.fleet_direction = 1

        #Scoring
        self.alien_points = 10
    
    def increase_speed(self):
        '''Increase speed settings'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)