import pygame as pg
import sys
from pygame.locals import *
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
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
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
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = 0
            elif event.type == MOUSEBUTTONDOWN:
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
wall_rect = wall_img.get_rect()
wall_green = fill(wall_img,GREEN)
wall_red = fill(wall_img,RED)
canon_button = pg.Rect(300,HEIGHT - 250,100,200)
canon_rect = canon_img.get_rect()
canon_green = fill(canon_img,GREEN)
canon_red = fill(canon_img,RED)
mine_button = pg.Rect(500,HEIGHT - 250,100,200)
mine_rect = mine_img.get_rect()
mine_green = fill(mine_img,GREEN)
mine_red = fill(mine_img,RED)

def collision_check(rect):
    for sprite in sp.building_sprites.sprites() + sp.enemy_sprites.sprites():
        if rect.left <= sprite.rect.right - camera.offset.x and \
            rect.right >= sprite.rect.left - camera.offset.x:
            return True
            
    return False

def build():
    running = 1
    click = 0
    selected = ""
    while running:

        #fps 설정
        CLOCK.tick(FPS)
        
        #종료
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = 0
            elif event.type == MOUSEBUTTONDOWN:
                click = 1
            elif event.type == MOUSEBUTTONUP:
                click = 0
        #카메라로 화면만 그리기(스프라이트 업데이트 안함)
        camera.draw()
        #마우스 위치 가져오기
        mx, my = pg.mouse.get_pos()
        

            
        if selected == "wall":
            wall_rect.center = (mx,my)
            if collision_check(wall_rect):
                SCREEN.blit(wall_red,wall_rect.topleft)

            else:
                SCREEN.blit(wall_green,wall_rect.topleft)
                if not click:
                    sp.Wall(pg.math.Vector2(mx+camera.offset.x,768-140))

        elif selected == "canon":
            canon_rect.center = (mx,my)
            if collision_check(canon_rect):
                SCREEN.blit(canon_red,canon_rect.topleft)

            else:
                SCREEN.blit(canon_green,canon_rect.topleft)
                if not click:
                    sp.Canon(pg.math.Vector2(mx+camera.offset.x,768-140))

        elif selected == "mine":
            mine_rect.center = (mx,my)
            if collision_check(mine_rect):
                SCREEN.blit(mine_red,mine_rect.topleft)

            else:
                SCREEN.blit(mine_green,mine_rect.topleft)
                if not click:
                    sp.Mine(sp.human1,pg.math.Vector2(mx+camera.offset.x,768-140))

        #버튼 클릭시 
        if click:
            if wall_button.collidepoint((mx, my)):
                selected = "wall"
            elif canon_button.collidepoint((mx,my)):
                selected = "canon"
            elif mine_button.collidepoint((mx,my)):
                selected = "mine"
        else:
            selected = ""

        pg.draw.rect(SCREEN, (255, 0, 0), wall_button)
        pg.draw.rect(SCREEN, (0, 255, 0), canon_button)
        pg.draw.rect(SCREEN, (0, 0, 255), mine_button)

        pg.display.flip()
    
main_menu()
pg.quit()
