import pygame
import math
import random
import sys

# Init pygame
pygame.init()
pygame.font.init()

# Create screen resolution
WIDTH = 400
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set title and icon 
pygame.display.set_caption('Journey of the Prairie King')
icon = pygame.transform.scale(pygame.image.load('assets/player.png'), (32, 32))
pygame.display.set_icon(icon)

# Set background image
background = pygame.transform.scale(pygame.image.load('assets/background.png'), (WIDTH, HEIGHT)).convert()

# Player image and pos
player_img = pygame.transform.scale(pygame.image.load('assets/player.png'), (20, 20))
# player_rect = player_img.get_rect(center = (playerX, playerY))

# Enemy image
enemy_image = pygame.transform.scale(pygame.image.load('assets/enemy.png'), (20, 20))

# Set bullet image
bullet_img = pygame.transform.scale(pygame.image.load('assets/bullet.png'), (5, 5))
# bullet_rect = bullet_img.get_rect(center = (bulletX, bulletY))

# Enemy base class, planning to implement more types.
class Hooman:
	def __init__(self, x, y, health = 100):
		self.x = x
		self.y = y
		self.health = health
		self.hooman_img = None
		self.bullet_img = None
		self.bullets = []
		self.cooldown_counter = 0

	def draw(self, window):
		window.blit(self.hooman_img, (int(self.x), int(self.y)))

	def get_width(self):
		return self.hooman_img.get_width()

	def get_height(self):
		return self.hooman_img.get_height()


# Enemy 1 class, inherits from Hooman
class Enemy(Hooman):
	def __init__(self, x, y, health = 100):
		super().__init__(x, y, health)
		self.hooman_img = enemy_image
		self.mask = pygame.mask.from_surface(self.hooman_img)

	def move(self, vel, x, y):
		# Find direction vector between enemy and player.
		dx = x - self.x
		dy = y - self.y
		dist = math.hypot(dx, dy)
		# Normalize vector.
		dx = dx/dist
		dy = dy/dist
		# Move along this normalized vector towards the player at current speed.
		self.x += dx * vel
		self.y += dy * vel


# Main player Class (No multiplayer in this game)
class Player:
	COOLDOWN = 45

	def __init__(self, x, y, health = 100):
		self.x = x
		self.y = y
		self.health = health
		self.player_img = player_img
		self.bullet_img = bullet_img
		self.mask = pygame.mask.from_surface(self.player_img)
		self.bullets = []
		self.cooldown_counter = 0

	def draw(self, window):
		window.blit(self.player_img, (self.x, self.y))
		for bullet in self.bullets:
			bullet.draw(window)

	def move_bullet(self, vel, objs):
		self.cooldown()
		for bullet in self.bullets:
			bullet.move(vel, bullet.horiz, bullet.vertical)
			for obj in objs:
				if bullet.collision(obj):
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
		return self.player_img.get_width()

	def get_height(self):
		return self.player_img.get_height()


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

	def move(self, vel, horiz, vertical):
		if horiz == -1:
			self.x += -vel
		if horiz == 1:
			self.x += vel
		if vertical == -1:
			self.y += -vel
		if vertical == 1:
			self.y += vel


def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

		
# Main class, set up game and game loop
def main():
	
	# Set FPS 
	FPS = 120
	clock = pygame.time.Clock()

	# Fonts
	font = pygame.font.SysFont('freesansbold.ttf', 32)

	# Set enemy list, enemy speed and enemy amount
	enemies = []
	enemy_speed = 0.3
	wave_length = 0

	# Initialize Player class in (x, y) coords
	player = Player(200, 200)
	player_speed = 1
	bullet_speed = 2
	bullets = []
	level = 0
	lives = 3
	lost = False

	def redraw_window():
		screen.blit(background, (0, 0))

		lives_text = font.render(f'Lives: {lives}', 1, (255, 255, 255))
		level_text = font.render(f'Level: {level}', 1, (255, 255, 255))

		screen.blit(lives_text, (5, 2))
		screen.blit(level_text, (WIDTH - level_text.get_width() - 5, 2))

		# Draw enemy sprite ingame
		for enemy in enemies:
			enemy.draw(screen)

		if lost:
			lost_text = font.render('You lost!', 1, (255, 255, 255))
			screen.blit(lost_text, (int(WIDTH/2 - lost_text.get_width()/2), int(HEIGHT/2 - lost_text.get_height()/2)))

		# Draw player sprite ingame
		player.draw(screen)
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
			wave_length += 5

			# Initialize enemies in loop
			for i in range(wave_length):
				door = random.choice(['left_door', 'top_door', 'right_door', 'down_door'])
				
				# If condition
				if door == 'left_door':
					enemy = Enemy(random.randrange(-200, -20), random.randrange(180, 220))
					enemies.append(enemy)
				if door == 'top_door':
					enemy = Enemy(random.randrange(180, 220), random.randrange(-100, -20))
					enemies.append(enemy)
				if door == 'right_door':
					enemy = Enemy(random.randrange(420, 500), random.randrange(180, 220))
					enemies.append(enemy)
				if door == 'down_door':
					enemy = Enemy(random.randrange(180, 220), random.randrange(420, 500))
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
		if keys[pygame.K_d] and player.x + player.get_width() < WIDTH - 25: # -25 because map sprite has his own borders
			player.x += player_speed
		if keys[pygame.K_w] and player.y > 25:
			player.y -= player_speed
		if keys[pygame.K_s] and player.y + player.get_height() < HEIGHT - 25: # -25 because map sprite has his own borders
			player.y += player_speed
		
		# Diagonall shooting
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
		if keys[pygame.K_RIGHT]:
			player.shoot(1, 0)
		if keys[pygame.K_UP]:
			player.shoot(0, -1)
		if keys[pygame.K_DOWN]:
			player.shoot(0, 1)

		
			
		# Enemy movement, TODO: track player
		for enemy in enemies:
			enemy.move(enemy_speed, player.x, player.y)

			if collide(enemy, player):
				print('collission')
				lives -= 1
				run = False
			
		player.move_bullet(bullet_speed, enemies)

		# Redraw and update sprites, dont delete
		redraw_window()
		pygame.display.update()


def main_menu():
	font = pygame.font.SysFont("freesansbold.ttf", 30)
	run = True
	while run:
		screen.blit(background, (0,0))
		title_text = font.render("Press any key to begin...", 1, (255,255,255))
		screen.blit(title_text, (int(WIDTH/2 - title_text.get_width()/2), int(HEIGHT/2 - title_text.get_height()/2)))
		
		pygame.display.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				main()
	pygame.quit()


# Call main function to start game
main_menu()