import libtcodpy as libtcod
import math


def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors, fov_radius):
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
                        libtcod.console_set_char_background(con, x, y, colors.get('explored_ground'), libtcod.BKGND_SET)

    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity, fov_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


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