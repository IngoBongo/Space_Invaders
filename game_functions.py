import sys
import pygame
import numpy
import pygame.surfarray as surfarray
from pygame.sprite import Group
from player_shot import PlayerShot
from block import Block
from life import Life
from text import Text

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

def update_screen(settings, screen, scoreboard, player, player_shots,
		ground_blocks, remaining_lives):
	"""Update every image on the screen then draw the screen."""
	# Set the background color.
	screen.fill(settings.black)
	
	# Draw player shots.
	player_shots.draw(screen)
	
	# Draw the player ship.
	player.blitme()
	ground_blocks.draw(screen)
	scoreboard.show_score()
	show_lives(settings, screen, player, remaining_lives)
	
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

def update_player_shots(settings, screen, player_shots, ground_blocks):
	"""
	Update position of player shots, explode shots that reach
	a certain height and then remove them.
	"""
	player_shots.update()
	
	for shot in player_shots:
		if not shot.is_red and shot.rect.bottom < 140:
			color_surface(shot.image, settings.red)
			shot.is_red = True
		if not shot.exploded and shot.rect.top < 82:
			shot.shot_explode(82)
		currentTime = pygame.time.get_ticks()
		if shot.exploded and currentTime - shot.timer > 300:
			player_shots.remove(shot)
	
	check_shot_ground_collisions(settings, screen, player_shots, 
		ground_blocks)

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
		block = Block(settings, screen)
		block.rect.x = settings.ground_offsetx + settings.block_size * column
		block.rect.y = settings.ground_height
		ground_blocks.add(block)
	
	return ground_blocks
	
def check_shot_ground_collisions(settings, screen, player_shots, 
		ground_blocks):
	"""Respond to shot-ground collisions."""
	collisions = pygame.sprite.groupcollide(player_shots, ground_blocks, False, True)
	
def create_lives(settings, screen, player):
	remaining_lives = Group()
	
	for number in range(player.remaining_lives - 1):
		new_life = Life(settings, screen)
		new_life.rect.x = (settings.life_ship_offsetx + 
			(settings.life_ship_spacing + new_life.rect.w) * number)
		new_life.rect.y = settings.life_height
		remaining_lives.add(new_life)
	
	return remaining_lives
	
def show_lives(settings, screen, player, remaining_lives):
	remaining_lives.draw(screen)
	lives_text = Text(settings, screen, 25, str(player.remaining_lives),
		settings.white, settings.life_text_offsetx, settings.life_height)
	lives_text.blitme()

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


