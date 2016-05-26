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
		self.prep_score_text()
		self.prep_player1_score()
		self.prep_hi_score()
		# TODO: self.prep_player2_score()
		
	def prep_score_text(self):
		"""Create rendered image for scoreboard text."""
		# Text for player 1 score, displayed at left side of screen.
		self.player1_score_text = Text(self.settings, self.screen, 25, 
			"S C O R E <  1  >", self.settings.white, 78, 
			self.settings.score_text_height)
			
		# Text for hi-score, displayed in middle of screen.
		self.hi_score_text = Text(self.settings, self.screen, 25, 
			"H  I  - S C O R E", self.settings.white, 0, 
			self.settings.score_text_height)
		# Center hi-score text.
		self.hi_score_text.set_rect_centerx(self.settings.screen_width / 2)
		
		# Text for player 2 score, displayed at right side of screen.
		self.player2_score_text = Text(self.settings, self.screen, 25, 
			"S C O R E <  2 >", self.settings.white, 
			self.settings.screen_width - self.player1_score_text.rect.right - 3,
			self.settings.score_text_height)
		
	def prep_player1_score(self):
		"""Create rendered image of score."""
		# Only show 4 digits for score,
		# Example: 12345 would be 2345.
		# Then add space between each character
		score = " ".join(str(self.player.score % 10000))
		if len(score) < 4:
			score = ("0 " * (4 - len(score))) + score
		self.score_image = Text(self.settings, self.screen, 25, score,
			self.settings.white, self.settings.player1_score_x,
			self.settings.score_height)
		
	def prep_hi_score(self):
		"""Create rendered image of hi-score."""
		# Only show 4 digits for score,
		# Example: 12345 would be 2345.
		# Then add space between each character
		hi_score = " ".join(str(self.game_stats.hi_score % 10000))
		if len(hi_score) < 4:
			hi_score = ("0 " * (4 - len(hi_score))) + hi_score
		self.hi_score_image = Text(self.settings, self.screen, 25, hi_score,
			self.settings.white, self.settings.hi_score_x,
			self.settings.score_height)
		
	#def prep_player2_score(self):
		# TODO: add player 2 score.

	def show_score(self):
		"""Draw most recent scoreboard to the screen."""
		# Draw text.
		self.player1_score_text.blitme()
		self.hi_score_text.blitme()
		self.player2_score_text.blitme()
		
		# Draw score.
		self.score_image.blitme()
		self.hi_score_image.blitme()
		
