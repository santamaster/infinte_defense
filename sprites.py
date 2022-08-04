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
        self.vector = None
        self.image = None
        self.rect = None
        self.vel = None
        creature_sprites.add(self)
        all_sprites.add(self)
    @abstractmethod
    def move(self):
        pass
    @abstractmethod
    def update(self):
        pass

#플레이어 스프라이트(추상클래스)
class Player(Creature,metaclass=ABCMeta):
    def __init__(self):
        super().__init__()
        self.hp = None
        self.coin = None
        player_sprites.add(self)
        #all_sprites.add(self)
    @abstractmethod
    def build(self):
        pass
    

#인간 클래스 정의
class Human(Player):
    def __init__(self):
        super().__init__()
        self.hp = 100
        self.vector = pg.math.Vector2(WIDTH/2,768-140)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = self.vector
        self.vel = PLAYER_VEL
        self.jumping = False
        self.jump_vel = 0
        self.jump_tick = 0
        #all_sprites.add(self)

    def move(self):
        #키 입력에 따른 플레이어 이동
        keys = pg.key.get_pressed()
        if keys[pg.K_d] and self.rect.right <= WIDTH:#오른쪽
            self.vector.x +=self.vel
        if keys[pg.K_a] and self.rect.left >=0:#왼쪽
            self.vector.x -=self.vel
        #점프 구현
        if keys[pg.K_w]:
            if not self.jumping: #만약 jumping이 False라면
                self.jumping = True
                self.jump_tick = PLAYER_JUMP_TICK
                self.jump_vel = self.jump_tick/2 * GRAVITY
        if self.jump_tick: #만약 jump_vel이 0이 아니라면
            self.vector.y -= self.jump_vel
            self.jump_vel -= GRAVITY
            self.jump_tick -=1
            if not self.jump_tick: #만약 jump_vel이 0이라면
                self.jumping = False
                self.vector.y -= self.jump_vel

        self.rect.center = self.vector
    def build(self):
        pass
    def update(self):
        self.move()




#플레이어를 공격하는 모든 적(추상 클래스)
class Enemy(Creature,metaclass=ABCMeta):
    def __init__(self):
        super().__init__()
        self.img = None
        enemy_sprites.add(self)

    @abstractmethod
    def attack(self):
        pass

class Zombie(Enemy):
    def __init__(self):
        super().__init__()

    def attack(self):
        pass

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