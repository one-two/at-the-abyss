import libtcodpy as libtcod
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap
from fov_functions import initialize_fov, recompute_fov
import random

def main():
    screen_width = 100
    screen_height = 70
    map_width = 100
    map_height = 65

    room_max_size = 16
    room_min_size = 10
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 9

    max_monsters_per_room = 3

    time = 0
    colors = {
        'dark_wall': libtcod.Color(0, 0, 0),#Color(0, 0, 50),
        'dark_ground': libtcod.Color(0, 0, 0),#Color(10, 10, 10),
        'explored_ground': libtcod.Color(2, 2, 0),
        'explored_wall': libtcod.Color(2, 2, 20),
        'medium_wall': libtcod.Color(10, 10, 50),
        'medium_ground': libtcod.Color(10, 10, 0),
        'light_wall': libtcod.Color(30, 30, 100),
        'light_ground': libtcod.Color(20, 20, 0)
    }

    player = Entity(0, 0, '@', libtcod.azure, 1, 'player', 10, blocks=True)
    #npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), 'S', libtcod.yellow, True)

    entities = [player]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    libtcod.console_init_root(screen_width, screen_height, 'not new window != 1', False)
    con = libtcod.console_new(screen_width, screen_height)
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    while not libtcod.console_is_window_closed():
        time += 1
        if (player.stamina < player.maxStamina): 
            player.stamina += 1
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors, fov_radius)
        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move and player.stamina == player.maxStamina:
            player.stamina = 0
            dx, dy = move
            dest_x = player.x + dx
            dest_y = player.y + dy

            if not game_map.is_blocked(dest_x, dest_y):
                target = get_blocking_entities_at_location(entities, dest_x, dest_y)

                if target:
                    print('voce chutou ' + target.name + ', pra que tanta violencia')
                else:
                    player.move(dx, dy)
                    fov_recompute = True

        
        if (time % 30) == 0:
            dx = random.randrange(-1,2)
            dy = random.randrange(-1,2)
            time = 0

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for entity in entities:
            if entity != player:
                if entity.stamina < entity.maxStamina: entity.stamina += 1
                else:
                    entity.stamina = 0
                    mx = random.choice([-1, 0, 1]) 
                    my = random.choice([-1, 0, 1])
                    destx = entity.x + mx
                    desty = entity.y + my
                    #print(str(mx) + ' , ' + str(my))
                    if not game_map.is_blocked(destx, desty):
                        target = get_blocking_entities_at_location(entities, destx, desty)
                        if target == player:
                            print('pau neles')
                        if target == None:
                            entity.move(mx, my)
                            fov_recompute = True
                    else:
                        target = get_blocking_entities_at_location(entities, destx*-1, desty*-1)
                        if target == player:
                            print('pau neles')
                        if target == None:
                            entity.move(mx*-1, my*-1)
                            fov_recompute = True

if __name__ == '__main__':
    main()