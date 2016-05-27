#================================#
#      Space Invaders Clone	     #
#================================#
#  Created by Hlynur Stefánsson  #
#   ~ github.com/hlynurstef ~	 #
#   ~ hlynurstef@gmail.com  ~	 #
#================================#

import pygame
import ctypes
import game_functions as func
from game_settings import Settings
from player import Player
from game_stats import GameStats
from scoreboard import ScoreBoard
from pygame.sprite import Group

def run_game():
	"""Main function for Space Invaders."""
	
	# Initialize game.
	pygame.mixer.pre_init(44100, -16, 1, 512)
	pygame.init()
	settings = Settings()
	
	# Ensure correct screen size to be displayed.
	ctypes.windll.user32.SetProcessDPIAware()
	
	# Set screensize and caption.
	screen = pygame.display.set_mode((settings.screen_width, 
		settings.screen_height))
	pygame.display.set_caption(settings.caption)
	
	# Screen flags.
	main_menu = True
	play_game = False
	# TODO: Implement Main Menu screen.
	
	# Make a clock object to set fps limit.	
	clock = pygame.time.Clock()
	
	# Make player object.
	player = Player(settings, screen)
	
	# Make GameStats object.
	game_stats = GameStats()
	
	# Make ScoreBoard object.
	scoreboard = ScoreBoard(settings, screen, player, game_stats)
	
	# Make player shot object Group.
	player_shots = Group()
	invader_shots = Group()
	
	# Make group for ground and initialise it.
	ground_blocks = func.create_ground(settings, screen)
	
	# Make list of shield groups.
	shields = [func.create_shield(settings, screen, number) 
			   for number in range(4)]
	
	# Make group for lives and initialise it.
	remaining_lives = func.create_lives(settings, screen, player)
	
	# Start the main loop for Space Invaders.
	while True:
		func.check_events(settings, screen, player, player_shots)
		
		player.update()
		func.update_player_shots(settings, screen, player_shots, 
			ground_blocks)
			
		func.update_screen(settings, screen, scoreboard, player,
			player_shots, ground_blocks, remaining_lives, shields)
		clock.tick(settings.fps)
	
run_game()
