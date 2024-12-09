import pygame as pg
from settings import *

class object_render:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_texture = self.wall_texture()
        self.sky_image = self.get_texture('assets/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_off = 0

    def draw (self):
        self.draw_background()
        self.render_object()

    def draw_background(self):
        self.sky_off = (self.sky_off + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image,(-self.sky_off,0))
        self.screen.blit(self.sky_image,(-self.sky_off + WIDTH,0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0,HALF_HEIGHT,WIDTH,HEIGHT))

    @staticmethod
    def get_texture (path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def render_object(self):
        list_objects = sorted(self.game.raycasting.objects_render, key=lambda t : t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)
    
    def wall_texture (self):
        return{
            1: self.get_texture('assets/textures/1.png'),
            2: self.get_texture('assets/textures/2.png'),
            3: self.get_texture('assets/textures/3.png'),
            4: self.get_texture('assets/textures/4.png'),
            5: self.get_texture('assets/textures/5.png'),
        }


