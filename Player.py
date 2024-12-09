from settings import *
import pygame as pg
import math

class Player:
    def __init__(self,game):
        self.game = game
        self.x,self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.player_walk = False
        self.shot = False

    def movement (self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx ,dy = 0,0
        speed = PLAYER_SPEED * 1
        speed_sin = speed * sin_a
        speed_cos = speed *cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
            self.player_walk = True
        if keys [pg.K_s]:
            num_key_pressed += 1
            dx -= speed_cos 
            dy -= speed_sin
            self.player_walk = True
        if keys [pg.K_a]:
            num_key_pressed +=1
            dx += speed_cos
            dy -= speed_sin
            self.player_walk = True
        if keys [pg.K_d]:
            num_key_pressed +=1
            dx -= speed_cos
            dy += speed_sin
            self.player_walk = True

    def update(self):
        self.movement()

    def pos(self):
        return self.x, self.y
    
    def map_pos(self):
        return int(self.x), int(self.y)
    
    def singleFire (self,event):
        if event.type == pg.K_SPACE:
            if event.button == 1 and not self.shot and not self.game.weapon.reload:
                self.shot = True
                self.game.weapon.reload = True
    
    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    