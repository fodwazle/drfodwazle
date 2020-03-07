import pygame as pg
import os
from pygame.locals import *
WIDTH = 800   # Window width: keep within screen resolution eg max 1366
HEIGHT = 500  # Window height: keep within screen resolution eg max 768
FPS = 30       # Frames Per Second: controls the running speed of the game

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

game_folder = os.path.dirname(__file__)
pg.display.__init__("rock, paper and scissors")
#input your classes here
"""
def draw_text(text, size, color, x, y):
	font = pg.font.Font(None, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.center = (x, y)
	#screen.blit(text_surface, text_rect)
	"""
class Button(pg.sprite.Sprite):
	def __init__(self, x, y, move):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((100, 50))
		self.image.fill(SILVER)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.move = move
		#self.draw_text(self.move, 48, BLACK, self.rect.centerx, self.rect.centery-30)
		
	def click(self):
		player.move = move
		print("Done!")
	def draw_text(self, text, size, color, x, y):
		self.font = pg.font.SysFont("comicsansms", size)
		self.text_surface = self.font.render(text, True, color)
		self.text_rect = self.text_surface.get_rect()
		self.text_rect.center = (x, y)
		screen.blit(self.text_surface, self.text_rect)
	def update(self):
		#self.draw_text(self.move, 48, BLACK, self.rect.centerx, self.rect.centery-30)
		mouse_pos = pg.mouse.get_pos()
		click = pg.mouse.get_pressed()
		if mouse_pos[1] > self.rect.right and mouse_pos[0] < self.rect.left and mouse_pos[0] > self.rect.bottom and mouse_pos[1] < self.rect.top and click == (1,0,0):
			self.click()
			
			
class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		#self.image = pg.Surface((112, 65))
		self.image = pg.Surface((82, 66))
		#self.image = pg.Surface((112, 69))
		self.pic_right = pg.image.load(r"rock.png")
		self.pic_left = pg.transform.flip(self.pic_right, True, False)
		self.pic = self.pic_right
		self.image.fill(WHITE)
		self.image.blit(self.pic, [0,0])
		self.image.set_colorkey(WHITE)
		#self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH / 5, HEIGHT / 2)
		
		
		self.move = ""
	def update(self):
		pass
player = Player()
game_folder = os.path.dirname(__file__)

os.environ["SDL_VIDEO_CENTERED"] = "1"

# initialise pygame and game window
pg.init()       # start pygame
font_name = pg.font.match_font("comic_sans")


# create game window. (screen is a variable. You can use anything e.g window, gameWindow, myEpicGame)
screen = pg.display.set_mode((WIDTH, HEIGHT)) # Note double brackets, as this is a Tuple
pg.display.set_caption("Rock, Paper and Scissors!") # The window title
clock = pg.time.Clock() # Keep track of framerate and other timing elements



# create a sprite group so all sprites can be updated and rendered together
all_sprites = pg.sprite.Group()

all_sprites.add(player)
buttons = pg.sprite.Group()
rock_button = Button(WIDTH / 5, HEIGHT * 4/5, "rock")
paper_button = Button(WIDTH / 2, HEIGHT * 4/5, "paper")
scissor_button = Button(WIDTH * 4/5, HEIGHT * 4/5, "scissor")
all_sprites.add(paper_button)
all_sprites.add(rock_button)
all_sprites.add(scissor_button)

buttons.add(rock_button)
buttons.add(paper_button)
buttons.add(scissor_button)

paper_button.draw_text(paper_button.move, 48, BLACK, paper_button.rect.centerx, paper_button.rect.centery-30)
rock_button.draw_text(rock_button.move, 48, BLACK, rock_button.rect.centerx, rock_button.rect.centery-30)
scissor_button.draw_text(scissor_button.move, 48, BLACK, scissor_button.rect.centerx, scissor_button.rect.centery-30)
# game loop
running = True # running is a variable. You can use anything e.g. continue, dontStop etc
while running:
	# keep loop running at correct speed
	clock.tick(FPS)
	#drawing text
	paper_button.draw_text(str(paper_button.move), 48, BLACK, paper_button.rect.centerx, paper_button.rect.centery-30)
	rock_button.draw_text(str(rock_button.move), 48, BLACK, rock_button.rect.centerx, rock_button.rect.centery-30)
	scissor_button.draw_text(str(scissor_button.move), 48, BLACK, scissor_button.rect.centerx, scissor_button.rect.centery-30)	
	
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
