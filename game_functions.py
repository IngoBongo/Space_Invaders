import sys

import pygame
from pygame.sprite import Group

from block import Block
from invader import Invader
from life import Life
from player_shot import PlayerShot
from invader_shot import InvaderShot
from text import Text
from random import randint


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


def update_screen(settings, screen, scoreboard, player, player_shots, ground_blocks, shields,
                  invaders, invader_shots, stats):
	"""Update every image on the screen then draw the screen."""
	# Set the background color.
	screen.fill(settings.black)

	# Draw player shots behind ship.
	player_shots.draw(screen)

	# Draw invader shots behind invaders.
	invader_shots.draw(screen)

	# Draw the player ship.
	if player.image_change_counter < 11:
		player.blitme()
	elif player.image_change_counter == 11:
		stats.ships_left -= 1
		player.reset_ship()
		stats.game_active = True
		
	# Draw the fleet.
	invaders.draw(screen)

	# Draw ground, scoreboard and lives.
	ground_blocks.draw(screen)
	scoreboard.show_score()
	show_lives(settings, screen, player, stats)

	# Draw shields.
	for shield in shields:
		shield.draw(screen)

	# Draw shot explosions.
	for shot in player_shots:
		if shot.exploded:
			shot.explosion.image.draw(screen)
	for shot in invader_shots:
		if shot.exploded:
			shot.explosion.image.draw(screen)

	# Make the most recently drawn screen visible.
	pygame.display.update()


def player_shoot(settings, screen, player, player_shots):
	"""Shoot from player if shot limit has not been reached."""
	if len(player_shots) < settings.playershot_limit and player.allowed_to_shoot:
		# Create shot and add to player_shots group.
		player_shot = PlayerShot(settings, screen, player)
		player_shots.add(player_shot)

		# Play shooting sound effect.
		settings.player_shoot.play()
		player.has_active_shot = True


def update_player_shots(settings, game_stats, player, player_shots, shields, invaders, invader_shots):
	"""Update position of player shots, explode shots that reach a certain height and then remove them."""
	# Update shot position.
	player_shots.update()

	for shot in player_shots:
		# Color shots above certain position and only color them once.
		if not shot.is_red and shot.rect.bottom < 150:
			color_surface(shot.image, settings.red)
			shot.is_red = True

		# Set shot to exploded if position is at top of screen.
		if not shot.exploded and shot.rect.top < 97:
			shot.explode(shot.rect.x - (settings.block_size * 3), shot.rect.y - (settings.block_size * 6))
			for block in shot.explosion.image:
				color_surface(block.image, settings.red)
		current_time = pygame.time.get_ticks()

		# Show explosion for a little bit and then remove it.
		if shot.exploded and current_time - shot.explosion.timer > 300:
			player_shots.remove(shot)
			player.has_active_shot = False

	check_shot_shield_collisions(settings, player_shots, shields)
	check_shot_shot_collision(settings, player_shots, invader_shots)
	check_shot_invader_collisions(settings, game_stats, player_shots, invaders, player)


def update_invader_shots(settings, invader_shots, ground_blocks, shields, frame_count, player, stats):
	"""Update position of invader shots."""
	frame_count += 1
	if frame_count == 3:

		# Update shot position.
		invader_shots.update()
		for shot in invader_shots:

			current_time = pygame.time.get_ticks()

			# Show explosion for a little bit and then remove it.
			if shot.exploded and current_time - shot.explosion.timer > 300:
				invader_shots.remove(shot)

		frame_count = 0
	check_shot_ground_collisions(settings, invader_shots, ground_blocks)
	check_invader_shot_shield_collisions(settings, invader_shots, shields)

	collisions = pygame.sprite.spritecollideany(player, invader_shots)
	if collisions and stats.game_active:
		collisions.explode(collisions.rect.x, collisions.rect.y)
		for block in collisions.explosion.image:
			color_surface(block.image, settings.green)
		player_killed(settings, stats, player)

	return frame_count


def player_killed(settings, stats, player):
	"""Respond to player being killed."""
	player.explode()

	if stats.ships_left > 0:
		stats.game_active = False


def color_surface(surface, rgb_color):
	"""Change color of surface to the value of rgb_color tuple."""
	arr = pygame.surfarray.pixels3d(surface)
	arr[:, :, 0:] = rgb_color[0]
	arr[:, :, 1:] = rgb_color[1]
	arr[:, :, 2:] = rgb_color[2]


