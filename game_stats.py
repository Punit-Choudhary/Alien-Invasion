class GameStats():
    '''Tracks statistics for Game.'''

    def __init__(self, a1_settings):
        '''Initialize statistics.'''
        self.a1_settings = a1_settings
        self.reset_stats()

        # Start Alien Invasion by Punit-Choudhary Game in an inactive state.
        self.game_active = False

        # High Score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        '''Initialize statistics that can change during the game.'''
        self.ships_left = self.a1_settings.ships_limit
        self.score = 0
        self.level = 1
        
    
