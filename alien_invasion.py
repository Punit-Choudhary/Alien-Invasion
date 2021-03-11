import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    # Initize pygame, settings and screen object
    pygame.init()
    a1_settings = Settings()
    screen = pygame.display.set_mode(
        (a1_settings.screen_width, a1_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Make a ship
    ship = Ship(screen)

    # Set the background color
    bg_color = (230, 230, 230)

    # Starts main loop for game
    while True:
        gf.check_events()
        gf.update_screen(a1_settings, screen, ship)

run_game()
