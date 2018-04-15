import pygame
import os
from pygame import mouse
from pygame.locals import *
from sys import exit
from tinydb import TinyDB, Query

import shop_interface
import char
import items

os.environ['SDL_VIDEO_CENTERED'] = '1'

# PyGame initialization
pygame.init()
pygame.font.init()
pygame.display.set_caption('Metholka RPG')

# player data
ch = None
name_to_load = None
db = None

# Initial pygame setup
font_name = pygame.font.get_default_font()
start_menu_font = pygame.font.Font('data/fonts/coders_crux.ttf', 40)
game_font = pygame.font.SysFont(font_name, 25)
screen_width = 512
screen_height = 480
black = (0, 0, 0)
red = (255, 0, 0)
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
clock = pygame.time.Clock()
FPS = 60

# Game Map Definition
# 'W' represents "walls" where player can't move
# 'O' represents where player can move
walls = []
level = [
    "OOOOOOOOOOOOOOOO",
    "OOOOOOOOOOOOOOOO",
    "OOOOOOOOOOOOOOOO",
    "OOOOOOOOOOOOOOOO",
    "OOOOOOOOOOOOOOOO",
    "WWWWWWWWWWWWWWWW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOOOOOOOOOOOW",
    "WWWWWWWOOWWWWWWW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOOOOOOOOOOOW",
    "WOOOOWWOOWWOOOOW",
    "WWWWWWWWWWWWWWWW"
]

DEFAULT_CURSOR = mouse.get_cursor()

_HAND_CURSOR = (
    "     XX         ",
    "    X..X        ",
    "    X..X        ",
    "    X..X        ",
    "    X..XXXXX    ",
    "    X..X..X.XX  ",
    " XX X..X..X.X.X ",
    "X..XX.........X ",
    "X...X.........X ",
    " X.....X.X.X..X ",
    "  X....X.X.X..X ",
    "  X....X.X.X.X  ",
    "   X...X.X.X.X  ",
    "    X.......X   ",
    "     X....X.X   ",
    "     XXXXX XX   ")
_HCURS, _HMASK = pygame.cursors.compile(_HAND_CURSOR, ".", "X")
HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)

dict_map_images = {
    'chao': 'resources/camadaChao.png',
    'chao2': 'resources/camadaChao2.png',
    'casa': 'resources/camadaCasa.png',
    'placas': 'resources/camadaPlacas.png'
}

dict_player_images = {
    'front': 'resources/playerFront.png',
    'back': 'resources/playerBack.png',
    'left': 'resources/playerLeft.png',
    'right': 'resources/playerRight.png'
}

background_start_menu = pygame.image.load('resources/start_menu.png').convert_alpha()
camada_chao = pygame.image.load(dict_map_images['chao']).convert()
camada_chao2 = pygame.image.load(dict_map_images['chao2']).convert_alpha()
camada_casa = pygame.image.load(dict_map_images['casa']).convert_alpha()
camada_placa = pygame.image.load(dict_map_images['placas']).convert_alpha()


class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(256, 256, 32, 32)
        self.sprite = pygame.image.load(dict_player_images['back']).convert_alpha()

    def move(self, dx, dy):
        if dx != 0:
            self.rect.x += dx
        if dy != 0:
            self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

    def change_sprite(self, side):
        if side == 1:
            self.sprite = pygame.image.load(dict_player_images['back']).convert_alpha()
        elif side == 2:
            self.sprite = pygame.image.load(dict_player_images['front']).convert_alpha()
        elif side == 3:
            self.sprite = pygame.image.load(dict_player_images['left']).convert_alpha()
        elif side == 4:
            self.sprite = pygame.image.load(dict_player_images['right']).convert_alpha()


class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

def create_shop_list_weapon():

    lista = ["Dagger 30", "Short Sword 80", "Long Sword 90", "Divine Sword 150", "Bow 45", "War Hammer 95", "Knife 25"]

    shop_list = list()

    for item in lista:
        novo = item.split()

        if len(novo) == 3:
            temp = " ".join(novo[0:2])
            novo[0] = temp
            novo[1] = novo[2]

        shop_list.append(items.Weapon(novo[0], novo[1]))

    return shop_list

def create_shop_list_armor():

    lista = ["Tunic 30", "Chain Armor 80", "Silver Armor 90", "Diamond Armor 150", "Boots 45", "Iron Shield 95",
             "Pants 25"]

    shop_list = list()

    for item in lista:
        novo = item.split()

        if len(novo) == 3:
            temp = " ".join(novo[0:2])
            novo[0] = temp
            novo[1] = novo[2]

        shop_list.append(items.Armor(novo[0], novo[1]))

    return shop_list

def create_shop_list_potion():

    lista = ["Minus Health 15", "Medium Health 30", "Big Health 70", "Full Restore 150"]

    shop_list = list()

    for item in lista:
        novo = item.split()

        if len(novo) == 3:
            temp = " ".join(novo[0:2])
            novo[0] = temp
            novo[1] = novo[2]

        shop_list.append(items.Potion(novo[0], novo[1]))

    return shop_list


