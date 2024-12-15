import pygame as pg
import sys
from settings import *
from Player import *
from Weapon import *
from animate_sprite import *
from Map import *
from raycasting import *
from object_render import *
from npc import *
from NPCs import *
from object_manage import * 
from bfs import *

pg.init()

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)  
        pg.mouse.set_visible(False)
        pg.display.set_caption("Game")         
        self.new_game()
        self.delta_time = 1
        self.clock = pg.time.Clock()
        pg.event.set_grab(True)
        self.triggerGlobal = False
        self.globalEvent = pg.USEREVENT + 0

    def new_game(self):
        self.player = Player(self)  
        self.weapon = Weapon(self)  
        self.map = Map(self)
        self.object_render = object_render(self)
        self.raycasting = raycaster(self)
        self.object_manager = object_manager(self)
        self.bfs = BFS (self)

    def update(self):
        self.player.update()
        self.player.movement()
        self.raycasting.update()
        self.object_manager.update()
        self.weapon.update()
        

    def check_events(self):
        self.triggerGlobal = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.globalEvent:
                self.triggerGlobal = True
            self.player.single_fire(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def draw(self):
        self.screen.fill((20, 20, 20))       
        self.player.draw()   
        self.object_render.draw()             
        self.weapon.draw()    
        self.map.draw()          
        pg.display.flip()    

if __name__ == '__main__':  
    game = Game()
    game.run()
