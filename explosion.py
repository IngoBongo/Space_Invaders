import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from block import Block


class Explosion(Sprite):
	"""A class representing an explosion."""
	
	def __init__(self, settings, screen, x, y, ship_shot, invader_shot, ship, invader, mystery):
		super(Explosion, self).__init__()
		self.settings = settings
		self.screen = screen
		self.x = x
		self.y = y
		
		self.set_image(ship_shot, invader_shot, ship, invader, mystery)
		
		# Set time of explosion
		self.timer = pygame.time.get_ticks()
		
		# TODO: create other kinds of explosions
	
	def set_image(self, ship_shot, invader_shot, ship, invader, mystery):
		if ship_shot:
			self.image = self.create_ship_shot_explosion(self.settings, 
				self.screen, self.x, self.y)
		elif invader_shot:
			self.image = self.create_invader_shot_explosion(self.settings,
			    self.screen, self.x, self.y)
		elif invader:
			self.image = pygame.image.load("images/explosions/invader_explosion.png")

	def create_ship_shot_explosion(self, settings, screen, x, y):
		"""Create and return explosion "sprite" as a group of Blocks. Top-left point of group is set to x, y."""
		explode_blocks = Group()
		
		for row in range(settings.player_shot_explode_rows):
			for column in range(settings.player_shot_explode_columns):
				if settings.player_shot_explode_array[row][column] == 'b':
					new_block = Block(settings, screen, settings.white, 
						x + (column * settings.block_size),
						y + (row * settings.block_size))
					explode_blocks.add(new_block)

		return explode_blocks

	def create_invader_shot_explosion(self, settings, screen, x, y):
		"""Create and return explosion "sprite" as a group of Blocks. Top-left point of group is set to x, y."""
		explode_blocks = Group()

		for row in range(settings.invader_shot_explode_rows):
			for column in range(settings.invader_shot_explode_columns):
				if settings.invader_shot_explode_array[row][column] == 'b':
					new_block = Block(settings, screen, settings.white,
						x + (column * settings.block_size),
						y + (row * settings.block_size))
					explode_blocks.add(new_block)

		return explode_blocks
