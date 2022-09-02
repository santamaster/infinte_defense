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

#플레이어
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        all_sprites.add(self)
        player_sprites.add(self)
        attackable_sprites.add(self)
        creature_sprites.add(self)
        #플레이어 기본 변수 
        self.hp_max = None
        self.hp = None
        self.vector = pg.math.Vector2(BG_WIDTH/2,768-140)
        self.image = None
        self.rect = None
        self.vel = None
        self.jumping = False
        self.jump_vel = 0
        self.jump_pw = 0
        self.gold = 0
        self.gold_cooldown = None
        self.gold_counter = 0

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

        self.rect.center = self.vector

    def update(self):
        self.move()
        self.gold_counter += 1
        if self.gold_counter >= self.gold_cooldown:
            self.gold_counter = 0
            self.gold += 1
        if self.hp <= 0:
            self.kill()

#인간
class Human(Player):
    def __init__(self):
        super().__init__()
        self.hp_max = HUMAN_HP
        self.hp = HUMAN_HP
        self.image = human_img
        self.rect = self.image.get_rect()
        self.rect.center = self.vector
        self.vel = HUMAN_VEL
        self.gold = HUMAN_START_GOLD
        self.gold_cooldown = HUMAN_GOLD_COOLDOWN
#마법사
class Wizard(Player):
    def __init__(self):
        super().__init__()
        self.hp_max = WIZARD_HP
        self.hp = WIZARD_HP
        self.image = wizard_img
        self.rect = self.image.get_rect()
        self.rect.center = self.vector
        self.vel = WIZARD_VEL
        self.gold = WIZARD_START_GOLD
        self.gold_cooldown = WIZARD_GOLD_COOLDOWN

#적
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy_sprites.add(self)
        creature_sprites.add(self)
        all_sprites.add(self)
        self.hp = None
        self.damage = None
        self.img = None
        self.vector = pg.math.Vector2(10,768 - 140)
        self.rect = None
        self.vel = None
        self.stop = 0
        self.attack_cooldown = None
        self.attack_counter = 0

    def attack(self):
        self.attack_counter += 1
        collided_sprites = pg.sprite.spritecollide(self,attackable_sprites,False)
        for sprite in collided_sprites:
            if self.attack_counter >= self.attack_cooldown:
                self.attack_counter = 0
                sprite.hp -=10
    
    def move(self):
        if pg.sprite.spritecollide(self,attackable_sprites,False):
            self.stop = 1
        else:
            self.stop = 0
        if not self.stop:
            #적과 가장 가까이 있는 플레이어를 타겟
            if player_sprites:
                target = sorted(player_sprites.sprites(),key = lambda sprite: abs(sprite.vector.x - self.vector.x))[0]
                if target.vector.x - self.vector.x > 0:
                    self.vector.x += self.vel
                elif target.vector.x - self.vector.x < 0:
                    self.vector.x -= self.vel
        self.rect.center = self.vector

    def update(self):
        self.move()
        self.attack()
        if self.hp <= 0:
            self.kill()

#좀비
class Zombie(Enemy):
    def __init__(self,spawn_location):
        super().__init__()
        self.hp = ZOMBIE_HP
        self.damage = 10
        self.vel = ZOMBIE_VEL
        self.image = zombie_img
        self.rect = self.image.get_rect()
        if spawn_location == "right":
            self.vector = pg.math.Vector2(BG_WIDTH-10,768 - 140)
        elif spawn_location == "left":
            self.vector = pg.math.Vector2(10,768-140)
        self.attack_cooldown = ZOMBIE_COOLDONW

#건물
class Building(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        building_sprites.add(self)
        attackable_sprites.add(self)
        all_sprites.add(self)
        self.hp = None
        self.image = None
        self.image_red = None
        self.image_green = None
        self.rect = None
        self.vector = None
    def update(self):
        if self.hp <= 0:
            self.kill()

#장벽
class Wall(Building):
    def __init__(self,vector):
        super().__init__()
        self.hp = WALL_HP
        self.image = wall_img
        self.rect = self.image.get_rect()
        self.vector = vector
        self.rect.center = self.vector

#대포
class Canon(Building):
    def __init__(self,vector):
        super().__init__()
        self.hp = CANON_HP
        self.dmg = CANON_DMG
        self.vector = vector
        if self.vector.x >= BG_WIDTH/2:
            self.image = canon_img
        else:
            self.image = canon_img_l
        self.rect = self.image.get_rect()
        self.rect.center = self.vector
        self.attack_cooldown = CANON_COOLDOWN
        self.attack_counter = 0
        self.attack_range = CANON_RANGE
    def attack(self):
        self.attack_counter += 1
        #사거리 안에 있는 적
        enemy_in_range = [ sprite for sprite in enemy_sprites.sprites() \
                if abs(sprite.vector.x - self.vector.x) <= self.attack_range]

        if enemy_in_range:
            #사거리 안에 있는 적들 중 가장 가까운 적
            target = sorted(enemy_in_range,key = lambda sprite: abs(sprite.vector.x - self.vector.x))[0]
            if self.attack_counter >= self.attack_cooldown:
                self.attack_counter = 0
                if target.vector.x - self.vector.x >= 0:
                    self.image = canon_img
                    CanonShot(self.dmg,"right",self.vector)
                elif target.vector.x - self.vector.x < 0:
                    self.image = canon_img_l
                    CanonShot(self.dmg,"left",self.vector)
            
        self.rect.center = self.vector

    def update(self):
        self.attack()
        if self.hp <= 0:
            self.kill()

#포탄
class CanonShot(pg.sprite.Sprite):
    def __init__(self,damage,direction,location):
        super().__init__()
        noncreature_sprites.add(self)
        all_sprites.add(self)
        self.vel = CANONSHOT_VEL
        self.dmg = damage
        self.direction = direction#1 = 오른쪽 -1 = 왼쪽
        self.image = canonshot_img
        self.rect = self.image.get_rect()
        self.vector = pg.math.Vector2(location.x,location.y)
        self.rect.center = self.vector

    def attack(self):
        collided_sprite = pg.sprite.spritecollide(self,enemy_sprites,False)
        if collided_sprite:
                collided_sprite[0].hp -= self.dmg
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
        self.rect.center = self.vector

    def update(self):
        self.move()
        self.attack()

class Mortar(Building):
    def __init__(self,vector):
        super().__init__()
        self.hp = MORTAR_HP
        self.damage = MORTAR_DMG
        self.vector = vector
        if self.vector.x >= BG_WIDTH/2:
            self.image = mortar_img
        else:
            self.image = mortar_img_l
        self.rect = self.image.get_rect()
        self.rect.center = self.vector
        self.attack_cooldown = CANON_COOLDOWN
        self.attack_counter = 0
        self.attack_range = CANON_RANGE
    def attack(self):
        pass
class Mine(Building):
    def __init__(self,player,vector):
        super().__init__()
        self.hp = MINE_HP
        self.gold_output = MINE_GOLD_OUTPUT
        self.gold_cooldown = MINE_GOLD_COOLDOWN
        self.mining_counter = 0
        self.player = player
        self.image = mine_img
        self.rect = self.image.get_rect()
        self.vector = vector
        self.rect.center = self.vector
    def mining(self):
        self.mining_counter +=1
        if self.mining_counter >= self.gold_cooldown:
            self.player.gold += self.gold_output
            self.mining_counter = 0
            
    def update(self):
        if self.hp <= 0:
            self.kill()
        self.mining()
        


# #바닥
# class Floor(pg.sprite.Sprite):
#     def __init__(self):
#         super().__init__()






#플레이어 생성
