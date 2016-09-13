import pygame
from pygame.sprite import Group
from pygame.sprite import Sprite

import game_functions as func
from explosion import Explosion


class PlayerShot(Sprite):
	"""A class representing a shot from the player."""
	
	def __init__(self, settings, screen, player):
		"""Initialize the PlayerShot and set its position."""
		super(PlayerShot, self).__init__()
		self.screen = screen
		self.settings = settings
		self.player = player
		
		# Load shot image and set its rect.
		self.image = pygame.transform.scale(pygame.image.load("images/shots/player_shot.png"), (3, 12))
		self.rect = self.image.get_rect()
		self.rect.centerx = player.rect.centerx
		self.rect.top = player.rect.top
		
		# Blocks making up the explosion will be stored in this group.
		self.explosion = Group()
		
		# Store a decimal value for the shot position.
		self.y = float(self.rect.y)
		self.center = float(player.rect.centerx)
		
		# Set exploded and color flag.
		self.exploded = False
		self.is_red = False
		
	def blitme(self):
		"""Draw the PlayerShot at it's current location."""
		self.screen.blit(self.image, self.rect)
	
	def update(self):
		"""Update position of bullet."""
		# Move shot up the screen if it hasn't exploded.
		if not self.exploded:
			self.y -= self.settings.playershot_speed
			# Update the rect.
			self.rect.y = self.y
			self.center = self.rect.centerx
	
	def explode(self, x, y):
		"""Set shot to exploded state."""
		self.exploded = True
		# Color shot black to hide it.
		func.color_surface(self.image, self.settings.black)
		# Create explosion "image".
		self.explosion = Explosion(self.settings, self.screen, x, y,
			True, False, False, False, False)
