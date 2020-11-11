# ITSE-1359 - Introduction to Scripting Languages-- Python
# Zeb Campbell - FINAL PROJECT - EARTH DEFENSE 2481 - November 26, 2019

import pygame
from pygame.sprite import Sprite
from os import path
import random

class Alien(Sprite):
	"""A CLASS FOR BASIC ALIEN ENEMIES"""
	def __init__(self, ai_game):
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		super().__init__()
		self.image = pygame.image.load('images/alien1.png')
		self.rect = self.image.get_rect()
		self.rect.x = (self.settings.screen.get_rect().right + self.rect.width)
		self.x = float(self.rect.x)

	def update(self):
		"""MOVES ALIEN TO THE LEFT"""
		self.x -= (self.settings.alien_speed)
		self.rect.x = self.x

class SuperAlien(Alien):
	def __init__(self, ai_game):
		"""INITIALIZE ATTRIBUTES FOR SUPER ALIEN CLASS"""
		super().__init__(ai_game)
		self.image = pygame.image.load('images/alien2.png')
		self.rect = self.image.get_rect()
		self.rect.x = (self.settings.screen.get_rect().right + self.rect.width)
		self.x = float(self.rect.x)
		self.super_alien_health = 75

	def update(self):
		"""MOVES SUPER ALIEN TO THE LEFT"""
		self.x -= (self.settings.alien_speed)
		self.rect.x = self.x

class AlienMissile(Sprite):
	"""A CLASS FOR THE ALIEN MISSILE"""
	def __init__(self, ai_game):
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		super().__init__()
		self.image = pygame.image.load('images/missile.png')
		self.rect = self.image.get_rect()
		self.rect.y = (self.settings.screen.get_rect().bottom + self.rect.height)
		self.y = float(self.rect.y)

	def update(self):
		"""MOVES MISSILE UP THE SCREEN"""
		self.y -= (self.settings.alien_speed)
		self.rect.y = self.y

