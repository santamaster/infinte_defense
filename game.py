import pygame as pg
from setting import *
import sprites as sp
import camera as c

#카메라 생성
camera = c.Camera(sp.all_sprites,sp.human1)
#루프
while RUNNING:

    #fps 설정
    CLOCK.tick(FPS)
    
    #종료
    for event in pg.event.get():
        if event.type == pg.QUIT:
            RUNNING = 0
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                RUNNING = 0
        elif event.type == pg.MOUSEWHEEL:
            camera.zoom(event.y)
            
    #카메라 움직이기
    camera.player_follow()

    #스프라이트 업데이트
    sp.all_sprites.update()

    #카메라로 화면 그리기
    camera.draw()
    
pg.quit()
