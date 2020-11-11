# ITSE-1359 - Introduction to Scripting Languages-- Python
# Zeb Campbell - FINAL PROJECT - EARTH DEFENSE 2481 - November 26, 2019

import pygame
from pygame.sprite import Sprite
from os import path
import random

class Health(Sprite):
	"""A CLASS FOR THE HEALTH SPRITE."""
	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.image = pygame.image.load('images/heart.png')
		self.rect = self.image.get_rect()
		self.rect.x = (self.settings.screen.get_rect().right + self.rect.width)
		self.x = float(self.rect.x)

	def update(self):
		"""MOVES HEALTH TO LEFT"""
		self.x -= (self.settings.bonus_speed)
		self.rect.x = self.x

class ExtraLife(Sprite):
	"""A CLASS FOR EXTRA LIFE SPRITES"""
	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.image = pygame.image.load('images/extralife.png')
		self.rect = self.image.get_rect()
		self.rect.x = (self.settings.screen.get_rect().right + self.rect.width)
		self.x = float(self.rect.x)

	def update(self):
		"""MOVE EXTRA LIFE TO LEFT"""
		self.x -= (self.settings.bonus_speed)
		self.rect.x = self.x
