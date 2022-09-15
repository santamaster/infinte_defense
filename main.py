import pygame as pg
from sys import exit
from pygame.locals import *
from setting import *
import sprites as sp
import camera as c
import ability as ab
from random import random,choice,sample

#초기화
def reset():
    for sprite in sp.all_sprites:
        sprite.kill()
    for sprite in sp.hp_bar_sprites:
        sprite.kill()
    sp.Canon.self_healing = 0
    sp.Mine.gold_cooldown_rate = 1
    sp.Canon.enhanced_attack_chance = 0
    sp.Canon.damage_rate = 1
    sp.Enemy.damage_rate = 1


#적 생성 시스템
def enemy_spawn(game_sec,player):
    spawn_location = "left","right"

    #시간이 지날수록 적이 더 빨리 나옴
    if game_sec <= 30:      #30초 이내
        if random()*FPS <= 0.2:  #1초당 0.1마리
            sp.Zombie(choice(spawn_location),player)
    elif game_sec <= 60:    #30~60초
        if random()*FPS <= 0.3:  #1초당 0.2마리
            sp.Zombie(choice(spawn_location),player)
    elif game_sec <= 120:   #60~120초
        if random()*FPS <= 0.5:  #1초당 0.5마리
            sp.Zombie(choice(spawn_location),player)
    else:                   #120초 이후
        if random()*FPS <= 1:    #1초당 1마리
            sp.Zombie(choice(spawn_location),player)

#자동으로 줄바꿈 및 화면 출력
def blit_text(rect, text, pos, color=WHITE):
    words = [word.split(' ') for word in text.splitlines()] 
    space = MYFONT.size(' ')[0]  
    max_width, max_height = rect.w,rect.h
    x, y = pos
    for line in words:
        for word in line:
            word_surface = MYFONT.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  
                y += word_height  
            SCREEN.blit(word_surface, (x+rect.x, y+rect.y))
            x += word_width + space
        x = pos[0]  
        y += word_height  

menu_frame_image = MENU_FRAME
menu_frame = menu_frame_image.get_rect()
menu_frame.center = (WIDTH/2,HEIGHT/2)

button_image = BUTTON

goto_main_menu = button_image.get_rect()
goto_main_menu.center = (WIDTH/2,HEIGHT/2 + 150)

go_back_text = MYFONT.render("돌아가기",True,BLACK)
go_back = button_image.get_rect()
go_back.center = (WIDTH/2,HEIGHT/2 - 50)

restart = button_image.get_rect()
restart.center = (WIDTH/2,HEIGHT/2 + 50)

goto_mainmenu_defeat = button_image.get_rect()
goto_mainmenu_defeat.center = (WIDTH/2,HEIGHT/2)

upgrade_image = UPGRADE_BUTTON
upgrade_button = upgrade_image.get_rect()
sell_image = SELL_BUTTON
sell_button = sell_image.get_rect()

build_image = BUILD_BUTTON
build_button = build_image.get_rect()
build_button.center = (WIDTH-100,HEIGHT-100)

ability_image = MENU_FRAME

ability1 = ability_image.get_rect()
ability1.center = (WIDTH/4*1,HEIGHT/2)

ability2 = ability_image.get_rect()
ability2.center = (WIDTH/4*2,HEIGHT/2)

ability3 = ability_image.get_rect()
ability3.center = (WIDTH/4*3,HEIGHT/2)

