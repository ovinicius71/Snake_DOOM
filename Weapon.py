import pygame as pg
from collections import deque
from Player import *

# Constantes
HALF_WIDTH = 960
HEIGHT = 1450

class Weapon:
    def __init__(self, game, path='assets/sprites/weapon/shotgun/0.png', scale=0.4):
        self.game = game
        self.scale = scale

        # Carregar e converter a imagem
        initial_image = pg.image.load(path).convert_alpha()  # Converter para 32 bits com transparência
        scaled_image = pg.transform.smoothscale(
            initial_image, 
            (int(initial_image.get_width() * scale), int(initial_image.get_height() * scale))
        )
        self.images = deque([scaled_image])  # Criar a deque com a imagem escalada
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, 
                           HEIGHT - self.images[0].get_height())
        self.num_images = len(self.images)
    
   

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)
