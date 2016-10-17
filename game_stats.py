class GameStats():
	"""A class to hold onto game statistics."""

	def __init__(self, settings):
		"""Initialize game statistics."""
		self.settings = settings
		self.hi_score = 0
		self.reset_game_stats()

		self.game_active = True

	def reset_game_stats(self):
		"""
		Reset every game stat that should be reset at the start of a new game.
		"""
		self.level = 1
		# TODO: Place score here instead of in the Player class
		self.score = 0
		self.ships_left = self.settings.player_lives