#게임
def game(character):
    if character == "human":
        player = sp.Human()
    elif character == "wizard":
        player = sp.Wizard()
    running = 1
    click = 0
    game_tick = 0
    menu = 0
    camera = c.Camera(player)
    upgrade_sell = 0
    selected_sprite = None
    select_ability = 0
    player_level = 1
    ability_list = []
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

        #플레이어 레벨 업
        if player_level < player.level:
            player_level = player.level

            if player_level == 2:
                ability123_list = sample(ab.level_2_ability,3)
            elif player_level == 3:
                ability123_list = sample(ab.level_3_ability,3)
            elif player_level == 4:
                ability123_list = sample(ab.level_4_ability,3)
            elif player_level == 5:
                ability123_list = sample(ab.level_5_ability,3)
            elif player_level == 6:
                ability123_list = sample(ab.level_6_ability,3)

            select_ability = 1
            sp.Message("level_up!",GREEN)
        
        if select_ability:
            if click:
                if ability1.collidepoint((mx,my)):
                    ability123_list[0]()
                    select_ability = 0
                elif ability2.collidepoint((mx,my)):
                    ability123_list[1]()
                    select_ability = 0
                elif ability3.collidepoint((mx,my)):
                    ability123_list[2]()
                    select_ability = 0
            camera.darkened_draw()

            SCREEN.blit(ability_image,ability1)
            blit_text(ability1,ab.ability_info[ability123_list[0]],(0,0))

            SCREEN.blit(ability_image,ability2)
            blit_text(ability2,ab.ability_info[ability123_list[1]],(0,0))

            SCREEN.blit(ability_image,ability3)
            blit_text(ability3,ab.ability_info[ability123_list[2]],(0,0))

            pg.display.flip()
            continue

        #메뉴 실행시
        if menu:
            #어두워진 화면 그리기(스프라이트 업데이트 안함)
            camera.darkened_draw()

            if click:
                if go_back.collidepoint((mx,my)):
                    menu = 0
                elif goto_main_menu.collidepoint((mx,my)):
                    reset()
                    break
                elif restart.collidepoint((mx,my)):
                    reset()
                    if character == "human":
                        player = sp.Human()
                    elif character == "wizard":
                        player = sp.Wizard()
                    game_tick = 0
                    menu = 0
                    camera = c.Camera(player)
                    upgrade_sell = 0
                    selected_sprite = None
                    player_level = 1

                    continue
            
            #메뉴 그리기
            SCREEN.blit(menu_frame_image,menu_frame)
            SCREEN.blit(button_image,goto_main_menu)
            SCREEN.blit(button_image,go_back)
            SCREEN.blit(button_image,restart)
            
            pg.display.flip()
            continue
        
        #플레이어의 체력이 0이하이면 게임 종료
        if player.hp <= 0:
            SCREEN.fill(BLACK)
            if click:
                if goto_mainmenu_defeat.collidepoint((mx, my)):
                    reset()
                    break

            SCREEN.blit(button_image,goto_mainmenu_defeat)

            msg_defeat = MYFONT.render("YOU DIE",True,WHITE)
            SCREEN.blit(msg_defeat,(WIDTH/2,HEIGHT/3))
            pg.display.flip()
            continue

        #적 생성
        enemy_spawn(game_sec,player)

        #카메라 움직이기
        camera.player_follow()

        #카메라로 화면 그리기
        camera.draw()

        #스프라이트 업데이트
        sp.all_sprites.update()
        
        #건물 설치 버튼
        SCREEN.blit(build_image,build_button)
        #버튼 클릭시 실행
        if build_button.collidepoint((mx, my)):
            if click:
                build(camera,player)
        
        #건물이 마우스와 충돌시 외각선
        for building in sp.building_sprites:
            if building.shown_rect.collidepoint((mx,my)):
                SCREEN.blit(building.outline_image,building.shown_rect)
                if click:
                    upgrade_sell = 1
                    selected_sprite = building

        
        #건물 업데이트 및 판매
        if upgrade_sell:
            upgrade_button.midbottom = selected_sprite.shown_rect.bottomright
            upgrade_button.move_ip(0,100)
            SCREEN.blit(upgrade_image,upgrade_button)
            sell_button.midbottom = selected_sprite.shown_rect.bottomleft
            sell_button.move_ip(0,100)
            SCREEN.blit(sell_image,sell_button)
            
            msg_sprite_level = MYFONT.render(f"{selected_sprite.level} level",True,WHITE)
            sprite_level_rect = msg_sprite_level.get_rect()
            sprite_level_rect.midbottom = selected_sprite.shown_rect.midtop
            sprite_level_rect.move_ip(0,-30)

            SCREEN.blit(msg_sprite_level,sprite_level_rect)
            if upgrade_button.collidepoint((mx,my)):
                if click:
                    if selected_sprite.level == selected_sprite.max_level:
                        sp.Message("이미 최대 레벨입니다.",RED)
                        upgrade_sell = 0
                        selected_sprite = None
                    elif player.gold >= selected_sprite.upgrade_price:
                        player.gold -= selected_sprite.upgrade_price
                        selected_sprite.upgrade()
                        sp.Message(f" {selected_sprite.level} 레벨로 업그레이드",WHITE)
                        upgrade_sell = 0
                        selected_sprite = None
                    elif player.gold <= selected_sprite.upgrade_price:
                        sp.Message("골드가 부족합니다.",RED)
                        upgrade_sell = 0
                        selected_sprite = None
            elif sell_button.collidepoint((mx,my)):
                if click:
                    player.gold += int(selected_sprite.price * REFUND_RATE)
                    selected_sprite.kill()
                    upgrade_sell = 0
                    selected_sprite = None
            elif selected_sprite.shown_rect.collidepoint((mx,my)):
                pass
            elif click:
                upgrade_sell = 0
                selected_sprite = None
        
        #플레이어 hp표시
        SCREEN.blit(HP_FRAME_IMG,(WIDTH - HP_FRAME_WIDTH - HP_FRAME_INTERVAL,HP_FRAME_INTERVAL))#체력바 프레임
        pg.draw.rect(SCREEN,RED,[WIDTH - HP_FRAME_INTERVAL - HP_FRAME_WIDTH*49/50,HP_FRAME_INTERVAL + HP_FRAME_HEIGHT/10, \
            player.hp / player.max_hp * HP_FRAME_WIDTH*24/25,HP_FRAME_HEIGHT*4/5])

        #현재 골드 표시
        msg_gold = MYFONT.render(f"골드 : {player.gold}",True,WHITE)
        SCREEN.blit(msg_gold,(10,10))

        #시간 표시
        msg_time = MYFONT.render(f"{game_sec//60}분 {game_sec%60}초",True,WHITE)
        SCREEN.blit(msg_time,(10,50))
        
        #플레이어 레벨 표시
        msg_level = MYFONT.render(f"레벨 : {player.level}",True,WHITE)
        SCREEN.blit(msg_level,(10,90))

        #플레이어 경험치 표시
        msg_exp = MYFONT.render(f"경험치 : {player.exp}/{player.reqired_exp}",True,WHITE)
        SCREEN.blit(msg_exp,(10,130))

        #총 골드 표시
        msg_total_gold = MYFONT.render(f"총 골드 : {player.total_gold}",True,WHITE)
        SCREEN.blit(msg_total_gold,(10,170))
        #fps 표시(선택)
        msg_fps = MYFONT.render(f"fps : {int((CLOCK.get_fps()))}",True,WHITE)
        SCREEN.blit(msg_fps,(10,210))
        
        pg.display.flip()

