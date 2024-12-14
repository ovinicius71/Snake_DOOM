import pygame as pg
import math
from settings import *

# Class responsible for handling the raycasting mechanics for rendering 3D effects in a 2D game.
class raycaster:
    def __init__(self, game):
        """
        Initializes the raycaster instance.
        :param game: Reference to the main game instance, containing player, map, and rendering settings.
        """
        self.game = game  # Reference to the game instance.
        self.ray_result = []  # Stores the results of the raycasting (depth, height, texture, offset).
        self.objects_render = []  # List of objects to render based on raycasting.
        self.textures = self.game.object_render.wall_texture  # References the textures used for walls.

    def get_objects_to_render(self):
        """
        Processes raycasting results to create the renderable objects for walls.
        Projects wall slices based on their depth and height.
        """
        self.objects_render = []  # Reset the list of objects to render.

        # Loop through each ray result to generate wall columns.
        for ray, values in enumerate(self.ray_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                # Wall is smaller than screen height; adjust scaling for proper rendering.
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                # Wall is larger than screen height; crop texture for rendering.
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 
                    HALF_TEXTURE_SIZE - texture_height // 2, 
                    SCALE, 
                    texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            # Append the depth, wall column, and position as a tuple.
            self.objects_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        """
        Performs raycasting to calculate the distance to walls and their properties.
        Casts NUM_RAYS rays in a field of view, determining the nearest wall hit for each ray.
        """
        self.ray_result = []  # Reset raycasting results.
        ox, oy = self.game.player.pos  # Player's current position (origin).
        x_map, y_map = self.game.player.map_pos  # Player's position in the map grid.

        ray_angle = self.game.player.angle - HALF_FOV + 0.001  # Starting angle for the first ray.

        # Iterate through each ray.
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)  # Sine of the ray angle.
            cos_a = math.cos(ray_angle)  # Cosine of the ray angle.
            vert_tex, hor_tex = 1, 1

            # Horizontal intersection calculations.
            y_h, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_h - oy) / sin_a
            x_h = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for _ in range(MAX_DEPTH):
                tile_hor = int(x_h), int(y_h)  # Current grid tile for horizontal intersections.
                if tile_hor in self.game.map.world_map:
                    hor_tex = self.game.map.world_map[tile_hor]  # Get texture ID for the tile.
                    break
                x_h += dx
                y_h += dy
                depth_hor += delta_depth

            # Vertical intersection calculations.
            x_v, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_v - ox) / cos_a
            y_v = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for _ in range(MAX_DEPTH):
                tile_vert = int(x_v), int(y_v)  # Current grid tile for vertical intersections.
                if tile_vert in self.game.map.world_map:
                    vert_tex = self.game.map.world_map[tile_vert]  # Get texture ID for the tile.
                    break
                x_v += dx
                y_v += dy
                depth_vert += delta_depth

            # Determine the closer intersection (horizontal or vertical).
            if depth_vert < depth_hor:
                depth, texture = depth_vert, vert_tex
                offset = y_v % 1 if cos_a > 0 else (1 - y_v % 1)
            else:
                depth, texture = depth_hor, hor_tex
                offset = (1 - x_h % 1) if sin_a > 0 else x_h % 1

            # Correct depth distortion due to ray angle.
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Calculate projected wall height based on depth.
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # Append raycasting results.
            self.ray_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE  # Increment ray angle for the next ray.

    def update(self):
        """
        Updates the raycasting and prepares the objects for rendering.
        This method is called every frame.
        """
        self.ray_cast()  # Perform raycasting to calculate wall positions and properties.
        self.get_objects_to_render()  # Generate renderable wall objects based on raycasting results.
