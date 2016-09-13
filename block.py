import pygame
from pygame.sprite import Sprite


class Block(Sprite):
	"""A class representing a single block."""
	
	def __init__(self, settings, screen, color, x, y):
		"""Initialize Block."""
		super(Block, self).__init__()
		self.screen = screen
		self.width = settings.block_size
		self.height = settings.block_size
		self.color = color
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
	def blitme(self):
		"""Draw the block at its current location."""
		self.screen.blit(self.image, self.rect)
	
	def update_position(self, x, y):
		self.rect.x = x
		self.rect.y = y
