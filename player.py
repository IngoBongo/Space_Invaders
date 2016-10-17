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
		self.set_ship_image()
		self.explosion_image = self.load_explosion_images()
		self.explosion_image_index = 0

		# Set the players starting position.
		self.set_starting_position()

		# Flags.
		self.moving_right = False
		self.moving_left = False
		self.allowed_to_shoot = True
		self.has_active_shot = False
		self.exploded = False

		# Set boundaries.
		self.left_boundary = settings.player_offsetx
		self.right_boundary = (settings.screen_width - 123)

		self.frame_count = 0
		self.image_change_counter = 0

	def set_ship_image(self):
		self.image = self.settings.player_ship_image
		self.rect = self.image.get_rect()

	def set_starting_position(self):
		self.rect.x = self.settings.player_offsetx
		self.rect.y = self.settings.player_y

	def load_explosion_images(self):
		return [pygame.image.load("images/explosions/ship_explosion" + str(i) + ".png")
				for i in range(1, 3)]

	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)

	def update(self):
		"""Update position of the player depending on movement flags."""
		if self.exploded:
			self.frame_count += 1
			if self.frame_count == 6:
				self.change_explosion_image()
				self.frame_count = 0
		else:
			# Update value of center based on movement flags
			if self.moving_right and self.rect.right < self.right_boundary:
				self.rect.centerx += self.settings.player_speed
			if self.moving_left and self.rect.left > self.left_boundary:
				self.rect.centerx -= self.settings.player_speed
			# Correct rect if player_speed makes ship go off screen.
			self.correct_rect()

	def change_explosion_image(self):
		self.explosion_image_index ^= 1
		self.image = self.explosion_image[self.explosion_image_index]
		self.image_change_counter += 1

	def correct_rect(self):
		"""Correct rect if ship is off screen."""
		if self.rect.right > self.right_boundary:
			self.rect.right = self.right_boundary
		elif self.rect.left < self.left_boundary:
			self.rect.left = self.left_boundary

	def reset_ship(self):
		self.frame_count = 0
		self.image_change_counter = 0
		self.exploded = False
		self.allowed_to_shoot = True
		self.set_ship_image()
		self.set_starting_position()

	def explode(self):
		"""Set player to exploded state."""
		self.exploded = True
		self.allowed_to_shoot = False
		self.explosion_image_index = 0
		self.image = self.explosion_image[0]
		self.rect.x = self.rect.x - 6
