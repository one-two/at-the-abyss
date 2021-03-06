import libtcodpy as libtcod
from entity import Entity
from render_functions import RenderOrder
from game_messages import Message
from entity import get_blocking_entities_at_location

class Damage_Area:
    def __init__(self, name, x, y, power, delay=0, owner=None, skill='skill', icon='x'):
        self.name = name
        self.skill = skill
        self.x = x
        self.y = y
        self.power = power
        self.delay = delay
        self.time = 0
        self.owner = owner
        self.icon = icon

    def CreateDamageEntity(self, game_map, dmg, entities):
        if not game_map.is_blocked(dmg.x, dmg.y):
            target = get_blocking_entities_at_location(entities, dmg.x, dmg.y)
            dmg_pixel = Entity(dmg.x, dmg.y, self.icon, libtcod.darker_red, 0, 'damage', 200, blocks = False, render_order=RenderOrder.EFFECT, damage=dmg)
            entities.append(dmg_pixel)

    def CauseDamage(self, entities):
        results = []
        for entity in entities:
            if self.x == entity.x and self.y == entity.y and entity.fighter and (self.owner != entity):
                damage = self.power - entity.fighter.defense
                if damage > 0:
                    results.append({'message': Message('{0} ataca {1} com um {2} e mandou {3} de dano.'.format(
                        self.name.capitalize(), entity.name, self.skill, str(round(damage))), libtcod.white)})
                    results.extend(entity.fighter.take_damage(damage))
                else:
                    results.append({'message': Message('{0} ataca {1} com um {2} mas nao bateu nada.'.format(
                        self.name.capitalize(), entity.name, self.skill),  libtcod.white)})
        return results

    