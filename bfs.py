from collections import deque
from functools import lru_cache

class BFS :
    def __init__(self, game):
        self.game = game
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.map = game.map.mini_map
        self.graph = {}
        self.get_graph()

    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_node = graph[cur_node]

            for nex_nod in next_node:
                if nex_nod not in visited and nex_nod not in self.game.object_manager.npc_position:
                    queue.append(nex_nod)
                    visited[nex_nod] = cur_node

        return visited
    
    def get_next_nodes (self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map ]


    @lru_cache
    def get_path (self, start, goal):
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)
        
        #step by step wooo baby 
        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]
    
    def get_graph (self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y) 