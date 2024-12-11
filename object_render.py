import pygame as pg
from settings import *

class object_render:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_texture = self.wall_texture()
        self.sky_image = self.get_texture('assets/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_off = 0
        self.digit_size = 50
        self.digit_image = [self.get_texture(f'assets/textures/digits/{i}.png', [self.digit_size] * 2) for i in range(11)]
        self.digit =dict(zip(map(str, range(11)), self.digit_image))

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
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digit[char], (195 + i * self.digit_size, 565))
        if health:  # Verifica se a string não está vazia
            self.screen.blit(self.digit['10'], (245 + i * self.digit_size, 565))

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        try:
            texture = pg.image.load(path).convert_alpha()
            return pg.transform.scale(texture, res)
        except FileNotFoundError:
            print(f"Erro: File not found - {path}")
            return pg.Surface(res)  # Retorna um placeholder em caso de erro

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