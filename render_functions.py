import libtcodpy as libtcod
import math
from enum import Enum

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width * 1)-1, y+1, libtcod.BKGND_NONE, libtcod.RIGHT,
                             '{0}: {1}/{2}'.format(name, value, maximum))

def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, colors, fov_radius, bar_width,
               panel_height, panel_y, mouse):
    # Draw all the tiles in the game map /in sight range
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                dist = math.sqrt( math.pow(x - entities[0].x,2) + math.pow(y - entities[0].y,2)  )
                # 'light_wall': libtcod.Color(30, 30, 100)
                # 'light_ground': libtcod.Color(20, 20, 0)

                if visible:
                    if wall:
                        # if dist > 4:
                        #     libtcod.console_set_char_background(con, x, y, colors.get('medium_wall'), libtcod.BKGND_SET)
                        # else:
                        #     libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                        clr = math.floor(31-((30*dist)/(fov_radius+1)))
                        libtcod.console_set_char_background(con, x, y, libtcod.Color(clr, clr, 100), libtcod.BKGND_SET)
                    else:
                        # if dist > 4:
                        #     libtcod.console_set_char_background(con, x, y, colors.get('medium_ground'), libtcod.BKGND_SET)
                        # else:
                        #     libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                        clr = math.floor(21-((20*dist)/(fov_radius+1)))
                        libtcod.console_set_char_background(con, x, y, libtcod.Color(clr, clr, 0), libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('explored_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_default_foreground(con, libtcod.darker_grey)
                        libtcod.console_set_char_background(con, x, y, colors.get('explored_ground'), libtcod.BKGND_SET)

    # Draw all entities in the list
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)

    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_print_ex(con, 1, screen_height -2, libtcod.BKGND_NONE, libtcod.LEFT, ' {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.max_hp))

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # print messages
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text.upper())
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)

    render_bar(panel, 1, 3, bar_width, 'ST', player.stamina, player.maxStamina, libtcod.light_gray, libtcod.dark_gray)

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)