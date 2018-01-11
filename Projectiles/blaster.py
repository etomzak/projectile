# Copyright (C) 2018
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

class Blaster(Projectile):
    """
    Quite a strong Projectile. A better BB.

    kwargs must contain:
        owner
        platforms
        walls
        targets
    """

    default_max_in_flight = 1
    default_number_shots = 3
    default_multi_shot = 5
    # Individual laser pulses are initialized with slightly different speeds
    #   so the pulses spread out
    speed = 15.0
    icon = "Blaster_icon.png"

    def __init__(self, kwargs):

        images = ["Blaster.png"]

        kwargs["images"]        = images
        kwargs["speed"]         = Blaster.speed
        kwargs["damage"]        = 10
        kwargs["radius"]        = 8

        Blaster.speed += 0.3
        if Blaster.speed >= 16.5:
            Blaster.speed = 15.0

        Projectile.__init__(self, kwargs)


    def reset(self, centerx, centery, direction):
        """
        Reset the Projectile (see Projectile.reset()).
        """

        # Only right, up, left, and down for now
        direction = round(direction/90) * 90
        Projectile.reset(self, centerx, centery, direction);


