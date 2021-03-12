import sys
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, a1_settings, screen, ship, bullets):
    '''Respond to Keypresses.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(a1_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    '''Respond to key releases.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(a1_settings, screen, ship, bullets):
    '''Respond to keypress and mouse events.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, a1_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(a1_settings, screen, ship, aliens, bullets):
    '''Update images on the screen and flip to the new screen.'''
    # Redraw the screen during each pass through the loop.
    screen.fill(a1_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)

def fire_bullet(a1_settings, screen, ship, bullets):
    '''Fire a bullet if limit not reached yet.'''
    # Create a new bullet and add it into the bullets group.
    if len(bullets) < a1_settings.bullets_allowed:
        new_bullet = Bullet(a1_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(bullets):
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

