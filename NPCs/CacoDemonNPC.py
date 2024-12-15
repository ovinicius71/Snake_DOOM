from NPC import *

class CacoDemonNPC(NPC):

    def __init__(self, game, path='assets/sprites/npc/caco_demon/0.png', pos=(10,6), scale=0.8, shift=0.38, animation_time=280):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35
