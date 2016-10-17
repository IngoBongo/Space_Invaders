import pygame
from pygame import Surface
from pygame import Rect
from text import Text

class ScoreBoard:
	"""A class to show the current and high score."""

	def __init__(self, settings, screen, stats):
		"""Initialize scoreboard."""
		self.screen = screen
		self.settings = settings
		self.stats = stats

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
		# Text for player 1 score, SCORE <1>.
		self.player1_score_text.append(Text(settings, self.screen, settings.font_size, "S C O R E <  1", settings.white,
		                                    75, settings.score_text_y))
		self.player1_score_text.append(Text(self.settings, self.screen, settings.font_size, ">", settings.white,
		                                    243, settings.score_text_y))

		# Text for hi-score, HI SCORE.
		self.hi_score_text.append(Text(settings, self.screen, settings.font_size, "H", settings.white,
		                               291, settings.score_text_y))
		self.hi_score_text.append(Text(settings, self.screen, settings.font_size, "I", settings.white,
		                               318, settings.score_text_y))
		self.hi_score_text.append(Text(settings, self.screen, settings.font_size, "S C O R E", settings.white,
		                               363, settings.score_text_y))

		# Text for player 2 score, SCORE <2>.
		self.player2_score_text.append(Text(settings, self.screen, settings.font_size, "S C O R E <", settings.white,
		                                    507, settings.score_text_y))
		self.player2_score_text.append(Text(settings, self.screen, settings.font_size, "2 >", settings.white,
		                                    651, settings.score_text_y))

	def prep_player1_score(self):
		"""Create rendered image of score."""
		# Add space between each character and add extra space after each occurrence of '1'.
		score = " ".join(str(self.stats.score)).replace("1", " 1")
		num_length = len(str(self.stats.score))

		if num_length < 4:
			score = ("0 " * (4 - num_length)) + score

		# Create score image.
		self.score_image = Text(self.settings, self.screen, 24, score, self.settings.white,
		                        self.settings.player1_score_x, self.settings.score_y)

	def prep_hi_score(self):
		"""Create rendered image of hi-score."""
		# Add space between each character and add extra space after each occurrence of '1'.
		hi_score = " ".join(str(self.stats.hi_score)).replace("1", " 1")
		num_length = len(str(self.stats.hi_score))

		if num_length < 4:
			hi_score = ("0 " * (4 - num_length)) + hi_score

		# Create hi_score image.
		self.hi_score_image = Text(self.settings, self.screen, 24, hi_score, self.settings.white,
		                           self.settings.hi_score_x, self.settings.score_y)

	# def prep_player2_score(self):
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
		self.prep_player1_score()
		self.prep_hi_score()
		self.score_image.blitme()
		self.hi_score_image.blitme()
