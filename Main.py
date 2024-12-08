import pygame as pg
import sys
from settings import *
#from Map import *
from Player import *
from Weapon import *
#from engine.Raycaster import *
#from sprite_object import *
class Game :
    def __init__(self):
        pg.init()
        self.new_game()
        self.delta_time = 1
        self.screen = pg.display.set_mode(RES)

    def new_game(self):
        self.player = Player(self)
        self.weapon = Weapon(self)
    
    def update(self):
        self.player.update()
        self.player.movement()
        pg.display.flip()
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type== pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            print ("")
            self.check_events()
            self.update()

    def draw(self):
        self.weapon.draw()

if __name__ == '__main__':
    game = Game()
    game.run()