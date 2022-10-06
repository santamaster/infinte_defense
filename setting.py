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
DEEP_PURPLE = (51,0,35)
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

def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pg.transform.smoothscale(surface, scale_size)
    surf = pg.transform.smoothscale(surf, surf_size)
    return surf

#폰트,배경 및 기타
MYFONT = pg.font.Font("resources\\font\\NeoDunggeunmoPro-Regular.ttf",30)
BACKGROUND_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\background.png").convert_alpha(),(BG_WIDTH,BG_HEIGHT))
BLURRED_BACKGROUDN_IMAGE = blurSurf(BACKGROUND_IMAGE.subsurface((BG_WIDTH/2-WIDTH/2,0,WIDTH,HEIGHT)),5)
GROUND_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\ground.png").convert_alpha(),(BG_WIDTH,BG_HEIGHT))
HP_FRAME_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\hp_bar_frame.png").convert_alpha(),(HP_FRAME_WIDTH,HP_FRAME_HEIGHT))
MENU_FRAME = pg.transform.scale(pg.image.load("resources\\images\\menu_frame.png").convert_alpha(),(250,100))
PLAY_FRAME = MENU_FRAME.copy()
DEFEAT_MENU_FRAME = pg.transform.scale(pg.image.load("resources\\images\\menu_frame.png").convert_alpha(),(200,80))
ABILITY_FRAME = pg.transform.scale(pg.image.load("resources\\images\\ability_frame.png").convert_alpha(),(300,500))
OUTLINE_ABILITY_FRAME = get_outline(ABILITY_FRAME)
BUILDING_FRAME = pg.transform.scale(pg.image.load("resources\\images\\ability_frame.png").convert_alpha(),(120,200))
OUTLINE_BUILDING_FRAME = get_outline(BUILDING_FRAME)
UPGRADE_BUTTON = pg.transform.scale(pg.image.load("resources\\images\\upgrade.png").convert_alpha(),(50,50))
SELL_BUTTON = pg.transform.scale(pg.image.load("resources\\images\\sell.png").convert_alpha(),(50,50))
BUILD_BUTTON = pg.transform.scale(pg.image.load("resources\\images\\build.png").convert_alpha(),(100,100))
REPLAY_BUTTON = pg.transform.scale(pg.image.load("resources\\images\\replay.png").convert_alpha(),(50,50))
GOTO_MAIN_MENU_BUTTON =pg.transform.scale(pg.image.load("resources\\images\\exit.png").convert_alpha(),(50,50))
PLAYER_IMAGE_SIZE = (128,128)
PLAYER_IMAGE_SPEED = 6/FPS
PLAYER_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\player1.png").convert_alpha(),PLAYER_IMAGE_SIZE)
PLAYER_IMAGES =set_size(PLAYER_IMAGE_SIZE,\
    *[pg.image.load("resources\\images\\player{}.png".format(i)).convert_alpha() for i in range(2,3+1)])

PLAYER_IMAGE_L = pg.transform.flip(PLAYER_IMAGE,True,False)
PLAYER_IMAGES_L = [pg.transform.flip(image,True,False) for image in PLAYER_IMAGES]

COIN_IMAGE = pg.image.load("resources\\images\\gold1.png").convert_alpha()

#ZOMBIE
ZOMBIE_IMAGE_SIZE = (128,128)
ZOMBIE_IMAGE_SPEED = 1/FPS
ZOMBIE_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\zombie1.png").convert_alpha(),ZOMBIE_IMAGE_SIZE)
ZOMBIE_IMAGES = set_size(ZOMBIE_IMAGE_SIZE,\
    *[pg.image.load("resources\\images\\zombie{}.png".format(i)).convert_alpha() for i in range(2,3+1)])

ZOMBIE_IMAGE_L = pg.transform.flip(ZOMBIE_IMAGE,True,False)
ZOMBIE_IMAGES_L = [pg.transform.flip(image,True,False) for image in ZOMBIE_IMAGES]

#SKELETON
SKELETON_IMAGE_SIZE = (128,128)
SKELETON_IMAGE_SPEED = 3/FPS
SKELETON_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\skeleton1.png").convert_alpha(),ZOMBIE_IMAGE_SIZE)
SKELETON_IMAGES = set_size(SKELETON_IMAGE_SIZE,\
    *[pg.image.load("resources\\images\\skeleton{}.png".format(i)).convert_alpha() for i in range(2,3+1)])

SKELETON_IMAGE_L = pg.transform.flip(SKELETON_IMAGE,True,False)
SKELETON_IMAGES_L = [pg.transform.flip(image,True,False) for image in SKELETON_IMAGES]
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
CANONSHOT_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\canonshot.png").convert_alpha(),(32,32))

#MORTAR
MORTAR_IMAGE_SIZE = (100,150)
MORTAR_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\mortar.png").convert_alpha(),MORTAR_IMAGE_SIZE)
OUTLINE_MORTAR = get_outline(MORTAR_IMAGE)
MORTARSHOT_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\canonshot.png").convert_alpha(),(50,50))
FIRE_IMAGE_SPEED = 12/FPS
FIRE_IMAGE_SIZE = (300,100)
FIRE_IMAGES = set_size(FIRE_IMAGE_SIZE,\
    *[pg.image.load("resources\\images\\fire{}.png".format(i)).convert_alpha() for i in range(1,5)])

#FIREBALL_THROWER
FIREBALL_THROWER_IMAGE_SIZE = (100,150)
FIREBALL_THROWER_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\mortar.png").convert_alpha(),FIREBALL_THROWER_IMAGE_SIZE)
FIREBALL_THROWER_IMAGE_L = pg.transform.flip(FIREBALL_THROWER_IMAGE,True,False)
OUTLINE_FIREBALL_THROWER = get_outline(FIREBALL_THROWER_IMAGE)
OUTLINE_FIREBALL_THROWER_L = get_outline(FIREBALL_THROWER_IMAGE_L)

FIREBALL_IMAGE = pg.transform.scale(pg.image.load("resources\\images\\fireball.png").convert_alpha(),(20,20))



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