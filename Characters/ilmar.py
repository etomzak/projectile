# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, os, random

# Add parent directory to path so can get Classes
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.player import Player
from Projectiles.slug import Slug

class Ilmar(Player):
    """
    An awesome, invincible tank!! (But it has a bad habbit of blowing up...)
    """

    def __init__(self, centerx, centery, floors=None, l_walls=None,
        r_walls=None, ceilings=None, targets=None, fired_projectiles=None):

        images = {'neutral': 'Ilmar_stand_straight.png',
                  'walk': {'right': {'straight': ['Ilmar_walk_straight.png'],
                                     'up': ['Ilmar_walk_up.png'],
                                     'down': ['Ilmar_walk_straight.png']}},
                  'stand': {'right': {'straight': ['Ilmar_stand_straight.png'],
                                      'up': ['Ilmar_stand_up.png'],
                                      'down': ['Ilmar_stand_straight.png']}},
                  'fly': {'right': {'straight': ['Ilmar_fly_straight.png'],
                                    'up': ['Ilmar_fly_up.png'],
                                    'down': ['Ilmar_fly_straight.png']}},
                  'dead': ['Ilmar_dead.png']}

        Player.__init__(
            self,
            centerx, centery,
            images,
            floors, l_walls, r_walls, ceilings,
            horizontal_speed=3.0, horizontal_inertia=40.0,
            multi_jumps=1, vertical_acceleration=0.1, jump_velocity=-5.0,
            fpi=4,
            projectile=Slug, num_projectiles=5,
            targets=targets,
            fired_projectiles=fired_projectiles,
            hp=1) # Ilmar's hp is never reduced so is effectively infinite


    def fire(self):
        """
        Fire a Slug.

        Override class default because Ilmar has some special behavior.
        """

        if self._box.avail_projectiles() == 0:
            return

        if self.hp <= 0:
            return

        # Or whatever else is in the _box
        slug = self._box.fire(1)[0]

        # Ilmar sometimes blows up
        if random.randint(0, 9) == 0:
            self.hp = 0
            self._box.recycle(slug)
            print("Projectile backfired")
            return

        direction = 0
        if self._point_v == 1: # Ilmar can't point down
            direction = 270
        elif self._point_h == -1:
            direction = 180

        slug.reset(centerx = self.rect.centerx, centery = self.rect.centery,
            direction=direction)


    def got_hit(self, projectile, attacker):
        """
        Signals that the Player got hit by a Projectile.

        Override default Player version, because Ilmar isn't hurt by
        Projectiles.
        """

        pass


