import pygame
from pygame.sprite import Sprite

class Block(Sprite):
	"""A class representing a single block."""
	
	def __init__(self, settings, screen):
		"""Initialize Block."""
		self.screen = screen
		self.width = settings.block_size
		self.height = settings.block_size
		self.color = settings.block_color
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(self.color)
		self.image.rect = self.image.get_rect()
		
	def blitme(self):
		"""Draw the block at its current location."""
		self.screen.blit(self.image, self.rect)
