# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, pygame, os, inspect
from pygame.locals import *

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.psprite import PSprite
from Classes.projectile import Projectile

class ProjectileBox(PSprite):
    """
    Manages Projectiles for a Character.

    Acts a bit like a pygame.sprite.Group, but can be drawn like a sprite.

    @param owner: Character that owns this Box. Must have a box_empty()
                  method.
    @param floors: pygame.sprite.Group of Platforms to be passed to Projectiles
    @param l_walls: pygame.sprite.Group of Walls to be passed to Projectiles
    @param r_walls: pygame.sprtie.Group of Walls to be passed to Projectiles
    @param ceilings: pygame.sprite.Group of Platforms to be passed to
                     Projectiles
    @param projectile_class: The Projectile class stored by this Box
    @param fired_projectiles: pygame.sprite.Group where in-flight Projectiles
                              should go (so Projectiles can outlive the Box)
    @param num_projectiles: Maximum number of simultaneous in-flight
                            Projectiles (None = Projectile default)
    @param max_shots: Number of Projectiles that can be fired before the Box
                      is exhausted (negative = infinite;
                      None = Projectile default)
    @param targets: pygame.sprite.Group of Characters that the Projectiles
                    in the Box might hit
    @param centerx: X-coordinate (only needed if Box is to be drawn)
    @param centery: Y-coordinate (only needed if Box is to be drawn)
    """

    def __init__(self, owner=None, floors=None, l_walls=None, r_walls=None,
            ceilings=None, projectile_class=None, fired_projectiles=None,
            num_projectiles=5, max_shots=-1, targets=None, centerx=0,
            centery=0):

        PSprite.__init__(self)

        self.owner = owner

    # If projectile_class is not given, then this Box will be a hollow shell
    #   of its true self (i.e., an empty placeholder)
        if projectile_class is None:
            return

    # Make sure projectile_class is ok
        if inspect.isclass(projectile_class) and \
                issubclass(projectile_class, Projectile) and \
                projectile_class is not Projectile:
            # all good
            pass
        else:
            raise TypeError("projectile must be a subclass of Projectile")

    # Create Projectiles
        self.fired_projectiles = fired_projectiles
        self.unused_projectiles = pygame.sprite.RenderPlain()


    # TODO: Horrible hack to get num_projectiles
        if num_projectiles is None:
            num_projectiles = projectile_class().max_in_flight

        for _ in range(num_projectiles):
            self.unused_projectiles.add(projectile_class(
                owner=self,
                platforms=pygame.sprite.RenderPlain(floors.sprites(),
                    ceilings.sprites()),
                walls=pygame.sprite.RenderPlain(l_walls.sprites(),
                    r_walls.sprites()),
                targets=targets))

    # Fill in Sprite stuff
        self.image = self.unused_projectiles.sprites()[0].image.copy()
        self.rect = self.image.get_rect(center=(centerx, centery))
        self._c_rect = self.rect.copy()

    # Ammo can be limited
        self._shots_fired = 0
        if max_shots is None:
            max_shots = self.unused_projectiles.sprites()[0].shots
        self._max_shots = max_shots


    def fire(self, num):
        """
        Fire num Projectiles.

        Returns the Projectiles fired so the caller can reset() them.

        Caller must ensure num Projectiles are available (e.g., with
        avail_projectiles()).
        """

        self._shots_fired += num

        # self._shots_fired > self._max_shots shouldn't actually happen
        if self._max_shots > 0 and self._shots_fired >= self._max_shots:
            self.owner.box_empty(self)

        prs = self.unused_projectiles.sprites()[0:num]
        self.unused_projectiles.remove(prs)
        self.fired_projectiles.add(prs)

        return prs


    def hit_a_target(self, projectile, target):
        """
        Signal that a Projectile owned by this Box has hit a target.

        Moves the Projectile back to the unused group and signals the Box's
        owner.

        This function is called by the Projectile.
        """

        self.fired_projectiles.remove(projectile)
        self.unused_projectiles.add(projectile)
        self.owner.hit_a_target(projectile, target)


    def recycle(self, projectile):
        """
        Move the projectile from the fired to the unused group.

        Gets rid of a Projectile without it hitting something.
        """

        self.fired_projectiles.remove(projectile)
        self.unused_projectiles.add(projectile)


    def avail_projectiles(self):
        """
        Check how many Projectiles are available to be fired.
        """

        if self._max_shots < 0:
            return len(self.unused_projectiles)
        else:
            return min(len(self.unused_projectiles),
                       self._max_shots-self._shots_fired)


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")

