# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, os

# Add parent directory to path so can get Classes
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.player import Player
from Projectiles.bb import BB

class Fred(Player):
    """
    Most basic playable character, Fred.
    """

    def __init__(self, centerx, centery, floors=None, l_walls=None,
        r_walls=None, ceilings=None, targets=None, fired_projectiles=None):

        images = {'neutral': 'Fred_neutral.png',
                  'walk': {'right': {'straight': ['Fred_walk_00.png',
                                                  'Fred_walk_02.png'],
                                     'up': ['Fred_walk_up_00.png',
                                            'Fred_walk_up_02.png'],
                                     'down': ['Fred_walk_down_00.png',
                                              'Fred_walk_down_02.png']}},
                  'stand': {'right': {'straight': ['Fred_stand.png'],
                                      'up': ['Fred_stand_up.png'],
                                      'down': ['Fred_stand_down.png']}},
                  'fly': {'right': {'straight': ['Fred_fly.png'],
                                    'up': ['Fred_fly_up.png'],
                                    'down': ['Fred_fly_down.png']}},
                  'dead': ['Fred_dead.png']}

        Player.__init__(
            self,
            centerx, centery,
            images,
            floors, l_walls, r_walls, ceilings,
            horizontal_speed=4.0, horizontal_inertia=20.0,
            multi_jumps=2, vertical_acceleration=0.2, jump_velocity=-5.0,
            fpi=4,
            projectile=BB, num_projectiles=10,
            targets=targets,
            fired_projectiles=fired_projectiles,
            hp=5)

        # Make Fred's collision box a bit narrower than the images
        self._c_rect.width = self.rect.width-6
        self._c_rect.centerx = self.rect.centerx





