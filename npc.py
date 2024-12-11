from animate_sprite import *
from random import randint, random
import math
from settings import *

class npc(animate_sprite) :
    def __init__(self, game, path='assets/sprites/npc/soldier/0.png', pos=(10.5,5), scale=0.8, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_image = self.get_images(self.path + '/attack')
        self.death_image = self.get_images(self.path + '/death')
        self.idle_image = self.get_images(self.path + '/idle')
        self.pain_image = self.get_images(self.path + '/pain')
        self.walk_image = self.get_images(self.path + '/walk')
        self.attack_distance = randint(4,8)
        self.size = 20
        self.speed = 0.03
        self.attack_accuracy = 0.20
        self.health = 100
        self.attack_damage = 20
        self.pain = False
        self.alive = True
        self.ray_value = False
        self.frame_count = 0
        self.player_trigger = False

    def update(self):
        pass

    def check_wall(self, x, y):
        return (x,y) not in self.game.map.world_map
    
    def check_collision(self, dx, dy ):
        if self.check_wall(int(self.x + dx * self.size), int (self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy
    
    def attack(self):
        if self.animation_trigger:
            if random() < self.attack_accuracy:
                self.game.player.get_damage(self.attack_damage)

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        
        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)    

    def animate_pain(self):
        self.animate(self.pain_image)
        if self.animation_trigger:
            self.pain = False
        
    def check_hit(self):
        if self.ray_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_count < len(self.death_image) - 1:
                self.death_image.rotate(-1)
                self.images = self.death_image[0]
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
                    self.animate(self.attack_image)
                    self.attack

                else:
                    self.animate(self.walk_image)
                    self.movement()

            elif self.player_trigger:
                self.animate(self.walk_image)
                self.movement()
            
            else:
                self.animate(self.idle_image)
        
        else:
            self.animate_death()

    @property
    def map_pos (self):
        return int(self.x), int(self.y)

        

