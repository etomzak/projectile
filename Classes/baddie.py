# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, os, inspect, pygame
from pygame.locals import *

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.character import Character
from Classes.projectileBox import ProjectileBox

class Baddie(Character):
    """
    NPC base class.

    Don't instantiate this class; subclass it.

    @param owner: The Level object that owns this Baddie
    @param centerx: Baddie spawn x-coordinate
    @param centery: Baddie spawn y-coordinate
    @param images: Dictionary pointing to the Baddie's image files
    @param floors: pygame.Group of Platforms that the sprite can stand on
    @param l_walls: pygame.Group of Walls that block the sprite moving right
    @param r_walls: pygame.Group of Walls that block the sprite moving left
    @param ceilings: pygame.Group of Platforms that the sprite is stuck under
    @param fpi: Frames per image for animation (larger is slower)
    @param projectile: The Projectile class that this Baddie uses
    @param num_projectiles: Maximum number of in-flight Projectiles this
        Baddie can have
    @param fired_projectiles: pygame.Group where fired Projectiles go. owner
        keeps track of these so they stay in play even if the Baddie dies.
        Since Projectiles have a reference to their originating Baddie, they
        effectively keep the Baddie in memory for a short time after the
        Baddie has died.
    @param targets: pygame.Group of Players that Projectiles fired by this
        Baddie might hit
    @param hp: Hit points (strength) of this Baddie
    @param points: Point value of hitting this Baddie
    """

    def __init__(self, owner, centerx, centery, images, floors=None,
        l_walls=None, r_walls=None, ceilings=None, fpi=4, projectile=None,
        num_projectiles=0, fired_projectiles=None, targets=None, hp=1,
        points=10):

        Character.__init__(self, centerx, centery, images, floors, l_walls,
            r_walls, ceilings, hp)

        self._owner = owner
        self.points = points

        # TODO: Move animation cycling to PSprite?
        self._walk_ctr = 0
        self._fpi = fpi

    # Set targets
        if targets is None:
            targets = pygame.sprite.RenderPlain()

    # Set up Projectiles
        # Use fired_projectiles from owner so Projectiles can outlive the
        #   Baddie
        self._box = ProjectileBox(
            owner             = self,
            floors            = floors,
            l_walls           = l_walls,
            r_walls           = r_walls,
            ceilings          = ceilings,
            projectile_class  = projectile,
            fired_projectiles = fired_projectiles,
            num_projectiles   = num_projectiles,
            max_shots         = -1,
            targets           = targets)


    def got_hit(self, projectile, attacker):
        """
        Signals that this Baddie got hit by a Projectile.

        Called by a Projectile.
        """

        self.hp -= projectile.damage
        if self.hp <= 0:
            self._owner.baddie_killed(self)


    def hit_a_target(self, projectile, target):
        """
        Signal that a Projectile fired by this Baddie has hit a target.

        Called by the Projectile.
        """

        pass


    def box_empty(self, box):
        """
        Signal that the currently used ProjectileBox is empty.

        Called by the ProjectileBox.
        """

        # Baddie currently assumes that it only uses its default box.

        print("Baddie ProjectileBox should not be empty")
        raise SystemExit


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")

