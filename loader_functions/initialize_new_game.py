import libtcodpy as libtcod
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level

from entity import Entity

from game_messages import MessageLog

from game_states import GameStates

from map_objects.game_map import GameMap

from render_functions import RenderOrder

def get_constants():
    window_title = 'Roguelike Tutorial Revised'

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

    menu_selection = 0
    room_max_size = 16
    room_min_size = 10
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 9

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

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'colors': colors
    }

    return constants

def get_game_variables(constants):    
    fighter_component = Fighter(hp=70, defense=1, power=4)
    inventory_component = Inventory(26)
    level_component = Level()
    player = Entity(0, 0, '@', libtcod.azure, 1, 'player', 10, blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component, level=level_component)
    #npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), 'S', libtcod.yellow, True)

    entities = [player]

    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state