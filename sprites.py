import pygame as pg
from pygame.locals import *
from setting import *
from random import random,randint
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
mortar_sprites = pg.sprite.Group()
fireball_thrower_sprites = pg.sprite.Group()
#게임 플레이에 영향을 미치지 않는 스프라이트 그룹
effect_sprites = pg.sprite.Group()
message_sprites = pg.sprite.Group()
hp_bar_sprites = pg.sprite.Group()

#플레이어
class Player(pg.sprite.Sprite): 
    max_level = 6
    hp = 1000
    vel = 10
    required_exp = [20,200,400,600,1000]
    gold_cooldown = 1* FPS
    gold_output = 3
    start_gold = 1000
    total_gold = start_gold
    total_killed_enemy = 0
    def __init__(self):
        super().__init__()
        all_sprites.add(self)
        player_sprites.add(self)
        attackable_sprites.add(self)
        creature_sprites.add(self)
        #플레이어 기본 변수 
        self.max_hp = Player.hp
        self.hp = Player.hp
        self.vector = pg.math.Vector2(BG_WIDTH/2,516)
        self.images = PLAYER_IMAGES
        self.images_l = PLAYER_IMAGES_L
        self.image_counter = 0
        self.image_count = len(self.images)
        self.image_speed = PLAYER_IMAGE_SPEED
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()
        self.vel = Player.vel
        self.hp_bar = pg.Rect(0,0,10,self.rect.width)
        self.jumping = False
        self.jump_vel = 0
        self.jump_pw = 0
        self.gold = Player.start_gold
        self.gold_output = Player.gold_output
        self.gold_cooldown = Player.gold_cooldown
        self.gold_counter = 0
        self.level = 1
        self.exp = 0
        self.reqired_exp = Player.required_exp[self.level-1]
        self.direction = "right"
    def move(self):
        #키 입력에 따른 플레이어 이동
        keys = pg.key.get_pressed()
        if keys[K_d] and self.rect.right <= BG_WIDTH:#오른쪽
            self.vector.x += self.vel
            if self.image_counter >= self.image_count-1:
                self.image_counter = 0
            else:
                self.image_counter +=self.image_speed
                self.image = self.images[int(self.image_counter)]
            self.direction = "right"
        elif keys[K_a] and self.rect.left >= 0:#왼쪽
            self.vector.x -= self.vel
            if self.image_counter >= self.image_count-1:
                self.image_counter = 0
            else:
                self.image_counter +=self.image_speed
                self.image = self.images_l[int(self.image_counter)]
            self.direction = "left"
        else:
            self.image_counter = 0
            if self.direction == "right":
                self.image = PLAYER_IMAGE
            elif self.direction =="left":
                self.image = PLAYER_IMAGE_L
        #점프 구현
        if keys[K_w]:
            if not self.jumping: #만약 jumping이 False라면
                JUMP_SOUND.play()
                self.jumping = True
                self.jump_pw = PLAYER_JUMP_PW
                self.jump_vel = self.jump_pw/2 * GRAVITY
            if self.direction == "right":
                self.image = PLAYER_IMAGE
            elif self.direction == "left":
                self.image = PLAYER_IMAGE_L
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
            Player.total_gold += self.gold_output
            self.gold += self.gold_output
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
            self.reqired_exp = Player.required_exp[self.level-1]


