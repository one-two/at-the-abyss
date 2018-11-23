import libtcodpy as libtcod
from game_messages import Message
from components.damage import Damage_Area

class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp

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
            results.append({'message': Message('{0} ataca {1} mas nao bateu nada.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})
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
            dmg0 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*1), round(self.power*1.3), delay=40, owner=self.owner)
            dmg1 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*2), round(self.power*1.3), delay=40, owner=self.owner)
            dmg2 = Damage_Area(self.owner.name, self.owner.x + 1, self.owner.y + (dy*3), round(self.power*1.3), delay=40, owner=self.owner)
            dmg3 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*3), round(self.power*1.3), delay=40, owner=self.owner)
            dmg4 = Damage_Area(self.owner.name, self.owner.x - 1, self.owner.y + (dy*3), round(self.power*1.3), delay=40, owner=self.owner)
            dmg5 = Damage_Area(self.owner.name, self.owner.x + 1, self.owner.y + (dy*4), round(self.power*1.3), delay=40, owner=self.owner)
            dmg6 = Damage_Area(self.owner.name, self.owner.x + 0, self.owner.y + (dy*4), round(self.power*1.3), delay=40, owner=self.owner)
            dmg7 = Damage_Area(self.owner.name, self.owner.x - 1, self.owner.y + (dy*4), round(self.power*1.3), delay=40, owner=self.owner)
        if self.owner.face == 'L' or self.owner.face == 'R':
            if self.owner.face == 'L': dx += 1
            if self.owner.face == 'R': dx -= 1
            trigger = True
            dmg0 = Damage_Area(self.owner.name, self.owner.x + (dx*1), self.owner.y + 0, round(self.power*1.3), delay=40, owner=self.owner)
            dmg1 = Damage_Area(self.owner.name, self.owner.x + (dx*2), self.owner.y + 0, round(self.power*1.3), delay=40, owner=self.owner)
            dmg2 = Damage_Area(self.owner.name, self.owner.x + (dx*3), self.owner.y + 1, round(self.power*1.3), delay=40, owner=self.owner)
            dmg3 = Damage_Area(self.owner.name, self.owner.x + (dx*3), self.owner.y + 0, round(self.power*1.3), delay=40, owner=self.owner)
            dmg4 = Damage_Area(self.owner.name, self.owner.x + (dx*3), self.owner.y - 1, round(self.power*1.3), delay=40, owner=self.owner)
            dmg5 = Damage_Area(self.owner.name, self.owner.x + (dx*4), self.owner.y + 1, round(self.power*1.3), delay=40, owner=self.owner)
            dmg6 = Damage_Area(self.owner.name, self.owner.x + (dx*4), self.owner.y + 0, round(self.power*1.3), delay=40, owner=self.owner)
            dmg7 = Damage_Area(self.owner.name, self.owner.x + (dx*4), self.owner.y - 1, round(self.power*1.3), delay=40, owner=self.owner)

        if trigger:
            dmg0.CreateDamageEntity(game_map, dmg0, entities)
            dmg1.CreateDamageEntity(game_map, dmg1, entities)
            dmg2.CreateDamageEntity(game_map, dmg2, entities)
            dmg3.CreateDamageEntity(game_map, dmg3, entities)
            dmg4.CreateDamageEntity(game_map, dmg4, entities)
            dmg5.CreateDamageEntity(game_map, dmg5, entities)
            dmg6.CreateDamageEntity(game_map, dmg6, entities)
            dmg7.CreateDamageEntity(game_map, dmg7, entities)

