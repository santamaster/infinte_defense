import pygame as pg
from setting import *
import sprites as sp

"""카메라는 플레이어를 중심으로 움직이고 다른 스프라이트들을 그림."""

class Camera():
    def __init__(self,player):
        self.player = player #따라다녀야 할 플레이어
        self.offset = pg.math.Vector2(self.player.vector.x-WIDTH/2,0)
    #player 따라다니기
    def player_follow(self):
        self.offset.x = self.player.vector.x-WIDTH/2
        if 0 >= self.offset.x:
            self.offset.x = 0
        elif self.offset.x >= BG_WIDTH-WIDTH:
            self.offset.x = BG_WIDTH-WIDTH

    def draw(self):
        #배경과 모든 스프라이트를 반대방향으로 이동시킨뒤 화면 출력
        #배경 화면 출력
        SCREEN.blit(background_img,(-self.offset.x,-self.offset.y))


        for sprite in sp.noncreature_sprites:
            SCREEN.blit(sprite.image,sprite.rect.move(-self.offset.x,-self.offset.y))
        for sprite in sp.building_sprites:
            SCREEN.blit(sprite.image,sprite.rect.move(-self.offset.x,-self.offset.y))
        for sprite in sp.enemy_sprites:
            SCREEN.blit(sprite.image,sprite.rect.move(-self.offset.x,-self.offset.y))
        for sprite in sp.player_sprites:
            SCREEN.blit(sprite.image,sprite.rect.move(-self.offset.x,-self.offset.y))
        # #fps 표시(선택)
        # msg_fps = myfont.render("fps : {}".format(int((CLOCK.get_fps()))),True,WHITE)
        # SCREEN.blit(msg_fps,(10,50))

        



    
    


    
   



        