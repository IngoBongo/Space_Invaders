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

def update_screen(settings, screen, player, player_shots, ground_blocks,
		remaining_lives):
	"""Update every image on the screen then draw the screen."""
	# Set the background color.
	screen.fill(settings.black)
	
	# Draw player shots.
	player_shots.draw(screen)
	
	# Draw the player ship.
	player.blitme()
	ground_blocks.draw(screen)
	show_score(settings, screen)
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
		if shot.rect.bottom < 140:
			color_surface(shot.image, settings.red)
		if shot.rect.bottom < 80:
			shot.shot_explode()
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
	for column in range(int(settings.screen_width / settings.block_size)):
		block = Block(settings, screen)
		block.rect.x = column * settings.block_size
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
		new_life.rect.x = 80 + (12 + new_life.rect.w) * number
		new_life.rect.y = settings.life_height
		remaining_lives.add(new_life)
	
	return remaining_lives
	
def show_lives(settings, screen, player, remaining_lives):
	remaining_lives.draw(screen)
	lives_text = Text(settings, screen, 32, str(player.remaining_lives),
		settings.white, 32, settings.life_height)
	lives_text.blitme()
	
def show_score(settings, screen):
	player1_score_text = Text(settings, screen, 22, "SCORE <1>",
		settings.white, 32, 32)
	hi_score_text = Text(settings, screen, 22, "HI-SCORE",
		settings.white, player1_score_text.rect.right + 90, 32)
	player2_score_text = Text(settings, screen, 22, "SCORE <2>",
		settings.white, hi_score_text.rect.right + 90, 32)
	
	player1_score_text.blitme()
	hi_score_text.blitme()
	player2_score_text.blitme()
	
"""
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
		aliens, bullets):
	Respond to bullet-alien collisions.
	# Remove any bullets and aliens that have collided.
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	
	if len(aliens) == 0:
		# If the entire fleet is destroyed, start a new level.
		bullets.empty()
		ai_settings.increase_speed()
		
		# Increase level.
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings, screen, ship, aliens)
"""
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


