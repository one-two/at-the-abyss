import libtcodpy as libtcod
import math
from components.fighter import Fighter
from components.ai import *
from random import randint
from entity import Entity
from render_functions import RenderOrder

def CreateMonster(monster_choice, x, y):
    if monster_choice == 'orc':
        fighter_component = Fighter(hp=20, defense=0, power=4, xp=35)
        ai_component = Orc()
        monster = Entity(x,y, 'o', libtcod.desaturated_green, 0,  'orc' + fighter_component.rank, 300, blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
        return monster
    elif monster_choice == 'troll':
        fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
        ai_component = Troll()
        monster = Entity(x,y, 'T', libtcod.darker_green, 0, 'troll', 200, blocks = True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
        return monster
    elif monster_choice == 'wyvern':
        fighter_component = Fighter(hp=20, defense=0, power=5, xp=40)
        ai_component = Wyvern()
        monster = Entity(x,y, 'w', libtcod.dark_violet, 0, 'wyvern', 200, blocks = True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
        return monster
    elif monster_choice == 'ranger':
        fighter_component = Fighter(hp=40, defense=1, power=7, xp=40)
        ai_component = Ranger()
        monster = Entity(x,y, 'r', libtcod.dark_sepia, 0, 'ranger', 200, blocks = True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
        return monster
    elif monster_choice == 'dragon':
        fighter_component = Fighter(hp=100, defense=5, power=16, xp=300)
        ai_component = Dragon()
        monster = Entity(x,y, 'D', libtcod.crimson, 0, 'dragao', 200, blocks = True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
        return monster