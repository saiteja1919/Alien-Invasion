import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien

def fire_bullet(ai_settings, screen, ship, bullets):
    '''Fire bullet if limit not reached yet'''
    #Create bullet and add to bullets group
    if(len(bullets) < ai_settings.bullets_allowed):
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keydown_events(event, ai_settings, stats, screen, sb, ship, bullets, aliens, playBtn):
    if event.key == pygame.K_RIGHT:
        #Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_r or event.key == pygame.K_p:
        reset_game(ai_settings, screen, stats, sb, aliens, bullets, ship, True)
    elif event.key == pygame.K_ESCAPE:
        if(stats.ships_left < 0):
            reset_game(ai_settings, screen, stats, sb, aliens, bullets, ship, True)
        else:
            pause_game(stats, playBtn)

def pause_game(stats, playBtn):
    if(stats.game_active):
        stats.game_active = False
        playBtn.msg = 'Resume'
        pygame.mouse.set_visible(True)
    else:
        stats.game_active = True
        playBtn.msg = 'Play'
        pygame.mouse.set_visible(False)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def reset_game(ai_settings, screen, stats, sb, aliens, bullets, ship, reset_stats):
    '''Reset game variables. Stats are set based on reset_stats flag'''
    if reset_stats:
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()

        # Reset the scoreboard images
        sb.prep_images()

    #Empty aliens and bullets
    aliens.empty()
    bullets.empty()

    #Create new fleet and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def check_play_button(ai_settings, screen, stats, sb, playBtn, ship, aliens, bullets, mouse_x, mouse_y):
    '''Start a new game when the player clicks play'''
    if playBtn.rect.collidepoint(mouse_x, mouse_y):
        if(playBtn.msg == 'Play' and not stats.game_active):
            reset_game(ai_settings, screen, stats, sb, aliens, bullets, ship, True)
            pygame.mouse.set_visible(False)     #Hide mouse cursor
        elif(playBtn.msg == 'Resume'):
            pause_game(stats, playBtn)


def check_events(ai_settings, stats, screen, sb, ship, aliens, bullets, playBtn):
    '''Respond to events'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, screen, sb, ship, bullets, aliens, playBtn)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, playBtn, ship, aliens, bullets, mouse_x, mouse_y)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, playBtn):
    '''Update images on the screen and flip to new screen'''
    screen.fill(ai_settings.bg_color)       #redraw screen each time
    #redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    #Draw the play button if the game status is inactive
    if not stats.game_active:
        playBtn.draw_button()

    #Make the most recently drawn screen visible
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Update position of bullets & get rid of old bullets'''
    #Update bullet positions
    bullets.update()

    #Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            #print('Bullets count ', len(bullets))

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    '''Check to see if there's a new high score'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def start_new_level(ai_settings, screen, stats, sb, ship, bullets, aliens):
    '''Start new level after aliens are hit'''
    '''#Destroy existing bullets and create new fleet'''
    bullets.empty()
    ai_settings.increase_speed()
    stats.level += 1
    sb.prep_level()
    create_fleet(ai_settings, screen, ship, aliens)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Respond to bullet-alien collisons'''
    #Remove any bullets and alients that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)     #consider superbullets
            sb.prep_score()
        check_high_score(stats, sb)

    if(len(aliens) == 0):
        start_new_level(ai_settings, screen, stats, sb, ship, bullets, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    '''Determine number of aliens that fit in a row'''
    available_spacce_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_spacce_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''Determine number of rows of aliens that fit on screen'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    #Create alien and place it in the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    '''Create a full fleet of aliens'''
    #Create an alien and find number of aliens in row
    #Spacing between aliens = one alien width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #Create fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''Respond to ship being hit by alien'''
    if stats.ships_left > 1:
        stats.ships_left -= 1 #Decrement ships left
        sb.prep_ships()

        reset_game(ai_settings, screen, stats, sb, aliens, bullets, ship, False)

        sleep(0.5)  #Pause
    else:
        stats.game_active = False
        stats.ships_left = -1
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''Check if any aliens have reached bottom of the screen'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treat this the same as ship hit
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''
    Check if the fleet is at an edge,
    and then update the positions of all aliens in the fleet
    '''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
        print('Ship hit !!!')

    #Looks for aliens hitting bottom
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def change_fleet_direction(ai_settings, aliens):
    '''Drop entire fleet and change fleet's direction'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    '''Respond appropriately if any aliens have reached an edge'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break