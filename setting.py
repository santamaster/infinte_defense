import pygame as pg

pg.init()

#색상 설정
WHITE = (255,255,255)
RED= (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (128,128,128)
BLACK = (0,0,0)

#시스템 설정
RUNNING = 1
WIDTH, HEIGHT = 1366,768 
BG_WIDTH,BG_HEIGHT=2732,768
SCREEN = pg.display.set_mode((WIDTH,HEIGHT))
CLOCK = pg.time.Clock()
FPS = 60
pg.display.set_caption("game_project")
CAMERA_VEL = 10
HP_FRAME_WIDTH = 400
HP_FRAME_HEIGHT = 40
HP_FRAME_INTERVAL = 20

#기본 설정
PLAYER_JUMP_PW = 30
GRAVITY = 3#중력

#PLAYER
HUMAN_VEL = 10
HUMAN_HP = 150

WIZARD_VEL = 15
WIZARD_HP = 100

#ENEMY
ZOMBIE_VEL = 5
ZOMBIE_HP = 100
ZOMBIE_DMG = 10



      

#리소스 파일(폰트,이미지,사운드)
myfont = pg.font.Font("resources\\font\\NeoDunggeunmoPro-Regular.ttf",30)
background_img = pg.transform.scale(pg.image.load("resources\\images\\background.png").convert_alpha(),(BG_WIDTH,BG_HEIGHT))
human_img = pg.image.load("resources\\images\\human.png").convert_alpha()
wizard_img = pg.image.load("resources\\images\\human.png").convert_alpha()

zombie_img = pg.image.load("resources\\images\\zombie.png").convert_alpha()
#floor_img = pg.image.load("resources\\images\\floor.png").convert_alpha()
hp_frame_img = pg.transform.scale(pg.image.load("resources\\images\\hp_bar_frame.png").convert_alpha(),(HP_FRAME_WIDTH,HP_FRAME_HEIGHT))