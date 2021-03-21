import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''A class to represent a single alien in the fleet.'''

    def __init__(self, a1_settings, screen):
        '''Initialize the alien and sets its starting position.'''
        super(Alien, self).__init__()
        self.screen = screen
        self.a1_settings = a1_settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien_red.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top of screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        '''Draw the alien at its current location.'''
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        '''Move the alien right or left.'''
        self.x += (self.a1_settings.alien_speed_factor * self.a1_settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        '''Return True if alien is at edges of screen.'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True