#적
class Enemy(pg.sprite.Sprite):
    damage_rate = 1
    get_gold = 0
    damaged_by_wall = 0
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
        self.status = "move"
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
                    target.hp -= self.attack_dmg * Enemy.damage_rate
                    if Enemy.damaged_by_wall:
                        if target in wall_sprites:
                            self.hp -= 10
            else:
                self.attack_counter += 1
                if self.attack_counter >= self.attack_cooldown:
                    self.attack_counter = 0
                    target.hp -= self.attack_dmg * Enemy.damage_rate
                    if Enemy.damaged_by_wall:
                        if target in wall_sprites:
                            self.hp -= 10
            if target.vector.x - self.vector.x > 0:
                self.image = ZOMBIE_IMAGE
            else:
                self.image = ZOMBIE_IMAGE_L
        else:
            self.attack_counter = 0
            self.first_attack_counter = 0
            self.status = "move"

    def move(self):
        #플레이어를 향해 이동
        if player_sprites:
            if self.status == "attack":
                return
            if self.image_counter >= self.image_count-1:
                    self.image_counter = 0
            else:
                self.image_counter += self.image_speed    

            if self.player.vector.x - self.vector.x > 0:
                self.vector.x += self.vel
                self.image = self.images[int(self.image_counter)]
                self.status = "move"

            elif self.player.vector.x - self.vector.x < 0:
                self.vector.x -= self.vel
                self.image = self.images_l[int(self.image_counter)]
                self.status = "move"

        self.rect.midbottom = self.vector
        self.range_rect.center = self.vector

    def update(self):
        self.move()
        self.attack()
        if self.hp <= 0:
            if Enemy.get_gold:
                self.player.gold +=15
                Player.total_gold +=15
                Earn_gold_effect(self)
            self.player.get_exp(self.exp)
            ENEMY_DEAD_SOUND.play()
            self.kill()
            Player.total_killed_enemy += 1

        
#좀비
class Zombie(Enemy):
    hp = [90,120,150]
    attack_dmg = [20,30,40]
    exp = [20,40,60]
    attack_cooldown = 1 * FPS
    first_attack_cooldown = 0.1*FPS
    attack_range = 50
    hp_bar_width = 70
    max_level = 3
    vel = 4
    def __init__(self,spawn_location,player,level=1):
        super().__init__(player)
        self.level = level
        self.max_hp = Zombie.hp[self.level-1]
        self.hp = Zombie.hp[self.level-1]
        self.exp = Zombie.exp[self.level-1]
        self.hp_bar_width = Zombie.hp_bar_width
        self.attack_dmg = Zombie.attack_dmg[self.level-1]
        self.attack_cooldown = Zombie.attack_cooldown
        self.first_attack_cooldown = Zombie.first_attack_cooldown
        self.vel = Zombie.vel
        self.images = ZOMBIE_IMAGES
        self.images_l = ZOMBIE_IMAGES_L
        self.image_counter = 0
        self.image_count = len(self.images)
        self.image_speed = ZOMBIE_IMAGE_SPEED

        if spawn_location == "right":
            self.image = ZOMBIE_IMAGE_L    
            self.rect = self.image.get_rect()
            self.range_rect = self.rect.inflate(2*Zombie.attack_range,0)
            self.vector = pg.math.Vector2(BG_WIDTH,516)
            self.rect.midbottom = self.vector
            self.range_rect.center = self.vector
        elif spawn_location == "left":
            self.image = ZOMBIE_IMAGE
            self.rect = self.image.get_rect()
            self.range_rect = self.rect.inflate(2*Zombie.attack_range,0)
            self.vector = pg.math.Vector2(0,516)
            self.rect.midbottom = self.vector
            self.range_rect.center = self.vector
        self.hp_bar = Hp_bar(self,Zombie.hp_bar_width)

