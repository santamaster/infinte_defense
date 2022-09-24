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
    sp.Wall.self_healing = 0
    sp.Mine.gold_cooldown_rate = 1
    sp.Canon.enhanced_attack_chance = 0
    sp.Canon.damage_rate = 1
    sp.Canon.attack_range = 800
    sp.Canon.double_barrel = 0
    sp.Mortar.lavashot = 0
    sp.Mortar.damage_rate = 1
    sp.Mortar.first_attack_cooldown_reduction = 1
    sp.Mortar.attack_cooldown = 1
    sp.MortarShot.time = 1*FPS
    sp.Enemy.damage_rate = 1
    sp.Enemy.get_gold = 0
    sp.Enemy.damaged_by_wall = 0
    ab.effect_list = []

#적 생성 시스템
def enemy_spawn(game_sec,player):
    spawn_location = "left","right"

    #시간이 지날수록 적이 더 빨리 나옴
    if game_sec <= 30:      #30초 이내
        if random()*FPS <= 0.2:  #1초당 0.1마리
            sp.Zombie(choice(spawn_location),player)
            sp.Skeleton(choice(spawn_location),player)
    elif game_sec <= 60:    #30~60초
        if random()*FPS <= 0.3:  #1초당 0.2마리
            sp.Zombie(choice(spawn_location),player)
            sp.Skeleton(choice(spawn_location),player)
    elif game_sec <= 120:   #60~120초
        if random()*FPS <= 0.5:  #1초당 0.5마리
            sp.Zombie(choice(spawn_location),player)
            sp.Skeleton(choice(spawn_location),player)
    else:                   #120초 이후
        if random()*FPS <= 1:    #1초당 1마리
            sp.Zombie(choice(spawn_location),player)
            sp.Skeleton(choice(spawn_location),player)


#자동으로 줄바꿈 및 화면 출력(가운데 정렬)
def blit_text(rect, text, pos, color=BLACK):
    words = sum([word.split(' ') for word in text.splitlines()],[])
    space,height = MYFONT.size(' ')
    lines = []
    max_width = rect.w
    centerx = rect.centerx
    recty = rect.top
    x = 0
    y = pos
    
    k = 0
    for i,word in enumerate(words):
        size = MYFONT.size(word)[0]
        if x + size >= max_width:
            lines.append(' '.join(words[k:i]))
            x = 0
            k = i
        x += size + space
    lines.append(' '.join(words[k:]))
    for line in lines:
        line_surface = MYFONT.render(line, 0, color)
        line_rect = line_surface.get_rect(center=(centerx,recty + y))
        SCREEN.blit(line_surface,line_rect)
        y += height


menu_frame_image = MENU_FRAME
menu_frame = menu_frame_image.get_rect()
menu_frame.center = (WIDTH/2,HEIGHT/2)


goto_main_menu_image = GOTO_MAIN_MENU_BUTTON
goto_main_menu = goto_main_menu_image.get_rect()
goto_main_menu.center = (WIDTH/2+50,HEIGHT/2)


replay_image = REPLAY_BUTTON
replay = replay_image.get_rect()
replay.center = (WIDTH/2-50,HEIGHT/2)

button_image = BUTTON

goto_mainmenu_defeat = button_image.get_rect()
goto_mainmenu_defeat.center = (WIDTH/2,HEIGHT/2)

upgrade_image = UPGRADE_BUTTON
upgrade_button = upgrade_image.get_rect()
sell_image = SELL_BUTTON
sell_button = sell_image.get_rect()

build_image = BUILD_BUTTON
build_button = build_image.get_rect()
build_button.center = (WIDTH-100,HEIGHT-100)

ability_frame = ABILITY_FRAME
outline_ability_frame = OUTLINE_ABILITY_FRAME

ability1 = ability_frame.get_rect()
ability1.center = (WIDTH/4*1,HEIGHT/2)

ability2 = ability_frame.get_rect()
ability2.center = (WIDTH/4*2,HEIGHT/2)

ability3 = ability_frame.get_rect()
ability3.center = (WIDTH/4*3,HEIGHT/2)

coin_image = COIN_IMAGE
coin_rect = coin_image.get_rect()

