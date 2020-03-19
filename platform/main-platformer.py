import pygame as pg
from settings import *
from spritesplatformer import *
from os import path
import pygame, os 
import weapons as wpn
import start
import csv
os.environ['SDL_VIDEO_CENTERED'] = '1'
from pygame.locals import *
class InputBox(pg.sprite.Sprite):
	def __init__(self, Width, Height, x, y, Text):
			pg.sprite.Sprite.__init__(self)
			self.image = pg.Surface((Width, Height))
			self.rect = self.image.get_rect()
	def update(self):
		pass
			

class Game:

	def __init__(self):		#initialize game window
		#creates window
		pg.init() # initialises pygame
		try:
			pygame.mixer.init() # start pygame sound library
		except:
			audio_present = False # sound card not present / disabled. use this flag in f
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption("Platformer")
		self.clock = pg.time.Clock() #FPS
		self.running = True
		self.font_name = pg.font.match_font(FONT_NAME)
		self.win = False
	def new(self):
		self.activeFrames = 0
		# start a new game
		self.deathscore = 0
		self.all_sprites = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		self.hitboxs = pg.sprite.Group()
		self.textboxs = pg.sprite.Group()
		self.bars = pg.sprite.Group()
		self.finishs = pg.sprite.Group()
		#groups created
		"""
		self.hitbox = Hitbox()
		self.all_sprites.add(self.hitbox)
		self.hitboxs.add(self.hitbox)		
		"""
		self.finish = Finish_line()
		self.all_sprites.add(self.finish)
		self.finishs.add(self.finish)
		self.health_bar = Health_bar()
		self.all_sprites.add(self.health_bar)
		self.mob_bar = Mob_health_bar()
		self.all_sprites.add(self.mob_bar)
		self.bars.add(self.mob_bar)
		self.input_box = InputBox(100, 100, WIDTH / 2, HEIGHT / 2, "")
		self.mob = Mob(WIDTH / 2, HEIGHT - 120)
		self.all_sprites.add(self.mob)
		self.mobs.add(self.mob)
		self.all_sprites.add(self.mob)
		
		self.stamina_bar = Stamina_bar()
		self.all_sprites.add(self.stamina_bar)
		self.bars.add(self.health_bar)
		self.bars.add(self.stamina_bar)
		self.player = Player(self)
		self.all_sprites.add(self.player)
		for plat in PLATFORM_LIST:
			self.p = Platform(*plat)
			self.all_sprites.add(self.p)
			self.platforms.add(self.p)
				
		if not paused:	
			self.run()
		
	
	def attack(self):
		self.hitbox = Hitbox(self.player.rect.centerx + (self.player.directionFacing.x * self.player.weaponEquipped[length]), self.player.rect.centery, self.player.weaponEquipped[length], 50)
		self.all_sprites.add(self.hitbox)
		self.hitboxs.add(self.hitbox)	
		
	def run(self):
		self.clock.tick(FPS) #sets the FPS
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()
			
	def mob_jump(self):
		self.mob.rect.y -= 1
		mob_hits = pg.sprite.spritecollide(self.mob, self.platforms, False)
		if mob_hits:
			self.mob.speed.y -= MOB_JUMP
	
	def update(self):
		global player_health
		self.number = randrange(1, 1000)
		if self.number ==  4:
			self.mob_jump()
			
		global stamina
		keys = pg.key.get_pressed()
		self.mob_bar.rect.centerx = self.mob.rect.centerx
		self.mob_bar.rect.y = self.mob.rect.top - 20
		if self.mob.health > 0:
			self.mob_bar.image = pg.Surface((self.mob.health // 5, 5))
		else:
			self.mob_bar.kill()
		if self.mob.Iframes <= 0:
			self.mob_bar.grey = False
		elif self.mob.Iframes > 0:
			self.mob_bar.grey = True
		
		if (keys[pg.K_LEFT] or keys[pg.K_RIGHT] or keys[pg.K_a] or keys[pg.K_d]) and keys[pg.K_LCTRL] and not exhausted and not self.player.attacking:
			stamina -= 2
		#invincibility
		#attack numbers
		self.player.windframes -= 1
		self.player.move_duration -= 1
		if self.player.windframes <= 0:
			self.activeFrames -= 1
		#game loop update
		self.all_sprites.update()
		
		
		if keys[pg.K_ESCAPE]:
			self.paused = True
		if self.player.move_duration <= 0:
			self.player.attacking = False

		if keys[pg.K_LSHIFT] and not self.player.attacking and self.player.windframes <= 0:
			self.player.move_duration = self.player.weaponEquipped[speed] * 60; self.activeFrames = 10; self.player.windframes = self.player.weaponEquipped[speed] * 60/3
			self.player.attacking = True
			
		if self.player.attacking and self.activeFrames > 0 and self.player.windframes <= 0:
			self.attack()

		# hit mobs?
		
		end = pg.sprite.spritecollide(self.player, self.finishs, False)
		if end:
			self.playing = False
			self.win = True
			self.show_win_screen()
		
		if self.player.rect.right >= self.finish.rect.left:
			self.win = True
			self.playing = False
			self.show_win_screen()
		hitbox_hit = pg.sprite.groupcollide(self.hitboxs, self.mobs, False, False)
		if hitbox_hit and self.mob.Iframes <= 0:
			self.mob.health -= self.player.weaponEquipped[attack]
			self.mob.Iframes = 60
		mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
		if mob_hits and self.player.Iframes <= 0:
			self.player.health -= MOB_ATTACK
			self.player.Iframes = 60
			player_health -= MOB_ATTACK
		
		
		#check to see if player is hitting a platform
		if self.player.vel.y > 0:
			hits = pg.sprite.spritecollide(self.player, self.platforms, False)
			if hits:
				self.player.pos.y = hits[0].rect.top 
				self.player.vel.y = 0
				midair = False
		
		hits = pg.sprite.spritecollide(self.mob, self.platforms, False)
		if hits:
			self.mob.pos.y = hits[0].rect.top 
			self.mob.speed.y = 0
			"""
			if self.mob.rect.x >= self.p.rect.right:
				self.mob.speed.x = -self.mob.speed.x
			if self.mob.rect.x <= self.p.rect.left:
				self.mob.speed.x = -self.mob.speed.x
				"""
		if self.player.vel.x > 0:
			if self.player.rect.right >= WIDTH * 3 / 4: #and self.player.acc.x > 0:
				#self.player.pos = WIDTH * 3 / 4
				self.player.pos.x -= abs(self.player.vel.x)
				self.mob.rect.right -= abs(self.player.vel.x)
				self.finish.rect.right -= abs(self.player.vel.x)
				for plat in self.platforms:
					plat.rect.right -= abs(self.player.vel.x)
		if self.player.vel.x < 0:
			if self.player.rect.left <= WIDTH / 4:
				self.player.pos.x += abs(self.player.vel.x)
				self.mob.rect.left += abs(self.player.vel.x)
				self.finish.rect.left += abs(self.player.vel.x)
				for plat in self.platforms:
					plat.rect.left += abs(self.player.vel.x)
		
		#death
		if self.player.health <= 0:
			self.playing = False
		if self.player.rect.top > HEIGHT:
			
			for sprite in self.all_sprites:
				sprite.rect.y -= max(self.player.vel.y, 10)    #later replace this with a game over screen
				if sprite.rect.bottom < 0:
					sprite.kill()
		if len (self.platforms) == 0:
			self.playing = False
			self.deathscore = self.deathscore + 1
		
		
		
		#if player reaches the last fourth of the screen
		
		#spawn new platforms all in notes in case i want to use it again
		"""
		while len(self.platforms) < 6:
			width = random.randrange(50, 100)
			p = Platform(random.randrange(0, WIDTH + width),
				     random.randrange(10, 50),
				     width, 20)
			self.platforms.add(p)
			self.all_sprites.add(p)
		"""
	
	def events(self):
		key_up = pg.key.get_pressed()
		#Game Loop Events
		for event in pg.event.get(): #this is here so that pygame will use all inputs not just ones down when the code was running throught this section
			if event.type == pg.QUIT:   # this is for closing the window
				if self.playing:
					self.playing = False
				self.running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE and not self.player.attacking:
					self.player.jump()
			
	def pause_screen(self):
		pass
		
	
	def draw(self):
		#Game Loop Draw
		self.screen.fill(BLUE)
		self.all_sprites.draw(self.screen)
		self.draw_text(str(self.deathscore), 22, WHITE, WIDTH / 2, 15)
		
		#this is allways last, after all of the other drawing 
		pg.display.flip()

	
	def show_start_screen(self):
		#game start screen
		self.screen.fill(BLACK)
		self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
		self.draw_text("Arrows to move space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
		self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
		pg.display.flip()
		self.wait_for_key()
		
	
	def show_win_screen(self):
		if not self.running and not self.win:
			return
		self.screen.fill(BLACK)
		self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
		self.draw_text("Congratulations!!" + start.name + "You won", 22, WHITE, WIDTH / 2, HEIGHT / 2)
		self.draw_text("Press a key to play again!", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
		pg.display.flip()
		self.wait_for_key()		
	def show_go_screen(self):
		#game over
		if not self.running and self.win:
			return
		self.screen.fill(BLACK)
		self.draw_text("Game over", 48, WHITE, WIDTH / 2, HEIGHT / 4)
		
		self.draw_text("Press a key to try again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)		
		pg.display.flip()
		self.wait_for_key()		
	
	def wait_for_key(self):
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in  pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.running = False
				if event.type == pg.KEYUP:
					waiting = False
			
	
	def draw_text(self, text, size, color, x, y):
		font = pg.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect) # text for death score
			
	def save(self):
		with open("save_data", "w", newline = "") as csvfile:
			file = csv.writer(csvfile, delimeter = "", quotechar = " | ", quoting=csv.QUOTE_MINIMAL)
			file.writerow([self.player.rect.x, self.player.rect.y])
g = Game()
g = Game()
g.show_start_screen()
g.new()

g.attack()
keys = pg.key.get_pressed()
while g.running and not g.win:
	g.new()
	g.show_go_screen()
	
	
pg.quit
	
