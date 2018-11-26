import libtcodpy as libtcod
import math
from components.fighter import Fighter
from components.ai import *
from random import randint
from entity import Entity
from render_functions import RenderOrder
from components.damage import Damage_Area

def UseSkill(weapon, player, game_map, entities):
    dx, dy = player.lastmove
    if weapon == 'dagger':
        dmg = Damage_Area(player.name, player.x + dx, player.y + dy, player.fighter.power, delay=40, owner=player, skill='corte')
        dmg2 = Damage_Area(player.name, player.x + (dx*2), player.y + (dy*2), player.fighter.power, delay=40, owner=player, skill='corte')
        dmg.CreateDamageEntity(game_map, dmg, entities)
        dmg2.CreateDamageEntity(game_map, dmg2, entities)

    if weapon.endswith('spear'):
        dmg = Damage_Area(player.name, player.x + dx, player.y + dy, player.fighter.power*0.9, delay=40, owner=player, skill='estocada')
        dmg2 = Damage_Area(player.name, player.x + (dx*2), player.y + (dy*2), player.fighter.power*0.9, delay=40, owner=player, skill='estocada')
        dmg3 = Damage_Area(player.name, player.x + (dx*3), player.y + (dy*3), player.fighter.power*0.9, delay=40, owner=player, skill='estocada')
        dmg4 = Damage_Area(player.name, player.x + (dx*4), player.y + (dy*4), player.fighter.power*0.9, delay=40, owner=player, skill='estocada')
        dmg5 = Damage_Area(player.name, player.x + (dx*5), player.y + (dy*5), player.fighter.power*0.9, delay=40, owner=player, skill='estocada')
        dmg.CreateDamageEntity(game_map, dmg, entities)
        dmg2.CreateDamageEntity(game_map, dmg2, entities)
        dmg3.CreateDamageEntity(game_map, dmg3, entities)
        dmg4.CreateDamageEntity(game_map, dmg4, entities)
        dmg5.CreateDamageEntity(game_map, dmg5, entities)

    if weapon.endswith('sword'):
        if (dx != 0):
            dmg0 = Damage_Area(player.name, player.x + (dx*2), player.y - 1, player.fighter.power*0.8, delay=20, owner=player, skill='golpe forte')
            dmg1 = Damage_Area(player.name, player.x + (dx*2), player.y + 0, player.fighter.power*0.8, delay=30, owner=player, skill='golpe forte')
            dmg2 = Damage_Area(player.name, player.x + (dx*2), player.y + 1, player.fighter.power*0.8, delay=40, owner=player, skill='golpe forte')
            dmg6 = Damage_Area(player.name, player.x + (dx*3), player.y + 0, player.fighter.power*0.8, delay=30, owner=player, skill='golpe forte')
            dmg3 = Damage_Area(player.name, player.x + (dx), player.y - 1, player.fighter.power*0.8, delay=20, owner=player, skill='golpe forte')
            dmg4 = Damage_Area(player.name, player.x + (dx), player.y + 0, player.fighter.power*0.8, delay=30, owner=player, skill='golpe forte')
            dmg5 = Damage_Area(player.name, player.x + (dx), player.y + 1, player.fighter.power*0.8, delay=40, owner=player, skill='golpe forte')
        if (dy != 0):
            dmg0 = Damage_Area(player.name, player.x - 1, player.y + (dy*2), player.fighter.power*0.8, delay=20, owner=player, skill='golpe forte')
            dmg1 = Damage_Area(player.name, player.x + 0, player.y + (dy*2), player.fighter.power*0.8, delay=30, owner=player, skill='golpe forte')
            dmg2 = Damage_Area(player.name, player.x + 1, player.y + (dy*2), player.fighter.power*0.8, delay=40, owner=player, skill='golpe forte')
            dmg6 = Damage_Area(player.name, player.x + 0, player.y + (dy*3), player.fighter.power*0.8, delay=30, owner=player, skill='golpe forte')
            dmg3 = Damage_Area(player.name, player.x - 1, player.y + dy, player.fighter.power*0.8, delay=20, owner=player, skill='golpe forte')
            dmg4 = Damage_Area(player.name, player.x + 0, player.y + dy, player.fighter.power*0.8, delay=30, owner=player, skill='golpe forte')
            dmg5 = Damage_Area(player.name, player.x + 1, player.y + dy, player.fighter.power*0.8, delay=40, owner=player, skill='golpe forte')
        dmg0.CreateDamageEntity(game_map, dmg0, entities)
        dmg1.CreateDamageEntity(game_map, dmg1, entities)
        dmg2.CreateDamageEntity(game_map, dmg2, entities)
        dmg3.CreateDamageEntity(game_map, dmg3, entities)        
        dmg4.CreateDamageEntity(game_map, dmg4, entities)
        dmg5.CreateDamageEntity(game_map, dmg5, entities)
        dmg6.CreateDamageEntity(game_map, dmg6, entities)
        