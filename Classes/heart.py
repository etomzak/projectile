# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, pygame, os
from pygame.locals import *

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))
from Classes.psprite import PSprite

class Heart(PSprite):
    """
    Heart object for collecting and increasing HP.

    @param centerx: X-coordinate
    @param centery: Y-coordinate
    """

    def __init__(self, centerx, centery):

        images = ['heart.png']

        PSprite.__init__(self, images)

        self.image = self._images[0]
        self.rect = self.image.get_rect(center=(centerx, centery))

        self.hp = 1


if __name__ == '__main__':
    print("Don't run me. Run projectile-game.py")

