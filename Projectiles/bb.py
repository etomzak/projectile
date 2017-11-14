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

    kwargs must contain:
        owner
        platforms
        walls
        targets
    """

    default_max_in_flight = 10
    default_number_shots = 30
    icon = "BB_icon.png"

    def __init__(self, kwargs):

        images = ["BB.png"]

        kwargs["images"]        = images
        kwargs["speed"]         = 6.0
        kwargs["damage"]        = 1
        kwargs["radius"]        = 2

        Projectile.__init__(self, kwargs)


    def reset(self, centerx, centery, direction):
        """
        Reset the Projectile (see Projectile.reset()).
        """

        # BB only supports right, up, left, and down for now
        direction = round(direction/90) * 90
        Projectile.reset(self, centerx, centery, direction);