hp_frame_image = HP_FRAME_IMAGE
hp_frame = hp_frame_image.get_rect(topright=(WIDTH - HP_FRAME_INTERVAL,HP_FRAME_INTERVAL))
#게임
def game():
    player = sp.Player()

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
                ab.get_level_2_ability()
                ability123_list = sample(ab.level_2_ability,3)
            elif player_level == 3:
                ab.get_level_3_ability()
                ability123_list = sample(ab.level_3_ability,3)
            elif player_level == 4:
                ab.get_level_4_ability()
                ability123_list = sample(ab.level_4_ability,3)
            elif player_level == 5:
                ab.get_level_5_ability()
                ability123_list = sample(ab.level_5_ability,3)
            elif player_level == 6:
                ab.get_level_6_ability()
                ability123_list = sample(ab.level_6_ability,3)

            select_ability = 1
            sp.Message("level_up!",GREEN)

        if select_ability:
            camera.darkened_draw()
            SCREEN.blit(ability_frame,ability1)
            blit_text(ability1,ab.ability_info[ability123_list[0]][0],ability1.height/4)
            blit_text(ability1,ab.ability_info[ability123_list[0]][1],ability1.height/2)

            SCREEN.blit(ability_frame,ability2)
            blit_text(ability2,ab.ability_info[ability123_list[1]][0],ability2.height/4)
            blit_text(ability2,ab.ability_info[ability123_list[1]][1],ability2.height/2)

            SCREEN.blit(ability_frame,ability3)
            blit_text(ability3,ab.ability_info[ability123_list[2]][0],ability3.height/4)
            blit_text(ability3,ab.ability_info[ability123_list[2]][1],ability3.height/2)
            if ability1.collidepoint((mx,my)):
                if click:
                    ability123_list[0]()
                    ability_list.append(ability123_list[0])
                    select_ability = 0
                SCREEN.blit(outline_ability_frame,ability1)
            elif ability2.collidepoint((mx,my)):
                if click:
                    ability123_list[1]()
                    ability_list.append(ability123_list[1])
                    select_ability = 0                
                SCREEN.blit(outline_ability_frame,ability2)
                
            elif ability3.collidepoint((mx,my)):
                if click:
                    ability123_list[2]()
                    ability_list.append(ability123_list[2])
                    select_ability = 0
                SCREEN.blit(outline_ability_frame,ability3)
            pg.display.flip()
            continue

        #메뉴 실행시
        if menu:
            #어두워진 화면 그리기(스프라이트 업데이트 안함)
            camera.darkened_draw()

            if click:
                if goto_main_menu.collidepoint((mx,my)):
                    reset()
                    break
                elif replay.collidepoint((mx,my)):
                    reset()
                    player = sp.Player()
                    game_tick = 0
                    menu = 0
                    camera = c.Camera(player)
                    upgrade_sell = 0
                    selected_sprite = None
                    player_level = 1
                    continue

                elif menu_frame.collidepoint((mx,my)):
                    pass
                else:
                    menu = 0
            
            #메뉴 그리기
            SCREEN.blit(menu_frame_image,menu_frame)
            SCREEN.blit(goto_main_menu_image,goto_main_menu)
            SCREEN.blit(replay_image,replay)
            
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
        game_tick += 1

        #효과 업데이트
        if ab.effect_list:
            for effect in ab.effect_list:
                effect.update()
        
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
            upgrade_button.move_ip(0,60)
            SCREEN.blit(upgrade_image,upgrade_button)
            if player.gold >= selected_sprite.upgrade_price:
                msg_upgrade_price = MYFONT.render(str(-selected_sprite.upgrade_price),True,WHITE)
            else:
                msg_upgrade_price = MYFONT.render(str(-selected_sprite.upgrade_price),True,RED)
            msg_upgrade_price_rect = msg_upgrade_price.get_rect(midbottom=selected_sprite.shown_rect.bottomright)
            msg_upgrade_price_rect.move_ip(0,90)
            SCREEN.blit(msg_upgrade_price,msg_upgrade_price_rect)
            
            sell_button.midbottom = selected_sprite.shown_rect.bottomleft
            sell_button.move_ip(0,60)
            SCREEN.blit(sell_image,sell_button)
            msg_sell_price = MYFONT.render(f"+{int(selected_sprite.price * REFUND_RATE)}",True,WHITE)
            msg_sell_price_rect = msg_sell_price.get_rect(midbottom=selected_sprite.shown_rect.bottomleft)
            msg_sell_price_rect.move_ip(0,90)
            SCREEN.blit(msg_sell_price,msg_sell_price_rect)
            
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
        SCREEN.blit(hp_frame_image,hp_frame)#체력바 프레임
        pg.draw.rect(SCREEN,RED,(WIDTH - HP_FRAME_INTERVAL - HP_FRAME_WIDTH*49/50,HP_FRAME_INTERVAL + HP_FRAME_HEIGHT/10, \
            player.hp / player.max_hp * HP_FRAME_WIDTH*24/25,HP_FRAME_HEIGHT*4/5))

        if hp_frame.collidepoint((mx,my)):
            msg_hp = MYFONT.render(f"{player.hp} / {player.max_hp}",True,WHITE)
            SCREEN.blit(msg_hp,(WIDTH - HP_FRAME_INTERVAL - HP_FRAME_WIDTH*49/50,HP_FRAME_INTERVAL + HP_FRAME_HEIGHT/10, \
                HP_FRAME_WIDTH*24/25,HP_FRAME_HEIGHT*4/5))


        #현재 골드 표시
        msg_gold = MYFONT.render(f"골드 : {player.gold}",True,WHITE)
        SCREEN.blit(msg_gold,(10,10))

        #시간 표시
        msg_time = MYFONT.render(f"{game_sec//60}분 {game_sec}초",True,WHITE)
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
            return 1
            
    return 0

