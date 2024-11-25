import pygame

class Player:
    def __init__(self,x,y,angle):
        self.x = x
        self.y = y
        self.angle = angle

    def move (self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += 5
        if keys[pygame.K_s]:
            self.x -= 5
        if keys[pygame.K_a]:
            self.angle -= 5
        if keys[pygame.K_d]:
            self.andle += 5