import pygame
from pygame.sprite import Group

from ship import Ship
import game_functions as gf
from settings import Settings
from game_stats import GameStats
from button import Button
from scoreboard import Scorboard

def run_game():
    #Initialize game and create game object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))     #called a surface
    pygame.display.set_caption('Alien Invasion')

    play_button = Button(ai_settings, screen, 'Play')   #Make play button

    stats = GameStats(ai_settings)          #Create game stats
    sb = Scorboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)        #Make Ship
    bullets = Group()                       #Make a group to store bullets in
    aliens = Group()                        # Create alien group

    gf.create_fleet(ai_settings, screen, ship, aliens)

#Surface is part of screen where you display game element(individual element of game)
#surface returned by display.set_mode() represents entire game window
    
    #Start main loop for game
    while(True):
        gf.check_events(ai_settings, stats, screen, sb, ship, aliens, bullets, play_button)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens( ai_settings, stats, screen, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

if __name__ == '__main__':
    run_game()
