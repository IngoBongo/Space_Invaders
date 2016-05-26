import pygame

class Settings():
	"""A class to store all settings for Space Invaders."""
	
	def __init__(self):
		"""Initialize game settings."""
		
		# Screen settings
		self.screen_width = 800
		self.screen_height = 700
		self.caption = "Space Invaders"
		
		# FPS settings
		self.fps = 60
		
		# Game font
		self.font = "fonts/space_invaders.ttf"
		
		# Game sounds
		self.player_shoot = pygame.mixer.Sound("sounds/player_shoot.wav")
		self.player_shoot.set_volume(0.2)
		
		# Color settings
		self.black = (0, 0 ,0)
		self.white = (255, 255, 255)
		self.red = (255, 0, 0)
		self.green = (0, 255, 0)
		self.blue = (0, 0, 255)
		
		# Player settings
		self.player_speed = 5
		self.player_offsetx = 106
		self.player_ship_image = pygame.image.load(
			"images/ships/player.png")
		self.player_lives = 3
		
		# Shot settings
		self.playershot_speed = 8
		self.playershot_limit = 1
		
		# Block settings
		self.block_size = 3
		self.block_color = self.green
		
		# Ground settings
		self.ground_height = self.screen_height - 56
		self.ground_offsetx = 50
		
		# Life settings
		self.life_height = self.screen_height - 50
		self.life_text_offsetx = 78
		self.life_ship_offsetx = 131
		self.life_ship_spacing = 9
		
		# Score Settings
		self.score_text_height = 26
		self.score_height = 51
		self.player1_score_x = 130
		self.hi_score_x = 330
