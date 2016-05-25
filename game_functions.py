import sys
import pygame
import numpy
import pygame.surfarray as surfarray
from pygame.sprite import Group
from player_shot import PlayerShot
from block import Block

def check_events(settings, screen, player, player_shots):
	"""Check for events and respond to them."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, settings, screen, player, player_shots)
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

def update_screen(settings, screen, player, player_shots, ground_blocks):
	"""Update every image on the screen then draw the screen."""
	# Set the background color.
	screen.fill(settings.black)
	
	# Draw player shots.
	for shot in player_shots:
		shot.blitme()
	
	# Draw the player ship.
	player.blitme()
	
	ground_blocks.draw(screen)
	
	# Make the most recently drawn screen visible.
	pygame.display.update()

def player_shoot(settings, screen, player, player_shots):
	"""Shoot from player if shot limit has not been reached."""
	if len(player_shots) < settings.playershot_limit:
		player_shot = PlayerShot(settings, screen, player)
		player_shots.add(player_shot)
		settings.player_shoot.play()

def update_player_shots(settings, player_shots):
	"""Update position of player shots and remove old shots."""
	player_shots.update()
	
	for shot in player_shots:
		if shot.rect.bottom < 140:
			color_surface(shot.image, settings.red)
		if shot.rect.bottom < 80:
			shot.shot_explode()
		currentTime = pygame.time.get_ticks()
		if shot.exploded and currentTime - shot.timer > 300:
				player_shots.remove(shot)

def color_surface(surface, rgb_color):
	"""Change color of surface to the value of rgb_color tuple."""
	arr = pygame.surfarray.pixels3d(surface)
	arr[:,:,0:] = rgb_color[0]
	arr[:,:,1:] = rgb_color[1]
	arr[:,:,2:] = rgb_color[2]

def create_ground(settings, screen):
	ground_blocks = Group()
	
	for column in range(int(settings.screen_width / settings.block_size)):
		block = Block(settings, screen)
		block.rect.x = column * settings.block_size
		block.rect.y = settings.ground_height
		ground_blocks.add(block)
		print(column * 4)
	
	return ground_blocks
	
"""
def makeBlockers(self, number=1):
	blockerGroup = pygame.sprite.Group()
	
	for row in range(5):
		for column in range(7):
			blocker = Blocker(10, GREEN, row, column)
			blocker.rect.x = 50 + (150 * number) + (column * blocker.width)
			blocker.rect.y = 375 + (row * blocker.height)
			blockerGroup.add(blocker)

	for blocker in blockerGroup:
		if (blocker.column == 0 and blocker.row == 0
			or blocker.column == 6 and blocker.row == 0):
			blocker.kill()

	return blockerGroup
"""


