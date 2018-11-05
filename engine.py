import libtcodpy as libtcod
from input_handlers import handle_keys
from entity import Entity
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap
import random

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    time = 0
    colors = {
        'dark_wall': libtcod.Color(0, 0, 150),
        'dark_ground': libtcod.Color(0, 0, 0)
    }

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.azure)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), 'S', libtcod.yellow)

    entities = [npc, player]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    libtcod.console_init_root(screen_width, screen_height, 'not new window != 1', False)
    con = libtcod.console_new(screen_width, screen_height)
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    while not libtcod.console_is_window_closed():
        time += 1
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        render_all(con, entities, game_map, screen_width, screen_height, colors)
        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
        
        if (time % 30) == 0:
            dx = random.randrange(-1,2)
            dy = random.randrange(-1,2)
            if not game_map.is_blocked(npc.x + dx, npc.y + dy):
                npc.move(dx, dy)
            time = 0

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()