class Skeleton(Enemy):
    hp = [60,80,100]
    attack_dmg = [50,70,100]
    exp = [20,40,60]
    attack_cooldown = 1 * FPS
    first_attack_cooldown = 0.1*FPS
    attack_range = 400
    hp_bar_width = 70
    max_level = 3
    vel = 6
    def __init__(self,spawn_location,player,level=1):
        super().__init__(player)
        self.level = level
        self.max_hp = Skeleton.hp[self.level-1]
        self.hp = Skeleton.hp[self.level-1]
        self.exp = Skeleton.exp[self.level-1]
        self.hp_bar_width = Skeleton.hp_bar_width
        self.attack_dmg = Skeleton.attack_dmg[self.level-1]
        self.attack_cooldown = Skeleton.attack_cooldown
        self.first_attack_cooldown = Skeleton.first_attack_cooldown
        self.vel = Skeleton.vel
        self.images = SKELETON_IMAGES
        self.images_l = SKELETON_IMAGES_L
        self.image_counter = 0
        self.image_count = len(self.images)
        self.image_speed = SKELETON_IMAGE_SPEED
    
        if spawn_location == "right":
            self.image = SKELETON_IMAGE_L
            self.rect = self.image.get_rect()
            self.range_rect = self.rect.inflate(2*Skeleton.attack_range,0)
            self.vector = pg.math.Vector2(BG_WIDTH,516)
            self.rect.midbottom = self.vector
            self.range_rect.center = self.vector
        elif spawn_location == "left":
            self.image = SKELETON_IMAGE
            self.rect = self.image.get_rect()
            self.range_rect = self.rect.inflate(2*Skeleton.attack_range,0)
            self.vector = pg.math.Vector2(0,516)
            self.rect.midbottom = self.vector
            self.range_rect.center = self.vector
        self.hp_bar = Hp_bar(self,Skeleton.hp_bar_width)
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
                    Arrow((self.vector.x,self.vector.y-50),target.vector,self.attack_dmg)
                    if Enemy.damaged_by_wall:
                        if target in wall_sprites:
                            self.hp -= 10
            else:
                self.attack_counter += 1
                if self.attack_counter >= self.attack_cooldown:
                    self.attack_counter = 0
                    Arrow((self.vector.x,self.vector.y-50),target.vector,self.attack_dmg)
                    if Enemy.damaged_by_wall:
                        if target in wall_sprites:
                            self.hp -= 10
            if target.vector.x - self.vector.x > 0:
                self.image = SKELETON_IMAGE
            else:
                self.image = SKELETON_IMAGE_L
        else:
            self.attack_counter = 0
            self.first_attack_counter = 0
            self.status = "move"

class Arrow(pg.sprite.Sprite):
    vel = 15
    power = 1
    def __init__(self,start_point,end_point,damage):
        super().__init__()
        all_sprites.add(self)
        noncreature_sprites.add(self)
        self.start_point = pg.math.Vector2(start_point)
        self.vector = pg.math.Vector2(start_point)
        self.end_point = pg.math.Vector2(end_point)
        self.attack_dmg = damage
        self.time = abs((self.end_point.x-self.start_point.x)/Arrow.vel)
        if self.end_point.x-self.start_point.x >= 0:
            self.delta_x = Arrow.vel
            self.image = SKELETON_ARROW_IMAGE
        else:
            self.delta_x = -Arrow.vel
            self.image = SKELETON_ARROW_IMAGE_L
        self.delta_y = Arrow.power
        self.delta_square_y = Arrow.power/(MortarShot.time/2)
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()
        ARROW_SOUND.play()
    def attack(self):
        collided_sprite = pg.sprite.spritecollide(self,attackable_sprites,False)
        if collided_sprite:
            collided_sprite[0].hp -= self.attack_dmg
            self.kill()
    def move(self):
        self.vector.x += self.delta_x
        self.vector.y -= self.delta_y
        self.delta_y -=self.delta_square_y
        self.rect.midbottom = self.vector
        if self.vector.y >= 516:
            self.kill()
    def update(self):
        self.move()
        self.attack()
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


