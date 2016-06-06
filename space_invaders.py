#===================================#
#       Space Invaders Clone	    #
#      Based off of SNES game:		#
# Space Invaders: The Original Game #
#===================================#
#    Created by Hlynur Stefánsson   #
#     ~ github.com/hlynurstef ~	    #
#     ~ hlynurstef@gmail.com  ~	    #
#===================================#

import pygame
import ctypes
import game_functions as func
from game_settings import Settings
from player import Player
from game_stats import GameStats
from scoreboard import ScoreBoard
from pygame.sprite import Group

class Game():
	"""A class representing the game."""
	
	def __init__(self):
		"""Initialize game."""
		pygame.mixer.pre_init(44100, -16, 1, 512)
		pygame.init()
		
		# Ensure correct screen size to be displayed.
		ctypes.windll.user32.SetProcessDPIAware()
		
		# Make settings object.
		self.settings = Settings()
		
		# Set screensize and caption.
		self.screen = pygame.display.set_mode((
			self.settings.screen_width, 
			self.settings.screen_height))
		pygame.display.set_caption(self.settings.caption)
		
		# Screen flags.
		self.main_menu = True
		self.play_game = False
		# TODO: Implement Main Menu screen.
		
		# Make a clock object to set fps limit.	
		self.clock = pygame.time.Clock()
		
		# Make player object.
		self.player = Player(self.settings, self.screen)
		
		# Make Invader Fleet.
		self.invaders = Group()
		func.create_fleet(self.settings, self.screen, self.invaders)
		
		# Make GameStats object.
		self.game_stats = GameStats()
		
		# Make ScoreBoard object.
		self.scoreboard = ScoreBoard(self.settings, self.screen, 
			self.player, self.game_stats)
		
		# Make player shot object Group.
		self.player_shots = Group()
		self.invader_shots = Group()
		
		# Make group for ground and initialise it.
		self.ground_blocks = func.create_ground(self.settings, 
			self.screen)
		
		# Make list of shield groups.
		self.shields = [func.create_shield(self.settings, self.screen, 
			number) 
			for number in range(4)]
		
		# Make group for lives and initialise it.
		self.remaining_lives = func.create_lives(self.settings, 
			self.screen, self.player)
		
	def run_game(self):
		"""Main function for Space Invaders."""
		
		# Start the main loop for Space Invaders.
		while True:
			func.check_events(self.settings, self.screen, self.player, 
				self.player_shots)
			
			self.player.update()
			
			# Only update shot when there is a shot on the screen.
			if self.player.has_active_shot:
				func.update_player_shots(self.settings, self.screen, 
					self.player, self.player_shots, self.ground_blocks,
					self.shields, self.invaders)
					
			func.update_invaders(self.settings, self.invaders)
				
			func.update_screen(self.settings, self.screen, 
				self.scoreboard, self.player, self.player_shots, 
				self.ground_blocks, self.remaining_lives, self.shields,
				self.invaders)
			
			# Set max fps.
			self.clock.tick(self.settings.fps)

if __name__ == '__main__':
	Game().run_game()
