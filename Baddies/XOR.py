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
    """

    def __init__(self, owner, centerx, centery, floors=None, l_walls=None,
        r_walls=None, ceilings=None, fired_projectiles=None, targets=None):

        images = {'neutral': 'XOR.png'}

        Baddie.__init__(
            self, owner,
            centerx, centery,
            images,
            floors, l_walls, r_walls, ceilings,
            fpi=4,
            projectile=BB, num_projectiles=12,
            fired_projectiles=fired_projectiles, targets=targets,
            hp=3,
            points=20)

    # XOR has small collision and hit areas
        self._c_rect = self.rect.copy().inflate(-18, -18)
        self.radius = 15

    # Movement characteristics
        self._speed = 1
        # XOR only moves left, right, up, or down
        self._dir = random.randint(0, 3) * 90
        # When XOR hits a barrier, it stops for a bit and doesn't fire
        self._stop_timer = 0

    # Firing characteristics
        # True when currently firing
        self._firing = False


    def update(self):
        """
        Update the location of this XOR.
        """

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

        dx = 0
        dy = 0

        if self._dir == 0:
            dx = self._speed
        elif self._dir == 90:
            dy = self._speed
        elif self._dir == 180:
            dx = -self._speed
        else:
            dy = -self._speed

        ddx, ddy, _, _ = self._basic_obstacle_collision(dx, dy)

        # No collision
        if ddx == 0 and ddy == 0:
            self.rect.centerx += dx
            self.rect.centery += dy
        # Collision: Move to obstacle and pick new direction
        else:
            self.rect.centerx = self.rect.centerx + dx + ddx
            self.rect.centery = self.rect.centery + dy + ddy
            self._dir = random.randint(0, 3) * 90
            self._stop_timer = 60

        self._c_rect.centerx = self.rect.centerx
        self._c_rect.centery = self.rect.centery


    def _fire(self):
        """
        Fire four Projectiles.
        """

        bbs = self._box.fire(4)
        for i in range(4):
            bbs[i].reset(self.rect.centerx, self.rect.centery, i*90)


