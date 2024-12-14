from animate_sprite import *
from random import randint, random
import math
from settings import *

class npc(AnimatedSprite):
    def __init__(self, game, path='assets/sprites/npc/soldier/0.png', pos=(10.5, 5), scale=0.8, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.load_images(f'{self.path}/attack')
        self.death_images = self.load_images(f'{self.path}/death')
        self.idle_images = self.load_images(f'{self.path}/idle')
        self.pain_images = self.load_images(f'{self.path}/pain')
        self.walk_images = self.load_images(f'{self.path}/walk')
        self.attack_distance = randint(4, 8)
        self.size = 20
        self.speed = 0.03
        self.attack_accuracy = 0.20
        self.health = 100
        self.attack_damage = 1
        self.pain = False
        self.alive = True
        self.ray_value = False
        self.frame_count = 0
        self.player_trigger = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.check_health()
        self.logic()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def attack(self):
        if self.animation_trigger:
            if random() < self.attack_accuracy:
                self.game.player.get_damage(self.attack_damage)

    def movement(self):
        next_pos = self.game.bfs.get_path(self.map_pos, self.game.player.map_pos)
        if not next_pos:
            return

        next_x, next_y = next_pos
        if next_pos not in self.game.object_manager.npc_position:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_collision(dx, dy)

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_hit(self):
        if self.ray_value and self.game.player.shot:
            print(f"Verificando hit no NPC. screen_x: {self.screen_x}, sprite_half_width: {self.sprite_half_width}")
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                print("NPC atingido pelo tiro do jogador.")
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                print(f"Dano aplicado: {self.game.weapon.damage}. Saúde restante do NPC: {self.health}")
                self.check_health()
            else:
                print("Tiro fora do alcance do NPC.")
        
        elif self.game.player.shot:
            print("O jogador não está atirando.")

    def animate_death(self):
        if not self.alive:
            if not self.game.triggerGlobal and self.frame_count < len(self.death_images) - 1:
                self.death_images.append(self.death_images.popleft())
                self.image = self.death_images[0]
                self.frame_count += 1

    def logic(self):
        if self.alive:
            self.ray_value = self.ray_player_npc()
            self.check_hit()

            if self.pain:
                self.animate_pain()
            elif self.ray_value:
                self.player_trigger = True
                if self.dist < self.attack_distance:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_v, wall_h = 0, 0
        player_v, player_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_v, player_h)
        wall_dist = max(wall_v, wall_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_player_npc():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y), (100 * self.x, 100 * self.y), 2)

    def check_health(self):
        if self.health <= 0:
            self.alive = False
