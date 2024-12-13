import pygame as pg
from collections import deque
from Player import *
from animate_sprite import *

# Constantes
HALF_WIDTH = 1250
HEIGHT = 2055

class Weapon(AnimatedSprite):
    def __init__(self, game, path='assets/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.weapon_pos = (
            HALF_WIDTH - self.image.get_width() // 2,
            HEIGHT - self.image.get_height()
        )
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.reload = False
        self.frame_counter = 0
        self.num_images = len(self.images)
        self.damage = 100

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def animation_shot(self):
        if self.reload:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reload = False
                    self.frame_counter = 0

    def update(self):
        self.check_animation_time()
        self.animation_shot()