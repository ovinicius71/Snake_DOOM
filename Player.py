from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.player_walk = False
        self.shot = False
        self.rel = 0
        self.health_delay = 50
        self.time_prev = pg.time.get_ticks()
        self.last_damage_time = pg.time.get_ticks()

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time  

        keys = pg.key.get_pressed()
        self.player_walk = False 

        if keys[pg.K_w]:  # Frente
            dx += speed * cos_a
            dy += speed * sin_a
            self.player_walk = True
        if keys[pg.K_s]:  # Para trás
            dx -= speed * cos_a
            dy -= speed * sin_a
            self.player_walk = True
        if keys[pg.K_a]:  # Para a esquerda
            dx += speed * sin_a
            dy -= speed * cos_a
            self.player_walk = True
        if keys[pg.K_d]:  # Para a direita
            dx -= speed * sin_a
            dy += speed * cos_a
            self.player_walk = True

        # Checar colisões antes de atualizar a posição
        if not self.check_wall_collision(dx, dy):
            self.x += dx
            self.y += dy

    def check_wall_collision(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        grid_x, grid_y = int(new_x), int(new_y)

        node = self.game.map.bsp_tree.find_region(grid_x, grid_y)

        for x in range(node.region[0], node.region[0] + node.region[2]):
            for y in range(node.region[1], node.region[1] + node.region[3]):
                if (x, y) in self.game.map.world_map:
                    if (grid_x, grid_y) == (x, y):
                        return True

        return False
    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def single_fire(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if not self.shot and not self.game.weapon.reload:
                self.shot = True
                self.game.weapon.reload = True

    def draw(self):
        pg.draw.line(
            self.game.screen,
            'yellow',
            (self.x * 100, self.y * 100),
            (self.x * 100 + WIDTH * math.cos(self.angle),
             self.y * 100 + WIDTH * math.sin(self.angle)),
            2
        )
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()

        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])

        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
        self.angle %= math.tau 

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_render.player_damage()
        self.last_damage_time = pg.time.get_ticks()

    def recover_health(self):
        """Recupera a vida após 10 segundos sem receber dano."""
        time_now = pg.time.get_ticks()
        
        # Verifica se passaram 10 segundos desde o último dano
        if time_now - self.last_damage_time >= 10000:  # 10000 milissegundos = 10 segundos
            if self.check_recover_delay() and self.health < PLAYER_MAX_HEALTH:
                self.health += 1

    def check_recover_delay(self):
        """Controla o intervalo entre cada ponto de recuperação de vida."""
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_delay:
            self.time_prev = time_now
            return True
        return False