# Copyright (C) 2017
# Author: Erik Tomusk
#
# This is free software, distributed under the GNU GPL version 3.
# This software comes with ABSOLUTELY NO WARRANTY.
# See GPLv3.txt for details.

import sys, pygame, os
from pygame.locals import *

# Add parent directory to path so can get Classes
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from Classes.projectile import Projectile

class BB(Projectile):
    """
    A basic, shootable thing.
    """

    def __init__(self, owner=None, platforms=None, walls=None, targets=None):

        images = ["BB.png"]
        Projectile.__init__(self, owner, images, platforms, walls, speed=6.0,
            damage=1, targets=targets, max_in_flight=10, shots=30)


    def reset(self, centerx, centery, direction):
        """
        Reset the Projectile (see Projectile.reset()).
        """

        # BB only supports right, up, left, and down for now
        direction = round(direction/90) * 90
        Projectile.reset(self, centerx, centery, direction);


