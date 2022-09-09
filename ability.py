import pygame as pg
from setting import *
import sprites as sp


def health_recovery():
    sp.Message("your hp is recovered",WHITE)
    for sprite in sp.player_sprites:
        sprite.hp = sprite.max_hp

def canon_increase_damage():
    sp.Message("canon damage is increased",WHITE)
    for attack_dmg in sp.Canon.attack_dmg:
        attack_dmg *= 1.5
    for sprite in sp.canon_sprites:
        sprite.attack_dmg  *= 1.5

def canon_enhanced_attack():
    sp.Message("canon enhanced attack avaliable",WHITE)
    sp.Canon.enhanced_attack_chance = 0.5


level_2_ability = [health_recovery,canon_increase_damage,canon_enhanced_attack]
