import pygame

class Text:
	"""A class representing text."""
	
	def __init__(self, settings, screen, font_size, message, color,
			x_pos, y_pos):
		"""Initialize text."""
		self.settings = settings
		self.screen = screen
		self.font = pygame.font.Font(settings.font, font_size)
		self.image = self.font.render(message, True, color)
		self.rect = self.image.get_rect()
		self.rect.x = x_pos
		self.rect.y = y_pos
		
	def blitme(self):
		"""Draw the text at its current position."""
		self.screen.blit(self.image, self.rect)

	def set_rect_centerx(self, centerx):
		self.rect.centerx = centerx
