import pygame
import math
import random
import sys

# Init pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Create screen resolution
WIDTH = 400
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set title and icon 
pygame.display.set_caption('Journey of the Prairie King')
icon = pygame.transform.scale(pygame.image.load('assets/icon.png'), (32, 32))
pygame.display.set_icon(icon)

# Music
pygame.mixer.music.load('sounds/ambient.mp3')

# Sound effects
cowboy_dead = pygame.mixer.Sound('sounds/cowboy_dead.wav')
enemy_dead1 = pygame.mixer.Sound('sounds/enemy_dead1.wav')
enemy_dead2 = pygame.mixer.Sound('sounds/enemy_dead2.wav')
#shoot_sound = pygame.mixer.Sound('sounds/test.wav')
#steps_sound = pygame.mixer.Sound('sounds/steps.wav')

# Set background image
background = pygame.transform.scale(pygame.image.load('assets/background.png'), (WIDTH, HEIGHT)).convert()
cactus_1 = pygame.transform.scale(pygame.image.load('assets/background1.png'), (WIDTH, HEIGHT)).convert()
cactus_2 = pygame.transform.scale(pygame.image.load('assets/background2.png'), (WIDTH, HEIGHT)).convert()
background_sprites = [cactus_1, cactus_1, cactus_2, cactus_2]

# Player sprites
idle_img = pygame.transform.scale(pygame.image.load('assets/idle.png'), (25, 25))
l1 = pygame.transform.scale(pygame.image.load('assets/l1.png'), (25, 25))
l2 = pygame.transform.scale(pygame.image.load('assets/l2.png'), (25, 25))
l3 = pygame.transform.scale(pygame.image.load('assets/l3.png'), (25, 25))
l4 = pygame.transform.scale(pygame.image.load('assets/l4.png'), (25, 25))
r1 = pygame.transform.scale(pygame.image.load('assets/r1.png'), (25, 25))
r2 = pygame.transform.scale(pygame.image.load('assets/r2.png'), (25, 25))
r3 = pygame.transform.scale(pygame.image.load('assets/r3.png'), (25, 25))
r4 = pygame.transform.scale(pygame.image.load('assets/r4.png'), (25, 25))
u1 = pygame.transform.scale(pygame.image.load('assets/u1.png'), (25, 25))
u2 = pygame.transform.scale(pygame.image.load('assets/u2.png'), (25, 25))
u3 = pygame.transform.scale(pygame.image.load('assets/u3.png'), (25, 25))
u4 = pygame.transform.scale(pygame.image.load('assets/u4.png'), (25, 25))
d1 = pygame.transform.scale(pygame.image.load('assets/d1.png'), (25, 25))
d2 = pygame.transform.scale(pygame.image.load('assets/d2.png'), (25, 25))
d3 = pygame.transform.scale(pygame.image.load('assets/d3.png'), (25, 25))
d4 = pygame.transform.scale(pygame.image.load('assets/d4.png'), (25, 25))
sprites_l, sprites_r, sprites_u, sprites_d = [l1, l2, l3, l4], [r1, r2, r3, r4], [u1, u2, u3, u4], [d1, d2, d3, d4]

# Enemy image
enemy_l = pygame.transform.scale(pygame.image.load('assets/enemy_left_foot.png'), (25, 25))
enemy_r = pygame.transform.scale(pygame.image.load('assets/enemy_right_foot.png'), (25, 25))
enemy_sprites = [enemy_l, enemy_l, enemy_r, enemy_r]

# Set bullet image
bullet_img = pygame.transform.scale(pygame.image.load('assets/bullet.png'), (8, 8))


class Enemy:
	def __init__(self, x, y, enemy_sprite_num):
			self.x = x
			self.y = y 
			self.enemy_speed = random.uniform(0.2, 0.5) # Default 0.2
			self.enemy_img = enemy_sprites[0]
			self.enemy_sprite_num = enemy_sprite_num
			self.moving = True
			
	def draw(self, screen):
		# I couldnt make an enemy_animation() function like player, TODO.
		animation_speed = 0.05

		if self.enemy_sprite_num >= 4:
			self.enemy_sprite_num = 0

		if self.moving:
			#Create rect for each enemy, for collisions.
			screen.blit(enemy_sprites[int(self.enemy_sprite_num)], self.get_rect())

			# Animate enemy sprites.
			self.enemy_sprite_num += animation_speed

			# Debugging HITBOX
			#pygame.draw.rect(screen, (0,255,255), self.get_rect(), 1)

	def move(self, x, y):
		# Find direc vector between enemy and player, and hyp(dx, dy)
		dx, dy = x - self.x, y - self.y 
		dist = math.hypot(dx, dy)
		# Normalize vectors
		dx, dy = dx/dist, dy/dist
		# Move along X or Y axis depending on distance
		if abs(dx) >= abs(dy):
			self.x += dx * self.enemy_speed
		elif abs(dy) > abs(dx):
			self.y += dy * self.enemy_speed

	def get_rect(self):
		return self.enemy_img.get_rect(topleft = (int(self.x), int(self.y)))

	def get_width(self):
		return self.enemy_img.get_width()

	def get_height(self):
		return self.enemy_img.get_height()

