import pygame as pg
from setting import *
import sprites as sp

#플레이어 체력 회복
def player_health_recovery():
    sp.Message("체력이 회복되었습니다.",WHITE)
    for sprite in sp.player_sprites:
        sprite.hp = sprite.max_hp

#대포 공격력 증가
def canon_increase_damage():
    sp.Message("대포의 공격력이 상승하였습니다.",WHITE)
    sp.Canon.damage_rate *= 1.3

#대포 강화된 공격
def canon_enhanced_attack():
    sp.Message("이제부터 대포가 강화된 공격을 사용할 수 있습니다.",WHITE)
    sp.Canon.enhanced_attack_chance = 0.5

#광산 채굴 속도 향상
def mine_faster():
    sp.Message("광산 채굴 속도 향상",WHITE)
    sp.Mine.gold_cooldown_rate *= 0.8

#장벽 자가 치유
def wall_self_healing():
    sp.Message("장벽 자가 치유",WHITE)
    sp.Wall.self_healing = 1

#골드 획득
def get_gold():
    sp.Message("골드를 획득하였습니다.")
    for sprite in sp.player_sprites:
        sprite.gold += 1000
        sprite.total_gold += 1000

#적 데미지 감소
def reduce_enemy_damage():
    sp.Enemy.damage_rate = 0.8




level_2_ability = [mine_faster,canon_increase_damage,wall_self_healing]
level_3_ability = [canon_increase_damage,canon_enhanced_attack,mine_faster]
level_4_ability = [canon_increase_damage,canon_enhanced_attack,mine_faster]
level_5_ability = [canon_increase_damage,canon_enhanced_attack,mine_faster]
level_6_ability = [canon_increase_damage,canon_enhanced_attack,mine_faster]

