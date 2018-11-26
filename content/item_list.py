import libtcodpy as libtcod
import math
from components.equippable import Equippable
from components.item import Item
from components.ai import *
from random import randint
from entity import Entity
from render_functions import RenderOrder
from components.equipment import EquipmentSlots

from item_functions import heal

def CreateItem(name, x, y, dungeon_level):
    bonus = randint(-20, 20)
    base = randint(0,dungeon_level//3)
    if base == 0: prefix = ''
    else: prefix = '+' + str(base) + ' '
    if bonus >= -20:
        prefix += 'rotten '
    elif bonus > -15:
        prefix += 'useless '
    elif bonus > -10:
        prefix += 'weak '
    elif bonus > -5:
        prefix += 'bad '
    elif bonus > 0:
        prefix += ''
    elif bonus > 5:
        prefix += 'good '
    elif bonus > 10:
        prefix += 'strong '
    elif bonus >= 15:
        prefix += 'powerful '
    elif bonus >= 20:
        prefix += 'overwhelming '

    bonus = bonus/100    

    if name == 'healing_potion':    
        item_component = Item(use_function=heal, amount=40 + math.ceil(40*bonus))
        item = Entity(x,y, '!', libtcod.violet, 0, prefix + 'possao', 0, render_order=RenderOrder.ITEM, item=item_component)
        return item
    #weapons
    elif name == 'spear':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3 + base + round((3+base)*bonus) , name=prefix + 'spear', cooldown=50)
        item = Entity(x, y, '/', libtcod.sky, 0, prefix + 'spear', equippable=equippable_component)
        return item
    elif name == 'sword':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2 + base + round((2+base)*bonus), name=prefix + 'sword', cooldown=50)
        item = Entity(x, y, '+', libtcod.sky, 0, prefix + 'sword', equippable=equippable_component)
        return item
    #shields
    elif name == 'shield':
        equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1 + round((1+base//2)*bonus) + base//2, name=prefix + 'shield')
        item = Entity(x, y, '[', libtcod.darker_orange, 0, prefix + 'shield', equippable=equippable_component)
        return item