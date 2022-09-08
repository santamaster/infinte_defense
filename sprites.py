import pygame as pg
from pygame.locals import *
from setting import *

#스프라이트 그룹
all_sprites = pg.sprite.Group()         #모든 스프라이트 그룹
player_sprites = pg.sprite.Group()      #플레이어 스프라이트 그룹
enemy_sprites = pg.sprite.Group()       #적 스프라이트 그룹
building_sprites = pg.sprite.Group()    #건물 스프라이트 그룹
noncreature_sprites = pg.sprite.Group() #비생물 스프라이트 그룹
creature_sprites = pg.sprite.Group()    #생물 스프라이트 그룹
attackable_sprites = pg.sprite.Group()  #적이 공격가능한 스프라이트 그룹

wall_sprites = pg.sprite.Group()
mine_sprites = pg.sprite.Group()
canon_sprites = pg.sprite.Group()

#게임 플레이에 영향을 미치지 않는 스프라이트 그룹
effect_sprites = pg.sprite.Group()
message_sprites = pg.sprite.Group()
hp_bar_sprites = pg.sprite.Group()

#플레이어
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        all_sprites.add(self)
        player_sprites.add(self)
        attackable_sprites.add(self)
        creature_sprites.add(self)
        #플레이어 기본 변수 
        self.max_hp = None
        self.hp = None
        self.vector = pg.math.Vector2(BG_WIDTH/2,516)
        self.image = None
        self.rect = None
        self.shown_rect = None
        self.vel = None
        self.hp_bar = None
        self.jumping = False
        self.jump_vel = 0
        self.jump_pw = 0
        self.gold = 0
        self.gold_output = 1
        self.gold_cooldown = None
        self.gold_counter = 0
        self.level = 1
        self.max_level = PLAYER_MAX_LEVEL
        self.exp = 0
        self.reqired_exp = PLAYER_REQIRED_EXP[self.level-1]
        #통계
        self.total_gold = 0
        self.kill_zombie_count = 0

    def move(self):
        #키 입력에 따른 플레이어 이동
        keys = pg.key.get_pressed()
        if keys[K_d] and self.rect.right <= BG_WIDTH:#오른쪽
            self.vector.x += self.vel
        if keys[K_a] and self.rect.left >= 0:#왼쪽
            self.vector.x -= self.vel
        #점프 구현
        if keys[K_w]:
            if not self.jumping: #만약 jumping이 False라면
                self.jumping = True
                self.jump_pw = PLAYER_JUMP_PW
                self.jump_vel = self.jump_pw/2 * GRAVITY
        if self.jump_pw: #만약 jump_vel이 0이 아니라면
            self.vector.y -= self.jump_vel
            self.jump_vel -= GRAVITY
            self.jump_pw -= 1
            if not self.jump_pw: #만약 jump_vel이 0이라면
                self.jumping = False
                self.vector.y -= self.jump_vel

        self.rect.midbottom = self.vector

    def update(self):
        self.move()
        self.gold_counter += 1
        if self.gold_counter >= self.gold_cooldown:
            self.gold_counter = 0
            self.gold += self.gold_output
            self.total_gold += self.gold_output
        if self.hp <= 0:
            self.kill()

    def get_exp(self,exp):
        self.exp += exp
        if self.exp >= self.reqired_exp:
            self.exp -= self.reqired_exp
            self.level_up()
    def level_up(self):
        if self.level < self.max_level:
            self.level += 1
            self.reqired_exp = self.reqired_exp[self.level-1]

#인간
class Human(Player):
    def __init__(self):
        super().__init__()
        self.max_hp = HUMAN_HP
        self.hp = HUMAN_HP
        self.image = human_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.vector
        self.hp_bar = pg.Rect(0,0,10,self.rect.width)
        self.vel = HUMAN_VEL
        self.gold = HUMAN_START_GOLD
        self.gold_cooldown = HUMAN_GOLD_COOLDOWN
        self.gold_output = HUMAN_GOLD_OUTPUT
#마법사
class Wizard(Player):
    def __init__(self):
        super().__init__()
        self.max_hp = WIZARD_HP
        self.hp = WIZARD_HP
        self.image = wizard_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.vector
        self.hp_bar = pg.Rect(0,0,10,self.rect.width)
        self.vel = WIZARD_VEL
        self.gold = WIZARD_START_GOLD
        self.gold_cooldown = WIZARD_GOLD_COOLDOWN
        self.gold_output = WIZARD_GOLD_OUTPUT

