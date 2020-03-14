import pygame as pg
import os
import pygame, sys
#from pygame.locals import *
import pygame.locals as pgl
import random
WIDTH = 800   # Window width: keep within screen resolution eg max 1366
HEIGHT = 500  # Window height: keep within screen resolution eg max 768
FPS = 30       # Frames Per Second: controls the running speed of the game
vec = pg.math.Vector2
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0 ,0 , 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0 , 255)
YELLOW = (255, 255, 0)
GRAY = (211,211,211)
SILVER = (175,175,175)
LIGHT_SILVER = (180, 180, 180)
pg.font.init() 
game_folder = os.path.dirname(__file__)
pg.display.__init__("rock, paper and scissors")
#input your classes here

screen = pg.display.set_mode((WIDTH, HEIGHT)) # Note double brackets, as this is a Tuple
def draw_text(text, size, color, x, y):
	font = pg.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	screen.blit(text_surface, text_rect) # text for death score


class Button(pg.sprite.Sprite):
	def __init__(self, x, y, move):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((100, 50))
		self.image.fill(SILVER)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.move = move
		self.draw_text(self.move, 15, BLACK, int(self.rect.width/2), int(self.rect.height / 2))
		
	def isOver(self, pos):
	#Pos is the mouse position or a tuple of (x,y) coordinates
		if (pos[0] > self.rect.x and pos[0] < self.rect.x + self.rect.width) and (pos[1] > self.rect.y and pos[1] < self.rect.y + self.rect.height):
		    #if pos[1] > self.y and pos[1] < self.y + self.height:
			return True
	    
		return False
	
	def draw_text(self, text, size, color, x, y):
		pg.font.init() 
		self.font = pg.font.SysFont("comicsansms", size)
		self.text_surface = self.font.render(text, True, color)
		self.text_rect = self.text_surface.get_rect()
		self.text_rect.center = (x, y)
		self.image.blit(self.text_surface, self.text_rect)
        
	def update(self):
		pos = pg.mouse.get_pos()
		
		for event in pg.event.get():
			pos = pg.mouse.get_pos()
			if event.type == pg.MOUSEBUTTONDOWN:
				if self.isOver(pos):
					player.move = self.move
					
			if event.type == pg.MOUSEMOTION:
				if self.isOver(pos):
					self.image.fill(LIGHT_SILVER)
					self.image.blit(self.text_surface, self.text_rect)
				else:
					self.image.fill(SILVER)
					self.image.blit(self.text_surface, self.text_rect)
				
button = Button(1,1,"")
class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		#self.image = pg.Surface((112, 65)) #for paper
		self.image = pg.Surface((82, 66)) # for rock
		#self.image = pg.Surface((112, 69)) # for scissors
		self.pic_right = pg.image.load(r"rock.png")
		self.pic = self.pic_right
		self.image.fill(WHITE)
		self.image.blit(self.pic, [0,0])
		self.image.set_colorkey(WHITE)
		#self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.y =  HEIGHT / 2
		self.rect.centerx = WIDTH / 5
		
		self.moving = False
		self.no_moves = 0
		self.speed = vec(0,0)
		
		self.score = 0
		self.move = ""
		self.draw_text(str(self.score), 16, BLACK, WIDTH / 5, 40)
	def update(self):
		if self.move != "":
			self.moving = True
			if self.rect.y <= HEIGHT / 3 and self.no_moves < 5:
				self.speed.y = 20
				self.no_moves += 1
			elif self.rect.y >= HEIGHT / 2 and self.no_moves < 5:
				self.speed.y = -20
				self.no_moves += 1
			self.rect.y += self.speed.y
			if self.no_moves >= 5:
				if self.move == "rock":
					self.pic_right = pg.image.load(r"rock.png")
					self.image = pg.Surface((82, 66))
				elif self.move == "scissors":
					self.pic_right = pg.image.load(r"scissors.png")
					self.image = pg.Surface((112, 69))
				else:
					self.pic_right = pg.image.load(r"paper.png")
					self.image = pg.Surface((112, 65))
				
				self.pic_left = pg.transform.flip(self.pic_right, True, False)
				self.pic = self.pic_right
				self.image.fill(WHITE)
				self.image.blit(self.pic, [0,0])
				self.speed.y = 0
				self.image.set_colorkey(WHITE)
				self.moving = False
				
	def draw_text(self, text, size, color, x, y):
		pg.font.init() 
		self.font = pg.font.SysFont("comicsansms", size)
		self.text_surface = self.font.render(text, True, color)
		self.text_rect = self.text_surface.get_rect()
		self.text_rect.center = (x, y)
		#self.image.blit(self.text_surface, self.text_rect)
			
