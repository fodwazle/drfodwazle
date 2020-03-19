TITLE = "My Video Game"
WIDTH = 900
HEIGHT = 700
FPS = 60
FONT_NAME = 'comic_sans'
#SPRITESHEET = "spritesheet_platformer.png"

#player properties
PLAYER_ACC = 3
SPRINT_ACC = 6.5
PLAYER_FRICTION = -0.7
PLAYER_GRAV = 1.5
PLAYER_JUMP = 30
DASH_MULTIPLIER = 20
global equipedWeapon
global name; name = 0; global attack; attack = 1; global speed; speed = 2; global length; length = 3
global stamina_usage; stamina_usage = 4; global reqNoHands; reqNoHands = 5; global effect; effect = 6
global exhausted; exhausted = False
global stamina; stamina = 250
global midair; midair = False
MAX_STAMINA = 250
global paused; paused = False
MOB_ACC = 2
MOB_JUMP = 35
MOB_ATTACK = 90

#starting platforms
PLATFORM_LIST = [(-300, HEIGHT - 40, WIDTH + 600, 80),  #x, y, w, h
                 (1000, HEIGHT * 3 / 4, 80, 40),
                 (125, HEIGHT - 350, 100, 40),
                 (500, HEIGHT - 200, 150, 40)]
#colours (Red, Green, Blue)
WHITE = (255, 255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
DARK_GREEN = (0, 150, 0)

