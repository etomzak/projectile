# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, os, pygame
from pygame.locals import *

# Add parent directory to path so can get Classes
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))
from Classes.countdownLevel import CountdownLevel
from Classes.wall import Wall
from Classes.platform import Platform

class BigRock(CountdownLevel):
    """
    A a level with a picture of a big rock in the background.

    @param baddie_classes: A list of available baddies
    @param power_ups: Dictionary of power-ups available to the player
    @param player_projectile_group: Where all Players' fired Projectiles go
    @param decoration_list: Where PSprites that need decorations go
    """

    def __init__(self, baddie_classes, power_ups=None,
            player_projectile_group=None, decoration_list=None):

        CountdownLevel.__init__(self, "BigRock.png", baddie_classes,
            power_ups, player_projectile_group, decoration_list)

        # This level doesn't use the standard box around the level area
        self.floors = pygame.sprite.Group()
        self.ceilings = pygame.sprite.Group()
        self.l_walls = pygame.sprite.Group()
        self.r_walls = pygame.sprite.Group()

        # Bottom-left corner obstacle
        self.floors.add(Platform(-40, 329, 66),
                        Platform(26, 454, 175))
        self.r_walls.add(Wall(25, 329, 125),
                         Wall(200, 454, 66))

        # Bottom-right corner obstacle
        self.l_walls.add(Wall(450, 454, 66))
        self.floors.add(Platform(450, 454, 231))

        # Center-left side obstacle
        self.floors.add(Platform(0, 204, 151))
        self.ceilings.add(Platform(0, 254, 26),
                          Platform(26, 229, 74),
                          Platform(100, 279, 26),
                          Platform(126, 229, 25))
        self.l_walls.add(Wall(0, 204, 51),
                         Wall(100, 230, 50))
        self.r_walls.add(Wall(25, 230, 25),
                         Wall(125, 230, 50),
                         Wall(150, 204, 26))

        # Top-left corner obstacle
        self.ceilings.add(Platform(-40, 129, 66),
                          Platform(26, 29, 174),
                          Platform(200, 79, 26))
        self.l_walls.add(Wall(200, 30, 50))
        self.r_walls.add(Wall(25, 30, 100),
                         Wall(225, -40, 120))

        # Top-right corner obstacle
        self.ceilings.add(Platform(475, 29, 125),
                          Platform(574, 254, 136))
        self.l_walls.add(Wall(475, -40, 70),
                         Wall(600, 30, 225))

        # Off-screen barriers
        self.floors.add(Platform(201, 520, 249))
        self.ceilings.add(Platform(226, -41, 249))
        self.l_walls.add(Wall(680, 255, 199))
        self.r_walls.add(Wall(-40, 130, 199))

        # Baddie shield
        self.floors.add(Platform(454, 80, 72))
        self.ceilings.add(Platform(454, 179, 72))
        self.l_walls.add(Wall(444, 94, 72))
        self.r_walls.add(Wall(539, 94, 72))

        # Floating boxes
        self.floors.add(Platform(100, 354, 51),
                        Platform(375, 304, 51),
                        Platform(200, 104, 26),
                        Platform(350, 79, 26))
        self.ceilings.add(Platform(100, 404, 51),
                          Platform(375, 329, 51),
                          Platform(200, 154, 26),
                          Platform(350, 179, 26))
        self.l_walls.add(Wall(100, 354, 51),
                         Wall(375, 304, 26),
                         Wall(200, 104, 51),
                         Wall(350, 79, 101))
        self.r_walls.add(Wall(150, 354, 51),
                         Wall(425, 304, 26),
                         Wall(225, 104, 51),
                         Wall(375, 79, 101))

        # Floating floors
        self.floors.add(Platform(274, 379, 103),
                        Platform(574, 354, 107),
                        Platform(199, 279, 78),
                        Platform(299, 229, 53),
                        Platform(424, 229, 128),
                        Platform(226, 131, 26),
                        Platform(324, 4, 78),
                        Platform(49, 104, 78))

        # Baddie spawn point
        self._baddie_spawn_x = 490
        self._baddie_spawn_y = 130

        # Center of where player should be spawned at start
        self.player_spawn_x = 50
        self.player_spawn_y = 425

        # Power-up stuff
        self._pu_spawn_x = 87
        self._pu_spawn_y = 60

        # Max number of baddies
        self._max_baddies = 10