class AI(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		#self.image = pg.Surface((112, 65)) #for paper
		self.image = pg.Surface((82, 66)) # for rock
		#self.image = pg.Surface((112, 69)) # for scissors
		self.pic_right = pg.image.load(r"rock.png")
		self.pic_left = pg.transform.flip(self.pic_right, True, False)
		self.pic = self.pic_left
		self.image.fill(WHITE)
		self.image.blit(self.pic, [0,0])
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.y =  HEIGHT / 2
		self.rect.centerx = WIDTH * 4/5
		self.move = random.choice(["rock", "paper", "scissors"])
		self.score = 0
	def update(self):
		if player.no_moves >= 5:
			if self.move == "rock":
				self.pic_right = pg.image.load(r"rock.png")
				self.pic_left = pg.transform.flip(self.pic_right, True, False)
				self.image = pg.Surface((82, 66))
			elif self.move == "scissors":
				self.pic_right = pg.image.load(r"scissors.png")
				self.pic_left = pg.transform.flip(self.pic_right, True, False)
				self.image = pg.Surface((112, 69))
			elif self.move == "paper":
				self.pic_right = pg.image.load(r"paper.png")
				self.pic_left = pg.transform.flip(self.pic_right, True, False)
				self.image = pg.Surface((112, 65))
			self.pic_left = pg.transform.flip(self.pic_right, True, False)
			self.pic = self.pic_left
			self.image.fill(WHITE)
			self.image.blit(self.pic, [0,0])
			
			self.image.set_colorkey(WHITE)
		self.rect.y = player.rect.y
		
def check_score():
	if player.move == ai.move:
		print("the same!")
	elif player.move == "scissors" and ai.move == "paper":
		player.score += 1
	elif player.move ==  "paper" and ai.move == "rock":
		player.score += 1
	elif player.move == "rock" and ai.move == "scissors":
		player.score += 1
	else:
		ai.score += 1
		
player = Player()
game_folder = os.path.dirname(__file__)

os.environ["SDL_VIDEO_CENTERED"] = "1"

# initialise pygame and game window
pg.init()       # start pygame
font_name = pg.font.match_font("comic_sans")
draw_text(str(player.score), 16, WHITE, WIDTH / 5, 40)

# create game window. (screen is a variable. You can use anything e.g window, gameWindow, myEpicGame)

pg.display.set_caption("Rock, Paper and Scissors!") # The window title
clock = pg.time.Clock() # Keep track of framerate and other timing elements



# create a sprite group so all sprites can be updated and rendered together
all_sprites = pg.sprite.Group()
ai = AI()
all_sprites.add(player)
all_sprites.add(ai)
buttons = pg.sprite.Group()
rock_button = Button(WIDTH / 5, HEIGHT * 4/5, "rock")
paper_button = Button(WIDTH / 2, HEIGHT * 4/5, "paper")
scissor_button = Button(WIDTH * 4/5, HEIGHT * 4/5, "scissors")
all_sprites.add(paper_button)
all_sprites.add(rock_button)
all_sprites.add(scissor_button)

buttons.add(rock_button)
buttons.add(paper_button)
buttons.add(scissor_button)

# game loop
running = True # running is a variable. You can use anything e.g. continue, dontStop etc
while running:
	clock.tick(FPS)
	#drawing text
	check_score()
	# process events stored by Pygame: mouse actions, keys pressed, timers etc
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		

	# update all the sprites kept in the sprite Group (size, position etc)
	all_sprites.update()

	


	#draw the background and other elements to invisible screen in memory only
	screen.fill(GRAY)
	all_sprites.draw(screen) # sprites already updated so draw them

	# after drawing to invisible screen flip display to make it visible
	pg.display.flip()

pg.quit()