#장벽
class Wall(Building):
    price = [250,300,400]
    hp = [1000,1500,2000]
    max_level = 3
    hp_bar_width = 100
    self_healing = 0
    heal_cooldown = 1*FPS
    def __init__(self,vector,player):
        super().__init__(player)
        wall_sprites.add(self)
        self.level = 1
        self.max_level = Wall.max_level
        self.price = Wall.price[self.level-1]
        self.upgrade_price = Wall.price[self.level]
        self.max_hp = Wall.hp[self.level-1]
        self.hp = Wall.hp[self.level-1]
        self.image = WALL_IMAGE
        self.outline_image = OUTLINE_WALL
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()
        self.vector = vector
        self.rect.midbottom = self.vector
        self.hp_bar_width = Wall.hp_bar_width
        self.hp_bar = Hp_bar(self,Wall.hp_bar_width)
        self.heal_counter = 0
    def upgrade(self):
        if self.level < self.max_level:
            self.level += 1
            self.max_hp = Wall.hp[self.level-1]
            self.hp = Wall.hp[self.level-1]
            self.price = Wall.price[self.level-1]
            if self.level == self.max_level:
                self.upgrade_price = None
            else:
                self.upgrade_price = Wall.price[self.level]

    def self_heal(self):
        self.heal_counter += 1
        if self.heal_counter >= Wall.heal_cooldown:
            self.hp += self.max_hp * 0.02
            if self.hp >= self.max_hp:
                self.hp = self.max_hp
            self.heal_counter = 0
    def update(self):
        if self.hp <= 0:
            self.kill()
        if Wall.self_healing:
            self.self_heal()

#대포
class Canon(Building):
    price = [300,400,500]
    hp = [500,700,1000]
    attack_dmg = [30,50,70]
    max_level = 3
    first_attack_cooldown = 0.5 * FPS
    attack_cooldown = 1 * FPS
    attack_range = 800
    damage_rate = 1
    enhanced_attack_chance = 0
    enhanced_attack_damage = 2
    hp_bar_width = 150
    double_barrel = 0
    double_barrel_interval = 0.1 * FPS
    def __init__(self,vector,player):
        super().__init__(player)
        canon_sprites.add(self)
        self.level = 1
        self.max_level = Canon.max_level
        self.max_hp = Canon.hp[self.level-1]
        self.hp = Canon.hp[self.level-1]
        self.attack_dmg = Canon.attack_dmg[self.level-1]
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
        self.attack_counter = 0
        self.first_attack_counter = 0
        self.first_attack = 0
        self.double_barrel = 0
        self.double_barrel_counter = 0
        self.price = Canon.price[self.level-1]
        self.upgrade_price = Canon.price[self.level]
        self.hp_bar = Hp_bar(self,Canon.hp_bar_width)
        self.total_damage_rate = 1
        self.target_direction = ""
    def attack(self):
        #사거리 안에 있는 적
        enemy_in_range = [ sprite for sprite in enemy_sprites.sprites() \
                if abs(sprite.vector.x - self.vector.x) <= Canon.attack_range]

        if enemy_in_range:
            self.total_damage_rate = Canon.damage_rate
            if Canon.enhanced_attack_chance >= random():
                self.total_damage_rate *= Canon.enhanced_attack_damage

            #사거리 안에 있는 적들 중 가장 가까운 적
            target = sorted(enemy_in_range,key = lambda sprite: abs(sprite.vector.x - self.vector.x))[0]
            if target.vector.x - self.vector.x >=0:
                self.target_direction = "right"
                self.image = CANON_IMAGE
                self.outline_image = OUTLINE_CANON
            else:
                self.target_direction = "left"
                self.image = CANON_IMAGE_L
                self.outline_image = OUTLINE_CANON_L

            if not self.first_attack:
                self.first_attack_counter +=1
                if self.first_attack_counter >=Canon.first_attack_cooldown:
                    self.first_attack = 1
                    CanonShot(self.attack_dmg*self.total_damage_rate,self.target_direction,self.vector)
                    self.double_barrel = 1
            else:
                self.attack_counter += 1
                if self.attack_counter >= Canon.attack_cooldown:
                    self.attack_counter = 0
                    CanonShot(self.attack_dmg*self.total_damage_rate,self.target_direction,self.vector)
                    self.double_barrel = 1
            

        else:
            self.first_attack_counter = 0
            self.attack_counter = 0
            self.first_attack = 0
        if Canon.double_barrel:
            if self.double_barrel:
                self.double_barrel_counter += 1
                if self.double_barrel_counter >= Canon.double_barrel_interval:
                    CanonShot(self.attack_dmg*self.total_damage_rate,self.target_direction,self.vector)
                    self.double_barrel_counter = 0
                    self.double_barrel = 0
            

    def upgrade(self):
        if self.level < Canon.max_level:
            self.level += 1
            self.max_hp = Canon.hp[self.level-1]
            self.hp = Canon.hp[self.level-1]
            self.price = Canon.price[self.level-1]
            self.attack_dmg = Canon.attack_dmg[self.level-1]
            if self.level == Canon.max_level:
                self.upgrade_price = None
            else:
                self.upgrade_price = Canon.price[self.level]
    def update(self):
        self.attack()
        if self.hp <= 0:
            self.kill()
        self.rect.midbottom = self.vector

