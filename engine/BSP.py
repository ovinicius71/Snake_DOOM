class BSPNode:
    def __init__(self, wall_segmente):
        self.wall = wall_segmente
        self.front = None
        self.back = None
    
class BSPTree :
    def __init__(self, walls):
        self.root = self.bild_tree(walls)

    def bild_tree (self, walls):
        if not walls:
            return None
        
        wall = walls[0]
        node = BSPNode (Wall)

        front_walls = []
        back_walls = []

        for other_wall in wall[1:]:
            if self.is_in_front(other_wall,wall):
                front_walls.append(other_wall)
            else:
                back_walls.append(other_wall)   
        
        node.front = self.bild_tree(front_walls)
        node.back = self.bild_tree(back_walls)
        return node
    
    def is_in_front (self,wall,reference_wall):
        #calculate segment location
        pass