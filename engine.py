import libtcodpy as libtcod
from input_handlers import handle_keys, handle_mouse
from entity import get_blocking_entities_at_location
from render_functions import render_all, clear_all, RenderOrder
from fov_functions import initialize_fov, recompute_fov
import random
from death_functions import kill_monster, kill_player
from game_states import GameStates
from player_attributes import PlayerAttributes
from time import sleep
from game_messages import Message
from components.damage import Damage_Area
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box

def game(player, entities, game_map, message_log, game_state, con, panel, constants):
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    menu_position = 0
    fov_recompute = True
    fov_map = initialize_fov(game_map)
    previous_game_state = game_state

    lastmove = (0, 0)
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
                        recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, constants['screen_width'], constants['screen_height'], constants['colors'], constants['fov_radius'], constants['bar_width'],
               constants['panel_height'], constants['panel_y'], mouse, game_state, menu_position)
        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        exit = action.get('exit')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        fullscreen = action.get('fullscreen')
        use  = action.get('use')
        drop = action.get('drop')
        equip = action.get('equip')
        strong_attack = action.get('strong_attack')
        show_character_screen = action.get('show_character_screen')

        click = mouse_action.get('left_click')

        if game_state == GameStates.PLAYER_DEAD:
            sleep(5)
            break
        act_results = []

        if click:
            cx, cy = click
            player.x = cx
            player.y = cy
            fov_recompute = True
        
        if game_state == GameStates.PLAYERS_TURN:
            if (player.stamina < player.maxStamina):
                player.stamina += 1
            if (player.cooldown < player.maxCooldown):
                player.cooldown += 1

        if move and player.stamina == player.maxStamina and game_state == GameStates.PLAYERS_TURN:
            player.stamina = 0
            dx, dy = move
            lastmove = move
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

        if strong_attack and player.cooldown >= 40:
            player.cooldown = 0
            dx, dy = lastmove
            dmg = Damage_Area(player.name, player.x + dx, player.y + dy, 7, delay=40)
            dmg2 = Damage_Area(player.name, player.x + (dx*2), player.y + (dy*2), 7, delay=40)
            dmg3 = Damage_Area(player.name, player.x + (dx*3), player.y + (dy*3), 7, delay=40)
            dmg4 = Damage_Area(player.name, player.x + (dx*4), player.y + (dy*4), 7, delay=40)
            dmg.CreateDamageEntity(game_map, dmg, entities)
            dmg2.CreateDamageEntity(game_map, dmg2, entities)
            dmg3.CreateDamageEntity(game_map, dmg3, entities)
            dmg4.CreateDamageEntity(game_map, dmg4, entities)
            
        if pickup and player.stamina == player.maxStamina and game_state == GameStates.PLAYERS_TURN:
            player.stamina = 0
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    act_results.extend(pickup_results)

                    break
                if entity.x == player.x and entity.y == player.y and entity.render_order == RenderOrder.CORPSE:
                    message_log.add_message(Message('Presunto! Uoba', libtcod.purple))
                    break
            else:
                message_log.add_message(Message('Nada no chao', libtcod.yellow))

        if use and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)
                    break
            else:
                message_log.add_message(Message('Nada a usar aqui.', libtcod.yellow))

        if show_inventory:
            menu_position = 0
            if game_state ==  GameStates.PLAYERS_TURN:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.SHOW_INVENTORY
            elif game_state == GameStates.SHOW_INVENTORY:
                game_state = previous_game_state
                menu_position = 0
        
        if show_character_screen:
            if game_state == GameStates.PLAYERS_TURN:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.CHARACTER_SCREEN
            elif game_state == GameStates.CHARACTER_SCREEN: 
                game_state = previous_game_state

        if (move or use or drop) and game_state == GameStates.SHOW_INVENTORY:
            if move and player.inventory.items:
                dx, dy = move
                if dy != 0:
                    menu_position += dy
                    if menu_position < 0:
                        menu_position = len(player.inventory.items) -1
                    if menu_position == len(player.inventory.items):
                        menu_position = 0
            if use and player.inventory.items:
                message_use = player.inventory.use(player.inventory.items[menu_position])
                act_results.extend(message_use)
                #print(player.inventory.items.pop(menu_position).name)
                if menu_position >= len(player.inventory.items)-1:
                    menu_position = len(player.inventory.items)-1
                    if menu_position < 0:
                        menu_position = 0
                if drop and player.inventory.items:
                    message_log.add_message(Message('Voce destruiu o item {0}'.format(player.inventory.items[menu_position].name), libtcod.yellow))
                    player.inventory.remove_item(player.inventory.items[menu_position])
                    if menu_position == len(player.inventory.items)-1:
                        menu_position -= 2
                        if menu_position < 0:
                            menu_position = 0
        
        if equip:
            equip_results = player.equipment.toggle_equip(equip)

            for equip_result in equip_results:
                equipped = equip_result.get('equipped')
                dequipped = equip_result.get('dequipped')

                if equipped:
                    message_log.add_message(Message('Voce equipou {0}'.format(equipped.name)))

                if dequipped:
                    message_log.add_message(Message('Voce desequipou {0}'.format(dequipped.name)))

        if game_state == GameStates.LEVEL_UP:
            if move:
                dx, dy = move
                if dy != 0:
                    menu_position += dy
                    if menu_position < 0:
                        menu_position =  2
                    if menu_position > 2:
                        menu_position = 0
            if use:
                if menu_position == 0:
                    player.fighter.max_hp += 20
                    player.fighter.hp += 20
                elif menu_position == 1:
                    player.fighter.power += 1
                elif menu_position == 2:
                    player.fighter.defense += 1
                game_state = previous_game_state
                
        if exit:
            if game_state == GameStates.SHOW_INVENTORY or game_state == GameStates.CHARACTER_SCREEN:
                game_state = previous_game_state
            else:
                save_game(player, entities, game_map, message_log, game_state)
                return True
        
        
        if game_state == GameStates.CHARACTER_SCREEN:
            if exit:
                game_state = previous_game_state

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        #damage environment/warning iterations
        for entity in entities[:]:
            if entity.damage:
                entity.damage.time += 1
                if entity.damage.time >= entity.damage.delay*0.7:
                    entity.color = libtcod.red
                if entity.damage.time >= entity.damage.delay:
                    act_results.extend(entity.damage.CauseDamage(entities))
                    entities.remove(entity)

        # player results calculation                 
        for player_turn_result in act_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            expired = player_turn_result.get('expired')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)
            
            if item_added:
                entities.remove(item_added)

            if expired:
                entities.remove(expired)
        
            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('Voce ganhou {0} de experiencia.'.format(xp)))

                if leveled_up:
                    message_log.add_message(Message(
                        'Voce alcancou o nivel {0}!'.format(
                            player.level.current_level) + '!', libtcod.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP
                    menu_position = 0

        # enemies moves calculation
        if game_state == GameStates.PLAYERS_TURN:
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

                                                
def main():
    constants = get_constants()

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)
    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])
    
    #player, entities, game_map, message_log, game_state = get_game_variables(constants)
    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False
    main_menu_background_image = libtcod.image_load('menu_background.png')
    menu_position = 0
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        if show_main_menu:

            if not show_load_error_message:
                main_menu(con, main_menu_background_image, constants['screen_width'],
                            constants['screen_height'], menu_position)

            if show_load_error_message:
                message_box(con, 'No save game to load', 50, constants['screen_width'], constants['screen_height'], -2)

            libtcod.console_flush()

            action = handle_keys(key)

            move = action.get('move')
            use  = action.get('use')
            space = action.get('strong_attack')
            exit = action.get('exit')

            if move:
                dx, dy = move
                if dy != 0:
                    menu_position += dy
                    if menu_position == -1:
                        menu_position = 2
                    if menu_position == 3:
                        menu_position = 0

            if show_load_error_message and (use or space):
                show_load_error_message = False
            elif menu_position == 0 and (use or space):
                player, entities, game_map, message_log, game_state = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif menu_position == 1 and (use or space):
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif (menu_position == 2 and (use or space)) or exit:
                break
        else:
            libtcod.console_clear(con)
            game(player, entities, game_map, message_log, game_state, con, panel, constants)

            show_main_menu = True

if __name__ == '__main__':
    main()