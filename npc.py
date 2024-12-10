from sprite_object import *
from random import randint, random

class npc(AnimatedSprite) :
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
        
        

