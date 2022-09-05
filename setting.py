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
BG_WIDTH,BG_HEIGHT=4000,768
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
REFUND_RATE = 0.7

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

#외각선따기
def get_outline(image,color=(0,0,0)):
    rect = image.get_rect()
    mask = pg.mask.from_surface(image)
    outline = mask.outline()
    outline_image = pg.Surface(rect.size).convert_alpha()
    outline_image.fill((0,0,0,0))
    for point in outline:
        outline_image.set_at(point,color)
    return outline_image

#폰트,배경 및 기타
myfont = pg.font.Font("resources\\font\\NeoDunggeunmoPro-Regular.ttf",30)
background_img = pg.transform.scale(pg.image.load("resources\\images\\background.png").convert_alpha(),(BG_WIDTH,BG_HEIGHT))
ground_img = pg.transform.scale(pg.image.load("resources\\images\\ground.png").convert_alpha(),(BG_WIDTH,BG_HEIGHT))
hp_frame_img = pg.transform.scale(pg.image.load("resources\\images\\hp_bar_frame.png").convert_alpha(),(HP_FRAME_WIDTH,HP_FRAME_HEIGHT))

#HUMAN
human_img = pg.image.load("resources\\images\\human.png").convert_alpha()
HUMAN_VEL = 10
HUMAN_HP = 1000
HUMAN_GOLD_COOLDOWN = 0.1*FPS #0.1초
HUMAN_START_GOLD = 1000

#WIZARD
wizard_img = pg.image.load("resources\\images\\human.png").convert_alpha()
WIZARD_VEL = 15
WIZARD_HP = 1000
WIZARD_GOLD_COOLDOWN = 0.1*FPS #0.1초
WIZARD_START_GOLD = 1000

#ZOMBIE
zombie_img = pg.image.load("resources\\images\\zombie.png").convert_alpha()
ZOMBIE_VEL = 5
ZOMBIE_HP = 90
ZOMBIE_DMG = 50
ZOMBIE_COOLDONW = 1*FPS#1초
ZOMBIE_FIRST_COOLDOWN = 0.1*FPS#0.1초
ZOMBIE_RANGE = 10


#WALL
wall_img = pg.image.load("resources\\images\\wall.png").convert_alpha()
outline_wall = get_outline(wall_img)
WALL_PRICE = [250,300]
WALL_HP = [1000,1500]
WALL_MAX_LEVEL = 2

#CANON
canon_img = pg.image.load("resources\\images\\canon.png").convert_alpha()
canon_img_l = pg.transform.flip(canon_img,True,False)
outline_canon = get_outline(canon_img)
outline_canon_l = get_outline(canon_img_l)
canonshot_img = pg.image.load("resources\\images\\canonshot.png").convert_alpha()
CANON_PRICE = [300,400,500]
CANON_HP = [500,700,1000]
CANON_DMG = [30,50,70]
CANONSHOT_VEL = 30
CANON_COOLDOWN = 1*FPS
CANON_FIRST_COOLDOWN = 0.5*FPS
CANON_RANGE = 800
CANON_MAX_LEVEL = 3

#MORTAR
mortar_img = pg.image.load("resources\\images\\canon.png").convert_alpha()
mortar_img_l = pg.transform.flip(mortar_img,True,False)
outline_mortar = get_outline(mortar_img)
outline_mortar_l = get_outline(mortar_img_l)
mortarshot_img = pg.image.load("resources\\images\\canonshot.png").convert_alpha()
MORTAR_PRICE = 500
MORTAR_HP = 500
MORTAR_DMG = 100

#MINE
mine_img = pg.image.load("resources\\images\\mine.png").convert_alpha()
outline_mine = get_outline(mine_img)
MINE_PRICE = [150,250,400]
MINE_HP = [300,400,600]
MINE_GOLD_OUTPUT = [20,40,80]
MINE_GOLD_COOLDOWN = 2*FPS
MINE_MAX_LEVEL = 3

#earn_gold_effect
earn_gold_effect_image = pg.transform.scale(pg.image.load("resources\\images\\gold.png").convert_alpha(),(45,45))
EARN_GOLD_EFFECT_VEL = -7
EARN_GOLD_EFFECT_HOLD_TIME = 0.25*FPS