def create_ground(settings, screen):
	"""Create a ground line under player."""
	ground_blocks = Group()

	# Calculate how many blocks fit on the screen and create them.
	for column in range(int((settings.screen_width / settings.block_size) -
									int((settings.ground_offsetx * 2) / settings.block_size))):
		block = Block(settings, screen, settings.green, settings.ground_offsetx + settings.block_size * column,
					  settings.ground_y)
		ground_blocks.add(block)

	return ground_blocks


def check_invader_shield_collisions(invaders, shields):
	"""Respond to invader-shield collisions."""
	for shield in shields:
		pygame.sprite.groupcollide(invaders, shield, False, True)


def check_shot_invader_collisions(settings, game_stats, player_shots, invaders, player):
	"""Respond to shot-invader collisions."""
	# Remove player_shot when colliding.
	collisions = pygame.sprite.groupcollide(player_shots, invaders, True, False)

	# Create explosion for killed invader.
	if collisions:
		# Player isn't allowed to shoot while invader explosion is displayed.
		player.allowed_to_shoot = False
		for shot, invaders in collisions.items():
			for invader in invaders:
				invader.explode(invader.rect.x - 3, invader.rect.y)
				settings.invader_killed.play()
				update_score(settings, game_stats, invader.row, player)


def update_score(settings, game_stats, row, player):
	"""Update player/hi score depending on invader row."""
	if row == 0:
		player.score = (player.score + settings.invader_1_score) % 10000
	elif row == 1 or row == 2:
		player.score = (player.score + settings.invader_2_score) % 10000
	else:
		player.score = (player.score + settings.invader_3_score) % 10000
	if player.score > game_stats.hi_score:
		game_stats.hi_score = player.score


def check_shot_ground_collisions(settings, invader_shots, ground_blocks):
	"""Respond to shot-ground collisions."""

	collisions = pygame.sprite.groupcollide(invader_shots, ground_blocks, False, False)
	if collisions:
		for shot, block_list in collisions.items():
			if not shot.exploded:
				shot.explode(shot.rect.x - 9, shot.rect.y - 3)
				pygame.sprite.groupcollide(shot.explosion.image, ground_blocks, False, True)
				for block in shot.explosion.image:
					color_surface(block.image, settings.green)


def check_invader_shot_shield_collisions(settings, invader_shots, shields):
	"""Respond to invader_shot-shield collisions."""

	for shield in shields:
		collisions = pygame.sprite.groupcollide(invader_shots, shield, False, False)

		if collisions:
			for shot, block_list in collisions.items():
				if not shot.exploded:
					shot.explode(shot.rect.x - 6, shot.rect.y)
					pygame.sprite.groupcollide(shot.explosion.image, shield, False, True)
					for block in shot.explosion.image:
						color_surface(block.image, settings.green)


def check_shot_shield_collisions(settings, player_shots, shields):
	"""Respond to shot-shield collisions."""

	for shield in shields:
		collisions = pygame.sprite.groupcollide(player_shots, shield, False, False)

		# If there were collisions find lowest block
		# that collided with shot.
		if collisions:

			# Set all blocks from the dictionary into a list.
			collision_blocks = []
			for shot, block_list in collisions.items():
				for block in block_list:
					collision_blocks.append(block)

			# Sort collided blocks ascending by rect.y value and then
			# get the block with the highest y value.
			collision_blocks.sort(key=lambda x: x.rect.y)
			first_block = collision_blocks[-1]

			# Set shot to exploded, color it and remove collided blocks.
			for shot in player_shots:
				shot.explode(first_block.rect.x - (settings.block_size * 3),
							 first_block.rect.y - (settings.block_size * 5))
				for block in shot.explosion.image:
					color_surface(block.image, settings.green)
				pygame.sprite.groupcollide(shot.explosion.image, shield, False, True)


def check_shot_shot_collision(settings, player_shots, invader_shots):
	"""Respond to player_shot/invader_shot collisions."""
	collisions = pygame.sprite.groupcollide(player_shots, invader_shots, False, False)

	if collisions:
		for shot in player_shots:
			# if shot hasn't collided with invader_shot then do collision
			if not shot.collided_with_invader_shot:
				shot.collided_with_invader_shot = True
				choice = randint(0, 3)
				# 0 = player_shot explodes
				# 1 = invader_shot explodes
				# 2 = both explode
				# 3 = neither explode
				if choice == 0:
					if not shot.exploded:
						for p_shot, i_shot_list in collisions.items():
							p_shot.explode(p_shot.rect.x - 9, p_shot.rect.y - 18)
				elif choice == 1:
					for p_shot, i_shot_list in collisions.items():
						for i_shot in i_shot_list:
							i_shot.explode(i_shot.rect.x, i_shot.rect.y)
				elif choice == 2:
					for p_shot, i_shot_list in collisions.items():
						p_shot.explode(p_shot.rect.x - 9, p_shot.rect.y - 18)
						for i_shot in i_shot_list:
							i_shot.explode(i_shot.rect.x, i_shot.rect.y)

