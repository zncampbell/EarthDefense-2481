import pygame
from time import *
from pygame.locals import *
import sys
import os
import random
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import *
from alien import *
from bonus import *

class EarthDefense:
	"""OVERALL CLASS FOR THE GAME."""

	def __init__(self):
		"""INITIALIZE GAME AND CREATE RESOURCES"""
		pygame.init()
		self.settings = Settings()
		os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"
		self.screen = pygame.display.set_mode((0,0), FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		self.settings.screen = self.screen
		pygame.display.set_caption("Earth Defense 2481")
		# THIS SETS UP THE GAME AND SPRITE GROUPS.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		self.alien = Alien(self)
		self.superalien = SuperAlien(self)
		self.ship = Ship(self)
		self.alienlaser = AlienLaser(self)
		self.alienmissile = AlienMissile(self)
		self.bullets = pygame.sprite.Group()
		self.lasers = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self.hearts = pygame.sprite.Group()
		self.extralife = pygame.sprite.Group()
		self.superaliens = pygame.sprite.Group()
		self.alienmissiles = pygame.sprite.Group()

		# CREATES THE PLAY BUTTON.
		self.play_button = Button(self, "Play")

	# THIS SECTION STARTS THE GAME RUNNING.
	def run_game(self):
		"""Start the main loop for the game."""
		DS = self.settings.screen
		x = 0
		clock = pygame.time.Clock()
		
		while True:
			self._check_events()
			# SETUP FOR SCROLLING BACKGROUND.
			rel_x = x % self.settings.bg.get_rect().width
			DS.blit(self.settings.bg, (rel_x - self.settings.bg.get_rect().width, 0))
			if rel_x < self.settings.screen_width:
				DS.blit(self.settings.bg, (rel_x, 0))
			x -= 1
			clock.tick(self.settings.bg_speed)

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_sprites()   

			self._update_screen()       
	  
	# THIS SECTION CHECKS THE PLAY BUTTON TO START THE GAME.
	def _check_play_button(self, mouse_pos):
		"""STARTS A NEW GAME"""
		if self.play_button.rect.collidepoint(mouse_pos):
			button_clicked = self.play_button.rect.collidepoint(mouse_pos)
			if button_clicked and not self.stats.game_active:
				# RESETS THE GAME SETTINGS
				self.settings.initialize_dynamic_settings()

				# CLEARS REMAINING ALIENS AND BULLETS.
				self.aliens.empty()
				self.superaliens.empty()
				self.alienmissiles.empty()
				self.lasers.empty()
				self.bullets.empty()
				self.hearts.empty()
				self.extralife.empty()

				# RESETS THE GAME STATS
				self.stats.reset_stats()
				self.stats.game_active = True
				self.sb.prep_score()
				self.sb.prep_level()
				self.sb.prep_ships()


				# CREATES TIMERS FOR USEREVENTS
				# CREATING ALIENS
				pygame.time.set_timer(USEREVENT+2, random.randrange(1500, 2500))
				# CREATING MISSILES
				pygame.time.set_timer(USEREVENT+4, random.randrange(6000, 15000))
				# CREATING HEALTH
				pygame.time.set_timer(USEREVENT+5, random.randrange(50000, 70000))
				# CREATING EXTRA LIFE
				pygame.time.set_timer(USEREVENT+6, random.randrange(100000, 120000))
				# CALLING ON SUPER ALIEN LASERS TO FIRE
				pygame.time.set_timer(USEREVENT+7, self.settings.laser_timer)

				# CENTERS THE SHIP
				self.ship.center_ship()     

				# HIDES THE MOUSE CURSOR
				pygame.mouse.set_visible(False)

# THIS SECTION CHECKS FOR VARIOUS EVENTS BEFORE AND DURING THE GAME.
	# THIS SECTION CHECKS FOR KEY DOWN EVENTS.
	def _check_keydown_events(self, event):
		"""RESPOND TO KEY PRESSES."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_UP:
			self.ship.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	# THIS SECTION CHECKS FOR KEY UP EVENTS
	def _check_keyup_events(self, event):
		"""RESPOND TO KEY RELEASES."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False   
		elif event.key == pygame.K_UP:
			self.ship.moving_up = False
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = False 

	# THIS SECTION CHECKS FOR EVENTS.
	def _check_events(self):
		"""RESPONDS TO KEY PRESSES, USEREVENTS, AND MOUSE CLICKS."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN: 
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
			elif event.type == USEREVENT+2:
				self._create_alien()
			elif event.type == USEREVENT+4:
				self._create_alien_missile()
			elif event.type == USEREVENT+5:
				self._create_health()  
			elif event.type == USEREVENT+6:
				self._create_extra_life()  
			elif event.type == USEREVENT+7:
				self._fire_laser()         

# THIS SECTION COVERS THE CREATION AND REMOVAL OF BULLETS.
	# THIS SECTION CREATES SHIP BULLETS
	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
	# THIS SECTION CREATES ALIEN LASERS
	def _fire_laser(self):
		for alien in self.superaliens.sprites():
			new_laser = AlienLaser(self)
			new_laser.x = alien.x
			new_laser.rect.midleft = alien.rect.midleft
			self.lasers.add(new_laser)

	# THIS SECTION UPDATES THE BULLETS AND LASERS AND REMOVES THEM WHEN OFF SCREEN.
	def _update_bullets(self):
		"""UPDATES POSITION OF BULLETS AND REMOVES THEM FROM SCREEN."""
		# UPDATE BULLET POSITIONS
		self.bullets.update()
		self.lasers.update()
		# GETS RID OF BULLETS AND LASERS OFF SCREEN
		for bullet in self.bullets.copy():
			if bullet.rect.left >= self.settings.screen.get_rect().right:
				self.bullets.remove(bullet)
		for laser in self.lasers.copy():
			if laser.rect.right <= self.settings.screen.get_rect().left:
				self.lasers.remove(laser)
		# CALLS FUNCTION TO CHECK FOR BULLET AND LASER COLLISIONS.
		self._check_bullet_alien_collisions()
		self._check_ship_collisions()

# THIS SECTION CREATES ALL SPRITES AND PROJECTILES.
	# THIS SECTION CREATES THE ALIEN AND SUPER ALIENS.
	def _create_alien(self):
		# CALLS FOR A RANDOM NUMBER.
		random_alien = random.randrange(1, 10)
		# BASIC ALIENS HAVE A HIGHER PROBABILITY OF BEING CREATED.
		if random_alien != 2:
			alien = Alien(self)
			alien_width, alien_height = alien.rect.size
			alien.rect.y = random.randrange(0 + alien_height, self.settings.screen_height - alien_height)
			self.aliens.add(alien)
		# SUPER ALIENS HAVE A MUCH LOWER PROBABILITY OF BEING CREATED.    
		elif random_alien == 2:
			superalien = SuperAlien(self)
			superalien_width, superalien_height = superalien.rect.size
			superalien.rect.y = random.randrange(0 + superalien_height, self.settings.screen_height - superalien_height)
			self.superaliens.add(superalien)

	# THIS SECTION CREATES THE ALIEN MISSILES.
	def _create_alien_missile(self):
		missile = AlienMissile(self)
		missile_width, missile_height = missile.rect.size
		missile.rect.x = random.randrange(0 + missile_width, self.settings.screen_width - missile_width)
		self.alienmissiles.add(missile)

	# THIS SECTION CREATES EXTRA HEALTH.      
	def _create_health(self):
		bonus = Health(self)
		bonus_width, bonus_height = bonus.rect.size
		bonus.rect.y = random.randrange(0 + bonus_height, self.settings.screen_height - bonus_height)
		self.hearts.add(bonus)

	# THIS SECTION CREATES AN EXTRA LIFE.
	def _create_extra_life(self):
		life = ExtraLife(self)
		life_width, life_height = life.rect.size
		life.rect.y = random.randrange(0 + life_height, self.settings.screen_height - life_height)
		self.extralife.add(life)
	 
# THIS SECTION UPDATES THE SCREEN AND UPDATES THE SPRITES.
	# THIS SECTION UPDATES THE SPRITES AND         
	def _update_sprites(self):
		"""UPDATES SPRITES AND CHECKS FOR COLLISIONS OR EXITING THE SCREEN."""
		# UPDATES ENEMY AND BONUS SPRITES ON THE SCREEN.
		self.aliens.update()
		self.hearts.update()
		self.extralife.update()
		self.superaliens.update()
		self.alienmissiles.update()
		# CALLS FUNCTIONS TO CHECK ON SPRITES EXITING THE SCREEN.
		self._check_sprites_left()
		self._check_sprites_top()

	# THIS SECTION UPDATES THE SCREEN IMAGES.
	def _update_screen(self):
			"""UPDATES THE IMAGES ON THE SCREEN AND FLIPS TO NEW SCREEN"""
			# DRAWS THE SHIP ON THE SCREEN.
			self.ship.blitme()
			# DRAWS THE BULLETS AND LASERS ON THE SCREEN.
			for bullet in self.bullets.sprites():
				bullet.draw_bullet()
			for laser in self.lasers.sprites():
				laser.draw_laser()
			# DRAWS THE SPRITES.
			self.aliens.draw(self.screen)
			self.hearts.draw(self.screen)
			self.extralife.draw(self.screen)
			self.superaliens.draw(self.screen)
			self.alienmissiles.draw(self.screen)
			# DRAWS THE SCORE AND HEALTHBAR.
			self.sb.show_score()
			self.sb.prep_ship_health()
			# CHECKS FOR LEVELING UP.
			if self.stats.score >= self.stats.lvl_tracking:
				self.stats.level += 1
				self.settings.increase_speed()
				self.sb.prep_level()
				self.stats.lvl_tracking_points *= 1.2
				self.stats.lvl_tracking += self.stats.lvl_tracking_points
				
			# DRAWS THE PLAY BUTTON IF GAME IS INACTIVE.
			if not self.stats.game_active:
				self.play_button.draw_button()
			# REFRESHES SCREEN
			pygame.display.flip()


# THIS SECTION CHECKS FOR HITS AND COLLISIONS.
	# THIS SECTION DETECTS DAMAGE TO THE SHIP FROM COLLISIONS.
	def _check_ship_collisions(self):
		"""MONITORS FOR COLLISIONS WITH ENEMIES AND SHIP AND LOWERS HEALTH"""
		# LOOKS FOR ENEMY AND SHIP COLLISIONS.
		if pygame.sprite.spritecollide(self.ship, self.aliens, True):
			self.stats.ship_health -= 25
			if self.stats.ship_health <= 0:
				self._ship_hit()
		if pygame.sprite.spritecollide(self.ship, self.lasers, True):
			self.stats.ship_health -= 25
			if self.stats.ship_health <= 0:
				self._ship_hit()
		if pygame.sprite.spritecollide(self.ship, self.superaliens, True):
			self.stats.ship_health -= 25
			if self.stats.ship_health <= 0:
				self._ship_hit()
		if pygame.sprite.spritecollide(self.ship, self.alienmissiles, True):
			self.stats.ship_health -= 50
	
			if self.stats.ship_health <= 0:
				self._ship_hit()
		# LOOKS FOR HEART AND SHIP COLLISIONS.
		if pygame.sprite.spritecollide(self.ship, self.hearts, True):
			if self.stats.ship_health < 100:
				self.stats.ship_health += 25
		# LOOKS FOR EXTRA LIFE AND SHIP COLLISIONS.
		if pygame.sprite.spritecollide(self.ship, self.extralife, True):
			if self.stats.ships_left < 3:
				self.stats.ships_left += 1
				self.sb.prep_ships()
				self.sb.prep_level()
			else:
				self.stats.score += 1000
				self.sb.prep_score()
				self.sb.check_high_score()

	# THIS SECTION ELIMINATES THE SHIP AFTER BEING KILLED DUE TO COLLISIONS.
	def _ship_hit(self):
		"""RESPONDS TO THE SHIP BEING KILLED BY AN ENEMY"""
		if self.stats.ships_left > 0:
			# DECREASES SHIPS AND PREPS NEW SHIP
			self.stats.ships_left -= 1
			self.sb.prep_ships()
			# CLEARS REMAINING ALIENS, PROJECTILES, AND BONUSES
			self.aliens.empty()
			self.superaliens.empty()
			self.alienmissiles.empty()
			self.lasers.empty()
			self.bullets.empty()
			self.hearts.empty()
			self.extralife.empty()
			# CENTERS THE SHIP
			self.ship.center_ship()
			# RETURNS SHIP HEALTH TO 100
			self.stats.ship_health = 100
			# PAUSE GAME
			sleep(0.5)
		# ENDS GAME
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	# CHECKS FOR COLLISIONS BETWEEN SHIP BULLETS AND ENEMIES.        
	def _check_bullet_alien_collisions(self):
		"""RESPONDS TO BULLET AND ALIEN COLLISIONS"""
		# BULLETS ARE REMOVED AND POINTS ARE CALCULATED.
		# ALSO CALCULATES HEALTH REDUCTIONS ON SUPER ALIEN CLASS.
		alien_collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)
		super_alien_collisions = pygame.sprite.groupcollide(
			self.bullets, self.superaliens, True, False)
		alien_missile_collisions = pygame.sprite.groupcollide(
			self.bullets, self.alienmissiles, True, True)    
		if alien_collisions:
			for alien in alien_collisions.values():
				self.stats.score += self.settings.normal_alien_points
				self.sb.prep_score()
				self.sb.check_high_score()
		for alien in super_alien_collisions.values():
			self.superalien.super_alien_health -=25
			if self.superalien.super_alien_health <= 0:
				self.superaliens.remove(alien)
				self.stats.score += self.settings.super_alien_points
				self.sb.prep_score()
				self.sb.check_high_score()
				self.superalien.super_alien_health = 75
		if alien_missile_collisions:        
			for alien in alien_missile_collisions.values():
				self.stats.score += self.settings.alien_missile_points
				self.sb.prep_score()
				self.sb.check_high_score()

# THIS SECTION CHECKS FOR SPRITES EXITING THE SCREEN.
	# THIS SECTION CHECKS FOR SPRITES EXITING THE LEFT.
	def _check_sprites_left(self):
		"""CHECKS FOR ANY SPRITES EXITING THE SCREEN LEFT."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.right <= screen_rect.left:
				self.aliens.remove(alien)
		for alien in self.superaliens.sprites():
			if alien.rect.right <= screen_rect.left:
				self.superaliens.remove(alien)
		for bonus in self.hearts.sprites():
			if bonus.rect.right <= screen_rect.left:
				self.hearts.remove(bonus)
		for life in self.extralife.sprites():
			if life.rect.right <= screen_rect.left:
				self.extralife.remove(life)

	# THIS SECTION CHECKS FOR SPRITES EXITING THE TOP.
	def _check_sprites_top(self):
		"""CHECKS FOR ALIENS EXITING THE TOP OF THE SCREEN"""
		screen_rect = self.screen.get_rect()
		for alien in self.alienmissiles.sprites():
			if alien.rect.bottom <= screen_rect.top:
				self.alienmissiles.remove(alien)
			   
if __name__ == '__main__':
	# Make a game instance, and run the game.
	ed = EarthDefense()
	ed.run_game()
