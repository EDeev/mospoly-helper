from random import choice

from data import *
from player import Player
from enemy import Enemy


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.ui = UI()

        # группы основных спрайтов видимых и нет
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()

        # группа спрайтов способных разрушиться
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # генерация карты
        self.create_map()

    def create_map(self):
        layouts = {
            'barryer': import_csv_layout('../data/map/барьеры.csv'),
            'stone': import_csv_layout('../data/map/камни.csv'),
            'entities': import_csv_layout('../data/map/мобы.csv')
        }
        graphics = {'stone': import_folder('../data/textures/stone')}

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'barryer':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'stone':
                            random_grass_image = choice(graphics['stone'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                 'stone', random_grass_image)
                        if style == 'entities':
                            if col == '2':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites,
                                                     self.destroy_attack, self.create_attack)
                            else:
                                Enemy("ninja", (x, y), [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites, self.damage_player, self.add_exp)

    def create_attack(self):  # создание атаки и спрайта оружия
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):  # разрушение разрушаемых объектов
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack(self):  # удары по другим объектам
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'stone':  # камни разрушаются с одного удара
                            target_sprite.kill()
                        else:  # мобы получают урон
                            target_sprite.get_damage(self.player)

    def damage_player(self, amount):
        self.player.health -= amount
        self.player.hurt_time = pygame.time.get_ticks()

    def add_exp(self, amount):
        self.player.exp += amount

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack()


# КАМЕРА СЛЕДЯЩАЯ ЗА ПЕРСОНАЖЕМ
class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # отрисовка основной карты
        self.floor_surf = pygame.image.load('../data/map/map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width  # ПОЛУЧЕНИЕ ПОЗИЦИИ ИГРОКА
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset  # ОТРИСОВКА ОСНОВНОЙ КАРТЫ ПОД ИГРОКОМ
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):  # ОТРИСОВКА МОБОВ
        enemy_sprites = []
        for sprite in self.sprites():
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy':
                enemy_sprites.append(sprite)

        for enemy in enemy_sprites:
            enemy.enemy_update(player)


# КЛАСС ОТРИСОВКИ ПЛИТОК
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        y_offset = HITBOX[sprite_type]
        self.image = surface

        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0, y_offset)


# КЛАСС ОРУЖИЯ
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        self.image = pygame.image.load(f'../data/textures/sword/{player.status.split("_")[0]}.png').convert_alpha()

        # отрисовка оружия по отношению к герою
        if player.status == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(-3, 16))
        elif player.status == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(3, 16))
        elif player.status == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 20))


# КЛАСС ИНТРЕФЕЙСА
class UI:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.SysFont("arial", 24)  # размер и формат чисел опыта

    def health_bar(self, player):
        pygame.draw.rect(self.screen, '#222222', pygame.Rect(10, 10, 120, 30))

        # перевод кол-ва здоровья в полоску
        ratio = player.health / player.stats['health']
        current_width = pygame.Rect(10, 10, 120, 30).width * ratio
        current_rect = pygame.Rect(10, 10, 120, 30).copy()
        current_rect.width = current_width

        pygame.draw.rect(self.screen, 'red', current_rect)
        pygame.draw.rect(self.screen, 'black', pygame.Rect(10, 10, 120, 30), 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, 'white')
        x = self.screen.get_size()[0] - 20  # место ячейки опыта
        y = self.screen.get_size()[1] - 1040
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.screen, '#222222', text_rect.inflate(20, 20))  # отрисовка опыта и серого фона
        self.screen.blit(text_surf, text_rect)

        pygame.draw.rect(self.screen, 'black', text_rect.inflate(20, 20), 3)  # отрисовка чёрной рамки

    def display(self, player):
        self.health_bar(player)
        self.show_exp(player.exp)
