import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group

def run_game():
    # Initize pygame, settings and screen object
    pygame.init()
    a1_settings = Settings()
    screen = pygame.display.set_mode(
        (a1_settings.screen_width, a1_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(a1_settings, screen)
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(a1_settings, screen,ship, aliens)

    # Starts main loop for game
    while True:
        gf.check_events(a1_settings, screen, ship,bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(a1_settings, screen, ship, aliens, bullets)

run_game()
