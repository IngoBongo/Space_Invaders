import sys
import pygame
import numpy
import pygame.surfarray as surfarray
from pygame.sprite import Group
from player_shot import PlayerShot
from block import Block
from life import Life
from text import Text
from explosion import Explosion

def check_events(settings, screen, player, player_shots):
	"""Check for events and respond to them."""
	for event in pygame.event.get():
		# Check if user presses X to quit.
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		# Check for keypress.
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, settings, screen, player, player_shots)
		# Check for keyrelease.
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, player)

def check_keydown_events(event, settings, screen, player, player_shots):
	"""Check for keypresses and respond to them."""
	# Exit game if player presses ESC key.
	if event.key == pygame.K_ESCAPE:
		pygame.quit()
		sys.exit()
	# Set movement flags, left and right arrow keys move player.
	if event.key == pygame.K_RIGHT:
		player.moving_right = True
	if event.key == pygame.K_LEFT:
		player.moving_left = True
	# Shoot with space key.
	if event.key == pygame.K_SPACE:
		player_shoot(settings, screen, player, player_shots)
	
def check_keyup_events(event, player):
	"""Check for keyreleases and respond to them."""
	# Set movement flags.
	if event.key == pygame.K_RIGHT:
		player.moving_right = False
	if event.key == pygame.K_LEFT:
		player.moving_left = False

def update_screen(settings, screen, scoreboard, player, player_shots,
		ground_blocks, remaining_lives, shields):
	"""Update every image on the screen then draw the screen."""
	# Set the background color.
	screen.fill(settings.black)
	
	# Draw player shots behind ship.
	player_shots.draw(screen)
	
	# Draw the player ship.
	player.blitme()
	
	# Draw ground, scoreboard and lives.
	ground_blocks.draw(screen)
	scoreboard.show_score()
	show_lives(settings, screen, player, remaining_lives)
	
	# Draw shields.
	for shield in shields:
		shield.draw(screen)
		
	# Draw explosions.
	for shot in player_shots:
		if shot.exploded:
			shot.explosion.image.draw(screen)
	
	# Make the most recently drawn screen visible.
	pygame.display.update()

def player_shoot(settings, screen, player, player_shots):
	"""Shoot from player if shot limit has not been reached."""
	if len(player_shots) < settings.playershot_limit:
		# Create shot and add to player_shots group.
		player_shot = PlayerShot(settings, screen, player)
		player_shots.add(player_shot)
		# Play shooting sound effect.
		settings.player_shoot.play()
		player.has_active_shot = True

def update_player_shots(settings, screen, player, player_shots, 
		ground_blocks, shields):
	"""
	Update position of player shots, explode shots that reach
	a certain height and then remove them.
	"""
	# Update shot position.
	player_shots.update()
	
	for shot in player_shots:
		# Color shots above certain position.
		if not shot.is_red and shot.rect.bottom < 150:
			color_surface(shot.image, settings.red)
			shot.is_red = True
		# Change sprite to exploded if position is at top of screen.
		if not shot.exploded and shot.rect.top < 97:
			shot.exploded = True
			# Color shot black to hide it.
			color_surface(shot.image, settings.black)
			# Create explosion "image".
			shot.explosion = Explosion(settings, screen, 
				shot.rect.x - (settings.block_size * 3),
				shot.rect.y - (settings.block_size * 6))
			# Color explosion red
			for block in shot.explosion.image:
				color_surface(block.image, settings.red)
		currentTime = pygame.time.get_ticks()
		# Show explosion for a little bit and then remove it.
		if shot.exploded and currentTime - shot.explosion.timer > 300:
			player_shots.remove(shot)
			player.has_active_shot = False
	
	check_shot_ground_collisions(settings, screen, player_shots, 
		ground_blocks)
	check_shot_shield_collisions(settings, screen, player_shots,
		shields)

def color_surface(surface, rgb_color):
	"""Change color of surface to the value of rgb_color tuple."""
	arr = pygame.surfarray.pixels3d(surface)
	arr[:,:,0:] = rgb_color[0]
	arr[:,:,1:] = rgb_color[1]
	arr[:,:,2:] = rgb_color[2]

def create_ground(settings, screen):
	"""Create a ground line under player."""
	ground_blocks = Group()
	
	# Calculate how many blocks fit on the screen and create them.
	for column in range(int((settings.screen_width / settings.block_size) - 
					    int((settings.ground_offsetx * 2) / settings.block_size))):
		block = Block(settings, screen, settings.green,
			settings.ground_offsetx + settings.block_size * column,
			settings.ground_y)
		ground_blocks.add(block)
	
	return ground_blocks
	
def check_shot_ground_collisions(settings, screen, player_shots, 
		ground_blocks):
	"""Respond to shot-ground collisions."""
	collisions = pygame.sprite.groupcollide(player_shots, ground_blocks, False, True)
	# TODO: should be invader_shots, not player_shots... only put that
	# like that for testing purposes.
	
def check_shot_shield_collisions(settings, screen, player_shots,
		shields):
	"""Respond to shot-shield collisions."""
	# TODO: FIX SHOT_EXPLOSION-SHIELD COLLISION DETECTION
	for shield in shields:
		collisions = pygame.sprite.groupcollide(player_shots, shield, False, False)
		if collisions:
			for shot in player_shots:
				shot.explosion = Explosion(settings, screen, 
					shot.rect.x - (settings.block_size * 3),
					shot.rect.y - (settings.block_size * 6))
				pygame.sprite.groupcollide(shot.explosion.image, shield, True, True)
				shot.exploded = True
				#player_shots.remove(shot)
			#pygame.sprite.groupcollide(player_shots, shield, True, True)
	
def create_lives(settings, screen, player):
	"""Create and return group of sprites for remaining lives."""
	remaining_lives = Group()
	
	for number in range(player.remaining_lives - 1):
		# Create life and add it to remainin_lives.
		new_life = Life(settings, screen, 
			(settings.life_ship_offsetx + (settings.life_ship_spacing + 
			39) * number), settings.life_y)
		remaining_lives.add(new_life)
	
	return remaining_lives
	
def show_lives(settings, screen, player, remaining_lives):
	"""Draw text and ship images for lives."""
	# Draw ship images.
	remaining_lives.draw(screen)
	
	# Render number of lives into image and draw it.
	lives_text = Text(settings, screen, settings.font_size,
		str(player.remaining_lives), settings.white, 
		settings.life_text_offsetx, settings.life_y)
	lives_text.blitme()

def create_shield(settings, screen, number):
	"""Create and return a group of blocks that make up a single shield."""
	shield_blocks = Group()
	
	for row in range(settings.shield_rows):
		for column in range(settings.shield_columns):
			if settings.shield_array[row][column] == 'b':
				new_block = Block(settings, screen, settings.green, 
					settings.shield_x + (132 * number + number * 3) + (column * settings.block_size),
					settings.shield_y + (row * settings.block_size))
				shield_blocks.add(new_block)

	return shield_blocks
