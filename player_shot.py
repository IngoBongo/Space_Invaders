import pygame
import time
from pygame.sprite import Sprite

class PlayerShot(Sprite):
	"""A class representing a shot from the player."""
	
	def __init__(self, settings, screen, player):
		"""Initialize the PlayerShot and set its position."""
		super(PlayerShot, self).__init__()
		self.screen = screen
		self.settings = settings
		self.player = player
		
		# Load shot image and set its rect.
		self.image = pygame.image.load("images/shots/player_shot.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = player.rect.centerx
		self.rect.top = player.rect.top
		
		# Load explode image.
		self.explode = pygame.image.load("images/explosions/ship_shot_explosion1.png")
		
		# Store a decimal value for the shot position.
		self.y = float(self.rect.y)
		self.center = float(player.rect.centerx)
		
		# Set exploded flag.
		self.exploded = False
		
		# Set timer.
		self.timer = pygame.time.get_ticks()
		
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
			

	def shot_explode(self):
		"""Change shot image into explode image."""
		# Change image.
		self.image = self.explode
		
		# Get new rect.
		self.rect = self.image.get_rect()
		self.rect.centerx = self.center
		self.rect.y = self.y
		
		# set exploded flag to true and set time of explosion.
		self.exploded = True
		self.timer = pygame.time.get_ticks()
		
	def get_shot_rect(self):
		"""Get rect of shot image."""
		
