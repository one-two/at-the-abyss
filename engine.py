import libtcodpy as libtcod
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from render_functions import render_all, clear_all, RenderOrder
from map_objects.game_map import GameMap
from fov_functions import initialize_fov, recompute_fov
import random
from components.fighter import Fighter
from components.inventory import Inventory
from death_functions import kill_monster, kill_player
from game_states import GameStates
from time import sleep
from game_messages import MessageLog

def main():
    screen_width = 100
    screen_height = 70
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1
    map_width = 100
    map_height = 63

    room_max_size = 16
    room_min_size = 10
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 9

    max_monsters_per_room = 3
    max_itens_per_room = 1

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
    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    player = Entity(0, 0, '@', libtcod.azure, 1, 'player', 10, blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component)
    #npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), 'S', libtcod.yellow, True)

    entities = [player]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    message_log = MessageLog(message_x, message_width, message_height)
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    libtcod.console_init_root(screen_width, screen_height, 'not new window != 1', False)
    con = libtcod.console_new(screen_width, screen_height)
    panel = libtcod.console_new(screen_width, panel_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_itens_per_room)
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    game_state = 1
    while not libtcod.console_is_window_closed():
        if (player.stamina < player.maxStamina): 
            player.stamina += 1
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, colors, fov_radius, bar_width,
               panel_height, panel_y, mouse)
        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        pickup = action.get('pickup')
        fullscreen = action.get('fullscreen')
        if game_state == GameStates.PLAYER_DEAD:
            sleep(5)
            break
        act_results = []
        if move and player.stamina == player.maxStamina:
            player.stamina = 0
            dx, dy = move
            dest_x = player.x + dx
            dest_y = player.y + dy

            if not game_map.is_blocked(dest_x, dest_y):
                target = get_blocking_entities_at_location(entities, dest_x, dest_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    act_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        
        for player_turn_result in act_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

        for entity in entities:
            if entity != player:
                if entity.stamina < entity.maxStamina and entity.maxStamina != 0: entity.stamina += 1 
                elif entity.fighter and entity.fighter.hp > 0:
                    entity.stamina = 0
                    enemy_turn_results = entity.ai.act(player, fov_map, game_map, entities)
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

if __name__ == '__main__':
    main()