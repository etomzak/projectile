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
    """

    def __init__(self, owner, centerx, centery, floors=None, l_walls=None,
        r_walls=None, ceilings=None, fired_projectiles=None, targets=None):

        images = {'neutral': 'Kreutzwald.png'}

        Baddie.__init__(
            self, owner,
            centerx, centery,
            images,
            floors, l_walls, r_walls, ceilings,
            fpi=4,
            projectile=None, num_projectiles=0, targets=targets,
            hp=1,
            points=5)

    # Movement characteristics
        # Kreutzwald is so slow-moving that its location is internally stored
        #   as floats. Otherwise, it could get stuck due to rounding errrors.
        # TODO: Double-check above assertion, esp. ceil() and floor() in
        #       update().
        self._speed = 1.0                   # Absolute velocity
        self._dir = math.radians(random.randint(0, 359))
                                            # Direction of movement (degrees)
        self._xf = float(centerx)           # x-coordinate as float
        self._yf = float(centery)           # y-coordinate as float


    def update(self):
        """
        Update the location of this Kreutzwald.
        """

        dxf = math.cos(self._dir) * self._speed
        dxy = math.sin(self._dir) * self._speed

        if dxf >= 0:
            dx = int(math.ceil(dxf))
        else:
            dx = int(math.floor(dxf))
        if dxy >= 0:
            dy = int(math.ceil(dxy))
        else:
            dy = int(math.floor(dxy))

        # Check for collisions with obstacles. Don't care which obstacles were
        #   hit.
        ddx, ddy, _, _ = self._basic_obstacle_collision(dx, dy)

        # No collision
        if ddx == 0 and ddy == 0:
            self._xf = self._xf + dxf
            self._yf = self._yf + dxy
            self.rect.centerx = round(self._xf)
            self.rect.centery = round(self._yf)
        # Collision: Move to obstacle and pick new direction
        else:
            self.rect.centerx = self.rect.centerx + dx + ddx
            self.rect.centery = self.rect.centery + dy + ddy
            self._xf = float(self.rect.centerx)
            self._yf = float(self.rect.centery)
            self._dir = math.radians(random.randint(0, 359))

        self._c_rect.centerx = self.rect.centerx
        self._c_rect.centery = self.rect.centery