"""
def create_lives(settings, screen, player):
	Create and return group of sprites for remaining lives.
	remaining_lives = Group()

	for number in range(player.remaining_lives - 1):
		# Create life and add it to remaining_lives.
		new_life = Life(settings, screen, (settings.life_ship_offsetx + (settings.life_ship_spacing + 39) * number),
		                settings.life_y)
		remaining_lives.add(new_life)

	return remaining_lives
"""

def show_lives(settings, screen, player, stats):
	"""Draw text and ship images for lives."""
	# Draw ship images.
	#remaining_lives.draw(screen)

	for number in range(stats.ships_left - 1):
		# Create life and add it to remaining_lives.
		new_life = Life(settings, screen, (settings.life_ship_offsetx + (settings.life_ship_spacing + 39) * number),
		                settings.life_y)
		new_life.blitme()

	# Render number of lives into image and draw it.
	lives_text = Text(settings, screen, settings.font_size, str(stats.ships_left), settings.white,
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


def create_fleet(settings, screen, invaders):
	"""Create a full fleet of invaders."""
	# Create the fleet of aliens.

	for row in range(settings.fleet_rows):
		for column in range(settings.fleet_columns):
			# Create an alien and place it in the fleet.
			if row == 0:
				offset, gap, length = 6, 24, 24
			elif row == 1 or row == 2:
				offset, gap, length = 0, 15, 33
			else:
				offset, gap, length = 0, 12, 36

			new_invader = Invader(settings, screen, row, column)
			new_invader.rect.x = settings.invader_start_x + offset + (column * (gap + length))
			new_invader.rect.y = settings.invader_start_y + (row * (settings.invader_height * 2))
			invaders.add(new_invader)


def update_invaders(settings, screen, invaders, shields, invader_shots, player, stats):
	check_fleet_boundary(settings, invaders)
	current_time = pygame.time.get_ticks()
	for invader in invaders.sprites():
		invader.update(current_time, stats)

		# Show explosion for a little bit and then remove it.
		if invader.exploded and current_time - invader.time_of_last_move > 300:
			invaders.remove(invader)
			player.allowed_to_shoot = True

	# 1.5% chance for invader to try shooting
	if randint(0, 199) < 3 and stats.game_active:
		invader_shoot(settings, screen, find_invader_shooter(invaders), invader_shots)

	# TODO: Causing lag, need to only check invader_shield_collision if lowest invader is at shield level?
	# check_invader_shield_collisions(invaders, shields)


def entire_fleet_has_moved(invaders):
	"""Return True if entire fleet has moved."""

	# Count how many invaders have moved.
	count = 0
	for invader in invaders.sprites():
		if invader.has_moved is True:
			count += 1

	# Check if every invader has moved.
	if count == len(invaders.sprites()):
		for invader in invaders.sprites():
			# Set every invader back to not moved.
			invader.has_moved = False
		return True


def check_fleet_boundary(settings, invaders):
	"""Check if any invader is at edge of boundary, change direction if so."""
	boundary_reached = False
	for invader in invaders.sprites():
		if invader.is_at_boundary():
			boundary_reached = True
			break

	if entire_fleet_has_moved(invaders) and boundary_reached:
		change_fleet_direction(settings, invaders)


def change_fleet_direction(settings, invaders):
	"""Moves invaders down and changes fleet direction."""
	settings.fleet_direction *= -1

	for invader in invaders.sprites():
		invader.rect.y += settings.invader_height
		invader.rect.x += settings.invader_move_x * settings.fleet_direction


def find_invader_shooter(invaders):
	column_set = set()

	# Create set of columns available
	for invader in invaders:
		column_set.add(invader.column)

	# Select one column at random
	column_list = list(column_set)
	col = column_list[randint(0, len(column_list) - 1)]

	# Select lowest invader in column as shooter
	row_invaders = []
	for invader in invaders:
		if invader.column == col:
			row_invaders.append(invader.row)

	row = max(row_invaders)

	for invader in invaders:
		if invader.column == col and invader.row == row:
			return invader


def invader_shoot(settings, screen, shooter, invader_shots):
	if len(invader_shots) < settings.invadershot_limit:
		invader_shot = InvaderShot(settings, screen, shooter)
		invader_shots.add(invader_shot)
