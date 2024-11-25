import pygame as pg
from settings import *
import os
from collections import deque

class SprinteObject:
    def __init__(self, game, path='assets/sprites/static_sprites/candlebra.png',pos = (10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player 
        self.x,self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
    
    def get_projection_sprite(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj *self.IMAGE_RATIO, proj
        image = pg.transform.scale(self.image,(proj_width,proj_height))
        self.sprite_half_width =proj_width//2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))