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
BG_WIDTH,BG_HEIGHT=1366*2,768
SCREEN = pg.display.set_mode((WIDTH,HEIGHT))
CLOCK = pg.time.Clock()
FPS = 60
pg.display.set_caption("game_project")

#기본 설정
CAMERA_VEL= 10
PLAYER_VEL = 10
PLAYER_JUMP_TICK = 30#점프 지속 시간 1 = 1/FPS초
GRAVITY = 3#중력

      

#리소스 파일(폰트,이미지,사운드)
myfont = pg.font.Font("resources\\font\\NeoDunggeunmoPro-Regular.ttf",30)
player_img = pg.image.load("resources\\images\\human.png").convert_alpha()
background_img = pg.transform.scale(pg.image.load("resources\\images\\background.png").convert_alpha(),(BG_WIDTH,BG_HEIGHT))
#floor_img = pg.image.load("resources\\images\\floor.png").convert_alpha()
