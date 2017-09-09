# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, os, inspect, pygame, math
from pygame.locals import *

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.character import Character
from Classes.projectileBox import ProjectileBox

class Baddie(Character):
    """
    NPC base class.

    Don't instantiate this class; subclass it.

    kwargs must contain:
        owner: The Level object that owns this Baddie
        floors: pygame.sprite.Group of Platforms that the sprite can stand on
        l_walls: pygame.sprite.Group of Walls that block the sprite moving
                 right
        r_walls: pygame.sprite.Group of Walls that block the sprite moving left
        ceilings: pygame.sprite.Group of Platforms that the sprite is stuck
                  under
        fpi: Frames per image for animation (larger is slower)
        projectile_class: The Projectile class that this Baddie uses
        num_projectiles: Maximum number of in-flight Projectiles this
                         Baddie can have
        fired_projectiles: pygame.sprite.Group where fired Projectiles go.
                           owner keeps track of these so they stay in play even
                           if the Baddie dies. Since Projectiles have a
                           reference to their originating Baddie, they
                           effectively keep the Baddie in memory for a short
                           time after the Baddie has died.
        targets: pygame.sprite Group of Players that Projectiles fired by this
                 Baddie might hit
        points: Point value of hitting this Baddie
        ... and whatever is required by Character
    """

    def __init__(self, kwargs):

        Character.__init__(self, kwargs)

        self._owner = kwargs["owner"]
        self.points = kwargs["points"]

        # TODO: Move animation cycling to PSprite?
        self._walk_ctr = 0
        self._fpi = kwargs["fpi"]

        # Whether to draw hit decoration
        self._hit_counter = 0

    # Set targets
        targets = kwargs["targets"]
        if targets is None:
            targets = pygame.sprite.RenderPlain()

    # Set up Projectiles
        # Use fired_projectiles from owner so Projectiles can outlive the
        #   Baddie
        b_kwargs = {"owner"             : self,
                    "floors"            : kwargs["floors"],
                    "l_walls"           : kwargs["l_walls"],
                    "r_walls"           : kwargs["r_walls"],
                    "ceilings"          : kwargs["ceilings"],
                    "projectile_class"  : kwargs["projectile_class"],
                    "fired_projectiles" : kwargs["fired_projectiles"],
                    "num_projectiles"   : kwargs["num_projectiles"],
                    "max_shots"         : -1,
                    "targets"           : kwargs["targets"],
                    "centerx"           : 0,
                    "centery"           : 0,
                    "decoration_list"   : kwargs["decoration_list"]}
        self._box = ProjectileBox(b_kwargs)

    # Decorations
        # Invincibility
        r = math.ceil(max(self.rect.width, self.rect.height) * 0.75)
        self._dec_invinc_surf = \
            pygame.Surface((r*2, r*2), flags=SRCALPHA).convert_alpha()
        self._dec_invinc_rect = self._dec_invinc_surf.get_rect()
        pygame.draw.circle(self._dec_invinc_surf, (255, 0, 0), (r, r), r-1, 0)


    def update(self):
        """
        Just generic decoration handling.
        """

        if self._hit_counter > 0:
            self._hit_counter -= 1
            if self._hit_counter == 0:
                self._decoration_list.remove(self)


    def got_hit(self, projectile, attacker):
        """
        Signals that this Baddie got hit by a Projectile.

        Called by a Projectile.
        """

        self.hp -= projectile.damage
        if self.hp <= 0:
            self._owner.baddie_killed(self)
            if self._hit_counter > 0:
                self._decoration_list.remove(self)
        else:
            if self._hit_counter == 0:
                self._decoration_list.append(self)
            self._hit_counter = 5



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


    def draw_decoration(self, screen):
        """
        Draw a circle around the Baddie to indicate being hit.
        """

        self._dec_invinc_rect.centerx = self.rect.centerx
        self._dec_invinc_rect.centery = self.rect.centery
        screen.blit(self._dec_invinc_surf, self._dec_invinc_rect)


    def clear_decoration(self, screen, background):
        """
        Clear circle.
        """

        screen.blit(background, self._dec_invinc_rect, self._dec_invinc_rect)


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")
