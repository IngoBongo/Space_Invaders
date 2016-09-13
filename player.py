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
		self.image = settings.player_ship_image
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		# Set the players starting position.
		self.rect.left = settings.player_offsetx
		self.rect.y = settings.player_y
		#self.rect.centery = self.screen_rect.centery
		
		# Store a decimal value for the ships center for fluid movement.
		self.center = float(self.rect.centerx)
		
		# Movement flags.
		self.moving_right = False
		self.moving_left = False
		
		# Lives remaining.
		self.remaining_lives = settings.player_lives
		
		# Set boundaries.
		self.left_boundary = settings.player_offsetx
		self.right_boundary = (settings.screen_width - 123)
		
		# Players score.
		self.score = 0
		
		# Active shot flag.
		self.has_active_shot = False
	
	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)
		
	def update(self):
		"""Update position of the player depending on movement flags."""
		# Update value of center based on movement flags
		if (self.moving_right and self.rect.right < self.right_boundary):
			self.rect.centerx += self.settings.player_speed
		if (self.moving_left and self.rect.left > self.left_boundary):
			self.rect.centerx -= self.settings.player_speed
		
		# Correct rect if player_speed makes ship go off screen.
		self.correct_rect()
	
	def correct_rect(self):
		"""Correct rect if ship is off screen."""
		if self.rect.right > self.right_boundary:
			self.rect.right = self.right_boundary
		elif self.rect.left < self.left_boundary:
			self.rect.left = self.left_boundary
		
	def reset_score(self):
		self.score = 0
