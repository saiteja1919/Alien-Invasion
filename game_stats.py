class GameStats():
    ''' Track statistics for Alien Invasion'''

    def __init__(self, ai_settings):
        '''Initialize statistics'''
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False         # Start game in active state
        self.score = 0
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        '''Initialise sstatistics that can change during the game'''
        self.ships_left = self.ai_settings.ship_limit
        self.game_active = True
        self.score = 0