import pygame as pg
from settings import *

class object_render:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_texture = self.wall_texture()
        self.sky_image = self.get_texture('assets/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_off = 0
        self.digit_size = 250
        self.hud_health_image = [self.get_texture(f'assets/sprites/hud_life/life_and_armor_hud_{-i + self.game.player.health}.png', [self.digit_size] * 2) for i in range(13)]
        self.digit =dict(zip(map(str, range(13)), self.hud_health_image))
        self.blood_screen = self.get_texture('assets/textures/blood_screen.png', RES)


    def draw(self):
        self.draw_background()
        self.render_object() 
        self.draw_health()

    def draw_background(self):
        self.sky_off = (self.sky_off + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_off, 0))
        self.screen.blit(self.sky_image, (-self.sky_off + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))
    
    def draw_health(self):
        health = max(0, min(self.game.player.health, 12))

        health_image = self.hud_health_image[-health + 13]

        self.screen.blit(health_image, (195, 1150))
        
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        try:
            texture = pg.image.load(path).convert_alpha()
            return pg.transform.scale(texture, res)
        except FileNotFoundError:
            print(f"Erro: File not found - {path}")
            return pg.Surface(res)  

    def render_object(self):
        try:
            list_objects = sorted(self.game.raycasting.objects_render, key=lambda t: t[0], reverse=True)
            for depth, image, pos in list_objects:
                self.screen.blit(image, pos)
        except AttributeError:
            print("Erro: 'objects_render' is not define")

    def wall_texture(self):
        return {
            1: self.get_texture('assets/textures/1.png'),
            2: self.get_texture('assets/textures/2.png'),
            3: self.get_texture('assets/textures/3.png'),
            4: self.get_texture('assets/textures/4.png'),
            5: self.get_texture('assets/textures/5.png'),
        }
    
    def player_damage(self):
        self.screen.blit(self.blood_screen,(0,0))