#포탄
class CanonShot(pg.sprite.Sprite):
    vel = 30
    def __init__(self,damage,direction,location):
        super().__init__()
        noncreature_sprites.add(self)
        all_sprites.add(self)
        self.attack_dmg = damage
        self.direction = direction
        self.image = CANONSHOT_IMAGE
        self.rect = self.image.get_rect()
        self.shown_rect = None
        self.vector = pg.math.Vector2(location.x,location.y-50)
        self.rect.midbottom = self.vector
        CANONSHOT_SOUND.play()
    def attack(self):
        collided_sprite = pg.sprite.spritecollide(self,enemy_sprites,False)
        if collided_sprite:
                collided_sprite[0].hp -= self.attack_dmg
                self.kill()
        
    def move(self):
        if self.direction == "right":
            self.vector.x += CanonShot.vel
            if self.vector.x > BG_WIDTH:
                self.kill()

        elif self.direction == "left":
            self.vector.x -= CanonShot.vel
            if self.vector.x < 0:
                self.kill()
        self.rect.midbottom = self.vector

    def update(self):
        self.move()
        self.attack()

class Mortar(Building):
    attack_range = 1200
    least_attack_range = 300
    first_attack_cooldown = 1*FPS
    attack_cooldown = 3*FPS
    first_attack_cooldown_reduction = 1
    attack_cooldown_reduction = 1
    price = [400,600,700]
    hp = [500,600,700]
    attack_dmg = [100,150,200]
    hp_bar_width = 100
    max_level = 3
    power = 30
    lavashot = 0
    damage_rate = 1
    def __init__(self,vector,player):
        super().__init__(player)
        mortar_sprites.add(self)
        self.level = 1
        self.max_level = Mortar.max_level
        self.max_hp = Mortar.hp[self.level-1]
        self.hp = Mortar.hp[self.level-1]
        self.attack_dmg = Mortar.attack_dmg[self.level-1]
        self.vector = vector
        self.image = MORTAR_IMAGE
        self.outline_image = OUTLINE_MORTAR
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()
        self.rect.midbottom = self.vector
        self.attack_counter = 0
        self.first_attack_counter = 0
        self.first_attack = 0
        self.price = Mortar.price[self.level-1]
        self.upgrade_price = Mortar.price[self.level]
        self.hp_bar = Hp_bar(self,Mortar.hp_bar_width)

    def attack(self):
        #사거리 안에 있는 적
        enemy_in_range = [ sprite for sprite in enemy_sprites.sprites() \
                if Mortar.least_attack_range < abs(sprite.vector.x - self.vector.x) < Mortar.attack_range]

        if enemy_in_range:
            #사거리 안에 있는 적들 중 가장 가까운 적
            target = sorted(enemy_in_range,key = lambda sprite: abs(sprite.vector.x - self.vector.x))[0]
            if not self.first_attack:
                self.first_attack_counter +=1
                if self.first_attack_counter >= Mortar.first_attack_cooldown* Mortar.first_attack_cooldown_reduction:
                    self.first_attack = 1
                    MortarShot(self.attack_dmg*Mortar.damage_rate,self.vector,target.vector,Mortar.power,Mortar.lavashot)
            else:
                self.attack_counter += 1
                if self.attack_counter >= Mortar.attack_cooldown* Mortar.attack_cooldown_reduction:
                    self.attack_counter = 0
                    MortarShot(self.attack_dmg*Mortar.damage_rate,self.vector,target.vector,Mortar.power,Mortar.lavashot)

        else:
            self.first_attack_counter = 0
            self.attack_counter = 0
            self.first_attack = 0
    
    def upgrade(self):
        if self.level < Mortar.max_level:
            self.level += 1
            self.max_hp = Mortar.hp[self.level-1]
            self.hp = Mortar.hp[self.level-1]
            self.price = Mortar.price[self.level-1]
            self.attack_dmg = Mortar.attack_dmg[self.level-1]
            if self.level == Mortar.max_level:
                self.upgrade_price = None
            else:
                self.upgrade_price = Mortar.price[self.level]
    def update(self):
        self.attack()
        if self.hp <= 0:
            self.kill()

