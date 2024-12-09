import pygame as pg
import sys
from settings import *
from Player import *
from Weapon import *

pg.init()

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)  # Configura o modo de vídeo antes de criar objetos
        pg.display.set_caption("Game")         # Configura um título para a janela (opcional)
        self.new_game()
        self.delta_time = 1
        

    def new_game(self):
        self.player = Player(self)  # Certifique-se de que Player funciona corretamente
        self.weapon = Weapon(self)  # Certifique-se de que Weapon funciona corretamente

    def update(self):
        self.player.update()
        self.player.movement()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

    def draw(self):
        self.screen.fill((20, 20, 20))  # Limpa a tela com uma cor de fundo
        self.weapon.draw()
        self.player.draw()  # Supondo que o jogador também tenha um método draw()
        pg.display.flip()   # Atualiza a tela

if __name__ == '__main__':  # Certifique-se de que RES esteja definido corretamente no settings
    game = Game()
    game.run()
