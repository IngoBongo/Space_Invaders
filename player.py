import pygame
from pygame.sprite import Sprite

class Player(Sprite):
	"""A class representing the player."""
	
	def __init__(self, settings, screen):
		"""Initialize the ship and set its starting position."""
		super(Player, self).__init__()
		self.screen = screen
		self.settings = settings
		
		# Load ship image and set rect for image and screen.
		self.image = pygame.image.load('images/ships/player.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		# Set the players starting position.
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom - 75
		#self.rect.centery = self.screen_rect.centery
		
		# Store a decimal value for the ships center for fluid movement.
		self.center = float(self.rect.centerx)
		
		# Movement flags.
		self.moving_right = False
		self.moving_left = False
	
	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)
		
	def update(self):
		"""Update position of the player depending on movement flags."""
		# Update value of center based on movement flags and
		# prevent player from moving off screen.
		if (self.moving_right and 
				self.rect.right < self.settings.screen_width):
			self.rect.centerx += self.settings.player_speed
		if (self.moving_left and self.rect.left > 0):
			self.rect.centerx -= self.settings.player_speed
		
		self.correct_rect()
	
	def correct_rect(self):
		"""Correct rect if ship is off screen."""
		if self.rect.right > self.settings.screen_width:
			self.rect.right = self.settings.screen_width
		elif self.rect.left < 0:
			self.rect.left = 0
		
