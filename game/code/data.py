from csv import reader
from os import walk
import pygame

# ОСНОВНЫЕ НАСТРОЙКИ
WIDTH = 1080
HEIGTH = 720
FPS = 60
TILESIZE = 64
HITBOX = {'player': -26, 'stone': -10, 'invisible': 0}

weapon_data = {'sword': {'cooldown': 10, 'damage': 1}}  # набор оружия
mobs_data = {'ninja': {'health': 100, 'exp': 250, 'damage': 6,  # тип и характеристики моба
                       'attack_type': 'leaf_attack', 'attack_sound': '../data/audio/hit.wav',
                       'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 10000}}


def import_csv_layout(path):  # ЗАГРУЗКА ФАЙЛОВ CSV КАРТЫ
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):  # ОБРАБОТКА КАРТИНОК
    surface_list = []

    for i, j, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
