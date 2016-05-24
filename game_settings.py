import pygame

class Settings():
	"""A class to store all settings for Space Invaders."""
	
	def __init__(self):
		"""Initialize game settings."""
		
		# Screen settings
		self.screen_width = 1024
		self.screen_height = 896
		# Offset x and y to make game screen "inside" the arcade.
		self.offsetx = 200
		self.offsety = 185
		self.caption = "Space Invaders"
		# Source for arcade background image:
		# http://orig02.deviantart.net/3ed1/f/2009/242/f/4/space_invaders_sprite_sheet_by_gooperblooper22.png
		self.background_arcade = pygame.image.load("images/background/arcade_big.png")
		
		# Game sounds
		self.get_sounds()
		
		# Color settings
		self.black = (0, 0 ,0)
		self.white = (255, 255, 255)
		self.green = (0, 255, 0)
		#self.game_screen_blue = (54, 48, 97)
		self.game_screen_blue = (49, 49, 104)
		
		# Player settings
		self.player_speed = 5
		
		# Shot settings
		self.playershot_speed = 5
		self.playershot_limit = 1
	
	def get_sounds(self):
		self.sounds = {}
		for sound_name in ["player_shoot"]:
			self.sounds[sound_name] = pygame.mixer.Sound(
						"sounds/{}.wav".format(sound_name))
			self.sounds[sound_name].set_volume(0.2)
