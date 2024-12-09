import pygame as pg
from collections import deque
from Player import *
from animate_sprite import *

# Constantes
HALF_WIDTH = 960
HEIGHT = 1450

class Weapon(animate_sprite):
    def __init__(self, game, path='assets/sprites/weapon/shotgun', pos=(HALF_WIDTH, HEIGHT), scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, pos=(0, 0), scale=scale, animation_time=animation_time)
        self.weapon_pos = (
            HALF_WIDTH - self.image.get_width() // 2,
            HEIGHT - self.image.get_height()
        )
        self.reload = False

    def draw(self):
        scaled_image = pg.transform.smoothscale(
            self.image,
            (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale))
        )
        self.game.screen.blit(scaled_image, self.weapon_pos)

    def animation_shot(self):
        if self.reload:
            self.animate()
            if not self.animation_trigger:  # Quando a animação termina
                self.reload = False
                self.game.player.shot = False

    def update(self):
        self.check_animation_time()
        self.animation_shot()