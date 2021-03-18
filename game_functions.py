import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, a1_settings, screen, stats, play_button, ship, aliens, bullets):
    '''Respond to Keypresses.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(a1_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(a1_settings, screen, stats, play_button, ship, aliens, bullets)

def check_keyup_events(event, ship):
    '''Respond to key releases.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(a1_settings, screen, stats, play_button, ship, aliens, bullets):
    '''Respond to keypress and mouse events.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,a1_settings, screen, stats, play_button, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(a1_settings, screen, stats, play_button, ship, aliens, 
            bullets, mouse_x, mouse_y)

def check_play_button(a1_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''Starts a new game when the player clicks Play.'''
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        start_game(a1_settings, screen, stats, play_button, ship, aliens, bullets)

def start_game(a1_settings, screen, stats, play_button, ship, aliens, bullets):
    # Reset the game settings.
    a1_settings.initialize_dynamic_settings()

    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(a1_settings, screen, ship, aliens)
    ship.center_ship()


def update_screen(a1_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    '''Update images on the screen and flip to the new screen.'''
    # Redraw the screen during each pass through the loop.
    screen.fill(a1_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if game is inactive.
    if not stats.game_active:
        play_button.draw_button()
    
    # Make the most recently drawn screen visible.
    pygame.display.flip()

def fire_bullet(a1_settings, screen, ship, bullets):
    '''Fire a bullet if limit not reached yet.'''
    # Create a new bullet and add it into the bullets group.
    if len(bullets) < a1_settings.bullets_allowed:
        new_bullet = Bullet(a1_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(a1_settings, screen, stats, sb, ship, aliens, bullets):
    '''Update position of bullets and get rid of old bullets.'''
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappered.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

    check_bullet_alien_collisions(a1_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(a1_settings, screen, stats, sb, ship, aliens, bullets):
    '''Respond to bullet-alien collisions.'''
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += a1_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet.
        bullets.empty()
        a1_settings.increase_speed()
        create_fleet(a1_settings, screen, ship, aliens)

def get_number_aliens_x(a1_settings, alien_width):
    '''Determine the number of aliens that fit in a row.'''
    available_space_x = a1_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(a1_settings, screen, aliens, alien_number, row_number):
    '''Create an alien and place it in the row.'''
    alien = Alien(a1_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(a1_settings, screen, ship, aliens):
    '''Create a full fleet of aliens.'''
    # Create an alien and find the number of aliens in a row.
    alien = Alien(a1_settings, screen)
    number_aliens_x = get_number_aliens_x(a1_settings, alien.rect.width)
    number_rows = get_number_rows(a1_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(a1_settings, screen, aliens, alien_number, row_number)

def get_number_rows(a1_settings, ship_height, alien_height):
    '''Determine the number of rows of aliens that fit on the screen.'''
    available_space_y = (a1_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(a1_settings, stats, screen, ship, aliens, bullets):
    '''Check if the fleet is at an edge,
       and then update the positions of all aliens in the fleet.'''
    check_fleet_edges(a1_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(a1_settings, stats, screen, ship, aliens, bullets)
    
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(a1_settings, stats, screen, ship, aliens, bullets)

def check_fleet_edges(a1_settings, aliens):
    '''Drop the entire fleet and change the fleet's direction.'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(a1_settings, aliens)
            break

def change_fleet_direction(a1_settings, aliens):
    '''Drop the entire fleet and change the fleet's direction.'''
    for alien in aliens.sprites():
        alien.rect.y += a1_settings.fleet_drop_speed
    a1_settings.fleet_direction *= -1

def ship_hit(a1_settings, stats, screen, ship, aliens, bullets):
    '''Respond to ship being hit by alien.'''
    if stats.ships_left > 0:
        # Decrement ship left
        stats.ships_left -= 1

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(a1_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(a1_settings, stats, screen, ship, aliens, bullets):
    '''Check if any alien has reached the bottom of the screen.'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(a1_settings, stats, screen, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    '''Checks to see if there's new high score.'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()