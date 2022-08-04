import pygame as pg
from setting import *

"""카메라는 플레이어를 중심으로 움직이고 다른 스프라이트들을 그림."""

class Camera():
    def __init__(self,sprite_group,player):
        self.sprite_group = sprite_group #그려야 할 스프라이트 그룹
        self.player = player 
        self.CAMERA_X = 0
        self.CAMERA_Y = 0

    #player 따라다니기
    def follow(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            if self.CAMERA_X > -BG_WIDTH/2 and self.player.vector.x >= 800:
                self.CAMERA_X -= CAMERA_VEL
                for sprite in self.sprite_group:
                    sprite.vector.x -= CAMERA_VEL
                    #sprite.vector.y +=CAMERA_Y
        elif keys[pg.K_a]:
            if self.CAMERA_X < 0 and self.player.vector.x <= 566:
                self.CAMERA_X += CAMERA_VEL
                for sprite in self.sprite_group:
                    sprite.vector.x += CAMERA_VEL
                    #sprite.vector.y +=CAMERA_Y

    #확대,축소
    def zoom(self,wheel):
        global background_img
        if wheel > 0:
            background_img = pg.transform.scale(background_img,(background_img.get_width()*2,background_img.get_height()*2))
            for sprite in self.sprite_group:
                sprite.image = pg.transform.scale(sprite.image,(sprite.image.get_width()*2,sprite.image.get_height()*2))
        elif wheel < 0:
            background_img = pg.transform.scale(background_img,(background_img.get_width()/2,background_img.get_height()/2))
            for sprite in self.sprite_group:
                sprite.image = pg.transform.scale(sprite.image,(sprite.image.get_width()/2,sprite.image.get_height()/2))

    def draw(self):
        #스크린 배경 색상
        SCREEN.blit(background_img,(self.CAMERA_X,0))

        #스프라이트 그룹 화면 출력
        for sprite in self.sprite_group:
            SCREEN.blit(sprite.image,sprite.rect)


        #fps 표시(선택)
        msg_fps = myfont.render("fps : {}".format(int((CLOCK.get_fps()))),True,WHITE)
        SCREEN.blit(msg_fps,(10,30))

        #시간 표시(선택)
        tick = pg.time.get_ticks()
        msg_time = myfont.render("time : {}".format(int(tick/1000)),True,WHITE)
        SCREEN.blit(msg_time,(10,10))
        pg.display.flip()


    
    


    
   



        