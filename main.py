import pygame as pg
from sys import exit
from pygame.locals import *
from setting import *
import sprites as sp
import camera as c

start = pg.Rect(0,0, 200, 50)
start.center = (WIDTH/2,HEIGHT/2)



#게임
def game(character):
    running = 1
    click = 0
    if character == "human":
        player = sp.Human()
    elif character == "wizard":
        player = sp.Wizard()
    else: #default
        player = sp.Human()
    camera = c.Camera(player)
    build_button = pg.Rect(WIDTH/2,HEIGHT/2, 200, 50)
    build_button.center = (WIDTH-100,HEIGHT-25)

    while running:

        #fps 설정
        CLOCK.tick(FPS)
        click = 0
        #종료
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = 0
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = 1
        #레벨 시스템 

        
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
                build(camera,player)
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

def collision_check(rect,camera):
    for sprite in sp.building_sprites.sprites() + sp.enemy_sprites.sprites():
        if rect.left <= sprite.rect.right - camera.offset.x and \
            rect.right >= sprite.rect.left - camera.offset.x:
            return True
            
    return False

def build(camera,player):
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
                exit()
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
            if not wall_button.collidepoint((mx, my)):
                wall_rect.center = (mx,my)
                if collision_check(wall_rect,camera):
                    SCREEN.blit(wall_red,wall_rect.topleft)

                else:
                    SCREEN.blit(wall_green,wall_rect.topleft)
                    if not click:
                        if player.gold >= WALL_PRICE:
                            sp.Wall(pg.math.Vector2(mx+camera.offset.x,768-140))
                            player.gold -= WALL_PRICE
                        else:
                            pass
        elif selected == "canon":
            if not canon_button.collidepoint((mx,my)):
                canon_rect.center = (mx,my)
                if collision_check(canon_rect,camera):
                    SCREEN.blit(canon_red,canon_rect.topleft)

                else:
                    SCREEN.blit(canon_green,canon_rect.topleft)
                    if not click:
                        if player.gold >= CANON_PRICE:
                            sp.Canon(pg.math.Vector2(mx+camera.offset.x,768-140))
                            player.gold -= CANON_PRICE
                        else:
                            pass

        elif selected == "mine":
            if not mine_button.collidepoint((mx,my)):
                mine_rect.center = (mx,my)
                if collision_check(mine_rect,camera):
                    SCREEN.blit(mine_red,mine_rect.topleft)

                else:
                    SCREEN.blit(mine_green,mine_rect.topleft)
                    if not click:
                        if player.gold >= MINE_PRICE:
                            sp.Mine(player,pg.math.Vector2(mx+camera.offset.x,768-140))
                            player.gold -= MINE_PRICE
                        else:
                            pass

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

#TODO:
def main_menu():
    while 1:
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()


        pg.display.flip()
    
main_menu()
pg.quit()