#적
class Enemy(pg.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        enemy_sprites.add(self)
        creature_sprites.add(self)
        all_sprites.add(self)
        self.player = player
        self.max_hp = None
        self.hp = None
        self.damage = None
        self.img = None
        self.vector = pg.math.Vector2(0,516)
        self.rect = None
        self.shown_rect = None
        self.range_rect = None
        self.vel = None
        self.stop = 0
        self.attack_dmg = 0
        self.attack_cooldown = 0
        self.attack_counter = 0
        self.first_attack_cooldown = 0
        self.first_attack_counter = 0
        self.first_attack = 0
        self.status = None
        self.exp = 0
    def attack(self):
        attackable_list = attackable_sprites.sprites()
        index = self.range_rect.collidelist(attackable_list)
        if not index == -1:
            self.status = "attack"
            target = attackable_list[index]
            if not self.first_attack:
                self.first_attack_counter += 1
                if self.first_attack_counter >= self.first_attack_cooldown:
                    self.first_attack = 1
                    target.hp -= self.attack_dmg
            else:
                self.attack_counter += 1
                if self.attack_counter >= self.attack_cooldown:
                    self.attack_counter = 0
                    target.hp -= self.attack_dmg

        else:
            self.attack_counter = 0
            self.first_attack_counter = 0
            self.status = "move"

    def move(self):
        #플레이어를 향해 이동
        if player_sprites:
            if self.status == "attack":
                return
            if self.player.vector.x - self.vector.x > 0:
                self.vector.x += self.vel
                self.status = "move"
            elif self.player.vector.x - self.vector.x < 0:
                self.vector.x -= self.vel
                self.status = "move"

        self.rect.midbottom = self.vector
        self.range_rect.center = self.vector

    def update(self):
        self.attack()
        self.move()
        if self.hp <= 0:
            self.player.get_exp(self.exp)
            self.kill()
            self.hp_bar.kill()
            
        self.hp_bar.update(self)

        
#좀비
class Zombie(Enemy):
    def __init__(self,spawn_location,player):
        super().__init__(player)
        self.max_hp = ZOMBIE_HP
        self.hp = ZOMBIE_HP
        self.exp = ZOMBIE_EXP
        self.hp_bar_width = ZOMBIE_HP_BAR_WIDTH
        self.attack_dmg = ZOMBIE_DMG
        self.attack_cooldown = ZOMBIE_COOLDONW
        self.first_attack_cooldown = ZOMBIE_FIRST_COOLDOWN
        self.vel = ZOMBIE_VEL
        self.image = ZOMBIE_IMAGE
        self.rect = self.image.get_rect()
        self.range_rect = self.rect.inflate(2*ZOMBIE_RANGE,0)
        if spawn_location == "right":
            self.vector = pg.math.Vector2(BG_WIDTH,516)
            self.rect.midbottom = self.vector
            self.range_rect.center = self.vector
        elif spawn_location == "left":
            self.vector = pg.math.Vector2(0,516)
            self.rect.midbottom = self.vector
            self.range_rect.center = self.vector
        self.hp_bar = Hp_bar(self,self.hp_bar_width)
    def update(self):
        self.attack()
        self.move()
        if self.hp <= 0:
            self.player.get_exp(self.exp)
            self.kill()
            self.hp_bar.kill()
        self.hp_bar.update(self)
#건물
class Building(pg.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        building_sprites.add(self)
        attackable_sprites.add(self)
        all_sprites.add(self)
        self.player = player
        self.max_hp = None
        self.hp = None
        self.image = None
        self.image_red = None
        self.image_green = None
        self.rect = None
        self.shown_rect = None
        self.vector = None
        self.hp_var = None
        self.level = 1
        self.max_level = None
        self.price = None
        self.upgrade_price = None
        self.hp_bar_width = 100
    def update(self):
        if self.hp <= 0:
            self.kill()
            self.hp_bar.kill()
        self.hp_bar.update(self)


#장벽
class Wall(Building):
    def __init__(self,vector,player):
        super().__init__(player)
        wall_sprites.add(self)
        self.level = 1
        self.max_level = WALL_MAX_LEVEL
        self.price = WALL_PRICE[self.level-1]
        self.upgrade_price = WALL_PRICE[self.level]
        self.max_hp = WALL_HP[self.level-1]
        self.hp = WALL_HP[self.level-1]
        self.image = WALL_IMAGE
        self.outline_image = OUTLINE_WALL
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()
        self.vector = vector
        self.rect.midbottom = self.vector
        self.hp_bar_width = WALL_HP_BAR_WIDTH

        self.hp_bar = Hp_bar(self,self.hp_bar_width)

    def upgrade(self):
        if self.level < self.max_level:
            self.level += 1
            self.max_hp = WALL_HP[self.level-1]
            self.hp = WALL_HP[self.level-1]
            self.price = WALL_PRICE[self.level-1]
            if self.level == self.max_level:
                self.upgrade_price = None
            else:
                self.upgrade_price = WALL_PRICE[self.level]

#대포
class Canon(Building):
    def __init__(self,vector,player):
        super().__init__(player)
        canon_sprites.add(self)
        self.level = 1
        self.max_level = CANON_MAX_LEVEL
        self.max_hp = CANON_HP[self.level-1]
        self.hp = CANON_HP[self.level-1]
        self.attack_dmg = CANON_DMG[self.level-1]
        self.vector = vector
        if self.vector.x >= BG_WIDTH/2:
            self.image = CANON_IMAGE
            self.outline_image = OUTLINE_CANON
        else:
            self.image = CANON_IMAGE_L
            self.outline_image = OUTLINE_CANON_L
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()
        self.rect.midbottom = self.vector
        self.attack_cooldown = CANON_COOLDOWN
        self.attack_counter = 0
        self.first_attack_cooldown = CANON_FIRST_COOLDOWN
        self.first_attack_counter = 0
        self.first_attack = 0
        self.attack_range = CANON_RANGE
        self.price = CANON_PRICE[self.level-1]
        self.upgrade_price = CANON_PRICE[self.level]
        self.hp_bar_width = CANON_HP_BAR_WIDTH
        self.hp_bar = Hp_bar(self,self.hp_bar_width)
        
    def attack(self):
        #사거리 안에 있는 적
        enemy_in_range = [ sprite for sprite in enemy_sprites.sprites() \
                if abs(sprite.vector.x - self.vector.x) <= self.attack_range]

        if enemy_in_range:
            #사거리 안에 있는 적들 중 가장 가까운 적
            target = sorted(enemy_in_range,key = lambda sprite: abs(sprite.vector.x - self.vector.x))[0]
            if not self.first_attack:
                self.first_attack_counter +=1
                if self.first_attack_counter >=self.first_attack_cooldown:
                    self.first_attack = 1
                    if target.vector.x - self.vector.x >= 0:
                        self.image = CANON_IMAGE
                        self.outline_image = OUTLINE_CANON
                        CanonShot(self.attack_dmg,"right",self.vector)
                    elif target.vector.x - self.vector.x < 0:
                        self.image = CANON_IMAGE_L
                        self.outline_image = OUTLINE_CANON_L
                        CanonShot(self.attack_dmg,"left",self.vector)
            else:
                self.attack_counter += 1
                if self.attack_counter >= self.attack_cooldown:
                    self.attack_counter = 0
                    if target.vector.x - self.vector.x >= 0:
                        self.image = CANON_IMAGE
                        self.outline_image = OUTLINE_CANON
                        CanonShot(self.attack_dmg,"right",self.vector)
                    elif target.vector.x - self.vector.x < 0:
                        self.image = CANON_IMAGE_L
                        self.outline_image = OUTLINE_CANON_L
                        CanonShot(self.attack_dmg,"left",self.vector)
        else:
            self.first_attack_counter = 0
            self.attack_counter = 0
            self.first_attack = 0

        self.rect.midbottom = self.vector

    def upgrade(self):
        if self.level < self.max_level:
            self.level += 1
            self.max_hp = CANON_HP[self.level-1]
            self.hp = CANON_HP[self.level-1]
            self.price = CANON_PRICE[self.level-1]
            self.attack_dmg = CANON_DMG[self.level-1]
            if self.level == self.max_level:
                self.upgrade_price = None
            else:
                self.upgrade_price = CANON_PRICE[self.level]
    def update(self):
        self.attack()
        if self.hp <= 0:
            self.kill()
            self.hp_bar.kill()
        self.hp_bar.update(self)

#포탄
class CanonShot(pg.sprite.Sprite):
    def __init__(self,damage,direction,location):
        super().__init__()
        noncreature_sprites.add(self)
        all_sprites.add(self)
        self.vel = CANONSHOT_VEL
        self.attack_dmg = damage
        self.direction = direction
        self.image = CANONSHOT_IMAGE
        self.rect = self.image.get_rect()
        self.shown_rect = None
        self.vector = pg.math.Vector2(location.x,location.y-50)
        self.rect.midbottom = self.vector

    def attack(self):
        collided_sprite = pg.sprite.spritecollide(self,enemy_sprites,False)
        if collided_sprite:
                collided_sprite[0].hp -= self.attack_dmg
                self.kill()
        
    def move(self):
        if self.direction == "right":
            self.vector.x += self.vel
            if self.vector.x > BG_WIDTH:
                self.kill()

        elif self.direction == "left":
            self.vector.x -= self.vel
            if self.vector.x < 0:
                self.kill()
        self.rect.midbottom = self.vector

    def update(self):
        self.move()
        self.attack()

class Mortar(Building):
    def __init__(self,vector,player):
        super().__init__(player)
        self.max_hp = MORTAR_HP
        self.hp = MORTAR_HP
        self.damage = MORTAR_DMG
        self.vector = vector
        if self.vector.x >= BG_WIDTH/2:
            self.image = MORTAR_IMAGE
            self.outline_image = OUTLINE_MORTAR
        else:
            self.image = MORTAR_IMAGE_L
            self.outline_image = OUTLINE_MORTAR_L
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()

        self.rect.midbottom = self.vector
        self.attack_cooldown = CANON_COOLDOWN
        self.attack_counter = 0
        self.attack_range = CANON_RANGE
    def attack(self):
        pass
    def update(self):
        pass

class Mine(Building):
    def __init__(self,vector,player):
        super().__init__(player)
        mine_sprites.add(self)
        self.level = 1
        self.max_level = MINE_MAX_LEVEL
        self.max_hp = MINE_HP[self.level-1]
        self.hp = MINE_HP[self.level-1]
        self.image = MINE_IMAGE
        self.outline_image = outline_mine
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()
        self.vector = vector
        self.rect.midbottom = self.vector
        self.gold_output = MINE_GOLD_OUTPUT[self.level-1]
        self.gold_cooldown = MINE_GOLD_COOLDOWN
        self.mining_counter = 0
        self.price = MINE_PRICE[self.level-1]
        self.upgrade_price = MINE_PRICE[self.level]
        self.hp_bar_width = MINE_HP_BAR_WIDTH
        self.hp_bar = Hp_bar(self,self.hp_bar_width)
    
    def mining(self):
        self.mining_counter += 1
        if self.mining_counter >= self.gold_cooldown:
            self.player.gold += self.gold_output
            self.player.total_gold +=self.gold_output
            self.mining_counter = 0
            Earn_gold_effect(self)
            
    def upgrade(self):
        if self.level < self.max_level:
            self.level += 1
            self.max_hp = MINE_HP[self.level-1]
            self.hp = MINE_HP[self.level-1]
            self.price = MINE_PRICE[self.level-1]
            self.gold_output = MINE_GOLD_OUTPUT[self.level-1]
            if self.level == self.max_level:
                self.upgrade_price = None
            else:
                self.upgrade_price = MINE_PRICE[self.level]
    def update(self):
        if self.hp <= 0:
            self.kill()
            self.hp_bar.kill()
        self.mining()
        self.hp_bar.update(self)
        

#건물 및 적 체력(각 스프라이트에 종속되어 있음)
class Hp_bar(pg.sprite.Sprite):
    def __init__(self,sprite,width):
        super().__init__()
        hp_bar_sprites.add(self)
        self.max_hp = sprite.max_hp
        self.hp = sprite.hp
        self.width = width
        self.interval = 10
        self.vector = pg.math.Vector2(sprite.rect.centerx-self.width*(1-self.hp/self.max_hp)/2,sprite.rect.top-self.interval)
        self.rect = pg.Rect(0,0,self.width,10)
        self.rect.center = self.vector
        self.shown_rect = self.rect.copy()
    def update(self,sprite):
        self.hp = sprite.hp
        self.rect.width = self.width * self.hp / self.max_hp
        self.vector = pg.math.Vector2(sprite.rect.centerx-self.width*(1-self.hp/self.max_hp)/2,sprite.rect.top-self.interval)
        self.rect.center = self.vector

#이펙트
class Effect(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        all_sprites.add(self)
        effect_sprites.add(self)

#골드 획득 이펙트
class Earn_gold_effect(Effect):
    def __init__(self,sprite):
        super().__init__()
        self.vector = pg.math.Vector2(sprite.rect.midtop)
        self.images = EARN_GOLD_EFFECT_IMAGES
        self.image_counter = 0
        self.image_count = len(self.images)
        self.image_speed = EARN_GOLD_EFFECT_SPEED
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()
        self.vel = EARN_GOLD_EFFECT_VEL
        self.hold_time = EARN_GOLD_EFFECT_HOLD_TIME
        self.counter = 0
        self.rect.center = self.vector

    def update(self):
        self.counter += 1
        if self.counter >= self.hold_time:
            self.kill()
        self.vector.y += self.vel
        self.rect.center = self.vector
        if self.image_counter >= self.image_count-1:
            self.image_counter = 0
        else:
            self.image_counter += self.image_speed
        self.image = self.images[int(self.image_counter)]

class Message(pg.sprite.Sprite):
    def __init__(self,message,color):
        super().__init__()
        #메세지는 항상 1개만 출력
        if len(message_sprites) >= 1:
            message_sprites.sprites()[0].kill()
            self.add(message_sprites)
        else:
            self.add(message_sprites)
        self.message = message
        self.color = color
        self.vector = pg.math.Vector2(WIDTH/2,100)
        self.text = myfont.render(self.message,True,self.color)
        self.rect = self.text.get_rect()
        self.rect.center = self.vector
        self.cooldown = MESSAGE_COOLDOWN
        self.counter = 0
    
    def update(self):
        self.counter += 1
        if self.counter >= self.cooldown:
            self.kill()