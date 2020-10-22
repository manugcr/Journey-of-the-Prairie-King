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
# background = pygame.transform.scale(pygame.image.load('assets/background.png'), (WIDTH, HEIGHT)).convert()
background_1 = pygame.transform.scale(pygame.image.load('assets/background_1.png'), (WIDTH, HEIGHT)).convert()
background_2 = pygame.transform.scale(pygame.image.load('assets/background_2.png'), (WIDTH, HEIGHT)).convert()

# Player sprites
idle_img = pygame.transform.scale(pygame.image.load('assets/idle.png'), (20, 20))

r1 = pygame.transform.scale(pygame.image.load('assets/r1.png'), (20, 20))
r2 = pygame.transform.scale(pygame.image.load('assets/r2.png'), (20, 20))
r3 = pygame.transform.scale(pygame.image.load('assets/r3.png'), (20, 20))
r4 = pygame.transform.scale(pygame.image.load('assets/r4.png'), (20, 20))
sprites_r = [r1, r2, r3, r4]

d1 = pygame.transform.scale(pygame.image.load('assets/d1.png'), (20, 20))
d2 = pygame.transform.scale(pygame.image.load('assets/d2.png'), (20, 20))
d3 = pygame.transform.scale(pygame.image.load('assets/d3.png'), (20, 20))
d4 = pygame.transform.scale(pygame.image.load('assets/d4.png'), (20, 20))
sprites_d = [d1, d2, d3, d4]

l1 = pygame.transform.scale(pygame.image.load('assets/l1.png'), (20, 20))
l2 = pygame.transform.scale(pygame.image.load('assets/l2.png'), (20, 20))
l3 = pygame.transform.scale(pygame.image.load('assets/l3.png'), (20, 20))
l4 = pygame.transform.scale(pygame.image.load('assets/l4.png'), (20, 20))
sprites_l = [l1, l2, l3, l4]

u1 = pygame.transform.scale(pygame.image.load('assets/u1.png'), (20, 20))
u2 = pygame.transform.scale(pygame.image.load('assets/u2.png'), (20, 20))
u3 = pygame.transform.scale(pygame.image.load('assets/u3.png'), (20, 20))
u4 = pygame.transform.scale(pygame.image.load('assets/u4.png'), (20, 20))
sprites_u = [u1, u2, u3, u4]

# Enemy image
enemy_r = pygame.transform.scale(pygame.image.load('assets/enemy_right_foot.png'), (20, 20))
enemy_l = pygame.transform.scale(pygame.image.load('assets/enemy_left_foot.png'), (20, 20))
enemy_sprites = [enemy_l, enemy_l, enemy_r, enemy_r]

# Set bullet image
bullet_img = pygame.transform.scale(pygame.image.load('assets/bullet.png'), (5, 5))


# Enemy base class, planning to implement more types.
class Hooman:
	def __init__(self, x, y, health = 100, enemy_speed = 0.2):
		self.x = x
		self.y = y
		self.health = health
		self.enemy_speed = enemy_speed
		self.hooman_img = None
		self.bullet_img = None
		self.bullets = []
		self.cooldown_counter = 0

	# def draw(self, window):
	# 	window.blit(self.hooman_img, (int(self.x), int(self.y)))

	def get_width(self):
		return self.hooman_img.get_width()

	def get_height(self):
		return self.hooman_img.get_height()


# Enemy 1 class, inherits from Hooman
class Enemy(Hooman):
	def __init__(self, x, y, walk, health = 100, enemy_speed = 0.2):
		super().__init__(x, y, health, enemy_speed)
		self.enemy_walk_count = walk
		self.enemy_speed = random.uniform(0.2, 0.5)
		self.hooman_img = enemy_sprites[0]
		self.mask = pygame.mask.from_surface(self.hooman_img)

	def move(self,x, y):
		# Find direction vector between enemy and player.
		dx = x - self.x
		dy = y - self.y
		dist = math.hypot(dx, dy)
		# Normalize vector.
		dx = dx/dist
		dy = dy/dist
		# Move along this normalized vector towards the player at current speed.
		self.x += dx * self.enemy_speed 
		self.y += dy * self.enemy_speed 

	def draw(self, window, moving):
		if self.enemy_walk_count + 1 >= 5:
			self.enemy_walk_count = 0

		if moving:
			screen.blit(enemy_sprites[int(self.enemy_walk_count)], (int(self.x), int(self.y)))
			self.enemy_walk_count += 0.1
			

