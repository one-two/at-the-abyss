import libtcodpy as libtcod
from game_messages import Message
from components.damage import Damage_Area
from random import randint
import math

def monsterrank(bonus):
    prefix = ''
    if bonus >= -15:
        prefix = ' inutil'
    if bonus > -10:
        prefix = ' fracote'
    if bonus > -5:
        prefix = ' fraco'
    if bonus > 0:
        prefix = ''
    if bonus > 5:
        prefix = ' forte'
    if bonus > 10:
        prefix = ' fortasso'
    if bonus >= 15:
        prefix = ' poderoso'
    return prefix

class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        bonus = randint(-15, 15)/100
        self.rank = monsterrank(bonus*100)
        self.base_max_hp = hp + math.ceil(hp*bonus)
        self.hp = self.base_max_hp
        self.base_defense = defense + math.ceil(defense*bonus)
        self.base_power = power + math.ceil(power*bonus)
        self.xp = xp + math.ceil(xp*bonus)

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            results.append({'dead' : self.owner, 'xp': self.xp})
        return results

    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{0} ataca {1} e mandou {2} de dano.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} ataca {1}, mas defendeu. 1 de dano.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})
            results.extend(target.fighter.take_damage(1))
        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def bash(self, target, game_map, entities):
        dx, dy = 0, 0
        trigger = False
        if self.owner.face == 'U' or self.owner.face == 'D':
            if self.owner.face == 'U': dy -= 1
            if self.owner.face == 'D': dy += 1
            trigger = True
            dmg0 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*1), round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg1 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*2), round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg2 = Damage_Area(self.owner.name, self.owner.x + 1, self.owner.y + (dy*3), round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg3 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*3), round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg4 = Damage_Area(self.owner.name, self.owner.x - 1, self.owner.y + (dy*3), round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg5 = Damage_Area(self.owner.name, self.owner.x + 1, self.owner.y + (dy*4), round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg6 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*4), round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg7 = Damage_Area(self.owner.name, self.owner.x - 1, self.owner.y + (dy*4), round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
        if self.owner.face == 'L' or self.owner.face == 'R':
            if self.owner.face == 'L': dx += 1
            if self.owner.face == 'R': dx -= 1
            trigger = True
            dmg0 = Damage_Area(self.owner.name, self.owner.x + (dx*1), self.owner.y + 0, round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg1 = Damage_Area(self.owner.name, self.owner.x + (dx*2), self.owner.y + 0, round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg2 = Damage_Area(self.owner.name, self.owner.x + (dx*3), self.owner.y + 1, round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg3 = Damage_Area(self.owner.name, self.owner.x + (dx*3), self.owner.y + 0, round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg4 = Damage_Area(self.owner.name, self.owner.x + (dx*3), self.owner.y - 1, round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg5 = Damage_Area(self.owner.name, self.owner.x + (dx*4), self.owner.y + 1, round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg6 = Damage_Area(self.owner.name, self.owner.x + (dx*4), self.owner.y + 0, round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')
            dmg7 = Damage_Area(self.owner.name, self.owner.x + (dx*4), self.owner.y - 1, round(self.power*1.4), delay=40, owner=self.owner, skill='tremor')

        if trigger:
            dmg0.CreateDamageEntity(game_map, dmg0, entities)
            dmg1.CreateDamageEntity(game_map, dmg1, entities)
            dmg2.CreateDamageEntity(game_map, dmg2, entities)
            dmg3.CreateDamageEntity(game_map, dmg3, entities)
            dmg4.CreateDamageEntity(game_map, dmg4, entities)
            dmg5.CreateDamageEntity(game_map, dmg5, entities)
            dmg6.CreateDamageEntity(game_map, dmg6, entities)
            dmg7.CreateDamageEntity(game_map, dmg7, entities)

    def slap(self, target, game_map, entities):
        dx, dy = 0, 0
        trigger = False
        if self.owner.face == 'U' or self.owner.face == 'D':
            if self.owner.face == 'U': dy -= 1
            if self.owner.face == 'D': dy += 1
            trigger = True
            dmg0 = Damage_Area(self.owner.name, self.owner.x - 1, self.owner.y + (dy*1), round(self.power*1.3), delay=40, owner=self.owner, skill='tapao')
            dmg1 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*1), round(self.power*1.3), delay=40, owner=self.owner, skill='tapao')
            dmg2 = Damage_Area(self.owner.name, self.owner.x + 1, self.owner.y + (dy*1), round(self.power*1.3), delay=40, owner=self.owner, skill='tapao')
        if self.owner.face == 'L' or self.owner.face == 'R':
            if self.owner.face == 'L': dx += 1
            if self.owner.face == 'R': dx -= 1
            trigger = True
            dmg0 = Damage_Area(self.owner.name, self.owner.x + (dx*1), self.owner.y - 1, round(self.power*1.3), delay=40, owner=self.owner, skill='tapao')
            dmg1 = Damage_Area(self.owner.name, self.owner.x + (dx*1), self.owner.y + 0, round(self.power*1.3), delay=40, owner=self.owner, skill='tapao')
            dmg2 = Damage_Area(self.owner.name, self.owner.x + (dx*1), self.owner.y + 1, round(self.power*1.3), delay=40, owner=self.owner, skill='tapao')

        if trigger:
            dmg0.CreateDamageEntity(game_map, dmg0, entities)
            dmg1.CreateDamageEntity(game_map, dmg1, entities)
            dmg2.CreateDamageEntity(game_map, dmg2, entities)

    def fire_cone(self, target, game_map, entities):
        dx, dy = 0, 0
        trigger = False
        if self.owner.face == 'U' or self.owner.face == 'D':
            if self.owner.face == 'U': dy -= 1
            if self.owner.face == 'D': dy += 1
            trigger = True
            dmg0 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*1), round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg1 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*2), round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg2 = Damage_Area(self.owner.name, self.owner.x + 1, self.owner.y + (dy*3), round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg3 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*3), round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg4 = Damage_Area(self.owner.name, self.owner.x - 1, self.owner.y + (dy*3), round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg5 = Damage_Area(self.owner.name, self.owner.x + 1, self.owner.y + (dy*4), round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg6 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*4), round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg7 = Damage_Area(self.owner.name, self.owner.x - 1, self.owner.y + (dy*4), round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg8 = Damage_Area(self.owner.name, self.owner.x + 2, self.owner.y + (dy*5), round(self.power*1.3), delay=50, owner=self.owner, skill='fogo', icon='f')
            dmg9 = Damage_Area(self.owner.name, self.owner.x + 1, self.owner.y + (dy*5), round(self.power*1.3), delay=50, owner=self.owner, skill='fogo', icon='f')
            dmg10= Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*5), round(self.power*1.3), delay=50, owner=self.owner, skill='fogo', icon='f')
            dmg11= Damage_Area(self.owner.name, self.owner.x - 1, self.owner.y + (dy*5), round(self.power*1.3), delay=50, owner=self.owner, skill='fogo', icon='f')
            dmg12= Damage_Area(self.owner.name, self.owner.x - 2, self.owner.y + (dy*5), round(self.power*1.3), delay=50, owner=self.owner, skill='fogo', icon='f')
        if self.owner.face == 'L' or self.owner.face == 'R':
            if self.owner.face == 'L': dx += 1
            if self.owner.face == 'R': dx -= 1
            trigger = True
            dmg0 = Damage_Area(self.owner.name, self.owner.x + (dx*1), self.owner.y + 0, round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg1 = Damage_Area(self.owner.name, self.owner.x + (dx*2), self.owner.y + 0, round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg2 = Damage_Area(self.owner.name, self.owner.x + (dx*3), self.owner.y + 1, round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg3 = Damage_Area(self.owner.name, self.owner.x + (dx*3), self.owner.y + 0, round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg4 = Damage_Area(self.owner.name, self.owner.x + (dx*3), self.owner.y - 1, round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg5 = Damage_Area(self.owner.name, self.owner.x + (dx*4), self.owner.y + 1, round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg6 = Damage_Area(self.owner.name, self.owner.x + (dx*4), self.owner.y + 0, round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg7 = Damage_Area(self.owner.name, self.owner.x + (dx*4), self.owner.y - 1, round(self.power*1.3), delay=40, owner=self.owner, skill='fogo', icon='f')
            dmg8 = Damage_Area(self.owner.name, self.owner.x + (dx*5), self.owner.y + 2, round(self.power*1.3), delay=50, owner=self.owner, skill='fogo', icon='f')
            dmg9 = Damage_Area(self.owner.name, self.owner.x + (dx*5), self.owner.y + 1, round(self.power*1.3), delay=50, owner=self.owner, skill='fogo', icon='f')
            dmg10= Damage_Area(self.owner.name, self.owner.x + (dx*5), self.owner.y - 0, round(self.power*1.3), delay=50, owner=self.owner, skill='fogo', icon='f')
            dmg11= Damage_Area(self.owner.name, self.owner.x + (dx*5), self.owner.y - 1, round(self.power*1.3), delay=50, owner=self.owner, skill='fogo', icon='f')
            dmg12= Damage_Area(self.owner.name, self.owner.x + (dx*5), self.owner.y - 2, round(self.power*1.3), delay=50, owner=self.owner, skill='fogo', icon='f')

        if trigger:
            dmg0.CreateDamageEntity(game_map, dmg0, entities)
            dmg1.CreateDamageEntity(game_map, dmg1, entities)
            dmg2.CreateDamageEntity(game_map, dmg2, entities)
            dmg3.CreateDamageEntity(game_map, dmg3, entities)
            dmg4.CreateDamageEntity(game_map, dmg4, entities)
            dmg5.CreateDamageEntity(game_map, dmg5, entities)
            dmg6.CreateDamageEntity(game_map, dmg6, entities)
            dmg7.CreateDamageEntity(game_map, dmg7, entities)
            dmg8.CreateDamageEntity(game_map, dmg8, entities)
            dmg9.CreateDamageEntity(game_map, dmg9, entities)
            dmg10.CreateDamageEntity(game_map, dmg10, entities)
            dmg11.CreateDamageEntity(game_map, dmg11, entities)
            dmg12.CreateDamageEntity(game_map, dmg12, entities)