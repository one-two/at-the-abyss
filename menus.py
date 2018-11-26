import libtcodpy as libtcod
from player_attributes import PlayerAttributes


def menu(con, header, options, width, screen_width, screen_height, menu_position):
    if len(options) > 26: raise ValueError('Limite de 26.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    index = 0
    for option_text in options:
        if index == menu_position:
            text = '> ' + option_text
        else:
            text = '  ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, player, inventory_width, screen_width, screen_height, menu_position):
    # show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Mala ta vazia.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (na mao principal)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (na mao secundaria)'.format(item.name))
            else:
                options.append(item.name)

    menu(con, header, options, inventory_width, screen_width, screen_height, menu_position)

def main_menu(con, background_image, screen_width, screen_height, menu_position):
    libtcod.image_blit_2x(background_image, 0, int(screen_width*0.1), int(screen_height*0.1))

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'olhe para o abismo')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                             '~ o ~')

    menu(con, '', ['Comecar do vazio', 'Continuar a existencia', 'Retornar a vida'], 24, screen_width, screen_height, menu_position)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height, menu_position):

    options = ['Constituicao (+20 HP, de {0})'.format(player.fighter.max_hp),
            'Forca (+1 ataque, de {0})'.format(player.fighter.power),
            'Dureza (+1 defesa, de {0})'.format(player.fighter.defense)]

    menu(con, header, options, menu_width, screen_width, screen_height, menu_position)

def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Personagem:')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Nivel: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experiencia atual: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experienca pra subir: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'HP maximo: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Ataque: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defesa: {0}'.format(player.fighter.defense))
    if player.equipment.main_hand:
        libtcod.console_print_rect_ex(window, 0, 10, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                    libtcod.LEFT, 'Mao Principal: {0}'.format(player.equipment.main_hand.name))
    if player.equipment.off_hand:
        libtcod.console_print_rect_ex(window, 0, 11, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                    libtcod.LEFT, 'Mao Secundaria: {0}'.format(player.equipment.off_hand.name))


    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)

def message_box(con, header, width, screen_width, screen_height, menu_position):
    menu(con, header, [], width, screen_width, screen_height, menu_position)