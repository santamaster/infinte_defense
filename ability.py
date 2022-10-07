import pygame as pg
from setting import *
import sprites as sp
import random
"""현재 능력 갯수 : 16"""

effect_list = []
#플레이어 체력 회복
def player_health_recovery():
    sp.Message("체력이 회복되었습니다.")
    for sprite in sp.player_sprites:
        sprite.hp = sprite.max_hp

#골드 획득
def get_gold():
    sp.Message("골드를 획득하였습니다.")
    for sprite in sp.player_sprites:
        sprite.gold += 1000
        sprite.total_gold += 1000

#적 데미지 감소
def reduce_enemy_damage():
    sp.Message("적이 입히는 피해가 감소합니다.")
    sp.Enemy.damage_rate = 0.8

#플레이어 얻는 골드 증가
def get_more_gold():
    sp.Message("플레이어가 1초당 얻는 골드가 3배로 증가합니다.")
    for sprite in sp.player_sprites:
        sprite.gold_output *= 3  
    
#적을 죽일 시 골드 획득
def get_gold_when_kill_enemy():
    sp.Message("적을 죽이면 15 골드를 획득합니다.")
    sp.Enemy.get_gold = 1

class Poison:
    interval = 1*FPS
    def __init__(self):
        effect_list.append(self)
        self.counter = 0
    def update(self):
        self.counter += 1
        if self.counter >= Poison.interval:
            for sprite in sp.enemy_sprites:
                sprite.hp -= sprite.max_hp * 0.05
            self.counter = 0 
#체력 감소
def poisoning():
    sp.Message("매초 적이 최대 체력의 5%만큼의 피해를 입습니다.")
    Poison()

class Build_gold:
    interval = 1*FPS
    def __init__(self):
        effect_list.append(self)
        self.counter = 0
    def update(self):
        self.counter += 1
        if self.counter >= Build_gold.interval:
            for sprite in sp.player_sprites:
                sprite.gold += len(sp.building_sprites)
            self.counter = 0

def building_gold():
    sp.Message("매초 건물 수만큼의 골드를 획득합니다.")
    Build_gold()

"""----------장벽----------"""
#장벽 자가 치유
def wall_self_healing():
    sp.Message("장벽 자가 치유")
    sp.Wall.self_healing = 1

#가시장벽
def attacking_wall():
    sp.Message("장벽을 공격한 적은 피해를 입습니다.")
    sp.Enemy.damaged_by_wall = 1
"""----------대포----------"""
#대포 공격력 증가
def canon_increase_damage():
    sp.Message("대포의 공격력이 상승하였습니다.")
    sp.Canon.damage_rate *= 1.3

#대포 강화된 공격
def canon_enhanced_attack():
    sp.Message("이제부터 대포가 강화된 공격을 사용할 수 있습니다.")
    sp.Canon.enhanced_attack_chance = 0.2

#사정거리 무제한
def canon_infite_range():
    sp.Message("대포의 사정거리가 무제한이 됩니다.")
    sp.Canon.attack_range = BG_WIDTH
    
def double_barrel():
    sp.Message("대포의 공격력이 감소하지만 연속해서 2번 공격합니다.")
    sp.Canon.double_barrel = 1
    sp.Canon.damage_rate *= 0.6

"""----------박격포----------"""
def lava_shot():
    sp.Message("박격포의 공격력이 감소하지만 포탄이 용암 지대를 만듭니다.")
    sp.Mortar.lavashot = 1
    sp.Mortar.damage_rate = 0.6

def fast_shot():
    sp.Message("박격포의 재사용 대기시간이 30% 감소합니다.")
    sp.Mortar.first_attack_cooldown_reduction *= 0.7
    sp.Mortar.attack_cooldown_reduction *= 0.7

"""----------광산----------"""
#광산 채굴 속도 향상
def mine_faster():
    sp.Message("광산 채굴 속도 향상")
    sp.Mine.gold_cooldown_rate *= 0.7




player_ability_list = []

level_2_ability = [canon_increase_damage,canon_enhanced_attack,double_barrel,\
    get_gold_when_kill_enemy,building_gold]
def get_level_2_ability():
    if len(sp.mine_sprites) >= 2:
        level_2_ability.append(mine_faster)
    if len(sp.wall_sprites) >= 2:
        level_2_ability.append(wall_self_healing)
        level_2_ability.append(attacking_wall)
    pass

