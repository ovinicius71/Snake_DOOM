from animate_sprite import *
from NPC import *
from random import choices, randrange
from NPCs.CacoDemonNPC import CacoDemonNPC
from NPCs.CyberDemonNPC import CyberDemonNPC
from NPCs.SoldierNPC import SoldierNPC


class object_manager:
    def __init__(self, game):
        """
        Initialize the ObjectManager to manage NPCs and animated sprites.
        
        :param game: Reference to the main game object.
        """
        self.game = game
        self.npc_list = []  # List of NPC objects
        self.sprite_list = []  # List of sprite objects
        self.npc_path = 'assets/sprites/npc/'  # Path to NPC sprites
        self.static_path = 'assets/sprites/static_sprites/'  # Path to static sprites
        self.animated_path = 'assets/sprites/animated_sprites/'  # Path to animated sprites
        self.anim_sprite_path = self.animated_path  # Alias for animated sprite path
        add_npc = self.add_npc 
        add_sprite = self.add_sprite

        self.num_enemies = 30  # Number of enemies to spawn
        self.weights = [70, 20, 10]  # Weight for NPC type probabilities
        self.types_npc = [CacoDemonNPC, CyberDemonNPC, SoldierNPC]  # Types of NPCs
        self.restrict_area = {(i, j) for i in range(10) for j in range(10)}  # Restricted spawn area
        self.npc_position = {}  # Positions of all NPCs

        # Spawn NPCs
        self.spawn_npc()

        # Add animated sprites
        self.add_initial_sprites()

    def add_sprite(self, sprite):
        """
        Add a sprite object to the sprite list.
        
        :param sprite: Sprite object to be added.
        """
        self.sprite_list.append(sprite)

    def generate_npc_position(self):
        """
        Generate a random position for an NPC that is not in a restricted area.
        
        :return: A valid position tuple (x, y).
        """
        pos = randrange(self.game.map.cols), randrange(self.game.map.rows)
        while pos in self.game.map.world_map or pos in self.restrict_area:
            pos = randrange(self.game.map.cols), randrange(self.game.map.rows)
        return pos

    def spawn_npc(self):
        """
        Spawn a specified number of NPCs at random positions.
        """
        for _ in range(self.num_enemies):
            npc = choices(self.types_npc, self.weights)[0]  # Select NPC type based on weight
            pos = self.generate_npc_position()
            self.add_npc(npc(self.game, pos=(pos[0] + 0.5, pos[1] + 0.5)))

    def add_npc(self, npc):
        """
        Add an NPC to the NPC list.
        
        :param npc: NPC object to be added.
        """
        self.npc_list.append(npc)

    def add_initial_sprites(self):
        """
        Add predefined animated sprites to the game.
        """
        positions = [
            (1.5, 1.5), (1.5, 7.5), (5.5, 3.25), (5.5, 4.75), (7.5, 2.5),
            (7.5, 5.5), (14.5, 1.5), (14.5, 4.5), (14.5, 5.5), (14.5, 7.5),
            (12.5, 7.5), (9.5, 7.5), (14.5, 12.5), (9.5, 20.5), (10.5, 20.5),
            (3.5, 14.5), (3.5, 18.5), (14.5, 24.5), (14.5, 30.5), (1.5, 30.5), (1.5, 24.5)
        ]

        for pos in positions:
            self.add_sprite(AnimatedSprite(self.game, pos=pos))

        # Add specific sprites with unique paths
        special_positions = [
            (14.5, 5.5), (14.5, 7.5), (12.5, 7.5), (9.5, 7.5), (14.5, 12.5), 
            (9.5, 20.5), (10.5, 20.5), (3.5, 14.5), (3.5, 18.5)
        ]
        for pos in special_positions:
            self.add_sprite(AnimatedSprite(self.game, path=self.anim_sprite_path + 'red_light/0.png', pos=pos))

    def update(self):
        """
        Update the positions of NPCs and animated sprites.
        """
        self.npc_position = {npc.map_pos for npc in self.npc_list if npc.alive}  # Update NPC positions
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
