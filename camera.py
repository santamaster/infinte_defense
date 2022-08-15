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
        #-----정보 표시-----#
        #플레이어 hp표시
        SCREEN.blit(hp_frame_img,(WIDTH - HP_FRAME_WIDTH - HP_FRAME_INTERVAL,HP_FRAME_INTERVAL))#체력바 프레임
        pg.draw.rect(SCREEN,RED,[WIDTH - HP_FRAME_INTERVAL - HP_FRAME_WIDTH*49/50,HP_FRAME_INTERVAL + HP_FRAME_HEIGHT/10, \
            self.player.hp / self.player.hp_max * HP_FRAME_WIDTH*24/25,HP_FRAME_HEIGHT*4/5])

        #현재 골드 표시
        msg_gold = myfont.render("gold : {}".format(self.player.gold),True,WHITE)
        SCREEN.blit(msg_gold,(10,10))

        #시간 표시(선택)
        tick = pg.time.get_ticks()
        msg_time = myfont.render("time : {}".format(tick//1000),True,WHITE)
        SCREEN.blit(msg_time,(10,30))
        
        #fps 표시(선택)
        msg_fps = myfont.render("fps : {}".format(int((CLOCK.get_fps()))),True,WHITE)
        SCREEN.blit(msg_fps,(10,50))

        



    
    


    
   



        