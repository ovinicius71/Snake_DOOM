from NPC import *

class SoldierNPC(NPC):
    
    def __init__(self, game, path='assets/sprites/npc/soldier/0.png', pos=(10.5,6), scale=0.8, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)