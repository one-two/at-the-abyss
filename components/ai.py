import math
import random
from entity import get_blocking_entities_at_location

class BasicMonster:
    def act(self, player, fov_map, game_map, entities):
        results = []
        mx = random.choice([-1, 0, 1]) 
        my = random.choice([-1, 0, 1])
        monster = self.owner
        destx = monster.x + mx
        desty = monster.y + my
        #print(str(mx) + ' , ' + str(my))
        if monster.distance_to(player) < 8:
            monster.move_astar(player, entities, game_map)
            monster.stamina = round(monster.maxStamina * 0.7)
            if monster.distance_to(player) < 2:
                #print('attack')
                attack_results = monster.fighter.attack(player)
                results.extend(attack_results)
        else:
            if not game_map.is_blocked(destx, desty):
                target = get_blocking_entities_at_location(entities, destx, desty)
                #if target == player:
                #    monster.fighter.attack(target)
                if target == None:
                    monster.move(mx, my)
            else:
                target = get_blocking_entities_at_location(entities, destx*-1, desty*-1)
                #if target == player:
                #    monster.fighter.attack(target)
                if target == None:
                    monster.move(mx*-1, my*-1)
        return(results)
        fov_recompute = True