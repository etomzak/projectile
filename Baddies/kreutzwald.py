# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, os, random, math, pygame

# Add parent directory to path so can get Classes
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.baddie import Baddie

class Kreutzwald(Baddie):
    """
    An eminently poppable baddie that doesn't attack.

    kwargs must contain:
        owner
        centerx
        centery
        floors
        l_walls
        r_walls
        ceilings
        fired_projectiles
        targets
    """

    def __init__(self, kwargs):

        images = {'neutral': 'Kreutzwald_move_00.png',
                  'move' : ['Kreutzwald_move_00.png', 'Kreutzwald_move_01.png',
                            'Kreutzwald_move_02.png', 'Kreutzwald_move_02.png',
                            'Kreutzwald_move_01.png', 'Kreutzwald_move_00.png'
                            ],
                  'dead' : ['Kreutzwald_dead_00.png', 'Kreutzwald_dead_01.png']
                            }

        kwargs["images"]           = images
        kwargs["fpi"]              = 4
        kwargs["projectile_class"] = None
        kwargs["num_projectiles"]  = 0
        kwargs["hp"]               = 1
        kwargs["points"]           = 5

        Baddie.__init__(self, kwargs)

    # Movement characteristics
        self._speed = 1.0                   # Absolute speed
        self._dir = math.radians(random.randint(0, 359))
                                            # Direction of movement (degrees)

    def update(self):
        """
        Update the location of this Kreutzwald.
        """

        Baddie.update(self)

        # If inactive (i.e., dying), don't do anything
        if not self.active:
            return

        (dxf, dyf) = self._get_movement()


        # Check for collisions with obstacles. Don't care which obstacles were
        #   hit.
        # dxf and dxy values passed to collision detection have the drift
        #   between the FP center and int center added to prevent Baddies from
        #   slowly passing through barriers
        ddx, ddy, _, _ = self._basic_obstacle_collision(
            dxf + self._xf - self.rect.centerx,
            dyf + self._yf - self.rect.centery)

        self._move(dxf + ddx, dyf + ddy)

        # If collision detected
        if ddx != 0 or ddy != 0:
            self._dir = math.radians(random.randint(0, 359))

