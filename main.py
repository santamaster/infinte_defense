import pygame as pg
from sys import exit
from pygame.locals import *
from setting import *
import sprites as sp
import camera as c
from random import random,choice

#초기화
def reset():
    for sprite in sp.all_sprites:
        sprite.kill()

#적 생성 시스템
def enemy_spawn(game_sec):
    spawn_location = "left","right"

    #시간이 지날수록 적이 더 빨리 나옴
    if game_sec <= 30:      #30초 이내
        if random()*FPS <= 0.2:  #1초당 0.1마리
            sp.Zombie(choice(spawn_location))
    elif game_sec <= 60:    #30~60초
        if random()*FPS <= 0.3:  #1초당 0.2마리
            sp.Zombie(choice(spawn_location))
    elif game_sec <= 120:   #60~120초
        if random()*FPS <= 0.5:  #1초당 0.5마리
            sp.Zombie(choice(spawn_location))
    else:                   #120초 이후
        if random()*FPS <= 1:    #1초당 1마리
            sp.Zombie(choice(spawn_location))

build_button = pg.Rect(WIDTH/2,HEIGHT/2, 200, 50)
build_button.center = (WIDTH-100,HEIGHT-25)

menu_frame = pg.Rect(0,0,300,500)
menu_frame.center = (WIDTH/2,HEIGHT/2)
goto_main_menu = pg.Rect(0,0,100,50)
goto_main_menu.center = (WIDTH/2,HEIGHT/2 + 150)
go_back = pg.Rect(0,0,100,50)
go_back.center = (WIDTH/2,HEIGHT/2 + 50)
goto_mainmenu_defeat = pg.Rect(0,0,200,100)
goto_mainmenu_defeat.center = (WIDTH/2,HEIGHT/2)
restart = pg.Rect(0,0,100,50)
restart.center = (WIDTH/2,HEIGHT/2 - 50)
#게임
def game(character):
    
    if character == "human":
        player = sp.Human()
    elif character == "wizard":
        player = sp.Wizard()
    else: #기본값(오류 방지)
        player = sp.Human()

    running = 1
    click = 0
    game_tick = 0
    menu = 0
    camera = c.Camera(player)

    while running:
        game_tick += 1
        game_sec = game_tick//FPS
        click = 0

        #fps 설정
        CLOCK.tick(FPS)

        #이벤트 처리
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if not menu:
                        menu = 1
                    else:
                        menu = 0
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = 1
        #마우스 위치 가져오기
        mx, my = pg.mouse.get_pos()
        
        #메뉴 실행시
        if menu:
            #어두워진 화면 그리기(스프라이트 업데이트 안함)
            camera.darkened_draw()

            if click:
                if goto_main_menu.collidepoint((mx,my)):
                    reset()
                    break
                elif go_back.collidepoint((mx,my)):
                    menu = 0
                elif restart.collidepoint((mx,my)):
                    reset()
                    if character == "human":
                        player = sp.Human()
                    elif character == "wizard":
                        player = sp.Wizard()
                    else: #기본값(오류 방지)
                        player = sp.Human()
                        
                    game_tick = 0
                    menu = 0
                    camera = c.Camera(player)
                    continue

            pg.draw.rect(SCREEN,YELLOW,menu_frame)
            pg.draw.rect(SCREEN,RED,goto_main_menu)
            pg.draw.rect(SCREEN,RED,go_back)
            pg.draw.rect(SCREEN,RED,restart)
            
            pg.display.flip()
            continue
        
        #플레이어 죽어서 없을 시 게임 종료
        if player.hp <= 0:
            SCREEN.fill(BLACK)
            if click:
                if goto_mainmenu_defeat.collidepoint((mx, my)):
                    reset()
                    break

            pg.draw.rect(SCREEN, (255, 0, 0), goto_mainmenu_defeat)

            pg.display.flip()
            continue

        #적 생성
        enemy_spawn(game_sec)

        #카메라 움직이기
        camera.player_follow()

        #스프라이트 업데이트
        sp.all_sprites.update()

        #카메라로 화면 그리기
        camera.draw()

        pg.draw.rect(SCREEN, (255, 0, 0), build_button)

        #버튼 클릭시 실행
        if build_button.collidepoint((mx, my)):
            if click:
                build(camera,player)
        #플레이어 hp표시
        SCREEN.blit(hp_frame_img,(WIDTH - HP_FRAME_WIDTH - HP_FRAME_INTERVAL,HP_FRAME_INTERVAL))#체력바 프레임
        pg.draw.rect(SCREEN,RED,[WIDTH - HP_FRAME_INTERVAL - HP_FRAME_WIDTH*49/50,HP_FRAME_INTERVAL + HP_FRAME_HEIGHT/10, \
            player.hp / player.max_hp * HP_FRAME_WIDTH*24/25,HP_FRAME_HEIGHT*4/5])

        #현재 골드 표시
        msg_gold = myfont.render("gold : {}".format(player.gold),True,WHITE)
        SCREEN.blit(msg_gold,(10,10))

        #시간 표시(선택)
        msg_time = myfont.render("{}분 {}초".format(game_sec//60,game_sec%60),True,WHITE)
        SCREEN.blit(msg_time,(10,50))


        pg.display.flip()


#건물 설치시 x축 충돌 확인
def collision_check(rect,camera):
    for sprite in sp.building_sprites.sprites() + sp.enemy_sprites.sprites():
        if rect.left <= sprite.rect.right - camera.offset.x and \
            rect.right >= sprite.rect.left - camera.offset.x:
            return True
            
    return False
    
exit_button = pg.Rect(WIDTH - 50,20,30,30)
cancel_button = pg.Rect(WIDTH - 70,100,50,50)
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

def build(camera,player):
    running = 1
    click = 0
    selected = ""
    while running:

        #fps 설정
        CLOCK.tick(FPS)
        
        #이벤트 처리
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

        #어두위진 화면 그리기(스프라이트 업데이트 안함)
        camera.darkened_draw()
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
            if exit_button.collidepoint((mx,my)):
                if not selected:
                    running = 0
            elif cancel_button.collidepoint((mx,my)):
                selected = ""

            elif wall_button.collidepoint((mx, my)):
                selected = "wall"
            elif canon_button.collidepoint((mx,my)):
                selected = "canon"
            elif mine_button.collidepoint((mx,my)):
                selected = "mine"
            
        else:
            selected = ""
        
        pg.draw.rect(SCREEN, (255,0,0),exit_button)
        pg.draw.rect(SCREEN,(255,0,0),cancel_button)
        pg.draw.rect(SCREEN, (255, 0, 0), wall_button)
        pg.draw.rect(SCREEN, (0, 255, 0), canon_button)
        pg.draw.rect(SCREEN, (0, 0, 255), mine_button)

        #현재 골드 표시
        msg_gold = myfont.render("gold : {}".format(player.gold),True,WHITE)
        SCREEN.blit(msg_gold,(10,10))

        pg.display.flip()

play_button = pg.Rect(0,0,200,100)
play_button.center = (WIDTH/2,HEIGHT/2)

def main_menu():
    click = 0
    character_list = ["human","wizard"]
    select = 0
    running = 1
    while running:
        SCREEN.fill(BLACK)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
                elif event.key == K_RIGHT:
                    select += 1
                    if select > len(character_list) - 1:
                        select = 0
                elif event.key == K_LEFT:
                    select -= 1
                    if select < 0:
                        select = len(character_list) - 1
            elif event.type == MOUSEBUTTONDOWN:
                click = 1
            elif event.type == MOUSEBUTTONUP:
                click = 0

        mx, my = pg.mouse.get_pos()

        if click:
            if play_button.collidepoint((mx, my)):
                game(character_list[select])
                click = 0
        
        msg_character = myfont.render("Character : {}".format(character_list[select]),True,WHITE)
        SCREEN.blit(msg_character,(WIDTH/2,HEIGHT/2 - 200))

        msg_title = myfont.render("game_project",True,WHITE)
        SCREEN.blit(msg_title,(WIDTH/2,100))
        
        pg.draw.rect(SCREEN, (255, 0, 0), play_button)
        
        pg.display.flip()
    
main_menu()
pg.quit()