class Player:
	COOLDOWN_TIME = 45

	def __init__(self, x, y):
		self.x = x 
		self.y = y 
		self.player_img = idle_img
		self.bullet_img = bullet_img
		self.bullets = []
		self.cooldown_count = 0

	def draw(self, left, right, up, down, screen):
		# Draw sprites for given direction
		if left:
			player_animation(self.x, self.y, 1)
		elif right:
			player_animation(self.x, self.y, 2)
		elif up:
			player_animation(self.x, self.y, 3)
		elif down:
			player_animation(self.x, self.y, 4)
		else:
			player_animation(self.x, self.y)

		# Draw bullet sprite on screen
		for bullet in self.bullets:
			bullet.draw(screen)

		# Debugging HITBOX
		#pygame.draw.rect(screen, (255,0,255), self.get_rect(), 1)

	def move_bullet(self, speed, enemies):
		self.cooldown()
		# Loops through all bullets in bullets[] 
		for bullet in self.bullets:
			# Move bullet with hor and vert direction
			bullet.move(speed, bullet.hor, bullet.vert)
			if bullet.off_screen(HEIGHT, WIDTH):
				self.bullets.remove(bullet)
			else: # Checks collision bullet-enemy
				for enemy in enemies:
					if bullet.collision(enemy.get_rect()): # Checks bullet - enemy collision
						pygame.mixer.Sound.play(random.choice([enemy_dead1, enemy_dead2]))
						enemies.remove(enemy)
						if bullet in self.bullets:
							self.bullets.remove(bullet)

	def cooldown(self):
		# COOLDOWN_TIME at top of Player class
		if self.cooldown_count >= self.COOLDOWN_TIME:
			self.cooldown_count = 0
		elif self.cooldown_count > 0:
			self.cooldown_count += 1

	def shoot(self, hor, vert):
		# Create new Bullet (using Bullet class) if cooldown equals 0
		if self.cooldown_count == 0:
			# Creates a bullet facing given direction
			bullet = Bullet(self.x, self.y, hor, vert)
			self.bullets.append(bullet)
			self.cooldown_count = 1
	
	def get_rect(self):
		return self.player_img.get_rect(topleft = (int(self.x), int(self.y)))
		
	def get_width(self):
		return self.player_img.get_width()
	
	def get_height(self):
		return self.player_img.get_height()


class Bullet:
	def __init__(self, x, y, hor, vert):
		self.x = x + 10 # + 10 so the bullet shoots from the middle of the player
		self.y = y + 10 # + 10 so the bullet shoots from the middle of the player
		self.hor = hor
		self.vert = vert
		self.bullet_img = bullet_img

	def draw(self, screen):
		# Draw bullet on player
		screen.blit(self.bullet_img, (self.x, self.y))

		# Debugging HITBOX
		#pygame.draw.rect(screen, (255,0,255), self.get_rect(), 1)

	def off_screen(self, height, width):
		# Delete bullet if outside bounds
		if self.x >= width or self.x <= 0:
			return True
		if self.y >= height or self.y <= 0:
			return True

	def move(self, speed, hor, vert):
		# Move bullet depending on player direction, 1 equals positive movement, -1 negative movement
		if hor == 1:
			self.x += speed
		elif hor == -1:
			self.x -= speed
		if vert == 1:
			self.y += speed
		elif vert == -1:
			self.y -= speed

	def collision(self, obj):
		return check_collision(self.get_rect(), obj)

	def get_rect(self):
		return self.bullet_img.get_rect(topleft = (int(self.x), int(self.y)))
	

def check_collision(obj1, obj2):
	# Checks collisions ONLY between rects. Returns True or False.
	return obj1.colliderect(obj2)

def player_animation(x, y, direction = None):
	global player_sprite_num
	animation_speed = 0.05

	# >= 4 because there are only 4 player sprites per direction
	if player_sprite_num >= 4:
		player_sprite_num = 0

	# 1 = left, 2 = right, 3 = up, 4 = down, None = idle
	if direction == 1:
		screen.blit(sprites_l[int(player_sprite_num)], (x, y))
		player_sprite_num += animation_speed
	elif direction == 2:
		screen.blit(sprites_r[int(player_sprite_num)], (x, y))
		player_sprite_num += animation_speed
	elif direction == 3:
		screen.blit(sprites_u[int(player_sprite_num)], (x, y))
		player_sprite_num += animation_speed
	elif direction == 4:
		screen.blit(sprites_d[int(player_sprite_num)], (x, y))
		player_sprite_num += animation_speed
	elif direction == None:
		screen.blit(idle_img, (x, y))

def background_animation():
	global background_sprite_num
	animation_speed = 0.01

	# >= 2 because there are only 2 background sprites
	if background_sprite_num >= 2:
		background_sprite_num = 0

	if background_sprite_num < 1:
		screen.blit(cactus_1, (0, 0))
		background_sprite_num += animation_speed
	elif  background_sprite_num >= 1:
		screen.blit(cactus_2, (0,0))
		background_sprite_num += animation_speed

