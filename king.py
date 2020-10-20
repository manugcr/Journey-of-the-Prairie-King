import pygame
import math
import random

# Init pygame
pygame.init()


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
		self.bullet_cooldown = 0

	def draw(self, window):
		window.blit(self.hooman_img, (int(self.x), int(self.y)))

	def get_width(self):
		return self.hooman_img.get_width()

	def get_height(self):
		return self.hooman_img.get_height()

# Ex child class of Hooman for player
# class Player(Hooman):
# 	def __init__(self, x, y, health = 100):
# 		super().__init__(x, y, health)
# 		self.hooman_img = player_img
# 		self.bullet_img = bullet_img
# 		self.mask = pygame.mask.from_surface(self.hooman_img)
# 		self.max_health = health

# 	def draw(self, window):
# 		window.blit(self.hooman_img, (self.x, self.y))


# Main player Class (No multiplayer in this game)
class Player:
	def __init__(self, x, y, health = 100):
		self.x = x
		self.y = y
		self.health = health
		self.player_img = player_img
		self.bullet_img = bullet_img
		self.bullets = []
		self.bullet_cooldown = 0

	def draw(self, window):
		window.blit(self.player_img, (self.x, self.y))

	def get_width(self):
		return self.player_img.get_width()

	def get_height(self):
		return self.player_img.get_height()

# Enemy 1 class, inherits from Hooman
class Enemy(Hooman):
	def __init__(self, x, y, health = 100):
		super().__init__(x, y, health)
		self.hooman_img = enemy_image
		self.mask = pygame.mask.from_surface(self.hooman_img)

	def move(self, speed):
		self.x += speed

# Main class, set up game and game loop
def main():
	
	# Set FPS 
	FPS = 120
	clock = pygame.time.Clock()


	# Set enemy list, enemy speed and enemy amount
	enemies = []
	enemy_speed = 0.5
	wave_length = 0

	# Initialize Player class in (x, y) coords
	player = Player(200, 200)
	player_speed = 2
	level = 0
	lives = 3

	def redraw_window():
		screen.blit(background, (0, 0))

		# Draw enemy sprite ingame
		for enemy in enemies:
			enemy.draw(screen)

		# Draw player sprite ingame
		player.draw(screen)

		pygame.display.update()

	# Game loop
	run = True
	while run:

		# Set ingame FPS
		clock.tick(FPS)


		if len(enemies) == 0:
			level += 1
			wave_length += 5

			# Initialize enemies in loop
			for i in range(wave_length):
				door =  'left_door' # random.choice(['left_door', 'top_door', 'right_door', 'down_door'])
				if door == 'left_door':
					enemy = Enemy(random.randrange(-200, -20), random.randrange(180, 220))
					enemies.append(enemy)
				
				# More doors, testing

				# if door == 'top_door':
				# 	enemy = Enemy(random.randrange(180, 220), random.randrange(-100, -20))
				# 	enemies.append(enemy)
				# if door == 'right_door':
				# 	enemy = Enemy(random.randrange(420, 500), random.randrange(180, 220))
				# 	enemies.append(enemy)
				# if door == 'down_door':
				# 	enemy = Enemy(random.randrange(180, 220), random.randrange(420, 500))
				# 	enemies.append(enemy)


		# QUIT event, dont delete
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False


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


		# Enemy movement, TODO: track player
		for enemy in enemies:
			enemy.move(enemy_speed)


		# Redraw and update sprites, dont delete
		redraw_window()
		pygame.display.update()

# Call main function to start game
main()