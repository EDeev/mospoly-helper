from data import *
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, destroy_attack, create_attack):
        super().__init__(groups)
        self.image = pygame.image.load('../data/textures/player/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX['player'])

        # стартовое положение спрайта
        self.import_player_assets()
        self.status = 'down'

        # параметры героя
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # оружик героя
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.create_attack = create_attack
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # характеристики героя
        self.stats = {'health': 300, 'attack': 10, 'speed': 5}
        self.max_stats = {'health': 300, 'attack': 20, 'speed': 10}
        self.health = self.stats['health']
        self.speed = self.stats['speed']
        self.exp = 0

        # import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('../data/audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

    def import_player_assets(self):  # получение всех картинок героя
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_stand': [], 'left_stand': [], 'up_stand': [], 'down_stand': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self.animations.keys():
            full_path = '../data/textures/player/' + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):  # кнопки
        if not self.attacking:
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            if mouse[0]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

    def get_status(self):  # положение героя на поле
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'stand' in self.status and not 'attack' in self.status:
                self.status = self.status + '_stand'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'stand' in self.status:
                    self.status = self.status.replace('_stand', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def cooldowns(self):  # таймер востановления удара
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def animate(self):  # анимирование героя
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def get_full_weapon_damage(self):  # нанесение врагу урона
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