class MortarShot(pg.sprite.Sprite):
    time = 1*FPS
    def __init__(self,damage,start_point,end_point,power,lavashot):
        super().__init__()
        all_sprites.add(self)
        noncreature_sprites.add(self)
        self.vector = pg.math.Vector2(start_point)
        self.start_point = pg.math.Vector2(start_point)
        self.end_point = pg.math.Vector2(end_point)
        self.attack_dmg = damage        
        self.image = MORTARSHOT_IMAGE
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.vector
        self.shown_rect = self.rect.copy()
        self.power = power
        self.delta_x = (self.end_point.x-self.start_point.x)/MortarShot.time
        self.delta_y = self.power
        self.delta_square_y = self.power/(MortarShot.time/2)
        self.lavashot = lavashot
        MORTARSHOT_BOM_SOUND.play()
    def attack(self):
        if self.vector.y > 516:
            MORTARSHOT_END_SOUND.play()
            collided_sprite = pg.sprite.spritecollide(self,enemy_sprites,False)
            if collided_sprite:
                for sprite in collided_sprite:
                    sprite.hp -= self.attack_dmg
            if self.lavashot:
                FireZone((self.vector.x,516),8,3*FPS)
            self.kill()
    def move(self):
        self.vector.x += self.delta_x
        self.vector.y -= self.delta_y
        self.delta_y -=self.delta_square_y
        self.rect.midbottom = self.vector

    def update(self):
        self.move()
        self.attack()

#화염 지대
class FireZone(pg.sprite.Sprite):
    def __init__(self,vector,damage,duration):
        super().__init__()
        all_sprites.add(self)
        noncreature_sprites.add(self)
        self.attack_dmg = damage
        self.vector = pg.math.Vector2(vector)
        self.images = FIRE_IMAGES
        self.image_counter = 0
        self.image_count = len(self.images)
        self.image_speed = FIRE_IMAGE_SPEED
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()
        self.rect.midbottom = self.vector
        self.damage_interval = 0.2*FPS
        self.interval_counter = 0
        self.duration = duration
        self.duration_counter = 0
    def attack(self):
        self.interval_counter += 1
        if self.interval_counter >= self.damage_interval:
            collided_sprite = pg.sprite.spritecollide(self,enemy_sprites,False)
            if collided_sprite:
                for sprite in collided_sprite:
                    sprite.hp -= self.attack_dmg
            self.interval_counter = 0
    def update(self):
        self.attack()
        self.duration_counter += 1
        if self.duration_counter >= self.duration:
            self.kill()
        self.rect.midbottom = self.vector
        if self.image_counter >=self.image_count-1:
            self.image_counter = 0
        else:
            self.image_counter += self.image_speed
        self.image = self.images[int(self.image_counter)]

