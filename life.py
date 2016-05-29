from pygame.sprite import Sprite

class Life(Sprite):
	"""A class representing one life."""
	
	def __init__(self, settings, screen, x, y):
		"""Initialize life."""
		super(Life, self).__init__()
		self.settings = settings
		self.screen = screen
		self.image = settings.player_ship_image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
