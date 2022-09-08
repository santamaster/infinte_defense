import pygame as pg
from setting import *
import sprites as sp

def health_recovery(player):
    player.hp = player.max_hp

def canon_increase_damage(sprite_group):
    for sprite in sprite_group:
        sprite.attack_dmg *= 1.1
    for dmg in CANON_DMG:
        dmg *= 1.1

def canon_enhanced_attack(sprite_group):
    for sprite in sprite_group:
        sprite.enhanced_attack = 1
    ENHANCED_ATTACK = 1