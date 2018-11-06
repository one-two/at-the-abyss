import math
import random
from entity import get_blocking_entities_at_location

class BasicMonster:
    def act(self, player, fov_map, game_map, entities):
        mx = random.choice([-1, 0, 1]) 
        my = random.choice([-1, 0, 1])
        monster = self.owner
        destx = monster.x + mx
        desty = monster.y + my
        #print(str(mx) + ' , ' + str(my))
        if monster.distance_to(player) < 8:
            monster.move_towards(player.x, player.y, game_map, entities)
            monster.stamina = round(monster.maxStamina * 0.7)
            if monster.distance_to(player) < 2:
                print('{0} te deu um socao'.format(monster.name))
        else:
            if not game_map.is_blocked(destx, desty):
                target = get_blocking_entities_at_location(entities, destx, desty)
                if target == player:
                    print('pau neles')
                if target == None:
                    monster.move(mx, my)
            else:
                target = get_blocking_entities_at_location(entities, destx*-1, desty*-1)
                if target == player:
                    print('pau neles')
                if target == None:
                    monster.move(mx*-1, my*-1)
        fov_recompute = True