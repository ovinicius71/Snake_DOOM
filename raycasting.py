import pygame as pg
import math
from settings import *

class raycaster:
    def __init__(self, game):
        self.game = game
        self.ray_result = []
        self.objects_render = []
        self.textures = self.game.object_render.wall_texture

    def get_objects_to_render(self):
        self.objects_render = []
        for ray, values in enumerate(self.ray_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2, SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_render.append((depth, wall_column, wall_pos))  # Corrigir para tupla
            
    def ray_cast(self):
        self.ray_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV + 0.001

        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # Cálculos horizontais
            y_h, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_h - oy) / sin_a
            x_h = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for _ in range(MAX_DEPTH):
                tile_hor = int(x_h), int(y_h)
                if tile_hor in self.game.map.world_map:
                    hor_tex = self.game.map.world_map[tile_hor]
                    break
                x_h += dx
                y_h += dy
                depth_hor += delta_depth

            # Cálculos verticais
            x_v, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_v - ox) / cos_a
            y_v = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for _ in range(MAX_DEPTH):
                tile_vert = int(x_v), int(y_v)
                if tile_vert in self.game.map.world_map:
                    vert_tex = self.game.map.world_map[tile_vert]
                    break
                x_v += dx
                y_v += dy
                depth_vert += delta_depth

            # Determinação da profundidade
            if depth_vert < depth_hor:
                depth, texture = depth_vert, vert_tex
                offset = y_v % 1 if cos_a > 0 else (1 - y_v % 1)
            else:
                depth, texture = depth_hor, hor_tex
                offset = (1 - x_h % 1) if sin_a > 0 else x_h % 1

            # Remoção do efeito "fisheye"
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Projeção
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # Resultado do raycasting
            self.ray_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE


    def update(self):
        self.ray_cast()
        self.get_objects_to_render()