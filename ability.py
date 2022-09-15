import pygame as pg
from setting import *
import sprites as sp

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

"""----------장벽----------"""
#장벽 자가 치유
def wall_self_healing():
    sp.Message("장벽 자가 치유")
    sp.Wall.self_healing = 1

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
    
"""----------박격포----------"""
#박격포 용암 공격
def lava_shot():
    sp.Message("박격포의 공격력이 감소하지만 포탄이 용암 지대를 만듭니다.")
    sp.Mortar.lavashot = 1
    sp.Mortar.damage_rate = 0.7

"""----------광산----------"""
#광산 채굴 속도 향상
def mine_faster():
    sp.Message("광산 채굴 속도 향상")
    sp.Mine.gold_cooldown_rate *= 0.8




level_2_ability = [mine_faster,canon_increase_damage,wall_self_healing]
level_3_ability = [canon_increase_damage,canon_enhanced_attack,mine_faster]
level_4_ability = [canon_increase_damage,canon_enhanced_attack,mine_faster]
level_5_ability = [canon_increase_damage,canon_enhanced_attack,mine_faster]
level_6_ability = [canon_increase_damage,canon_enhanced_attack,mine_faster]

ability_info = {player_health_recovery:"플레이어의 체력을 최대로 회복합니다",\
                get_gold:"1000골드를 획득합니다",\
                reduce_enemy_damage:"적의 공격력이 20% 감소합니다.",\

                wall_self_healing:"장벽이 매초 1%씩 체력을 회복합니다.",\

                canon_increase_damage:"대포의 공격력이 30% 증가합니다.",\
                canon_enhanced_attack:"대포가 공격시 20% 확률로 2배로 증가한 공격을 날립니다.",\
                canon_infite_range:"대포의 사정거리가 무제한이 됩니다.",\

                lava_shot:"박격포의 공격력이 30% 감소하지만 박격포의 포탄이 용암지대를 만듭니다.",\

                mine_faster:"광산의 채굴 속도가 20% 빨라집니다.",\

                }