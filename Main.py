import pygame as pg
import sys
from settings import *
from Player import *
from Weapon import *
from animate_sprite import *

pg.init()

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)  
        pg.mouse.set_visible(False)
        pg.display.set_caption("Game")         
        self.new_game()
        self.delta_time = 1
        pg.event.set_grab(True)
        self.triggerGlobal = False
        self.globalEvent = pg.USEREVENT + 0

    def new_game(self):
        self.player = Player(self)  
        self.weapon = Weapon(self)  

    def update(self):
        self.player.update()
        self.player.movement()

    def check_events(self):
        self.triggerGlobal = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.globalEvent:
                self.triggerGlobal = True
            self.player.singleFire(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

    def draw(self):
        self.screen.fill((20, 20, 20))  
        self.weapon.draw()
        self.player.draw()  
        pg.display.flip()   

if __name__ == '__main__':  
    game = Game()
    game.run()
