import math
import random
from entity import get_blocking_entities_at_location

def ChangeFace(player, monster):
    distx = monster.x - player.x
    disty = monster.y - player.y

    if abs(disty) < abs(distx):
        if distx < 0:
            return 'L'
        else:
            return 'R'
    else:
        if disty < 0:
            return 'D'
        else:
            return 'U'

class Troll:
    def act(self, player, fov_map, game_map, entities):
        results = []
        mx = random.choice([-1, 0, 1]) 
        my = random.choice([-1, 0, 1])
        monster = self.owner
        destx = monster.x + mx
        desty = monster.y + my
        if monster.distance_to(player) < 9:
            monster.move_astar(player, entities, game_map)
            monster.stamina = round(monster.maxStamina * 0.7)
            if monster.distance_to(player) < 6:
                if random.randint(1, 6) > 1:
                    monster.fighter.bash(player, game_map, entities)
            if monster.distance_to(player) < 3:
                attack_results = monster.fighter.attack(player)
                results.extend(attack_results)
        else:
            if not game_map.is_blocked(destx, desty):
                target = get_blocking_entities_at_location(entities, destx, desty)
                if target == None:
                    monster.move(mx, my)
            else:
                target = get_blocking_entities_at_location(entities, destx*-1, desty*-1)
                if target == None:
                    monster.move(mx*-1, my*-1)
        monster.face = ChangeFace(player, monster)

        return(results)
        fov_recompute = True

class Orc:
    def act(self, player, fov_map, game_map, entities):
        results = []
        mx = random.choice([-1, 0, 1]) 
        my = random.choice([-1, 0, 1])
        monster = self.owner
        destx = monster.x + mx
        desty = monster.y + my
        if monster.distance_to(player) < 9:
            monster.move_astar(player, entities, game_map)
            monster.stamina = round(monster.maxStamina * 0.7)
            if monster.distance_to(player) < 3:
                if random.randint(1, 6) > 4:
                    monster.fighter.slap(player, game_map, entities)
                    pass
            if monster.distance_to(player) < 2:
                attack_results = monster.fighter.attack(player)
                results.extend(attack_results)
        else:
            if not game_map.is_blocked(destx, desty):
                target = get_blocking_entities_at_location(entities, destx, desty)
                if target == None:
                    monster.move(mx, my)
            else:
                target = get_blocking_entities_at_location(entities, destx*-1, desty*-1)
                if target == None:
                    monster.move(mx*-1, my*-1)
        monster.face = ChangeFace(player, monster)

        return(results)
        fov_recompute = True

class Dragon:
    def act(self, player, fov_map, game_map, entities):
        results = []
        mx = random.choice([-1, 0, 1]) 
        my = random.choice([-1, 0, 1])
        monster = self.owner
        destx = monster.x + mx
        desty = monster.y + my
        if monster.distance_to(player) < 8:
            monster.stamina = round(monster.maxStamina * 0.7)
            if monster.distance_to(player) < 8:
                if random.randint(1, 6) > 4:
                    monster.fighter.fire_cone(player, game_map, entities)
                else:
                    monster.move_astar(player, entities, game_map)
            if monster.distance_to(player) < 2:
                attack_results = monster.fighter.attack(player)
                results.extend(attack_results)
        else:
            if not game_map.is_blocked(destx, desty):
                target = get_blocking_entities_at_location(entities, destx, desty)
                if target == None:
                    monster.move(mx, my)
            else:
                target = get_blocking_entities_at_location(entities, destx*-1, desty*-1)
                if target == None:
                    monster.move(mx*-1, my*-1)
        monster.face = ChangeFace(player, monster)

        return(results)
        fov_recompute = True

class Wyvern:
    def act(self, player, fov_map, game_map, entities):
        results = []
        mx = random.choice([-1, 0, 1]) 
        my = random.choice([-1, 0, 1])
        monster = self.owner
        destx = monster.x + mx
        desty = monster.y + my
        if monster.distance_to(player) < 9:
            monster.stamina = round(monster.maxStamina * 0.7)
            if monster.distance_to(player) < 9:
                if random.randint(1, 6) > 4:
                    monster.fighter.windblow(player, game_map, entities)
                    pass
                else:
                    monster.move_astar(player, entities, game_map)
            if monster.distance_to(player) < 2:
                attack_results = monster.fighter.attack(player)
                results.extend(attack_results)
        else:
            if not game_map.is_blocked(destx, desty):
                target = get_blocking_entities_at_location(entities, destx, desty)
                if target == None:
                    monster.move(mx, my)
            else:
                target = get_blocking_entities_at_location(entities, destx*-1, desty*-1)
                if target == None:
                    monster.move(mx*-1, my*-1)
        monster.face = ChangeFace(player, monster)

        return(results)
        fov_recompute = True

class Ranger:
    def act(self, player, fov_map, game_map, entities):
        results = []
        mx = random.choice([-1, 0, 1]) 
        my = random.choice([-1, 0, 1])
        monster = self.owner
        destx = monster.x + mx
        desty = monster.y + my
        if monster.distance_to(player) < 9:
            monster.stamina = round(monster.maxStamina * 0.7)
            if monster.distance_to(player) > 1:
                if monster.x == player.x or monster.y == player.y:
                    if random.randint(1, 10) > 3:
                        monster.fighter.shoot(player, game_map, entities)
            if monster.distance_to(player) < 2:
                attack_results = monster.fighter.attack(player)
                results.extend(attack_results)
            monster.move_away(player.x, player.y, game_map, entities)
        else:
            if not game_map.is_blocked(destx, desty):
                target = get_blocking_entities_at_location(entities, destx, desty)
                if target == None:
                    monster.move(mx, my)
            else:
                target = get_blocking_entities_at_location(entities, destx*-1, desty*-1)
                if target == None:
                    monster.move(mx*-1, my*-1)
        monster.face = ChangeFace(player, monster)

        return(results)
        fov_recompute = True