# ITSE-1359 - Introduction to Scripting Languages-- Python
# Zeb Campbell - FINAL PROJECT - EARTH DEFENSE 2481 - November 26, 2019

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
	"""A CLASS FOR THE SHIP BULLETS"""
	def __init__(self, ai_game):
		"""CREATES BULLET AT SHIP'S LOCATION"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color
		# CREATES BULLET AT (0, 0) AND THEN CORRECTS POSITION
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
			self.settings.bullet_height)
		self.rect.midright = ai_game.ship.rect.midright
		# STORES BULLET POSITION AS A DECIMAL POSITION
		self.x = float(self.rect.x)

	def update(self):
		"""MOVES BULLET ACROSS THE SCREEN"""
		# UPDATES DECIMAL POSITION
		self.x += self.settings.bullet_speed
		# UPDATES THE RECT POSITION
		self.rect.x = self.x

	def draw_bullet(self):
		"""DRAWS BULLET ON THE SCREEN"""
		pygame.draw.rect(self.screen, self.color, self.rect)


class AlienLaser(Sprite):
	"""A CLASS FOR ALIEN LASERS"""
	def __init__(self, ai_game):	
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.laser_color
		self.rect = pygame.Rect(0, 0, self.settings.laser_width,
			self.settings.laser_height)
		self.rect.midleft = ai_game.alien.rect.midleft
		# STORES LASER AS DECIMAL POSITION
		self.x = float(self.rect.x)

	def update(self):
		"""MOVES LASER ACROSS SCREEN."""
		# UPDATES DECIMAL POSITION OF LASER
		self.x -= self.settings.laser_speed
		# UPDATES RECT POSITION
		self.rect.x = self.x

	def draw_laser(self):
		"""DRAWS LASER ON SCREEN"""
		pygame.draw.rect(self.screen, self.color, self.rect)




