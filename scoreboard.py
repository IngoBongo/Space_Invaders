import pygame
from pygame import Surface
from pygame import Rect
from text import Text

class ScoreBoard:
	"""A class to show the current and high score."""

	def __init__(self, settings, screen, player, game_stats):
		"""Initialize scoreboard."""
		self.screen = screen
		self.settings = settings
		self.game_stats = game_stats
		self.player = player

		# Prep score images.
		self.player1_score_text = []
		self.hi_score_text = []
		self.player2_score_text = []
		self.prep_score_text(settings)
		self.prep_player1_score()
		self.prep_hi_score()
		# TODO: self.prep_player2_score()

	def prep_score_text(self, settings):
		"""Create rendered image for scoreboard text."""
		# Text for player 1 score, displayed at left side of screen.
		self.player1_score_text.append(Text(settings, self.screen,
			settings.font_size, "S C O R E <  1", settings.white,
			75, settings.score_text_y))
		self.player1_score_text.append(Text(self.settings, self.screen,
			settings.font_size, ">", settings.white,
			243, settings.score_text_y))

		# Text for hi-score, displayed in middle of screen.
		self.hi_score_text.append(Text(settings, self.screen,
			settings.font_size, "H", settings.white,
			291, settings.score_text_y))
		self.hi_score_text.append(Text(settings, self.screen,
			settings.font_size, "I", settings.white,
			318, settings.score_text_y))
		self.hi_score_text.append(Text(settings, self.screen,
			settings.font_size, "S C O R E", settings.white,
			363, settings.score_text_y))

		# Text for player 2 score, displayed at right side of screen.
		self.player2_score_text.append(Text(settings, self.screen,
			settings.font_size, "S C O R E <", settings.white,
			507, settings.score_text_y))
		self.player2_score_text.append(Text(settings, self.screen,
			settings.font_size, "2 >", settings.white,
			651, settings.score_text_y))

	def prep_player1_score(self):
		"""Create rendered image of score."""
		# Only show 4 digits for score,
		# Example: 12345 would be 2345.
		# Then add space between each character
		score = " ".join(str(self.player.score % 10000))
		if len(score) < 4:
			score = ("0 " * (4 - len(score))) + score
		self.score_image = Text(self.settings, self.screen, 24, score,
			self.settings.white, self.settings.player1_score_x,
			self.settings.score_y)

	def prep_hi_score(self):
		"""Create rendered image of hi-score."""
		# Only show 4 digits for score,
		# Example: 12345 would be 2345.
		# Then add space between each character
		hi_score = " ".join(str(self.game_stats.hi_score % 10000))
		if len(hi_score) < 4:
			hi_score = ("0 " * (4 - len(hi_score))) + hi_score
		self.hi_score_image = Text(self.settings, self.screen, 24,
			hi_score, self.settings.white, self.settings.hi_score_x,
			self.settings.score_y)

	#def prep_player2_score(self):
		# TODO: add player 2 score.

	def show_score(self):
		"""Draw most recent scoreboard to the screen."""
		# Draw "PLAYER <1>"
		for text in self.player1_score_text:
			text.blitme()

		# DRAW "HI-SCORE"
		for text in self.hi_score_text:
			text.blitme()
		# Draw dash since the dash in the font is of incorrect size.
		pygame.draw.rect(self.screen, self.settings.white,
			Rect(339, 36, 15, 3))

		# Draw "PLAYER <2>"
		for text in self.player2_score_text:
			text.blitme()

		# Draw score.
		self.score_image.blitme()
		self.hi_score_image.blitme()