# Main player Class (No multiplayer in this game)
class Player:
	COOLDOWN = 45

	def __init__(self, x, y, health = 100):
		self.x = x
		self.y = y
		self.health = health
		self.idle_img = idle_img
		self.bullet_img = bullet_img
		self.mask = pygame.mask.from_surface(self.idle_img)
		self.bullets = []
		self.cooldown_counter = 0

	def draw(self, window, right, down, left, up):
		global walk_count
		animation_speed = 0.1

		if walk_count + 1 >= 5:
			walk_count = 0
		
		if right:
			screen.blit(sprites_r[int(walk_count)], (self.x,self.y))
			walk_count += animation_speed
		elif down:
			screen.blit(sprites_d[int(walk_count)], (self.x,self.y))
			walk_count += animation_speed
		elif left:
			screen.blit(sprites_l[int(walk_count)], (self.x,self.y))
			walk_count += animation_speed
		elif up:
			screen.blit(sprites_u[int(walk_count)], (self.x,self.y))
			walk_count += animation_speed
		else:
			screen.blit(idle_img, (self.x,self.y))

		for bullet in self.bullets:
			bullet.draw(window)

	def move_bullet(self, vel, objs):
		self.cooldown()
		for bullet in self.bullets:
			bullet.move(vel, bullet.horiz, bullet.vertical)
			if bullet.off_screen(HEIGHT, WIDTH):
				self.bullets.remove(bullet)
			else:
				for obj in objs:
					if bullet.collision(obj):
						pygame.mixer.Sound.play(random.choice([enemy_dead1, enemy_dead2]))
						objs.remove(obj)
						if bullet in self.bullets:
							self.bullets.remove(bullet)

	def cooldown(self):
		if self.cooldown_counter >= self.COOLDOWN:
			self.cooldown_counter = 0
		elif self.cooldown_counter > 0:
			self.cooldown_counter += 1

	def shoot(self, dir1, dir2):
		if self.cooldown_counter == 0:
			bullet = Bullet(self.x, self.y, dir1, dir2)
			self.bullets.append(bullet)
			self.cooldown_counter = 1

	def get_width(self):
		return self.idle_img.get_width()

	def get_height(self):
		return self.idle_img.get_height()


class Bullet:
	def __init__(self, x, y, horiz, vertical):
		self.x = x
		self.y = y
		self.bullet_img = bullet_img
		self.mask = pygame.mask.from_surface(self.bullet_img)
		self.vertical = vertical
		self.horiz = horiz
		
	def draw(self, window):
		window.blit(self.bullet_img, (self.x, self.y))

	def collision(self, obj):
		return collide(self, obj)

	def off_screen(self, height, width):
		if self.y >= height or self.y <= 0:
			return True
		if self.x >= width or self.x <= 0:
			return True

	def move(self, vel, horiz, vertical):
		if horiz == 1:
			self.x += vel
		elif horiz == -1:
			self.x -= vel
		if vertical == 1:
			self.y += vel
		elif vertical == -1:
			self.y -= vel


