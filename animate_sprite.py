import pygame as pg
import os
from collections import deque

class animate_sprite:
    def __init__(self, game, path='assets/sprites/weapon/shotgun/', pos=(11, 3), scale=0.5, shift=0.16, animation_time=120):
        self.game = game
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_image(self.path)
        if not self.images:
            raise ValueError(f"No images found in path: {self.path}")
        self.image = self.images[0]  # Inicializa com a primeira imagem
        self.animation_time_pr = pg.time.get_ticks()
        self.animation_trigger = False
        self.pos = pos  # Posição da animação
        self.scale = scale
        self.shift = shift

    def update(self):
        self.check_animation_time()
        self.animate()

    def animate(self):
        if self.animation_trigger:
            self.images.rotate(-1)  # Gira a deque
            self.image = self.images[0]  # Atualiza a imagem atual
            

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_pr > self.animation_time:
            self.animation_time_pr = time_now
            self.animation_trigger = True

    def get_image(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images

    def draw(self):
        screen_pos = (self.pos[0], self.pos[1])  # Ajusta a posição para a escala da tela
        scaled_image = pg.transform.smoothscale(
            self.image,
            (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale))
        )
        self.game.screen.blit(scaled_image, screen_pos)