#화염구 투척기
class FireballThrower(Building):
    hp = [400,500,600]
    max_level = 3
    price = [400,500,600]
    attack_dmg = [4,6,10]
    hp_bar_width = 150
    attack_range = 600
    first_attack_cooldown = 0.01*FPS
    attack_cooldown = 0.1*FPS
    damage_rate = 1
    ball_height = (30,50)
    def __init__(self,vector,player):
        super().__init__(player)
        fireball_thrower_sprites.add(self)
        self.level = 1
        self.max_level = FireballThrower.max_level
        self.max_hp = FireballThrower.hp[self.level-1]
        self.hp = FireballThrower.hp[self.level-1]
        self.attack_dmg = FireballThrower.attack_dmg[self.level-1]
        self.vector = vector
        if self.vector.x >= BG_WIDTH/2:
            self.image = FIREBALL_THROWER_IMAGE
            self.outline_image = OUTLINE_FIREBALL_THROWER
        else:
            self.image = FIREBALL_THROWER_IMAGE_L
            self.outline_image = OUTLINE_FIREBALL_THROWER_L
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()
        self.rect.midbottom = self.vector
        self.attack_counter = 0
        self.first_attack_counter = 0
        self.first_attack = 0
        self.price = FireballThrower.price[self.level-1]
        self.upgrade_price = FireballThrower.price[self.level]
        self.hp_bar = Hp_bar(self,FireballThrower.hp_bar_width)
        self.index = 0
    def attack(self):
        #사거리 안에 있는 적
        enemy_in_range = [ sprite for sprite in enemy_sprites.sprites() \
                if abs(sprite.vector.x - self.vector.x) < FireballThrower.attack_range]

        if enemy_in_range:
            #사거리 안에 있는 적들 중 가장 가까운 적
            target = sorted(enemy_in_range,key = lambda sprite: abs(sprite.vector.x - self.vector.x))[0]
            if target.vector.x - self.vector.x >=0:
                self.image = FIREBALL_THROWER_IMAGE
                self.outline_image = OUTLINE_FIREBALL_THROWER
            else:
                self.image = FIREBALL_THROWER_IMAGE_L
                self.outline_image = OUTLINE_FIREBALL_THROWER_L
            if not self.first_attack:
                self.first_attack_counter +=1
                if self.first_attack_counter >= FireballThrower.first_attack_cooldown:
                    self.first_attack = 1
                    Fireball(self.attack_dmg*FireballThrower.damage_rate,self.vector,target.vector,FireballThrower.ball_height[self.index])
                    if self.index == 0:
                        self.index = 1
                    else:
                        self.index = 0
            else:
                self.attack_counter += 1
                if self.attack_counter >= FireballThrower.attack_cooldown:
                    self.attack_counter = 0
                    Fireball(self.attack_dmg*FireballThrower.damage_rate,self.vector,target.vector,FireballThrower.ball_height[self.index])
                    if self.index == 0:
                        self.index = 1
                    else:
                        self.index = 0

        else:
            self.first_attack_counter = 0
            self.attack_counter = 0
            self.first_attack = 0
        
    
    def upgrade(self):
        if self.level < FireballThrower.max_level:
            self.level += 1
            self.max_hp = FireballThrower.hp[self.level-1]
            self.hp = FireballThrower.hp[self.level-1]
            self.price = FireballThrower.price[self.level-1]
            self.attack_dmg = FireballThrower.attack_dmg[self.level-1]
            if self.level == FireballThrower.max_level:
                self.upgrade_price = None
            else:
                self.upgrade_price = FireballThrower.price[self.level]
    def update(self):
        self.attack()
        if self.hp <= 0:
            self.kill()


class Fireball(pg.sprite.Sprite):
    time = 0.3*FPS
    def __init__(self,damage,start_point,end_point,ball_height):
        super().__init__()
        all_sprites.add(self)
        noncreature_sprites.add(self)
        self.vector = pg.math.Vector2(start_point)
        self.vector.y -= ball_height
        self.start_point = pg.math.Vector2(start_point)
        self.end_point = pg.math.Vector2(end_point)
        self.attack_dmg = damage        
        self.image = FIREBALL_IMAGE
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.vector
        self.shown_rect = self.rect.copy()
        self.delta_x = (self.end_point.x-self.start_point.x)/Fireball.time
        self.delta_y = -ball_height/Fireball.time
        FIREBALL_SOUND.play()
        if self.delta_x >= 0:
            self.vector.x += 60
        else:
            self.vector.x -= 60

    def attack(self):
        if self.vector.y > self.start_point.y:
            collided_sprite = pg.sprite.spritecollide(self,enemy_sprites,False)
            if collided_sprite:
                for sprite in collided_sprite:
                    sprite.hp -= self.attack_dmg
            self.kill()
    def move(self):
        self.vector.x += self.delta_x
        self.vector.y -= self.delta_y
        self.rect.midbottom = self.vector

    def update(self):
        self.move()
        self.attack()