exit_image = SELL_BUTTON
exit_button = exit_image.get_rect()
exit_button.center = (WIDTH-100,HEIGHT-100)

building_frame = BUILDING_FRAME
outline_building_frame = OUTLINE_BUILDING_FRAME

wall_button = building_frame.get_rect(center=(125,HEIGHT-150))
wall_rect = WALL_IMAGE.get_rect()
wall_green = fill(WALL_IMAGE,GREEN)
wall_red = fill(WALL_IMAGE,RED)


canon_button = building_frame.get_rect(center=(325,HEIGHT-150))
canon_rect = CANON_IMAGE.get_rect()
canon_green = fill(CANON_IMAGE,GREEN)
canon_red = fill(CANON_IMAGE,RED)

mine_button = building_frame.get_rect(center=(525,HEIGHT-150))
mine_rect = MINE_IMAGE.get_rect()
mine_green = fill(MINE_IMAGE,GREEN)
mine_red = fill(MINE_IMAGE,RED)

mortar_button = building_frame.get_rect(center=(725,HEIGHT-150))
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
        SCREEN.blit(building_frame,wall_button)
        blit_text(wall_button,"장벽",wall_button.height/4,DEEP_PURPLE)
        blit_text(wall_button,f"{sp.Wall.price[0]} 골드",wall_button.height/4*3,DEEP_PURPLE)

        SCREEN.blit(building_frame,canon_button)
        blit_text(canon_button,"대포",canon_button.height/4,DEEP_PURPLE)
        blit_text(canon_button,f"{sp.Canon.price[0]} 골드",canon_button.height/4*3,DEEP_PURPLE)

        SCREEN.blit(building_frame,mine_button)
        blit_text(mine_button,"광산",mine_button.height/4,DEEP_PURPLE)
        blit_text(mine_button,f"{sp.Mine.price[0]} 골드",mine_button.height/4*3,DEEP_PURPLE)

        SCREEN.blit(building_frame,mortar_button)
        blit_text(mortar_button,"박격포",mortar_button.height/4,DEEP_PURPLE)
        blit_text(mortar_button,f"{sp.Mortar.price[0]} 골드",mortar_button.height/4*3,DEEP_PURPLE)

        if wall_button.collidepoint((mx,my)):
            SCREEN.blit(outline_building_frame,wall_button)
        
        elif canon_button.collidepoint((mx,my)):
            SCREEN.blit(outline_building_frame,canon_button)
            
        elif mine_button.collidepoint((mx,my)):
            SCREEN.blit(outline_building_frame,mine_button)
            
        elif mortar_button.collidepoint((mx,my)):
            SCREEN.blit(outline_building_frame,mortar_button)
        #현재 골드 표시
        msg_gold = MYFONT.render("골드 : {}".format(player.gold),True,WHITE)
        SCREEN.blit(msg_gold,(10,10))

        pg.display.flip()


msg_title = MYFONT.render("game_project",True,DEEP_PURPLE)
msg_title_rect = msg_title.get_rect(center=(WIDTH/2,100))

play_image = PLAY_FRAME
play_button = play_image.get_rect(center=(WIDTH/2,HEIGHT/2+100))
msg_play = MYFONT.render("플레이!",True,DEEP_PURPLE)
msg_play_white = MYFONT.render("플레이!",True,WHITE)

msg_play_rect = msg_play.get_rect(center=(WIDTH/2,HEIGHT/2+100))

end_image = PLAY_FRAME
end_button = end_image.get_rect(center=(WIDTH/2,HEIGHT/2+250))
msg_end = MYFONT.render("종료",True,DEEP_PURPLE)
msg_end_white = MYFONT.render("종료",True,WHITE)
msg_end_rect = msg_end.get_rect(center=(WIDTH/2,HEIGHT/2+250))
def main_menu():
    click = 0
    running = 1
    while running:
        
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
            elif event.type == MOUSEBUTTONDOWN:
                click = 1
            elif event.type == MOUSEBUTTONUP:
                click = 0

        mx, my = pg.mouse.get_pos()

        if click:
            if play_button.collidepoint((mx, my)):
                game()
                click = 0
            elif end_button.collidepoint((mx,my)):
                running = 0
                click = 0

        SCREEN.blit(BLURRED_BACKGROUDN_IMAGE,(0,0))
        SCREEN.blit(msg_title,msg_title_rect)
        

        SCREEN.blit(play_image,play_button)
        if play_button.collidepoint((mx,my)):
            SCREEN.blit(msg_play_white,msg_play_rect)      
        else:
            SCREEN.blit(msg_play,msg_play_rect)      

        SCREEN.blit(end_image,end_button)
        if end_button.collidepoint((mx,my)):
            SCREEN.blit(msg_end_white,msg_end_rect) 
        else:
            SCREEN.blit(msg_end,msg_end_rect) 

        pg.display.flip()
    
main_menu()
pg.quit()
