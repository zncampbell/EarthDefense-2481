# ITSE-1359 - Introduction to Scripting Languages-- Python
# Zeb Campbell - FINAL PROJECT - EARTH DEFENSE 2481 - November 26, 2019

import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
	"""CLASS FOR SCOREKEEPING"""
	def __init__(self, ai_game):
		"""INITIALIZE SCOREKEEPING ATTRIBUTES."""
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats

		# FONT SETTINGS
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)

		# PREPARE INITIAL IMAGES
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
		self.prep_ship_health()

	def prep_score(self):
		"""TURNS SCORE INTO IMAGE"""
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, 
			self.text_color)

		# DISPLAYS SCORE IN TOP RIGHT OF SCREEN
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def show_score(self):
		"""PREPS SCORE AND SHIPS"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def prep_high_score(self):
		"""TURNS HIGH SCORE INTO IMAGE"""
		high_score = round(self.stats.high_score, -1)
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True, 
			self.text_color)

		# CENTERS HIGH SCORE AT TOP OF SCREEN
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.right = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def check_high_score(self):
		"""CHECKS HIGH SCORE."""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	def prep_level(self):
		"""TURNS LEVEL INTO IMAGE."""
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str, True, 
			self.text_color)
		# POSITIONS LEVEL UNDER SCORE.
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		"""SHOWS REMAINING SHIPS"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_game)
			# Position the level below the score.
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)

	def prep_ship_health(self):
		"""SHOWS SHIP HEALTH BAR"""
		if self.stats.ship_health == 100:
			self.ship_health_image = pygame.image.load('images/health100.png')
		elif self.stats.ship_health == 75:
			self.ship_health_image = pygame.image.load('images/health75.png')
		elif self.stats.ship_health == 50:
			self.ship_health_image = pygame.image.load('images/health50.png')
		elif self.stats.ship_health == 25:
			self.ship_health_image = pygame.image.load('images/health25.png')
		self.ship_health_rect = self.ship_health_image.get_rect()
		self.ship_health_rect.left = 10
		self.ship_health_rect.top = 50
		self.screen.blit(self.ship_health_image, self.ship_health_rect)

