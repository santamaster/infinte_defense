import pygame as pg
from setting import *
import sprites as sp
import camera as c

def main_menu():
    click = 0
    while 1:
        SCREEN.fill((0,0,0))
        mx, my = pg.mouse.get_pos()
        button_1 = pg.Rect(WIDTH/2,HEIGHT/2, 200, 50)
        pg.draw.rect(SCREEN, (255, 0, 0), button_1)
        #버튼 클릭시 게임 실행
        if button_1.collidepoint((mx, my)):
            if click:
                game()
 
        click = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = 1
                    
        pg.display.flip()

camera = c.Camera(sp.all_sprites,sp.human1)
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
                running = 0
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = 0
            # elif event.type == pg.MOUSEWHEEL:
            #     camera.zoom(event.y)
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
        button_1 = pg.Rect(WIDTH/2,HEIGHT/2, 200, 50)
        pg.draw.rect(SCREEN, (255, 0, 0), button_1)
        #버튼 클릭시 게임 실행
        if button_1.collidepoint((mx, my)):
            if click:
                build()
        pg.display.flip()

def build():
    running = 1
    click = 0
    while running:

        #fps 설정
        CLOCK.tick(FPS)
        click = 0
        #종료
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = 0
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = 0
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = 1

        #카메라로 화면 그리기
        camera.draw()

        #마우스 위치 가져오기
        mx, my = pg.mouse.get_pos()
        button_1 = pg.Rect(100,HEIGHT - 250,100,200)
        button_2 = pg.Rect(300,HEIGHT - 250,100,200)
        pg.draw.rect(SCREEN, (255, 0, 0), button_1)
        pg.draw.rect(SCREEN, (255, 0, 0), button_2)

        #버튼 클릭시 
        if button_1.collidepoint((mx, my)):
            if click:
                pass
        elif button_2.collidepoint((mx,my)):
            if click:
                pass

        pg.display.flip()
    
main_menu()
pg.quit()
