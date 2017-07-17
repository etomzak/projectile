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

    @param centerx: Character spawn x-coordinate
    @param centery: Character spawn y-coordinate
    @param images: Dictionary pointing to the Character's image files. It's
        assumed that all Characters will have at least a 'neutral' image in
        the dictionary.
    @param floors: pygame.Group of Platforms that the sprite can stand on
    @param l_walls: pygame.Group of Walls that block the sprite moving right
    @param r_walls: pygame.Group of Walls that block the sprite moving left
    @param ceilings: pygame.Group of Platforms that the sprite is stuck under
    @param hp: Hit points (strength) of this Character
    """

    def __init__(self, centerx, centery, images, floors=None, l_walls=None,
        r_walls=None, ceilings=None, hp=1):

        PSprite.__init__(self, images, floors, l_walls, r_walls, ceilings)

    # Initialize image and related variables (images loaded by
    #   Character.__init__())
        if 'neutral' not in self._images:
            raise ValueError("Expecting Player images to contain 'neutral'")

        self.image = self._images['neutral']
        # rect is used for running into obstacles; radius is used by
        #   Projectiles to determine a hit
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width + self.rect.height) / 4.0

        self.rect.centerx = centerx
        self.rect.centery = centery
        self._c_rect = self.rect.copy()

        self.hp = hp
        self._max_hp = hp

    # If this Character is currently active (hit-able, moveable, visible)
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

