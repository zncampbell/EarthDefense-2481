# ITSE-1359 - Introduction to Scripting Languages-- Python
# Zeb Campbell - FINAL PROJECT - EARTH DEFENSE 2481 - November 26, 2019

import pygame.font

class Button:
	def __init__(self, ai_game, msg):
		"""INITIALIZE BUTTON ATTRIBUTES"""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		# SETS DIMS AND PROPERTIES OF BUTTON
		self.width, self.height = 200, 50
		self.button_color = (145, 145, 145)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		# BUILD BUTTON'S RECT OBJECT
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		# PREPS BUTTON MESSAGE
		self._prep_msg(msg)

	def _prep_msg(self, msg):
		"""TURNS MESSAGE INTO RENDERED IMAGE"""
		self.msg_image = self.font.render(msg, True, self.text_color, 
			self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		# DRAWS BLANK BUTTON AND MESSAGE.
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)