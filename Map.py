from engine.BSP import BSPTree

class GameMap:
    def __init__(self):
        self.walls = self.load_map ()
        self.bsp_tree = BSPTree(self.walls)

    def load_map (self):
        #load map whith a list wall
        return [
            ((100,100),(300,300)),
            ((300,100), (300,300)),
            ((300,300), (100,300)),
            ((100,300), (100,100)),
        ]
