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

    kwargs must contain:
        centerx
        centery
        floors
        l_walls
        r_walls
        ceilings
        targets
        fired_projectiles
    """

    def __init__(self, kwargs):

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
                  'dead': ['Fred_dead_00.png', 'Fred_dead_01.png',
                           'Fred_dead_02.png', 'Fred_dead_03.png']}

        kwargs["images"]                = images
        kwargs["horizontal_speed"]      = 4.0
        kwargs["horizontal_inertia"]    = 20.0
        kwargs["multi_jumps"]           = 2
        kwargs["vertical_acceleration"] = 0.2
        kwargs["jump_velocity"]         = -5.0
        kwargs["fpi"]                   = 4
        kwargs["projectile_class"]      = BB
        kwargs["max_in_flight"]         = 10
        kwargs["hp"]                    = 20

        Player.__init__(self, kwargs)

        # Make Fred's collision box a bit narrower than the images
        self._c_rect.width = self.rect.width-8
        self._c_rect.centerx = self.rect.centerx