def main():
	# Clock Setup
	FPS = 120
	clock = pygame.time.Clock()
	
	# Font Setup, arial, comicsans, helvetica, verdana etc
	font = pygame.font.SysFont('freesansbold', 32)

	# Music
	pygame.mixer.music.play(-1)

	# Background animation setup
	global background_sprite_num
	background_sprite_num = 0

	# Initialize Player class, Player facing direction
	player = Player(200, 200)
	player_speed = 1
	left = False
	right = False
	up = False
	down = False
	# Number to change between items in player sprite list
	global player_sprite_num
	player_sprite_num = 0

	# Enemy setup
	enemies = []
	enemy_sprite_num = 0

	# Bullet setup
	bullets = []
	bullet_speed = 2

	# Level setup
	level = 0
	wave_lenght = 10
	lives = 3
	lost = False

	# Refresh screen function
	def redraw_window():
		# Update Background 
		screen.blit(background, (0, 0))
		background_animation()
		
		# Text
		lives_text = font.render(f'Lives: {lives}', 1, (255, 255, 255))
		level_text = font.render(f'Level: {level}', 1, (255, 255, 255))
		screen.blit(lives_text, (5, 2))
		screen.blit(level_text, (WIDTH - level_text.get_width() - 5, 2))

		# Update Enemies
		for enemy in enemies:
			enemy.draw(screen)

		# Update Player
		player.draw(left, right, up, down, screen)

		# Update screen
		pygame.display.update()


	# GAME LOOP
	run = True
	while run:
		# Set clock FPS
		clock.tick(FPS)

		# QUIT GAME LOOP, DONT DELETE
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				sys.exit()


		# Player movement keymap
		# Map boundaries added in conditionals
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] and player.x > 25:
			player.x -= player_speed
			left, right, up, down = True, False, False, False
		if keys[pygame.K_d] and player.x + player.get_width() < WIDTH - 25:
			player.x += player_speed
			left, right, up, down = False, True, False, False
		if keys[pygame.K_w] and player.y > 25:
			player.y -= player_speed
			left, right, up, down = False, False, True, False
		if keys[pygame.K_s] and player.y + player.get_height() < HEIGHT - 25:
			player.y += player_speed
			left, right, up, down = False, False, False, True
		if not keys[pygame.K_s] and not keys[pygame.K_w] and not keys[pygame.K_d] and not keys[pygame.K_a]:
			left, right, up, down = False, False, False, False

		# Diagonal shooting
		if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
			player.shoot(-1, -1)
		if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
			player.shoot(-1, 1)
		if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
			player.shoot(1, -1)
		if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
			player.shoot(1, 1)

		# Shooting keys
		if keys[pygame.K_LEFT]:
			player.shoot(-1, 0)
			left, right, up, down = True, False, False, False
		if keys[pygame.K_RIGHT]:
			player.shoot(1, 0)
			left, right, up, down = False, True, False, False
		if keys[pygame.K_UP]:
			player.shoot(0, -1)
			left, right, up, down = False, False, True, False
		if keys[pygame.K_DOWN]:
			player.shoot(0, 1)
			left, right, up, down = False, False, False, True


		# ENEMIES
		if len(enemies) == 0:
			level += 1
			wave_lenght += 5

			# Initialize enemies in loop
			for i in range(wave_lenght):
				# Choose door to spawn enemy
				door = random.choice(['left_door', 'right_door', 'top_door', 'down_door'])
				if door == 'left_door':
					enemy = Enemy(random.randrange(-200, -20), random.randrange(180, 220), enemy_sprite_num)
					enemies.append(enemy)
				if door == 'right_door':
					enemy = Enemy(random.randrange(420, 500), random.randrange(180, 220), enemy_sprite_num)
					enemies.append(enemy)
				if door == 'top_door':
					enemy = Enemy(random.randrange(180, 220), random.randrange(-100, -20), enemy_sprite_num)
					enemies.append(enemy)
				if door == 'down_door':
					enemy = Enemy(random.randrange(180, 220), random.randrange(420, 500), enemy_sprite_num)
					enemies.append(enemy)

		# Enemy movement
		for enemy in enemies:
			enemy.move(player.x, player.y)

			if check_collision(enemy.get_rect(), player.get_rect()):
				pygame.mixer.Sound.play(cowboy_dead)
				pygame.mixer.music.stop()
				lives -= 1
				level = 0
				wave_lenght = 5
				enemies.clear()
				bullets.clear()
				pygame.time.delay(3000)
				pygame.mixer.music.play(-1)
				redraw_window()
				if lives < 0:
					pygame.mixer.music.stop()
					run = False

		# REFRESH WINDOW USING FUNCTION
		player.move_bullet(bullet_speed, enemies)
		redraw_window()
		pygame.display.update()

def main_menu():
	font = pygame.font.SysFont("freesansbold", 32)
	run = True
	while run:
		screen.blit(background, (0,0))
		title_text = font.render("Press space to begin...", 1, (255,255,255))
		screen.blit(title_text, (int(WIDTH/2 - title_text.get_width()/2), int(HEIGHT/2 - title_text.get_height()/2)))
		
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					main()
	pygame.quit()


# Call main_menu function to start game
main_menu()