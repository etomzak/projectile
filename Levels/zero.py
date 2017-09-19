# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, os

# Add parent directory to path so can get Classes
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))
from Classes.countdownLevel import CountdownLevel
from Classes.wall import Wall
from Classes.platform import Platform

class Zero(CountdownLevel):
    """
    A basic, playable level.

    @param baddie_classes: A list of available baddies
    @param power_ups: Dictionary of power-ups available to the player
    @param player_projectile_group: Where all Players' fired Projectiles go
    @param decoration_list: Where PSprites that need decorations go
    """

    def __init__(self, baddie_classes, power_ups=None,
            player_projectile_group=None, decoration_list=None):

        CountdownLevel.__init__(self, "Level_Zero.png", baddie_classes,
            power_ups, player_projectile_group, decoration_list)

        # Use barriers provided by Level class, and add some more

        # Bottom u-shaped thick obstacle
        self.floors.add(Platform(36, 448, 568),
                           Platform(32, 416, 4),
                           Platform(604, 416, 4))
        self.ceilings.add(Platform(32, 451, 576))
        self.l_walls.add(Wall(32, 416, 36),
                         Wall(604, 416, 32))
        self.r_walls.add(Wall(35, 416, 32),
                         Wall(607, 416, 36))

        # Two lower _-shaped thick obstacles
        self.floors.add(Platform(1, 384, 63),
                           Platform(576, 384, 63))
        self.ceilings.add(Platform(1, 388, 63),
                          Platform(576, 388, 63))
        self.l_walls.add(Wall(576, 384, 4))
        self.r_walls.add(Wall(63, 384, 4))

        # Two upper _-shaped thick obstacles
        self.floors.add(Platform(64, 32, 192),
                           Platform(384, 32, 192))
        self.ceilings.add(Platform(64, 35, 192),
                          Platform(384, 35, 192))
        self.l_walls.add(Wall(64, 32, 4),
                         Wall(384, 32, 4))
        self.r_walls.add(Wall(255, 32, 4),
                         Wall(575, 32, 4))

        # All the simple landing floors
        self.floors.add(Platform(224, 352, 192),
                           Platform(32, 288, 32),
                           Platform(288, 288, 64),
                           Platform(576, 288, 32),
                           Platform(1, 192, 31),
                           Platform(192, 192, 64),
                           Platform(384, 192, 64),
                           Platform(608, 192, 31),
                           Platform(32, 96, 32),
                           Platform(576, 96, 32))

        # Two one-way walls
        self.l_walls.add(Wall(256, 96, 128))
        self.r_walls.add(Wall(383, 96, 128))

        # The lone ceiling
        self.ceilings.add(Platform(256, 62, 128))

        # Baddie spawn point
        self._baddie_spawn_x = 160
        self._baddie_spawn_y = 128

        # Center of where player should be spawned at start
        self.player_spawn_x = 18
        self.player_spawn_y = 350

        # Power-up stuff
        self._pu_spawn_x = 480
        self._pu_spawn_y = 128

        # Max number of baddies
        self._max_baddies = 5

