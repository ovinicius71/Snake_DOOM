import pygame as pg

class BSPNode:
    def __init__(self, region, objects=None):
        self.region = region  
        self.objects = objects if objects else [] 
        self.left = None
        self.right = None

class BSPTree:
    def __init__(self, map_data):
        self.root = None
        self.map_data = map_data  
        self.build_bsp()

    def build_bsp(self):
        initial_region = (0, 0, len(self.map_data[0]), len(self.map_data))
        self.root = self.split_region(initial_region)

    def split_region(self, region, depth=0):
        x, y, width, height = region
        if width <= 1 or height <= 1 or depth > 5: 
            return BSPNode(region)
        
        # Toggle between vertical and horizontal split
        if depth % 2 == 0:  # division vertical
            split_line = x + width // 2
            left_region = (x, y, split_line - x, height)
            right_region = (split_line, y, x + width - split_line, height)
        else:  # Division horizontal
            split_line = y + height // 2
            left_region = (x, y, width, split_line - y)
            right_region = (x, split_line, width, y + height - split_line)
        
        # make the nodes recursively
        node = BSPNode(region)
        node.left = self.split_region(left_region, depth + 1)
        node.right = self.split_region(right_region, depth + 1)
        return node

    def find_region(self, x, y):
        # Traverse the tree to find the region where (x, y) is located
        node = self.root
        while node.left or node.right:
            if node.left and self.is_point_in_region(x, y, node.left.region):
                node = node.left
            elif node.right:
                node = node.right
            else:
                break
        return node

    @staticmethod
    def is_point_in_region(x, y, region):
        rx, ry, rw, rh = region
        return rx <= x < rx + rw and ry <= y < ry + rh

    def draw_bsp_regions(self, screen):
        def draw_node(node):
            if node is None:
                return

            # Desenhar a região atual
            x, y, width, height = node.region
            pg.draw.rect(screen, 'blue', (x * 100, y * 100, width * 100, height * 100), 1)

            # Recursivamente desenhar os filhos
            draw_node(node.left)
            draw_node(node.right)

        draw_node(self.root)

