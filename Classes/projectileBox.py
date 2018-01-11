# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, pygame, os, inspect, copy
from pygame.locals import *

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.psprite import PSprite
from Classes.projectile import Projectile

class ProjectileBox(PSprite):
    """
    Manages Projectiles for a Character.

    Acts a bit like a pygame.sprite.Group, but can be drawn like a sprite.

    kwargs must contain:
        owner: Character that owns this Box. Must have a box_empty() method.
        floors: pygame.sprite.Group of Platforms to be passed to Projectiles
        l_walls: pygame.sprite.Group of Walls to be passed to Projectiles
        r_walls: pygame.sprtie.Group of Walls to be passed to Projectiles
        ceilings: pygame.sprite.Group of Platforms to be passed to Projectiles
        projectile_class: The Projectile class stored by this Box
        fired_projectiles: pygame.sprite.Group where in-flight Projectiles
                           should go (so Projectiles can outlive the Box)
        num_projectiles: Maximum number of simultaneous in-flight
                         Projectiles (None = Projectile default)
        max_shots: Number of Projectiles that can be fired before the Box
                   is exhausted (negative = infinite;
                   None = Projectile default)
        targets: pygame.sprite.Group of Characters that the Projectiles
                 in the Box might hit
        centerx: X-coordinate (only needed if Box is to be drawn)
        centery: Y-coordinate (only needed if Box is to be drawn)
        ... and whatever is required by PSprite
    """

    def __init__(self, kwargs):

    # Set up images filed for PSprite
        kwargs["images"] = None
        if "projectile_class" in kwargs:
            if kwargs["projectile_class"] is not None:
                # kwargs["projectile_class"].icon can be None
                kwargs["images"] = kwargs["projectile_class"].icon
        else:
            kwargs["projectile_class"] = None

    # Initialize PSprite
        PSprite.__init__(self, kwargs)

        self.owner = kwargs["owner"]

    # If projectile_class is not given, then this Box will be a hollow shell
    #   of its true self (i.e., an empty placeholder)
        if kwargs["projectile_class"] is None:
            return

    # Make sure projectile_class is ok
        if inspect.isclass(kwargs["projectile_class"]) and \
                issubclass(kwargs["projectile_class"], Projectile) and \
                kwargs["projectile_class"] is not Projectile:
            # all good
            pass
        else:
            raise TypeError("projectile must be a subclass of Projectile")

        # How many Projectiles fire() actually fires
        self._multi_shot = kwargs["projectile_class"].default_multi_shot

    # Create Projectiles
        self.fired_projectiles = kwargs["fired_projectiles"]
        self.unused_projectiles = pygame.sprite.RenderPlain()

        p_kwargs = {"owner"           : self,
                    "platforms"       : pygame.sprite.Group(
                                          kwargs["floors"].sprites(),
                                          kwargs["ceilings"].sprites()),
                    "walls"           : pygame.sprite.Group(
                                          kwargs["l_walls"].sprites(),
                                          kwargs["r_walls"].sprites()),
                    "targets"         : kwargs["targets"],
                    "decoration_list" : kwargs["decoration_list"]}

        if "num_projectiles" not in kwargs:
            self.max_in_flight = 5
        elif kwargs["num_projectiles"] is None:
            self.max_in_flight = \
                kwargs["projectile_class"].default_max_in_flight
        else:
            self.max_in_flight = kwargs["num_projectiles"]

        self.max_in_flight *= self._multi_shot

        while len(self.unused_projectiles) < self.max_in_flight:
            self.unused_projectiles.add(kwargs["projectile_class"](p_kwargs))

    # Fill in Sprite stuff
        # If no icon given, copy a Projectile's image
        # _has_icon is if the Projectile has defined an icon image
        if self._images is None:
            self._has_icon = False
            self.image = self.unused_projectiles.sprites()[0].image.copy()
        else:
            self._has_icon = True
            self.image = self._images

        self.rect = self.image.get_rect(center=(kwargs["centerx"],
                                                kwargs["centery"]))
        self._c_rect = self.rect.copy()

    # Ammo can be limited
        self._shots_fired = 0

        if "max_shots" not in kwargs:
            self._max_shots = -1
        elif kwargs["max_shots"] is None:
            self._max_shots = kwargs["projectile_class"].default_number_shots
        else:
            self._max_shots = kwargs["max_shots"]


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

        prs = self.unused_projectiles.sprites()[0:num*self._multi_shot]
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
            return len(self.unused_projectiles) // self._multi_shot
        else:
            return min(len(self.unused_projectiles) // self._multi_shot,
                       self._max_shots-self._shots_fired)


    def enable_box(self):
        """
        Only enable box decoration if no icon given.
        """

        if not self._has_icon:
            PSprite.enable_box(self)


    def disable_box(self):
        """
        Only disable box decoration if no icon given.
        """

        if not self._has_icon:
            PSprite.disable_box(self)


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")

