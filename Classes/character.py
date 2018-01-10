# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, os, pygame
from pygame.locals import *

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.psprite import PSprite

class Character(PSprite):
    """
    Base class for all characters (player-controlled and NPC).

    kwargs must contain:
        owner: The Level object that owns this Character
        centerx: Character spawn x-coordinate
        centery: Character spawn y-coordinate
        images["neutral"]: default image (see also PSprite)
        hp: Hit points (strength) of this Character
        ... and whatever is required by PSprite
    """

    def __init__(self, kwargs):

        PSprite.__init__(self, kwargs)

        self._owner = kwargs["owner"]

    # Initialize image and related variables (images loaded by
    #   Character.__init__())
        if 'neutral' not in self._images:
            raise ValueError("Expecting Player images to contain 'neutral'")

        self.image = self._images['neutral']
        # rect is used for running into obstacles; radius is used by
        #   Projectiles to determine a hit
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width + self.rect.height) / 4.0

        self.rect.centerx = kwargs["centerx"]
        self.rect.centery = kwargs["centery"]
        # TODO: _c_rect maybe not best name since now accessed by Level
        self._c_rect = self.rect.copy()

        self.hp = kwargs["hp"]
        self._max_hp = kwargs["hp"]

    # If this Character is currently active (hit-able, moveable, maybe visible)
        self.active = True


    def got_hit(self, projectile, attacker):
        """
        Signals that this Character got hit by a Projectile.

        Called by a Projectile.

        Just a stub.
        """
        pass


    def add_hp(self, hp):
        """
        Increase HP of Character by up to amount hp.
        """

        self.hp += hp
        if self.hp > self._max_hp:
            self.hp = self._max_hp


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")

