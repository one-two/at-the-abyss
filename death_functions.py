import libtcodpy as libtcod

from game_states import GameStates
from render_functions import RenderOrder

def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red
    return 'u ded', GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_messge = '{0} is ded'.format(monster.name.capitalize())

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'carcassa de ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_messge