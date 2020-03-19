 #SPRITE CLASSES
import start
from settings import *
import pygame as pg
vec = pg.math.Vector2
import weapons as wpn
from random import randrange
global player_health
player_health = 361
from pygame.locals import *
class Player(pg.sprite.Sprite):
	def __init__(self, game):
		global player_health
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = pg.Surface((35, 50))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH / 2, HEIGHT / 2)
		
		#self.vx = 0
		#self.vy = 0
		
		self.pos = vec(WIDTH / 2, HEIGHT / 2)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		
		self.attacking = True
		self.move_duration = 0
		self.windframes = 0
		self.weaponEquipped = start.weaponEquipped
		self.dashing = False
		self.directionFacing = vec(0, 0)
		self.health = 361
		self.invincible = False
		self.Iframes = 0
		
		player_health = self.health
	def jump(self):
	#check to see if on platform
		self.rect.y -= 1
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect.y += 2
		global stamina
		if hits:
			self.vel.y = -PLAYER_JUMP
		"""
		if not hits and not exhausted:
			stamina -= 45
			self.vel.y = -20
			"""

	def Dash(self):
		keys = pg.key.get_pressed()
		self.acc *= DASH_MULTIPLIER
	def update(self):
		if self.Iframes > 0:
			self.image.fill(GREY)
		else:
			self.image.fill(RED)
		global player_health
		player_health = self.health
		self.Iframes -= 1
		global stamina
		self.directionFacing = pg.math.Vector2(self.directionFacing.x, 0)
		global exhausted
		self.acc = vec(0, PLAYER_GRAV)
		
		#going left
		keys = pg.key.get_pressed()
		if (keys[pg.K_LEFT] or keys[pg.K_a]) and not (self.attacking or self.dashing):
			self.acc.x = -PLAYER_ACC
			self.directionFacing.x = -1
			if keys[pg.K_LCTRL] and not exhausted and not self.attacking:
				self.acc.x = -SPRINT_ACC
				self.directionFacing.x = -1
				

				#going right
		if (keys[pg.K_RIGHT] or keys[pg.K_d]) and not self.attacking:
			self.acc.x = PLAYER_ACC
			self.directionFacing.x = 1
			if keys[pg.K_LCTRL]and not exhausted and not self.attacking:
				self.acc.x = SPRINT_ACC
				self.directionFacing.x = 1
		if keys[pg.K_UP]:
			self.directionFacing.y = -1
		if keys[pg.K_DOWN]:
			self.directionFacing.y = 1
				
		#dashing
		if keys[pg.K_RETURN] and not self.attacking and not self.dashing:
			self.Dash()
		#aplies friction
		self.acc.x += self.vel.x * PLAYER_FRICTION
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
		self.rect.midbottom = self.pos
		if keys[pg.K_LSHIFT] and not self.attacking and self.windframes <= 0:
                        stamina -= self.weaponEquipped[stamina_usage]
		
	

class Platform(pg.sprite.Sprite):
	
	def __init__(self, x, y, w, h):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((w - 2, h))
		self.image.fill(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		

class Mob(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.pic_right = pg.image.load(r"demon.png")
		self.pic_left = pg.transform.flip(self.pic_right, True, False)
		self.pic = self.pic_right
		self.image = pg.Surface((130, 150))
		self.image.fill(WHITE)
		self.image.blit(self.pic, [0,0])
		self.image.set_colorkey(WHITE)
		self.image.convert()
		self.rect = self.image.get_rect()
		self.speed = vec(3,0)
		self.health = 300
		self.pos = vec(400, HEIGHT - 40)
		self.rect.x = 0
		self.rect.y = 500
		self.Iframes = 0
		self.image_flipped = False
		self.platform_touching = None

	
	def update(self):
		if self.speed.x > 0:
			self.pic = self.pic_right
			self.image = pg.Surface((130, 150))
			self.image.fill(WHITE)
			self.image.blit(self.pic, [0,0])
			self.image.set_colorkey(WHITE)
			self.image.convert()
			self.rect = self.image.get_rect()			
			self.image_flipped = False
		elif self.speed.x < 0 and not self.image_flipped:
			self.pic = self.pic_left
			self.image = pg.Surface((130, 150))
			self.image.fill(WHITE)
			self.image.blit(self.pic, [0,0])
			self.image.set_colorkey(WHITE)
			self.image.convert()
			self.rect = self.image.get_rect()			
			self.image_flipped = True
		self.Iframes -= 1
		self.image.blit(self.pic, [0,0])
		self.speed.y = PLAYER_GRAV
		self.pos += self.speed
		self.rect.midbottom = self.pos	
		if self.rect.left <= 0:
			self.speed.x *= -1
			
		if self.rect.right >= WIDTH:
			self.speed.x *= -1
			
		if self.health <= 0:
                        self.kill()
		"""
		#self.rect.x += self.speedx 
		self.acc.x += self.vel.x * PLAYER_FRICTION
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
		self.rect.midbottom = self.pos
		"""

class Hitbox(pg.sprite.Sprite):      
	def __init__(self, x = 0, y = 0, width = 100, height = 100):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((width, height))
		self.image.fill(GREY)
		self.rect = self.image.get_rect()
		self.speedx = 0
		self.speedy = 0
		self.rect.centerx = x
		self.rect.centery = y
	def update(self):
		self.kill()

class Stamina_bar(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		
		self.image = pg.Surface((stamina, 20))
		self.image.fill(DARK_GREEN)
		self.rect = self.image.get_rect()
		self.rect.y = 80
		self.rect.x = 60
		
	def update(self):
		global exhausted
		global stamina
		stamina += 1
		
		keys = pg.key.get_pressed()
		
		if keys[pg.K_LEFT] and keys[pg.K_LCTRL]and not exhausted:
			stamina -= 2
			
		elif keys[pg.K_RIGHT] and keys[pg.K_LCTRL] and not exhausted:
			stamina -= 2
			
		
		if stamina <= 0:
			stamina = 0
			exhausted = True
		if stamina >= 70:
			exhausted = False
			
		if stamina >= MAX_STAMINA:
			stamina = MAX_STAMINA
		self.image = pg.Surface((stamina, 20))
		self.image.fill(DARK_GREEN)
class Health_bar(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		global player_health
		self.image = pg.Surface((player_health, 20))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.y = 40
		self.rect.x = 60
	def update(self):
		global player_health
		self.image = pg.Surface((player_health, 20))
		self.image.fill(RED)

class Mob_health_bar(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((300 // 5, 5))
		self.image.fill(RED)
		self.rect = self.image.get_rect()		
		self.rect.centerx = 400
		self.rect.y = HEIGHT - 40
		self.grey = False
	def update(self):
		if not self.grey:
			self.image.fill(RED)
		elif self.grey:
			self.image.fill(GREY)
class Finish_line(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((10, HEIGHT))
		self.image.fill(GREY)
		self.rect = self.image.get_rect()
		self.rect.left = WIDTH + 298
		self.rect.centery = HEIGHT / 2
	def update(self):
		self.image.fill(GREY)
		
		
	