import pygame as pg
from setting import *
from abc import *
#스프라이트 그룹
all_sprites = pg.sprite.Group()
noncreature_sprites = pg.sprite.Group()
creature_sprites = pg.sprite.Group()
player_sprites = pg.sprite.Group()
enemy_sprites = pg.sprite.Group()


#움직이는 모든 스프라이트(추상 클래스)
class Creature(pg.sprite.Sprite,metaclass=ABCMeta):
    def __init__(self):
        super().__init__()
        creature_sprites.add(self)
        all_sprites.add(self)
    @abstractmethod
    def move(self):
        pass
    @abstractmethod
    def update(self):
        pass

#플레이어 스프라이트(추상클래스)
class Player(Creature):
    def __init__(self):
        super().__init__()
        player_sprites.add(self)
        #플레이어 기본 변수 
        self.hp_max = 100
        self.hp = 100
        self.coin = 0
        self.vector = pg.math.Vector2(BG_WIDTH/2,768-140)
        self.image = None
        self.rect = None
        self.vel = None
        self.jumping = False
        self.jump_vel = 0
        self.jump_pw = 0
        
    def move(self):
        #키 입력에 따른 플레이어 이동
        keys = pg.key.get_pressed()
        if keys[pg.K_d] and self.rect.right <= BG_WIDTH:#오른쪽
            self.vector.x += self.vel
        if keys[pg.K_a] and self.rect.left >= 0:#왼쪽
            self.vector.x -= self.vel
        #점프 구현
        if keys[pg.K_w]:
            if not self.jumping: #만약 jumping이 False라면
                self.jumping = True
                self.jump_pw = PLAYER_JUMP_PW
                self.jump_vel = self.jump_pw/2 * GRAVITY
        if self.jump_pw: #만약 jump_vel이 0이 아니라면
            self.vector.y -= self.jump_vel
            self.jump_vel -= GRAVITY
            self.jump_pw -=1
            if not self.jump_pw: #만약 jump_vel이 0이라면
                self.jumping = False
                self.vector.y -= self.jump_vel

        self.rect.center = self.vector
    
    def build(self):
        pass
    def update(self):
        self.move()
        #if self.hp <=0:
        #    self.kill()
    

#인간 클래스 정의
class Human(Player):
    def __init__(self):
        super().__init__()
        self.hp_max = HUMAN_HP
        self.hp = HUMAN_HP
        self.image = human_img
        self.rect = self.image.get_rect()
        self.rect.center = self.vector
        self.vel = HUMAN_VEL
        self.unbeatable = False
#마법사 클래스 정의
class Wizard(Player):
    def __init__(self):
        super().__init__()
        self.hp_max = WIZARD_HP
        self.hp = WIZARD_HP
        self.image = wizard_img
        self.rect = self.image.get_rect()
        self.rect.center = self.vector
        self.vel = WIZARD_VEL

#플레이어를 공격하는 모든 적
class Enemy(Creature):
    def __init__(self):
        super().__init__()
        enemy_sprites.add(self)
        self.hp = None
        self.damage = None
        self.img = None
        self.vector = pg.math.Vector2(BG_WIDTH-10,768-140)
        self.rect = None
        self.vel = None
    def attack(self):
        collided_sprite = pg.sprite.spritecollide(self,player_sprites,False)
        for sprite in collided_sprite:
            sprite.hp -=10
    def move(self):
        #적과 가장 가까이 있는 플레이어를 타겟으로 한다.
        target = sorted(player_sprites.sprites(),key = lambda sprite: abs(sprite.vector.x - self.vector.x))[0]
        if target.vector.x - self.vector.x >0:
            self.vector.x += self.vel
        elif target.vector.x - self.vector.x <0:
            self.vector.x -= self.vel

        self.rect.center = self.vector
    def update(self):
        self.move()
        self.attack()

class Zombie(Enemy):
    def __init__(self):
        super().__init__()
        self.hp = ZOMBIE_HP
        self.damage = 10
        self.vel = ZOMBIE_VEL
        self.image = zombie_img
        self.rect = self.image.get_rect()
        self.rect.center = self.vector


#움직이지 않는 모든 스프라이트(추상 클래스)
class NonCreature(pg.sprite.Sprite,metaclass=ABCMeta):
    def __init__(self):
        super().__init__()
        self.image = None
        noncreature_sprites.add(self)
        all_sprites.add(self)
        
#바닥
class Floor(NonCreature):
    def __init__(self):
        super().__init__()





#플레이어 생성
human1 = Human()
#적 생성
zomebie1 = Zombie()