def check_pos(p_centerx, p_centery):
    if 123 >= p_centerx >= 56 and p_centery <= 224:
        show_text('PRESS (E)')
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_e]:
            st = shop_interface.StoreWindow(ch, create_shop_list_weapon(), "Weapon Store", save_char)
            st.start_window()

    if 296 >= p_centerx >= 230 and p_centery <= 224:
        show_text('PRESS (E)')
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_e]:
            st = shop_interface.StoreWindow(ch, create_shop_list_armor(), "Armor Store", save_char)
            st.start_window()
    if 445 >= p_centerx >= 380 and p_centery <= 224:
        show_text('PRESS (E)')
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_e]:
            st = shop_interface.StoreWindow(ch, create_shop_list_potion(), "Potion Store", save_char)
            st.start_window()


def load_initial_map():
    screen.blit(camada_chao, (0, 0))
    screen.blit(camada_casa, (0, 0))
    screen.blit(player.sprite, player.rect)
    screen.blit(camada_chao2, (0, 0))
    screen.blit(camada_placa, (0, 0))


def show_text(text_display):
    text = game_font.render(text_display, 1, (0, 0, 0))
    screen.blit(text, (32, 450))


def create_walls():
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            x += 32
        y += 32
        x = 0


def create_text(text, font, color):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()

    return text_surf, text_rect


def game_intro():
    intro = True

    main_text = pygame.font.Font('data/fonts/coders_crux.ttf', 70)
    option_text = pygame.font.Font('data/fonts/coders_crux.ttf', 35)

    start_game_name_surf, start_game_name_rect = create_text('START GAME', option_text, black)
    quit_game_name_surf, quit_game_name_rect = create_text('QUIT', option_text, black)

    while intro:
        mouse_pos = mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_name_surf, game_name_text_rect = create_text('METHOLKA KINGDOM', main_text, black)

        game_name_text_rect.center = ((screen_width / 2), (screen_height / 3))
        start_game_name_rect.center = ((screen_width / 2), (screen_height / 1.8))
        quit_game_name_rect.center = ((screen_width / 2), (screen_height / 1.5))

        screen.blit(background_start_menu, (0, 0))
        screen.blit(game_name_surf, game_name_text_rect)
        screen.blit(start_game_name_surf, start_game_name_rect)
        screen.blit(quit_game_name_surf, quit_game_name_rect)

        if ((start_game_name_rect.right >= mouse_pos[0] >= start_game_name_rect.left) and (
                        start_game_name_rect.bottom >= mouse_pos[1] >= start_game_name_rect.top)) or (
                    (quit_game_name_rect.right >= mouse_pos[0] >= quit_game_name_rect.left) and (
                                quit_game_name_rect.bottom >= mouse_pos[1] >= quit_game_name_rect.top)):
            mouse.set_cursor(*HAND_CURSOR)
            if event.type == MOUSEBUTTONDOWN:
                mouse.set_cursor(*DEFAULT_CURSOR)
                game_loop(player)
        else:
            mouse.set_cursor(*DEFAULT_CURSOR)
        pygame.display.update()
        clock.tick(FPS)


def game_loop(player):
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_w] or pressed_keys[K_UP]:
            player.move(0, -3)
            player.change_sprite(1)
        elif pressed_keys[K_s] or pressed_keys[K_DOWN]:
            player.move(0, 3)
            player.change_sprite(2)

        if pressed_keys[K_a] or pressed_keys[K_LEFT]:
            player.move(-3, 0)
            player.change_sprite(3)
        elif pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            player.move(3, 0)
            player.change_sprite(4)

        load_initial_map()
        check_pos(player.rect.centerx, player.rect.centery)

        pygame.display.update()
        clock.tick(FPS)

def save_char():
    if db is not None:
        query = Query()

        player_dict = dict(ch)

        inventory = []
        for i in ch.inventory:
            inventory.append(dict(ch.inventory[ch.inventory.index(i)]))

        player_dict['inventory'] = inventory

        if not db.search(query.name == ch.name):
            db.insert(player_dict)
        else:
            db.update(player_dict, query.name == ch.name)


def load_char_if_saved():
    query = Query()

    if db is not None:
        var = db.search(query.name == name_to_load)

        if var:
            var = var[0]
            ch.name = var.get('name')
            ch.coins = var.get('coins')
            inventory = var.get('inventory')
            
            player_inventory = []
            for thing in inventory:
                if thing.get('type') == 'item':
                    item = items.Item(thing.get('name'), thing.get('price'))
                    player_inventory.append(item)
                elif thing.get('type') == 'weapon':
                    weap = items.Weapon(thing.get('name'), thing.get('price'), thing.get('damage'))
                    player_inventory.append(weap)
                elif thing.get('type') == 'armor':
                    armor = items.Armor(thing.get('name'), thing.get('price'), thing.get('defense'))
                    player_inventory.append(armor)
                elif thing.get('type') == 'potions':
                    potion = items.Potion(thing.get('name'), thing.get('price'), thing.get('health'))
                    player_inventory.append(potion)

            ch.inventory = player_inventory


if __name__ == "__main__":
    db = TinyDB('game_data.json')

    ch = char.Char()
    name_to_load = 'Player01'

    if not load_char_if_saved():
        save_char()

    player = Player()
    create_walls()
    game_intro()
    game_loop(player)
