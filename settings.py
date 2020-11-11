# ITSE-1359 - Introduction to Scripting Languages-- Python
# Zeb Campbell - FINAL PROJECT - EARTH DEFENSE 2481 - November 26, 2019

import pygame
from pygame.locals import *
import os

class Settings:
	"""A CLASS FOR SETTINGS FOR EARTH DEFENSE 2481"""
	def __init__(self):
		"""INITIALIZE STATIC GAME SETTINGS"""
		# SCREEN SETTINGS
		self.screen = pygame.display.set_mode((1200, 800))
		self.screen_width = 1200
		self.screen_height = 800
		self.bg = pygame.image.load(os.path.join('images','bg.png')).convert()
		self.bg = pygame.transform.scale(self.bg, (self.screen_width, self.screen_height))
		self.bgX = 0
		self.bgX2 = self.bg.get_width()

		# SHIP SETTINGS
		self.ship_speed = 3.0
		self.ship_limit = 3
		self.ship_health = 100

		# SHIP BULLET SETTINGS
		self.bullet_speed = 3.0
		self.bullet_width = 25
		self.bullet_height = 5
		self.bullet_color = (0, 255, 0)
		self.bullets_allowed = 20

		# SLIEN LASER SETTINGS
		self.laser_speed = 3.0
		self.laser_width = 25
		self.laser_height = 5
		self.laser_color = (255, 0, 0)
		self.laser_timer = 5000

		# BACKGROUND FPS
		self.bg_speed = 120

		# ALIEN SETTINGS
		self.alien_speed = 1.5
		self.alien_missile_speed = 4.0
		
		# SPEED OF BONUSES
		self.bonus_speed = 2.0
		
		# INCREASES SPEED
		self.speedup_scale = 1.3

		# INCREASES SCORING
		self.score_scale = 1.3

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""INITIALIZE SETTINGS THAT CAN CHANGE THROUGHOUT THE GAME."""
		self.ship_speed = 3.0
		self.bullet_speed = 3.0
		self.alien_speed = 1.5
		self.bonus_speed = 2.0
		self.alien_missile_speed = 4.0

		# SCORING
		self.normal_alien_points = 50
		self.super_alien_points = 75
		self.alien_missile_points = 100

	def increase_speed(self):
		"""INCREASE SPEED SETTINGS AND POINT VALUES"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.laser_speed *= self.speedup_scale
		self.alien_missile_speed *= self.speedup_scale
		self.bonus_speed *= self.speedup_scale

		self.normal_alien_points = int(self.normal_alien_points * self.score_scale)
		self.super_alien_points = int(self.super_alien_points * self.score_scale)
		self.alien_missile_points = int(self.alien_missile_points * self.score_scale)


		