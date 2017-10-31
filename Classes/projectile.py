# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, pygame, os, math, inspect
from pygame.locals import *

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.psprite import PSprite

class Projectile(PSprite):
    """
    Base class for projectiles.

    Don't instantiate this class; subclass it.

    It's intended that Projectiles are constructed once and then recycled.
    I.e., a ProjectileBox should create a bunch of Projectiles, but only draw
    them once they've been fired. Once the Projectiles collide with something,
    they're not destroyed, just no longer drawn. This avoids the overhead of
    constructing a new Projectile, loading images, etc, every time the user
    presses fire.

    kwargs must contain:
        owner: The ProjectileBox objact that fired this Projectile
        images: Dictionary pointing to the sprite's image files
                The Projectile class assumes that images are in a single
                array (possibly of length 1)
        platforms: pygame.Group of Platforms that will be used as
                   horizontal obstacles that the Projectile can't cross
        walls: pygame.Group of Walls that are used as vertical obstacles
        speed: How fast this type of Projectile moves
        damage: How many HP damage this Projectile does
        targets: Characters that this Projectile might hit
        ... and whatever is required by PSprite

    kwargs can contain:
        radius: How big the Projectile is when calculating target collisions
                (inferred from image size if not given)

    class variables:
        default_max_in_flight: Suggested value for how many of these
                               Projectiles can be in flight at once
        default_number_shots: Suggested value for ProjectileBox._max_shots
                              (i.e., how many can be fired before a Box runs
                              out)

    *Projectile Collisions*

    On collision:
        Projectile.has_collided = True   -- this Projectile has hit something
                                            and should be cleaned up

        Projectile.target.got_hit()      -- target knows what hit it

        Projectile._owner.hit_a_target() -- owner knows its Projectile has hit
                                            something
    """

    default_max_in_flight = 10
    default_number_shots = 30

    def __init__(self, kwargs):

        kwargs["floors"]   = kwargs["platforms"]
        kwargs["l_walls"]  = kwargs["walls"]
        kwargs["r_walls"]  = kwargs["walls"]
        kwargs["ceilings"] = kwargs["platforms"]

        PSprite.__init__(self, kwargs)

        self._owner = kwargs["owner"]

    # The constructor above sets up _images
    # Define image and rect; pygame uses these for drawing
        self.image = self._images[0]
        self.rect = self.image.get_rect()
        self._c_rect = self.rect.copy()
        if "radius" in kwargs:
            self.radius = kwargs["radius"]
        else:
            self.radius = (self.rect.width + self.rect.height) / 4.0

    # Set class variables
        self._speed = kwargs["speed"]
        self.damage = kwargs["damage"]
        self._dir = 0 #direction

        # If the Projectile has collided with something
        self.has_collided = False

        self.targets = kwargs["targets"]
        if self.targets is None:
            self.targets = pygame.sprite.RenderPlain()


    def reset(self, centerx, centery, direction):
        """
        Reset the Projectile.

        Projectile will be centered at (centerx, centery), and pointed in
        direction. direction is in degrees clockwise from the positive x-axis.
        I.e, 0=right, 90=down, 180=left, 270=up.
        """

        self.image = self._images[0]
        # _dir is direction in range [0, 360) degrees, but stored in radians
        #   to avoid repeated conversion to radians later
        self._dir = math.radians(direction % 360)
        # TODO: Much more work required to handle animated Projectiles and
        #       Projectiles that change direction mid-flight
        # If a Projectile adjusts _c_rect, then its reset() will need to make
        #   the adjustment after Projectile.reset() is called
        # math.sin(), math.cos() are left-haned b/c pygame's y is flipped.
        #   pygames' rotate is right-handed.
        self.image = pygame.transform.rotate(self._images[0], -direction)
        self.rect = self.image.get_rect()
        self._c_rect = self.rect.copy()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self._c_rect.centerx = centerx
        self._c_rect.centery = centery

        self.has_collided = False


    def update(self):
        """
        Update Projectile location and do collision detection.
        """
        # TODO: Collisions with obstacles are tested before collisions with
        #       Characters. This might lead to some weird shadowing/shielding
        #       behavior. Revisit if it becomes and issue.

        dx = round(math.cos(self._dir) * self._speed)
        dy = round(math.sin(self._dir) * self._speed)

        _, _, targetA, targetB = self._basic_obstacle_collision(dx, dy)

        if targetA is not None:
            self._owner.hit_a_target(self, targetA)
            self.has_collided = True
        elif targetB is not None:
            self._owner.hit_a_target(self, targetB)
            self.has_collided = True

        self.rect.move_ip(dx, dy)
        self._c_rect.move_ip(dx, dy)

        targets = pygame.sprite.spritecollide(self, self.targets, False,
            pygame.sprite.collide_circle)

        # Hit first active target
        if len(targets) != 0:
            for target in targets:
                if target.active:
                    target.got_hit(self, self._owner)
                    self._owner.hit_a_target(self, target)
                    self.has_collided = True
                    break


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")

