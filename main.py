import pygame as pg
import sys
from setting import *
import sprites as sp
import camera as c

start = pg.Rect(0,0, 200, 50)
start.center = (WIDTH/2,HEIGHT/2)

def main_menu():
    click = 0
    while 1:
        
        click = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = 1

        SCREEN.fill(BLACK)
        mx, my = pg.mouse.get_pos()
        pg.draw.rect(SCREEN, (255, 0, 0), start)
        
        #버튼 클릭시 게임 실행
        if start.collidepoint((mx, my)):
            if click:
                game()

        pg.display.flip()
    

camera = c.Camera(sp.all_sprites,sp.human1)
build_button = pg.Rect(WIDTH/2,HEIGHT/2, 200, 50)
build_button.center = (WIDTH-100,HEIGHT-25)
#게임
def game():
    running = 1
    click = 0
    while running:

        #fps 설정
        CLOCK.tick(FPS)
        click = 0
        #종료
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = 0
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = 1
                    
        
        #카메라 움직이기
        camera.player_follow()

        #스프라이트 업데이트
        sp.all_sprites.update()

        #카메라로 화면 그리기
        camera.draw()

        #마우스 위치 가져오기
        mx, my = pg.mouse.get_pos()
        pg.draw.rect(SCREEN, (255, 0, 0), build_button)

        #버튼 클릭시 게임 실행
        if build_button.collidepoint((mx, my)):
            if click:
                build()
        pg.display.flip()

wall_button = pg.Rect(100,HEIGHT - 250,100,200)
canon_button = pg.Rect(300,HEIGHT - 250,100,200)
mine_button = pg.Rect(500,HEIGHT - 250,100,200)


def build():
    running = 1
    click = 0
    drag = 0
    while running:

        #fps 설정
        CLOCK.tick(FPS)
        click = 0
        
        #종료
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = 0
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = 1
                    drag = 1

        #카메라로 화면 그리기
        camera.draw()

        #마우스 위치 가져오기
        mx, my = pg.mouse.get_pos()
        
        pg.draw.rect(SCREEN, (255, 0, 0), wall_button)
        pg.draw.rect(SCREEN, (0, 255, 0), canon_button)
        pg.draw.rect(SCREEN, (0, 0, 255), mine_button)

        #버튼 클릭시 
        if click:
            if wall_button.collidepoint((mx, my)):
                pass
            elif canon_button.collidepoint((mx,my)):
                pass
            elif mine_button.collidepoint((mx,my)):
                pass

        pg.display.flip()
    
main_menu()
pg.quit()