def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

		
# Main class, set up game and game loop
def main():
	global walk_count
	
	# Set FPS 
	FPS = 120
	clock = pygame.time.Clock()

	# Fonts
	font = pygame.font.SysFont('freesansbold.ttf', 32)

	# Set enemy list, enemy speed and enemy amount
	enemies = []
	# enemy_speed = 0.3
	enemy_walk_count = 0
	wave_length = 0

	# Initialize Player class in (x, y) coords
	player = Player(200, 200)
	pygame.mixer.music.play(-1)
	player_speed = 1
	bullet_speed = 2
	bullets = []
	level = 0
	lives = 3
	lost = False

	# Animation
	right = False
	down = False
	left = False
	up = False
	walk_count = 0

	def redraw_window():
		screen.blit(background_1, (0, 0))

		#lives_text = font.render(f'Lives: {lives}', 1, (255, 255, 255))
		#level_text = font.render(f'Level: {level}', 1, (255, 255, 255))
		#screen.blit(lives_text, (5, 2))
		#screen.blit(level_text, (WIDTH - level_text.get_width() - 5, 2))

		# Draw enemy sprite ingame
		for enemy in enemies:
			moving = True
			enemy.draw(screen, moving)

		# Draw player sprite ingame
		player.draw(screen, right, down, left, up)
		pygame.display.update()

	# Game loop
	run = True
	while run:

		# Set ingame FPS
		clock.tick(FPS)

		if lives <= 0:
			lost = True

		if len(enemies) == 0:
			level += 1
			wave_length += 10
			print(wave_length)

			# Initialize enemies in loop
			for i in range(wave_length):
				door = random.choice(['left_door', 'top_door', 'right_door', 'down_door'])
				
				# If condition
				if door == 'left_door':
					enemy = Enemy(random.randrange(-200, -20), random.randrange(180, 220), enemy_walk_count)
					enemies.append(enemy)
				if door == 'top_door':
					enemy = Enemy(random.randrange(180, 220), random.randrange(-100, -20), enemy_walk_count)
					enemies.append(enemy)
				if door == 'right_door':
					enemy = Enemy(random.randrange(420, 500), random.randrange(180, 220), enemy_walk_count)
					enemies.append(enemy)
				if door == 'down_door':
					enemy = Enemy(random.randrange(180, 220), random.randrange(420, 500), enemy_walk_count)
					enemies.append(enemy)

		# QUIT event, dont delete
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				sys.exit()

		# Player movement key mapping
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] and player.x > 25:
			player.x -= player_speed
			left, right, up, down = True, False, False, False
		if keys[pygame.K_d] and player.x + player.get_width() < WIDTH - 25: # -25 because map sprite has his own borders (cactus)
			player.x += player_speed
			left, right, up, down = False, True, False, False
		if keys[pygame.K_w] and player.y > 25:
			player.y -= player_speed
			left, right, up, down = False, False, True, False
		if keys[pygame.K_s] and player.y + player.get_height() < HEIGHT - 25: # -25 because map sprite has his own borders (cactus)
			player.y += player_speed
			left, right, up, down = False, False, False, True
		if not keys[pygame.K_s] and not keys[pygame.K_w] and not keys[pygame.K_d] and not keys[pygame.K_a]:
			left, right, up, down = False, False, False, False

		# Diagonal shooting
		if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
			player.shoot(-1, -1)
		if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
			player.shoot(1, -1)
		if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
			player.shoot(-1, 1)
		if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
			player.shoot(1, 1)

		# Shooting keys
		if keys[pygame.K_LEFT]:
			player.shoot(-1, 0)
			left, right, up, down = True, False, False, False
			#pygame.mixer.Sound.play(shoot_sound)
		if keys[pygame.K_RIGHT]:
			player.shoot(1, 0)
			left, right, up, down = False, True, False, False
			#pygame.mixer.Sound.play(shoot_sound)
		if keys[pygame.K_UP]:
			player.shoot(0, -1)
			left, right, up, down = False, False, True, False
			#pygame.mixer.Sound.play(shoot_sound)
		if keys[pygame.K_DOWN]:
			player.shoot(0, 1)
			left, right, up, down = False, False, False, True
			#pygame.mixer.Sound.play(shoot_sound)

		# Enemy movement
		for enemy in enemies:
			enemy.move(player.x, player.y)

			if collide(enemy, player):
				pygame.mixer.Sound.play(cowboy_dead)				
				pygame.mixer.music.stop()
				lives -= 1
				pygame.time.delay(2800)
				run = False
			
		player.move_bullet(bullet_speed, enemies)

		# Redraw and update sprites, dont delete
		redraw_window()
		pygame.display.update()


def main_menu():
	font = pygame.font.SysFont("freesansbold.ttf", 30)
	run = True
	while run:
		screen.blit(background_1, (0,0))
		title_text = font.render("Press any key to begin...", 1, (255,255,255))
		screen.blit(title_text, (int(WIDTH/2 - title_text.get_width()/2), int(HEIGHT/2 - title_text.get_height()/2)))
		
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				main()
	pygame.quit()


# Call main_menu function to start game
main_menu()