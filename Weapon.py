from settings import *

class Weapon():

    def __init__(self,game,path ='assets/sprites/weapon/shotgun/0.png',scale = 0.4, animation_time = 90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images= deque (
            [pg.transform.smoothscale(img, (self.images.get_width() * scale, self.images.get_height() * scale ))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.num_images = len(self.images)

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    
