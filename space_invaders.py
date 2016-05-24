# Space Invaders Clone
# Created by Hlynur Stefánsson
# Start date 23/05/2016
# github.com/hlynurstef
# hlynurstef@gmail.com

import pygame
import ctypes
import game_functions as func
from game_settings import Settings
from player import Player
from pygame.sprite import Group

def run_game():
	"""Main function for Space Invaders."""
	# Initialize game and create settings and screen object.
	pygame.mixer.pre_init(44100, -16, 1, 512)
	pygame.init()
	settings = Settings()
	# Ensure correct screen size to be displayed.
	ctypes.windll.user32.SetProcessDPIAware()
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
	
	# Make player shot object.
	player_shots = Group()
	invader_shots = Group()
	
	# Start the main loop for Space Invaders.
	while True:
		func.check_events(settings, screen, player, player_shots)
		player.update()
		func.update_player_shots(settings, player_shots)
		func.update_screen(settings, screen, player, player_shots)
		clock.tick(60)
	
run_game()
