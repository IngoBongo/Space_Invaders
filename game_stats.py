class GameStats():
	"""A class to hold onto game statistics."""
	
	def __init__(self):
		"""Initialize game statistics."""
		self.hi_score = 0
		self.level = 1
		
	def reset_game_stats(self):
		"""
		Reset every game stat that should be reset
		at the start of a new game/level.
		"""
		self.level = 1
