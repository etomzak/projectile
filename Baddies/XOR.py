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
from Projectiles.bb import BB

class XOR(Baddie):
    """
    A scary-looking, stronger baddie that fires lots of BBs.

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

        images = {'neutral': 'XOR_move_00.png',
                  'move' : ['XOR_move_00.png', 'XOR_move_01.png',
                            'XOR_move_02.png', 'XOR_move_03.png',
                            'XOR_move_03.png', 'XOR_move_02.png',
                            'XOR_move_01.png', 'XOR_move_00.png'],
                  'dead' : ['XOR_dead_00.png', 'XOR_dead_01.png',
                            'XOR_dead_02.png', 'XOR_dead_02.png']}

        kwargs["images"]           = images
        kwargs["fpi"]              = 4
        kwargs["projectile_class"] = BB
        kwargs["num_projectiles"]  = 12
        kwargs["hp"]               = 3
        kwargs["points"]           = 20

        Baddie.__init__(self, kwargs)

    # XOR has small collision and hit areas
        self._c_rect = self.rect.copy().inflate(-18, -18)
        self.radius = 15

    # Movement characteristics
        self._speed = 1
        # XOR only moves left, right, up, or down
        self._dir = math.radians(random.randint(0, 3) * 90)
        # When XOR hits a barrier, it stops for a bit and doesn't fire
        self._stop_timer = 0

    # Firing characteristics
        # True when currently firing
        self._firing = False


    def update(self):
        """
        Update the location of this XOR.
        """

        Baddie.update(self)

        # If inactive (i.e., dying), don't do anything
        if not self.active:
            return

        if self._stop_timer != 0:
            self._stop_timer -= 1
            return

        avail_prs = self._box.avail_projectiles()

        # Fire aggressively when moving
        if not self._firing and avail_prs >= 12:
            self._firing = True

        if self._firing and avail_prs >= 4:
            self._fire()

        if self._firing and self._box.avail_projectiles() < 4:
            self._firing = False

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
            self._dir = math.radians(random.randint(0, 3) * 90)
            self._stop_timer = 60


    def _fire(self):
        """
        Fire four Projectiles.
        """

        bbs = self._box.fire(4)
        for i in range(4):
            bbs[i].reset(self.rect.centerx, self.rect.centery, i*90)


