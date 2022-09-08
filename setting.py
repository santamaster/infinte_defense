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
CAMERA_VEL = 10
HP_FRAME_WIDTH = 400
HP_FRAME_HEIGHT = 40
HP_FRAME_INTERVAL = 20

#기본 설정
PLAYER_JUMP_PW = 30
GRAVITY = 3#중력
REFUND_RATE = 0.7
MESSAGE_COOLDOWN = 1*FPS


#크기 정하기
def set_size(size,*images):
    changed_images = []
    for image in images:
        changed_images.append(pg.transform.scale(image,size))
    return changed_images

    
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

#외각선 따기
def get_outline(image,outline_thickness=3,color=(255,255,255,255)):
    mask = pg.mask.from_surface(image)
    mask_size = mask.get_size()
    scaled_mask = mask.scale((mask_size[0]-outline_thickness*2,mask_size[1]-outline_thickness*2))
    mask.erase(scaled_mask,(outline_thickness,outline_thickness))

    return mask.to_surface(setcolor=color,unsetcolor=(0,0,0,0))

#폰트,배경 및 기타
myfont = pg.font.Font("resources\\font\\NeoDunggeunmoPro-Regular.ttf",30)
background_img = pg.transform.scale(pg.image.load("resources\\images\\background.png").convert_alpha(),(BG_WIDTH,BG_HEIGHT))
ground_img = pg.transform.scale(pg.image.load("resources\\images\\ground.png").convert_alpha(),(BG_WIDTH,BG_HEIGHT))
hp_frame_img = pg.transform.scale(pg.image.load("resources\\images\\hp_bar_frame.png").convert_alpha(),(HP_FRAME_WIDTH,HP_FRAME_HEIGHT))
MENU_FRAME = pg.image.load("resources\\images\\menu_frame.png").convert_alpha()
BUTTON = pg.image.load("resources\\images\\button.png").convert_alpha()

#PLAYER
PLAYER_REQIRED_EXP = [1000,1500,2000,3000,5000]
PLAYER_MAX_LEVEL = 6

#HUMAN
human_img = pg.image.load("resources\\images\\human.png").convert_alpha()
HUMAN_VEL = 10
HUMAN_HP = 1000
HUMAN_GOLD_COOLDOWN = 0.5*FPS #0.1초
HUMAN_GOLD_OUTPUT = 1
HUMAN_START_GOLD = 1000

#WIZARD
wizard_img = pg.image.load("resources\\images\\human.png").convert_alpha()
WIZARD_VEL = 15
WIZARD_HP = 1000
WIZARD_GOLD_COOLDOWN = 0.5*FPS #0.1초
WIZARD_GOLD_OUTPUT = 1
WIZARD_START_GOLD = 1000

#ZOMBIE
ZOMBIE_IMAGE_SIZE = (100,150)
ZOMBIE_IMAGE = pg.image.load("resources\\images\\zombie.png").convert_alpha()
ZOMBIE_VEL = 5
ZOMBIE_HP = 90
ZOMBIE_DMG = 50
ZOMBIE_COOLDONW = 1*FPS#1초
ZOMBIE_FIRST_COOLDOWN = 0.1*FPS#0.1초
ZOMBIE_RANGE = 10
ZOMBIE_HP_BAR_WIDTH = 70
ZOMBIE_EXP = 20

#WALL
WALL_IMAGE_SIZE = (100,150)
WALL_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\wall.png").convert_alpha(),WALL_IMAGE_SIZE)
OUTLINE_WALL = get_outline(WALL_IMAGE)
WALL_PRICE = [250,300]
WALL_HP = [1000,1500]
WALL_MAX_LEVEL = 2
WALL_HP_BAR_WIDTH = 100

#CANON
CANON_IMAGE_SIZE = (150,100)
CANON_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\canon.png").convert_alpha(),CANON_IMAGE_SIZE)
CANON_IMAGE_L = pg.transform.flip(CANON_IMAGE,True,False)
OUTLINE_CANON = get_outline(CANON_IMAGE)
OUTLINE_CANON_L = get_outline(CANON_IMAGE_L)
CANONSHOT_IMAGE = pg.image.load("resources\\images\\canonshot.png").convert_alpha()
CANON_PRICE = [300,400,500]
CANON_HP = [500,700,1000]
CANON_DMG = [30,50,70]
CANONSHOT_VEL = 30
CANON_COOLDOWN = 1*FPS
CANON_FIRST_COOLDOWN = 0.5*FPS
CANON_RANGE = 800
CANON_MAX_LEVEL = 3
CANON_HP_BAR_WIDTH = 150

#MORTAR
MORTAR_IMAGE = pg.image.load("resources\\images\\canon.png").convert_alpha()
MORTAR_IMAGE_L = pg.transform.flip(MORTAR_IMAGE,True,False)
OUTLINE_MORTAR = get_outline(MORTAR_IMAGE)
OUTLINE_MORTAR_L = get_outline(MORTAR_IMAGE_L)
MORTARSHOT_IMAGE = pg.image.load("resources\\images\\canonshot.png").convert_alpha()
MORTAR_PRICE = 500
MORTAR_HP = 500
MORTAR_DMG = 100

#MINE
MINE_IMAGE_SIZE = (150,100)
MINE_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\mine.png").convert_alpha(),MINE_IMAGE_SIZE)
outline_mine = get_outline(MINE_IMAGE)
MINE_PRICE = [150,250,400]
MINE_HP = [300,400,600]
MINE_GOLD_OUTPUT = [20,40,80]
MINE_GOLD_COOLDOWN = 2*FPS
MINE_MAX_LEVEL = 3
MINE_HP_BAR_WIDTH = 150

#earn_gold_effect
EARN_GOLD_EFFECT_SIZE = (30,30)
EARN_GOLD_EFFECT_SPEED = 12/FPS
EARN_GOLD_EFFECT_IMAGES = set_size(EARN_GOLD_EFFECT_SIZE,\
    *[pg.image.load("resources\\images\\gold{}.png".format(i)).convert_alpha() for i in range(1,5)])
EARN_GOLD_EFFECT_VEL = -6
EARN_GOLD_EFFECT_HOLD_TIME = 0.35*FPS