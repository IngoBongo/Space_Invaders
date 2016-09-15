import pygame
from pygame.sprite import Group
from pygame.sprite import Sprite
from random import randint


import game_functions as func
from explosion import Explosion


class InvaderShot(Sprite):
	"""A class representing a shot from an invader."""

	def __init__(self, settings, screen, invader):
		"""Initialize the InvaderShot and set its position."""
		super(InvaderShot, self).__init__()
		self.screen = screen
		self.settings = settings
		self.invader = invader

		# Load shot image and set its rect.
		self.images = []
		self.load_images()
		self.shot_variant = 0
		self.image_index = 0
		self.image = self.images[self.image_index]
		self.rect = self.image.get_rect()
		self.rect.centerx = invader.rect.centerx
		self.rect.bottom = invader.rect.bottom

		# Blocks making up the explosion will be stored in this group.
		self.explosion = Group()

		# Store a decimal value for the shot position.
		self.y = float(self.rect.y)
		self.center = float(invader.rect.centerx)

		# Set exploded flag.
		self.exploded = False

	def load_images(self):
		"""Choose random invader_shot animation variation and load all images for it."""
		self.shot_variant = randint(1, 3)
		if self.shot_variant == 3:
			self.images = [pygame.image.load("images/shots/invader-shot" +
			                                 str(self.shot_variant) + "-" + str(n) + ".png") for n in range(1, 4)]
		else:
			self.images = [pygame.image.load("images/shots/invader-shot" +
			                                 str(self.shot_variant) + "-" + str(n) + ".png") for n in range(1, 5)]

	def blitme(self):
		"""Draw the InvaderShot at it's current location."""
		self.screen.blit(self.image, self.rect)

	def change_image(self):
		if self.shot_variant == 3:
			self.image_index = (self.image_index + 1) % 3
		else:
			self.image_index = (self.image_index + 1) % 4
		self.image = self.images[self.image_index]

	def update(self):
		"""Update position of shot."""
		# Move shot down the screen if it hasn't exploded yet.
		if not self.exploded:
			self.y += self.settings.invadershot_speed
			# Update the rect
			self.rect.y = self.y
			self.center = self.rect.centerx

	def explode(self, x, y):
		"""Set shot to exploded state."""
		self.exploded = True
		# Color shot black to hide it.
		func.color_surface(self.image, self.settings.black)
		# Create explosion "image".
		self.explosion = Explosion(self.settings, self.screen, x, y,
		                           False, True, False, False, False)
