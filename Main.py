import pygame
from player import Player
from game_map import GameMap
from engine.raycaster import Raycaster

pygame.init()

#setting up the screen
width, height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake Doom")

#initializing
clock = pygame.time.Clock()
player = Player(x = 100, y = 100, angle = 0)
game_map = GameMap()
raycaster = Raycaster(screen, player, game_map)

#main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        screen.fill((0,0,0))
        