level_3_ability = [get_gold, get_more_gold,get_gold_when_kill_enemy,poisoning,building_gold,wall_self_healing,attacking_wall,canon_increase_damage,\
    canon_enhanced_attack,canon_infite_range,double_barrel,lava_shot,fast_shot,mine_faster]
def get_level_3_ability():

    #겹치는 능력 제거
    for ability in player_ability_list:
        if ability in level_3_ability:
            level_3_ability.remove(ability)


level_4_ability = [get_gold,reduce_enemy_damage, get_more_gold,get_gold_when_kill_enemy,poisoning,building_gold,wall_self_healing,attacking_wall,canon_increase_damage,\
    canon_enhanced_attack,canon_infite_range,double_barrel,lava_shot,fast_shot,mine_faster]
def get_level_4_ability():
    #플레이어 체력이 50% 이하일 때
    for player in sp.player_sprites:
        if player.hp/player.max_hp <= 0.5:
            level_4_ability.append(player_health_recovery)

    #겹치는 능력 제거
    for ability in player_ability_list:
        if ability in level_4_ability:
            level_4_ability.remove(ability)

level_5_ability = [get_gold,reduce_enemy_damage, get_more_gold,get_gold_when_kill_enemy,poisoning,building_gold,wall_self_healing,attacking_wall,canon_increase_damage,\
    canon_enhanced_attack,canon_infite_range,double_barrel,lava_shot,fast_shot,mine_faster]
def get_level_5_ability():
    #플레이어 체력이 50% 이하일 때
    for player in sp.player_sprites:
        if player.hp/player.max_hp <= 0.5:
            level_5_ability.append(player_health_recovery)


    #겹치는 능력 제거
    for ability in player_ability_list:
        if ability in level_5_ability:
            level_5_ability.remove(ability)

level_6_ability = [get_gold,reduce_enemy_damage, get_more_gold,get_gold_when_kill_enemy,poisoning,building_gold,wall_self_healing,attacking_wall,canon_increase_damage,\
    canon_enhanced_attack,canon_infite_range,double_barrel,lava_shot,fast_shot,mine_faster]
def get_level_6_ability():
    #플레이어 체력이 50% 이하일 때
    for player in sp.player_sprites:
        if player.hp/player.max_hp <= 0.5:
            level_6_ability.append(player_health_recovery)

    #겹치는 능력 제거
    for ability in player_ability_list:
        if ability in level_6_ability:
            level_6_ability.remove(ability)

ability_info = {player_health_recovery:["체력 회복","플레이어의 체력을 최대로 회복합니다"],\
                get_gold:["일확천금","1000골드를 획득합니다"],\
                reduce_enemy_damage:["적 약화","적의 공격력이 20% 감소합니다."],\
                get_more_gold:["연금술사","플레이어가 1초당 얻는 골드가 3배 증가합니다."],\
                get_gold_when_kill_enemy:["수금","적을 죽이면 15 골드를 획득합니다."],\
                poisoning:["중독","매초 적이 최대 체력의 5%만큼 피해를 입습니다."],\
                building_gold:["생산 기지","매초 건물 수만큼의 골드를 획득합니다."],\

                wall_self_healing:["자가 회복","장벽이 매초 1%씩 체력을 회복합니다."],\
                attacking_wall:["가시 장벽","장벽을 공격한 적은 20의 피해를 입습니다."],\

                canon_increase_damage:["공격 강화","대포의 공격력이 30% 증가합니다."],\
                canon_enhanced_attack:["강화된 공격","대포가 공격시 20% 확률로 2배로 증가한 공격을 날립니다."],\
                canon_infite_range:["사정거리 무한","대포의 사정거리가 무제한이 됩니다."],\
                double_barrel:["더블 배럴","대포의 공격력이 40% 감소하지만 연속해서 2번 공격합니다."],\

                lava_shot:["용암 발사","박격포의 공격력이 40% 감소하지만 박격포의 포탄이 용암지대를 만듭니다."],\
                fast_shot:["빠른 공격","박격포의 재사용 대기시간이 30% 감소합니다."],\
                mine_faster:["가속","광산의 채굴 속도가 30% 빨라집니다."],\

                }

