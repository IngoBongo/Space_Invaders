import pygame
from pygame.sprite import Sprite

class PlayerShot(Sprite):
	"""A class representing a shot from the player."""
	
	def __init__(self, settings, screen, player):
		"""Initialize the PlayerShot and set its position."""
		super(PlayerShot, self).__init__()
		self.screen = screen
		self.settings = settings
		
		# Load PlayerShot image and set its rect.
		self.image = pygame.image.load("images/shots/player_shot.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = player.rect.centerx
		self.rect.top = player.rect.top
		
		# Store a decimal value for the PlayerShot.
		self.y = float(self.rect.y)
		
	def blitme(self):
		"""Draw the PlayerShot at it's current location."""
		self.screen.blit(self.image, self.rect)
	
	def update(self):
		"""Update position of bullet."""
		# Move PlayerShot up the screen.
		self.y -= self.settings.playershot_speed
		# Update the rect.
		self.rect.y = self.y
