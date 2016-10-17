import pygame
import game_functions as func

class Settings():
	"""A class to store all settings for Space Invaders."""

	def __init__(self):
		"""Initialize game settings."""

		# Screen settings
		self.screen_width  = 768
		self.screen_height = 672
		self.caption       = "Space Invaders"

		# FPS settings
		self.fps = 60

		# Font settings
		self.font      = "fonts/space_invaders.ttf"
		self.font_size = 24

		# Game sounds
		self.player_shoot 	= pygame.mixer.Sound("sounds/player_shoot.wav")
		self.player_shoot.set_volume(0.2)
		self.invader_killed = pygame.mixer.Sound("sounds/invaderkilled.wav")

		# Color settings
		self.black 	= (0, 0, 0)
		self.white 	= (255, 255, 255)
		self.red   	= (255, 0, 0)
		self.green 	= (0, 255, 0)
		self.blue  	= (0, 0, 255)

		# Player settings
		self.player_speed      = 3
		self.player_offsetx	   = 102
		self.player_y          = self.screen_height - 96
		self.player_ship_image = pygame.image.load("images/ships/player.png")
		self.player_lives      = 3

		# Invader settings
		self.invader_start_x 		= 126
		self.invader_start_y 		= 120
		self.invader_move_x 		= 6
		self.invader_height 		= 24
		self.invader_left_boundary 	= 72
		self.invader_right_boundary = 690
		self.invader_move_time		= 1000
		self.invader_1_score		= 30
		self.invader_2_score		= 20
		self.invader_3_score		= 10

		# Fleet settings
		self.fleet_rows      = 5
		self.fleet_columns 	 = 11
		self.fleet_direction = 1

		# Block settings
		self.block_size = 3

		# Shot settings
		self.playershot_speed = 12
		self.playershot_limit = 1
		self.invadershot_speed = 12
		self.invadershot_limit = 3

		# Ground settings
		self.ground_y       = self.screen_height - 54
		self.ground_offsetx = 48

		# Life settings
		self.life_y            = self.screen_height - 48
		self.life_text_offsetx = 75
		self.life_ship_offsetx = 126
		self.life_ship_spacing = 9

		# Score settings
		# Text
		self.score_text_y 	 = 24
		# Numbers
		self.player1_score_x = 123
		self.hi_score_x      = 315
		self.score_y         = 48

		# Explosion settings
		self.player_shot_explode_rows    = 8
		self.player_shot_explode_columns = 8
		self.player_shot_explode_array   = [
			['b', '.', '.', '.', 'b', '.', '.', 'b'],
			['.', '.', 'b', '.', '.', '.', 'b', '.'],
			['.', 'b', 'b', 'b', 'b', 'b', 'b', '.'],
			['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
			['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
			['.', 'b', 'b', 'b', 'b', 'b', 'b', '.'],
			['.', '.', 'b', '.', '.', 'b', '.', '.'],
			['b', '.', '.', 'b', '.', '.', '.', 'b']]

		self.invader_shot_explode_rows = 8
		self.invader_shot_explode_columns = 6
		self.invader_shot_explode_array = [
			['.', '.', 'b', '.', '.', '.'],
			['b', '.', '.', '.', 'b', '.'],
			['.', '.', 'b', 'b', '.', 'b'],
			['.', 'b', 'b', 'b', 'b', '.'],
			['b', '.', 'b', 'b', 'b', '.'],
			['.', 'b', 'b', 'b', 'b', 'b'],
			['b', '.', 'b', 'b', 'b', '.'],
			['.', 'b', '.', 'b', '.', 'b']]

		# Shield settings
		self.shield_rows    = 16
		self.shield_columns = 22
		self.shield_x       = 144
		self.shield_y       = self.screen_height - 168
		# '.' == nothing
		# 'b' == Block()
		self.shield_array   = [
		['.', '.', '.', '.', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '.', '.', '.', '.'],
		['.', '.', '.', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '.', '.', '.'],
		['.', '.', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '.', '.'],
		['.', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '.'],
		['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
		['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
		['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
		['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
		['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
		['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
		['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
		['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
		['b', 'b', 'b', 'b', 'b', 'b', 'b', '.', '.', '.', '.', '.', '.', '.', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
		['b', 'b', 'b', 'b', 'b', 'b', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
		['b', 'b', 'b', 'b', 'b', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'b', 'b', 'b', 'b', 'b', 'b'],
		['b', 'b', 'b', 'b', 'b', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'b', 'b', 'b', 'b', 'b', 'b']]
