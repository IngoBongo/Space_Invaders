import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from block import Block

class Explosion(Sprite):
	"""A class representing an explosion."""
	
	def __init__(self, settings, screen, x, y,):
		super(Explosion, self).__init__()
		self.settings = settings
		self.screen = screen
		
		self.image = self.create_ship_shot_explosion(settings, screen, x, y)
		
		# Set time of explosion
		self.timer = pygame.time.get_ticks()
		
		# TODO: create other kinds of explosions

	def create_ship_shot_explosion(self, settings, screen, x, y):
		"""
		Create and return explosion "sprite" as a group of Blocks.
		Topleft point of group is set to x, y.
		"""
		explode_blocks = Group()
		
		for row in range(settings.player_shot_explode_rows):
			for column in range(settings.player_shot_explode_columns):
				if settings.player_shot_explode_array[row][column] == 'b':
					new_block = Block(settings, screen, settings.white, 
						x + (column * settings.block_size),
						y + (row * settings.block_size))
					explode_blocks.add(new_block)

		return explode_blocks
