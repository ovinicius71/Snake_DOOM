import pygame as pg
import os
from collections import deque
import math
from settings import *

class animate_sprite:
    def __init__(self, game, path='assets/sprites/static_sprites/candlebra.png', pos=(11, 3), scale=0.5, shift=0.16, animation_time=120):
        self.game = game
        self.animation_time = animation_time
        self.path = path
        self.images = self.load_images(self.path)
        if not self.images:
            raise ValueError(f"No images found in path: {self.path}")
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False
        self.pos = pos  # Animation position
        self.scale = scale
        self.shift = shift
        self.x, self.y = pos
        self.player = game.player
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def update(self):
        self.check_animation_time()
        self.animate(self.images)
        self.get_sprite()

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)  # Rotate the deque
            self.image = self.images[0]  # Update the current image

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def load_images(self, path):
        if os.path.isfile(path):
            path = os.path.dirname(path)  # Ajusta para o diretório pai se for um arquivo

        if not os.path.isdir(path):
            raise NotADirectoryError(f"The path '{path}' is not a directory or does not exist.")

        images = deque()
        for file_name in sorted(os.listdir(path)):
            full_path = os.path.join(path, file_name)
            if os.path.isfile(full_path):
                try:
                    img = pg.image.load(full_path).convert_alpha()
                    images.append(img)
                except pg.error as e:
                    print(f"Error loading image {full_path}: {e}")
        if not images:
            raise ValueError(f"No valid images found in directory: {path}")
        return images



    def draw(self):
        screen_pos = (int(self.pos[0] * 100), int(self.pos[1] * 100))  # Scale position for screen
        scaled_image = pg.transform.smoothscale(
            self.image,
            (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale))
        )
        self.game.screen.blit(scaled_image, screen_pos)

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (int(proj_width), int(proj_height)))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.objects_render.append((self.norm_dist, image, pos))
