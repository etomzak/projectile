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
                  'dead': ['Ilmar_dead_00.png', 'Ilmar_dead_01.png',
                           'Ilmar_dead_02.png', 'Ilmar_dead_03.png']}

        kwargs["images"]                = images
        kwargs["horizontal_speed"]      = 3.0
        kwargs["horizontal_inertia"]    = 40.0
        kwargs["multi_jumps"]           = 1
        kwargs["vertical_acceleration"] = 0.1
        kwargs["jump_velocity"]         = -5.0
        kwargs["fpi"]                   = 4
        kwargs["projectile_class"]      = Slug
        kwargs["num_projectiles"]       = 5
        # Ilmar's hp is never reduced so is effectively infinite
        kwargs["hp"]                    = 1

        Player.__init__(self, kwargs)


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
        slugs = self._box.fire(1)

        # Ilmar sometimes blows up
        if random.randint(0, 9) == 0:
            self.hp = 0
            for slug in slugs:
                self._box.recycle(slug)
            print("Projectile backfired")
            return

        direction = 0
        if self._point_v == 1: # Ilmar can't point down
            direction = 270
        elif self._point_h == -1:
            direction = 180

        for slug in slugs:
            slug.reset(centerx = self.rect.centerx,
                centery = self.rect.centery, direction=direction)


    def got_hit(self, projectile, attacker):
        """
        Signals that the Player got hit by a Projectile.

        Override default Player version, because Ilmar isn't hurt by
        Projectiles.
        """

        pass


    def reset(self, centerx=None, centery=None, bottom=None):
        """
        Ilmar doesn't need to be invincible.
        """

        Player.reset(self, centerx, centery)
        self._invincible_counter = 0
        self._decoration_list.remove(self)

