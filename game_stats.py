# ITSE-1359 - Introduction to Scripting Languages-- Python
# Zeb Campbell - FINAL PROJECT - EARTH DEFENSE 2481 - November 26, 2019

class GameStats:
	"""TRACKING STATS FOR EARTH DEFENSE 2481."""
	def __init__(self, ai_game):
		"""INITIALIZE STATS"""
		self.settings = ai_game.settings
		self.reset_stats()

		# STARTS THE GAME IN AN INACTIVE STATE
		self.game_active = False

		# HIGH SCORE DOES NOT RESET.
		self.high_score = 0
	# RESETS THE STATS
	def reset_stats(self):
		"""INITIALIZE STATS THAT CAN CHANGE IN GAME"""
		self.ships_left = self.settings.ship_limit
		self.ship_health = self.settings.ship_health
		self.score = 0
		self.level = 1
		self.lvl_tracking = 2500
		self.lvl_tracking_points = 2500