#광산
class Mine(Building):
    hp = [300,400,600]
    max_level = 3
    price = [200,350,500]
    gold_output = [15,25,35]
    gold_cooldown = 2 * FPS
    gold_cooldown_rate = 1
    hp_bar_width = 150
    def __init__(self,vector,player):
        super().__init__(player)
        mine_sprites.add(self)
        self.level = 1
        self.max_level = Mine.max_level
        self.max_hp = Mine.hp[self.level-1]
        self.hp = Mine.hp[self.level-1]
        self.image = MINE_IMAGE
        self.outline_image = OUTLINE_MINE
        self.rect = self.image.get_rect()
        self.shown_rect = self.rect.copy()
        self.vector = vector
        self.rect.midbottom = self.vector
        self.gold_cooldown = Mine.gold_cooldown
        self.gold_output = Mine.gold_output[self.level-1]
        self.mining_counter = 0
        self.price = Mine.price[self.level-1]
        self.upgrade_price = Mine.price[self.level]
        self.hp_bar = Hp_bar(self,Mine.hp_bar_width)
    
    def mining(self):
        self.mining_counter += 1
        if self.mining_counter >= self.gold_cooldown*Mine.gold_cooldown_rate:
            self.player.gold += self.gold_output
            Player.total_gold += self.gold_output
            self.mining_counter = 0
            Earn_gold_effect(self)
            
    def upgrade(self):
        if self.level < Mine.max_level:
            self.level += 1
            self.max_hp = Mine.hp[self.level-1]
            self.hp = Mine.hp[self.level-1]
            self.price = Mine.price[self.level-1]
            self.gold_output = Mine.gold_output[self.level-1]
            if self.level == Mine.max_level:
                self.upgrade_price = None
            else:
                self.upgrade_price = Mine.price[self.level]
    def update(self):
        if self.hp <= 0:
            self.kill()
        self.mining()



#건물 및 적 체력(각 스프라이트에 종속되어 있음)
class Hp_bar(pg.sprite.Sprite):
    def __init__(self,sprite,width):
        super().__init__()
        hp_bar_sprites.add(self)
        self.sprite = sprite
        self.max_hp = sprite.max_hp
        self.hp = sprite.hp
        self.width = width
        self.interval = 10
        self.vector = pg.math.Vector2(sprite.rect.centerx-self.width*(1-self.hp/self.max_hp)/2,sprite.rect.top-self.interval)
        self.rect = pg.Rect(0,0,self.width,10)
        self.rect.center = self.vector
        self.shown_rect = self.rect.copy()
    def update(self):
        self.hp = self.sprite.hp
        self.max_hp = self.sprite.max_hp
        self.rect.width = self.width * self.hp / self.max_hp
        self.vector = pg.math.Vector2(self.sprite.rect.centerx-self.width*(1-self.hp/self.max_hp)/2,self.sprite.rect.top-self.interval)
        self.rect.center = self.vector
        #스프라이트가 죽으면 삭제
        if not self.sprite.alive():
            self.kill()

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
        COIN_SOUND.play()

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
    def __init__(self,message,color=WHITE):
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
        self.text = MYFONT.render(self.message,True,self.color)
        self.rect = self.text.get_rect()
        self.rect.center = self.vector
        self.cooldown = MESSAGE_COOLDOWN
        self.counter = 0
    
    def update(self):
        self.counter += 1
        if self.counter >= self.cooldown:
            self.kill()

