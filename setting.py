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
MYFONT = pg.font.Font("resources\\font\\NeoDunggeunmoPro-Regular.ttf",30)
BACKGROUND_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\background.png").convert_alpha(),(BG_WIDTH,BG_HEIGHT))
GROUND_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\ground.png").convert_alpha(),(BG_WIDTH,BG_HEIGHT))
HP_FRAME_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\hp_bar_frame.png").convert_alpha(),(HP_FRAME_WIDTH,HP_FRAME_HEIGHT))
MENU_FRAME = pg.transform.scale(pg.image.load("resources\\images\\frame.png").convert_alpha(),(300,500))
ABILITY_FRAME =MENU_FRAME.copy()
OUTLINE_ABILITY_FRAME = get_outline(ABILITY_FRAME)
BUILDING_FRAME = pg.transform.scale(pg.image.load("resources\\images\\frame.png").convert_alpha(),(120,200))
OUTLINE_BUILDING_FRAME = get_outline(BUILDING_FRAME)
BUTTON = pg.image.load("resources\\images\\button.png").convert_alpha()
UPGRADE_BUTTON = pg.transform.scale(pg.image.load("resources\\images\\upgrade.png").convert_alpha(),(50,50))
SELL_BUTTON = pg.transform.scale(pg.image.load("resources\\images\\sell.png").convert_alpha(),(50,50))
BUILD_BUTTON = pg.transform.scale(pg.image.load("resources\\images\\build.png").convert_alpha(),(100,100))
REPLAY_BUTTON = pg.transform.scale(pg.image.load("resources\\images\\replay.png").convert_alpha(),(50,50))
GOTO_MAIN_MENU_BUTTON =pg.transform.scale(pg.image.load("resources\\images\\exit.png").convert_alpha(),(50,50))
PLAYER_IMAGE = pg.image.load("resources\\images\\player.png").convert_alpha()
COIN_IMAGE = pg.image.load("resources\\images\\gold1.png").convert_alpha()

#ZOMBIE
ZOMBIE_IMAGE_SIZE = (100,150)
ZOMBIE_IMAGE = pg.image.load("resources\\images\\zombie.png").convert_alpha()

#SKELETON
SKELETON_IMAGE_SIZE = (100,150)
SKELETON_IMAGE = pg.image.load("resources\\images\\zombie.png").convert_alpha()
SKELETON_ARROW_IMAGE = pg.image.load("resources\\images\\arrow.png").convert_alpha()
SKELETON_ARROW_IMAGE_L = pg.transform.flip(SKELETON_ARROW_IMAGE,True,False)

#WALL
WALL_IMAGE_SIZE = (100,150)
WALL_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\wall.png").convert_alpha(),WALL_IMAGE_SIZE)
OUTLINE_WALL = get_outline(WALL_IMAGE)

#CANON
CANON_IMAGE_SIZE = (150,100)
CANON_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\canon.png").convert_alpha(),CANON_IMAGE_SIZE)
CANON_IMAGE_L = pg.transform.flip(CANON_IMAGE,True,False)
OUTLINE_CANON = get_outline(CANON_IMAGE)
OUTLINE_CANON_L = get_outline(CANON_IMAGE_L)
CANONSHOT_IMAGE = pg.image.load("resources\\images\\canonshot.png").convert_alpha()

#MORTAR
MORTAR_IMAGE_SIZE = (100,150)
MORTAR_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\mortar.png").convert_alpha(),MORTAR_IMAGE_SIZE)
OUTLINE_MORTAR = get_outline(MORTAR_IMAGE)
MORTARSHOT_IMAGE = pg.image.load("resources\\images\\canonshot.png").convert_alpha()
FIRE_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\fire.png").convert_alpha(),(300,100))
#MINE
MINE_IMAGE_SIZE = (150,100)
MINE_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\mine.png").convert_alpha(),MINE_IMAGE_SIZE)
OUTLINE_MINE = get_outline(MINE_IMAGE)

#earn_gold_effect
EARN_GOLD_EFFECT_SIZE = (30,30)
EARN_GOLD_EFFECT_SPEED = 12/FPS
EARN_GOLD_EFFECT_IMAGES = set_size(EARN_GOLD_EFFECT_SIZE,\
    *[pg.image.load("resources\\images\\gold{}.png".format(i)).convert_alpha() for i in range(1,5)])
EARN_GOLD_EFFECT_VEL = -6
EARN_GOLD_EFFECT_HOLD_TIME = 0.35*FPS