#건물 설치시 x축 충돌 확인
def collision_check(rect,camera):
    for sprite in sp.building_sprites.sprites() + sp.enemy_sprites.sprites():
        if rect.left <= sprite.rect.right - camera.offset.x and \
            rect.right >= sprite.rect.left - camera.offset.x:
            return True
            
    return False

exit_image = SELL_BUTTON
exit_button = exit_image.get_rect()
exit_button.center = (WIDTH-100,HEIGHT-100)

wall_button = pg.Rect(100,HEIGHT - 250,100,200)
wall_rect = WALL_IMAGE.get_rect()
wall_green = fill(WALL_IMAGE,GREEN)
wall_red = fill(WALL_IMAGE,RED)
canon_button = pg.Rect(300,HEIGHT - 250,100,200)
canon_rect = CANON_IMAGE.get_rect()
canon_green = fill(CANON_IMAGE,GREEN)
canon_red = fill(CANON_IMAGE,RED)
mine_button = pg.Rect(500,HEIGHT - 250,100,200)
mine_rect = MINE_IMAGE.get_rect()
mine_green = fill(MINE_IMAGE,GREEN)
mine_red = fill(MINE_IMAGE,RED)
mortar_button = pg.Rect(700,HEIGHT - 250,100,200)
mortar_rect = MORTAR_IMAGE.get_rect()
mortar_green = fill(MORTAR_IMAGE,GREEN)
mortar_red = fill(MORTAR_IMAGE,RED)
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
                    if not click:
                        sp.Message("여기에 건물을 설치할 수 없습니다.",RED)
                else:
                    SCREEN.blit(wall_green,wall_rect.topleft)
                    if not click:
                        if player.gold >= sp.Wall.price[0]:
                            sp.Wall(pg.math.Vector2(mx+camera.offset.x,516),player)
                            player.gold -= sp.Wall.price[0]
                        else:
                            sp.Message("골드가 충분하지 않습니다.",RED)

        elif selected == "canon":
            if not canon_button.collidepoint((mx,my)):
                canon_rect.center = (mx,my)
                if collision_check(canon_rect,camera):
                    SCREEN.blit(canon_red,canon_rect.topleft)
                    if not click:
                        sp.Message("여기에 건물을 설치할 수 없습니다.",RED)
                else:
                    SCREEN.blit(canon_green,canon_rect.topleft)
                    if not click:
                        if player.gold >= sp.Canon.price[0]:
                            sp.Canon(pg.math.Vector2(mx+camera.offset.x,516),player)
                            player.gold -= sp.Canon.price[0]
                        else:
                            sp.Message("골드가 충분하지 않습니다.",RED)

        elif selected == "mine":
            if not mine_button.collidepoint((mx,my)):
                mine_rect.center = (mx,my)
                if collision_check(mine_rect,camera):
                    SCREEN.blit(mine_red,mine_rect.topleft)
                    if not click:
                        sp.Message("여기에 건물을 설치할 수 없습니다.",RED)
                else:
                    SCREEN.blit(mine_green,mine_rect.topleft)
                    if not click:
                        if player.gold >= sp.Mine.price[0]:
                            sp.Mine(pg.math.Vector2(mx+camera.offset.x,516),player)
                            player.gold -= sp.Mine.price[0]
                        else:
                            sp.Message("골드가 충분하지 않습니다.",RED)

        elif selected == "mortar":
            if not mortar_button.collidepoint((mx,my)):
                mortar_rect.center = (mx,my)
                if collision_check(mortar_rect,camera):
                    SCREEN.blit(mortar_red,mortar_rect.topleft)
                    if not click:
                        sp.Message("여기에 건물을 설치할 수 없습니다.",RED)
                else:
                    SCREEN.blit(mortar_green,mortar_rect.topleft)
                    if not click:
                        if player.gold >= sp.Mortar.price[0]:
                            sp.Mortar(pg.math.Vector2(mx+camera.offset.x,516),player)
                            player.gold -= sp.Mortar.price[0]
                        else:
                            sp.Message("골드가 충분하지 않습니다.",RED)
        if click:
            if exit_button.collidepoint((mx,my)):
                if not selected:
                    running = 0
            elif wall_button.collidepoint((mx, my)):
                selected = "wall"
            elif canon_button.collidepoint((mx,my)):
                selected = "canon"
            elif mine_button.collidepoint((mx,my)):
                selected = "mine"
            elif mortar_button.collidepoint((mx,my)):
                selected = "mortar"
            
        else:
            selected = ""

        SCREEN.blit(exit_image,exit_button)        
        pg.draw.rect(SCREEN, (255, 0, 0), wall_button)
        pg.draw.rect(SCREEN, (0, 255, 0), canon_button)
        pg.draw.rect(SCREEN, (0, 0, 255), mine_button)
        pg.draw.rect(SCREEN, (255, 255, 255), mortar_button)

        #현재 골드 표시
        msg_gold = MYFONT.render("골드 : {}".format(player.gold),True,WHITE)
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
        
        msg_character = MYFONT.render("Character : {}".format(character_list[select]),True,WHITE)
        SCREEN.blit(msg_character,(WIDTH/2,HEIGHT/2 - 200))

        msg_title = MYFONT.render("game_project",True,WHITE)
        SCREEN.blit(msg_title,(WIDTH/2,100))
        
        pg.draw.rect(SCREEN, (255, 0, 0), play_button)
        
        pg.display.flip()
    
main_menu()
pg.quit()
