import pygame
from pygame.sprite import Sprite

class Invader(Sprite):
	"""A class representing a single Invader."""
	
	def __init__(self, settings, screen, row, x, y):
		"""Initialize the Invader."""
		super(Invader, self).__init__()
		self.settings = settings
		self.screen = screen
		self.row = row
		
		# Set direction to start moving right, 1 == right, -1 == left.
		self.direction = 1
		
		# Load invader images, set starting image and rect.
		self.images = []
		self.load_images()
		self.image_index = 0
		self.image = self.images[self.image_index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
		# Set time of last time invader moved/time of instatiation.
		self.time_of_last_move = pygame.time.get_ticks()
		
		# Set moved flag.
		self.has_moved = False
		self.exploded = False
		
	def change_image(self):
		"""Change to next image."""
		# Use bitwise XOR to toggle index between 0 and 1.
		self.image_index = self.image_index ^ 1
		self.image = self.images[self.image_index]
	
	def change_direction(self):
		"""Change direction."""
		self.direction *= -1

	def load_images(self):
		"""Load invader image based on it's row position."""
		if self.row == 0:
			number = "1"
		elif self.row == 1 or self.row == 2:
			number = "2"
		else:
			number = "3"
		
		self.images = [pygame.image.load("images/invaders/invader" + 
			number + "-" + str(n) + ".png")
			for n in range(1, 3)]
	
	def blitme(self):
		"""Draw the invader at its current position."""
		self.screen.blit(self.image, self.rect)
		
	def update(self, current_time):
		"""Update position of invader."""
		# Check if its time to move, only move if not exploded.
		if (current_time - self.time_of_last_move >= self.settings.invader_move_time
			and not self.exploded):
			# Move invader, change image and set time of move.
			self.rect.x += self.settings.invader_move_x * self.settings.fleet_direction
			self.change_image()
			self.time_of_last_move = current_time
			self.has_moved = True
	
	def is_at_boundary(self):
		"""Returns True if invader is at left or right boundary."""
		if self.row == 0:
			offset_x, offset_y = 6, 6
		elif self.row == 1 or self.row == 2:
			offset_x, offset_y = 3, 0
		else:
			offset_x, offset_y = 0, 0
			
		if self.rect.right + offset_x >= self.settings.invader_right_boundary:
			return True
		elif self.rect.left + offset_y <= self.settings.invader_left_boundary:
			return True
	
	def explode(self, x, y):
		"""Set shot to exploded state."""
		self.exploded = True
		self.image = pygame.image.load("images/explosions/invader_explosion.png")
		if self.row == 0:
			self.rect.x -= 6
		self.time_of_last_move = pygame.time.get_ticks()
