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
WIDTH, HEIGHT = 1366,768 
BG_WIDTH,BG_HEIGHT=2732,768
SCREEN = pg.display.set_mode((WIDTH,HEIGHT))
CLOCK = pg.time.Clock()
FPS = 60
pg.display.set_caption("game_project")
LEVEL = 1
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
HUMAN_GOLD_COOLDOWN = 0.1*FPS #0.1초
HUMAN_START_GOLD = 1000

WIZARD_VEL = 15
WIZARD_HP = 100
WIZARD_GOLD_COOLDOWN = 0.1*FPS #0.1초
WIZARD_START_GOLD = 1000
#ENEMY
ZOMBIE_VEL = 5
ZOMBIE_HP = 90
ZOMBIE_DMG = 100
ZOMBIE_COOLDONW = 0.5*FPS#0.5초

#WALL
WALL_PRICE = 250
WALL_HP = 1000

#CANON
CANON_PRICE = 300
CANON_HP = 500
CANON_DMG = 30
CANONSHOT_VEL = 50
CANON_COOLDOWN = 1*FPS
CANON_RANGE = 500

#MORTAR
MORTAR_PRICE = 500
MORTAR_HP = 500
MORTAR_DMG = 100
#MINE
MINE_PRICE = 150
MINE_HP = 300
MINE_GOLD_OUTPUT = 10
MINE_GOLD_COOLDOWN = 1*FPS

#색깔 채우기
def fill(surface, color):
    new_surface = surface.copy()
    w, h = surface.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = new_surface.get_at((x, y))[3]
            new_surface.set_at((x, y), pg.Color(r, g, b, a))
    return new_surface



#리소스 파일(폰트,이미지,사운드)
myfont = pg.font.Font("resources\\font\\NeoDunggeunmoPro-Regular.ttf",30)
background_img = pg.transform.scale(pg.image.load("resources\\images\\background.png").convert_alpha(),(BG_WIDTH,BG_HEIGHT))
hp_frame_img = pg.transform.scale(pg.image.load("resources\\images\\hp_bar_frame.png").convert_alpha(),(HP_FRAME_WIDTH,HP_FRAME_HEIGHT))

#플레이어
human_img = pg.image.load("resources\\images\\human.png").convert_alpha()
wizard_img = pg.image.load("resources\\images\\human.png").convert_alpha()
#적
zombie_img = pg.image.load("resources\\images\\zombie.png").convert_alpha()

#건물
wall_img = pg.image.load("resources\\images\\wall.png").convert_alpha()

#대포
canon_img = pg.image.load("resources\\images\\canon.png").convert_alpha()
canon_img_l = pg.transform.flip(canon_img,True,False)
canonshot_img = pg.image.load("resources\\images\\canonshot.png").convert_alpha()

#박격포
mortar_img = pg.image.load("resources\\images\\canon.png").convert_alpha()
mortar_img_l = pg.transform.flip(mortar_img,True,False)
mortarshot_img = pg.image.load("resources\\images\\canonshot.png").convert_alpha()


mine_img = pg.image.load("resources\\images\\mine.png").convert_alpha()


#floor_img = pg.image.load("resources\\images\\floor.png").convert_alpha()
