import math

class Raycaster:
    def __init__(self,screen,player,game_map):
        self.screen = screen
        self.player = player
        self.game_map = game_map

    def render(self):
        for ray_angle in range (-30,30): #field of view
            angle = self.player.angle + math.radians(ray_angle)
            hit = self.cast_ray(angle)
            if hit :
                self.draw_wall(hit)
    
    def cast_ray(self, angle):
        #Using BSP Tree to find the nearest wall
        node = self.game_map.bsp_tree.root
        return self.traverse_bsp(node,angle)
    
    def traverse_bsp(self, angle):
        #Traverse the BSP Tree to find the visible segment
        pass

    def draw_wall(self, hit):
        #draw wall in the screen
        pass
    